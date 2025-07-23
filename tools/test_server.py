#!/usr/bin/env python3
"""
Server testing framework for NimbleTools Community MCP Registry

Tests actual MCP server functionality by running Docker containers and making HTTP requests.
"""

import asyncio
import json
import logging
import sys
import time
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import yaml
import httpx
import docker
from docker.errors import DockerException
import subprocess

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MCPServerTester:
    """Tests MCP servers by running them in Docker containers"""
    
    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.docker_client = None
        self.test_results: List[Dict[str, Any]] = []
        
    def _get_docker_client(self) -> docker.DockerClient:
        """Get Docker client with error handling"""
        if self.docker_client is None:
            try:
                self.docker_client = docker.from_env()
                # Test connection
                self.docker_client.ping()
            except DockerException as e:
                raise RuntimeError(f"Failed to connect to Docker: {e}")
        return self.docker_client
    
    def load_server_definition(self, server_path: Path) -> Dict[str, Any]:
        """Load server definition from server.yaml"""
        server_yaml_path = server_path / "server.yaml"
        
        if not server_yaml_path.exists():
            raise FileNotFoundError(f"server.yaml not found in {server_path}")
        
        with open(server_yaml_path, 'r') as f:
            return yaml.safe_load(f)
    
    async def wait_for_server(self, base_url: str, max_attempts: int = 30) -> bool:
        """Wait for server to be ready by checking health endpoint"""
        async with httpx.AsyncClient() as client:
            for attempt in range(max_attempts):
                try:
                    response = await client.get(f"{base_url}/health", timeout=5.0)
                    if response.status_code == 200:
                        logger.info(f"✅ Server ready after {attempt + 1} attempts")
                        return True
                except httpx.RequestError:
                    pass
                
                await asyncio.sleep(1)
        
        logger.error(f"❌ Server not ready after {max_attempts} attempts")
        return False
    
    async def test_health_endpoint(self, base_url: str) -> Dict[str, Any]:
        """Test the health endpoint"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{base_url}/health", timeout=10.0)
                
                return {
                    "test": "health_endpoint",
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "details": response.json() if response.status_code == 200 else response.text
                }
            except Exception as e:
                return {
                    "test": "health_endpoint", 
                    "success": False,
                    "error": str(e)
                }
    
    async def test_tools_endpoint(self, base_url: str) -> Dict[str, Any]:
        """Test the tools listing endpoint"""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{base_url}/tools", timeout=10.0)
                
                success = response.status_code == 200
                tools = []
                
                if success:
                    data = response.json()
                    tools = data.get('tools', [])
                    # Validate tools structure
                    for tool in tools:
                        if not all(key in tool for key in ['name', 'description', 'parameters']):
                            success = False
                            break
                
                return {
                    "test": "tools_endpoint",
                    "success": success,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "tools_count": len(tools),
                    "tools": [tool.get('name') for tool in tools],
                    "details": response.json() if response.status_code == 200 else response.text
                }
            except Exception as e:
                return {
                    "test": "tools_endpoint",
                    "success": False,
                    "error": str(e)
                }
    
    async def test_tool_execution(self, base_url: str, tool: Dict[str, Any]) -> Dict[str, Any]:
        """Test executing a specific tool"""
        tool_name = tool.get('name')
        
        async with httpx.AsyncClient() as client:
            try:
                # Use example input if available, otherwise create minimal input
                test_input = {}
                
                if 'examples' in tool and tool['examples']:
                    example = tool['examples'][0]
                    test_input = example.get('input', {})
                else:
                    # Generate minimal input based on schema
                    schema = tool.get('schema', {})
                    properties = schema.get('properties', {})
                    required = schema.get('required', [])
                    
                    for param in required:
                        if param in properties:
                            param_type = properties[param].get('type', 'string')
                            if param_type == 'string':
                                test_input[param] = 'test'
                            elif param_type == 'number':
                                test_input[param] = 1
                            elif param_type == 'boolean':
                                test_input[param] = True
                            elif param_type == 'object':
                                test_input[param] = {}
                            elif param_type == 'array':
                                test_input[param] = []
                
                response = await client.post(
                    f"{base_url}/tools/{tool_name}",
                    json=test_input,
                    timeout=15.0
                )
                
                success = response.status_code in [200, 201]
                
                return {
                    "test": f"tool_{tool_name}",
                    "success": success,
                    "status_code": response.status_code,
                    "response_time": response.elapsed.total_seconds(),
                    "input": test_input,
                    "output_size": len(response.content) if response.content else 0,
                    "details": response.json() if success else response.text[:200] + "..." if len(response.text) > 200 else response.text
                }
            except Exception as e:
                return {
                    "test": f"tool_{tool_name}",
                    "success": False,
                    "input": test_input,
                    "error": str(e)
                }
    
    async def test_server_functionality(self, base_url: str, server_def: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Test all server functionality"""
        tests = []
        
        # Test health endpoint
        health_result = await self.test_health_endpoint(base_url)
        tests.append(health_result)
        
        # Test tools endpoint
        tools_result = await self.test_tools_endpoint(base_url)
        tests.append(tools_result)
        
        # Test individual tools if tools endpoint works
        if tools_result.get('success'):
            tools = server_def.get('tools', [])
            for tool in tools:
                tool_result = await self.test_tool_execution(base_url, tool)
                tests.append(tool_result)
        
        return tests
    
    def run_docker_container(self, image: str, port: int, env_vars: Dict[str, str] = None) -> Tuple[Any, str]:
        """Run Docker container and return container object and base URL"""
        client = self._get_docker_client()
        
        try:
            # Pull image if not present
            logger.info(f"🐳 Pulling Docker image: {image}")
            client.images.pull(image)
            
            # Prepare environment variables
            environment = env_vars or {}
            
            # Run container
            logger.info(f"🚀 Starting container: {image}")
            container = client.containers.run(
                image,
                detach=True,
                ports={f'{port}/tcp': ('127.0.0.1', 0)},  # Bind to random port
                environment=environment,
                remove=True,  # Auto-remove when stopped
                name=f"mcp-test-{int(time.time())}"
            )
            
            # Get the actual port
            container.reload()
            host_port = container.ports[f'{port}/tcp'][0]['HostPort']
            base_url = f"http://localhost:{host_port}"
            
            logger.info(f"📡 Container running at: {base_url}")
            return container, base_url
            
        except DockerException as e:
            logger.error(f"❌ Failed to run container: {e}")
            raise
    
    def stop_container(self, container: Any) -> None:
        """Stop and clean up container"""
        try:
            logger.info("🛑 Stopping container...")
            container.stop(timeout=10)
            logger.info("✅ Container stopped")
        except Exception as e:
            logger.warning(f"⚠️  Error stopping container: {e}")
    
    async def test_server(self, server_path: Path, env_vars: Dict[str, str] = None) -> Dict[str, Any]:
        """Test an individual server"""
        server_name = server_path.name
        logger.info(f"🧪 Testing server: {server_name}")
        
        try:
            # Load server definition
            server_def = self.load_server_definition(server_path)
            image = server_def['deployment']['image']
            port = server_def['deployment']['port']
            
            # Run container
            container, base_url = self.run_docker_container(image, port, env_vars)
            
            try:
                # Wait for server to be ready
                if not await self.wait_for_server(base_url):
                    return {
                        "server": server_name,
                        "success": False,
                        "error": "Server failed to start within timeout",
                        "tests": []
                    }
                
                # Run functionality tests
                tests = await self.test_server_functionality(base_url, server_def)
                
                # Calculate overall success
                success = all(test.get('success', False) for test in tests)
                
                return {
                    "server": server_name,
                    "success": success,
                    "image": image,
                    "base_url": base_url,
                    "tests": tests,
                    "test_count": len(tests),
                    "passed_tests": sum(1 for test in tests if test.get('success', False)),
                    "failed_tests": sum(1 for test in tests if not test.get('success', False))
                }
                
            finally:
                self.stop_container(container)
                
        except Exception as e:
            logger.error(f"❌ Error testing server {server_name}: {e}")
            return {
                "server": server_name,
                "success": False,
                "error": str(e),
                "tests": []
            }
    
    async def test_all_servers(self, registry_path: Path, env_vars: Dict[str, str] = None) -> Dict[str, Any]:
        """Test all servers in the registry"""
        servers_dir = registry_path / "servers"
        
        if not servers_dir.exists():
            raise FileNotFoundError(f"Servers directory not found: {servers_dir}")
        
        server_dirs = [d for d in servers_dir.iterdir() if d.is_dir()]
        
        if not server_dirs:
            raise ValueError("No server directories found")
        
        logger.info(f"🧪 Testing {len(server_dirs)} servers...")
        
        results = []
        for server_dir in sorted(server_dirs):
            result = await self.test_server(server_dir, env_vars)
            results.append(result)
            self.test_results.append(result)
        
        # Calculate summary statistics
        total_servers = len(results)
        passed_servers = sum(1 for result in results if result.get('success', False))
        failed_servers = total_servers - passed_servers
        
        total_tests = sum(result.get('test_count', 0) for result in results)
        passed_tests = sum(result.get('passed_tests', 0) for result in results)
        failed_tests = sum(result.get('failed_tests', 0) for result in results)
        
        return {
            "summary": {
                "total_servers": total_servers,
                "passed_servers": passed_servers,
                "failed_servers": failed_servers,
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "failed_tests": failed_tests,
                "success_rate": passed_tests / total_tests if total_tests > 0 else 0
            },
            "results": results
        }
    
    def print_results(self, results: Dict[str, Any]) -> None:
        """Print test results in a formatted way"""
        summary = results['summary']
        
        print("\n" + "=" * 60)
        print("🧪 MCP SERVER TESTING RESULTS")
        print("=" * 60)
        
        print(f"📊 SUMMARY:")
        print(f"   Servers tested: {summary['total_servers']}")
        print(f"   ✅ Passed: {summary['passed_servers']}")
        print(f"   ❌ Failed: {summary['failed_servers']}")
        print(f"   🧪 Total tests: {summary['total_tests']}")
        print(f"   ✅ Passed tests: {summary['passed_tests']}")
        print(f"   ❌ Failed tests: {summary['failed_tests']}")
        print(f"   📈 Success rate: {summary['success_rate']:.1%}")
        
        print(f"\n📋 DETAILED RESULTS:")
        for result in results['results']:
            server_name = result['server']
            success = result.get('success', False)
            status = "✅" if success else "❌"
            
            print(f"\n{status} {server_name}")
            
            if 'error' in result:
                print(f"     Error: {result['error']}")
            else:
                passed = result.get('passed_tests', 0)
                failed = result.get('failed_tests', 0)
                print(f"     Tests: {passed} passed, {failed} failed")
                
                # Show individual test results
                for test in result.get('tests', []):
                    test_name = test.get('test', 'unknown')
                    test_success = test.get('success', False)
                    test_status = "✅" if test_success else "❌"
                    print(f"       {test_status} {test_name}")
                    
                    if not test_success and 'error' in test:
                        print(f"          Error: {test['error']}")


async def test_single_server(server_path: str, env_vars: Dict[str, str] = None) -> bool:
    """Test a single server directory"""
    tester = MCPServerTester()
    path = Path(server_path)
    
    print(f"🧪 Testing server: {path.name}")
    print("-" * 40)
    
    result = await tester.test_server(path, env_vars)
    
    # Print individual result
    success = result.get('success', False)
    status = "✅" if success else "❌"
    
    print(f"\n{status} {result['server']}")
    
    if 'error' in result:
        print(f"   Error: {result['error']}")
        return False
    
    passed = result.get('passed_tests', 0)
    failed = result.get('failed_tests', 0)
    print(f"   Tests: {passed} passed, {failed} failed")
    
    # Show test details
    for test in result.get('tests', []):
        test_name = test.get('test', 'unknown')
        test_success = test.get('success', False)
        test_status = "✅" if test_success else "❌"
        print(f"     {test_status} {test_name}")
        
        if 'response_time' in test:
            print(f"        Response time: {test['response_time']:.3f}s")
        
        if not test_success and 'error' in test:
            print(f"        Error: {test['error']}")
    
    return success


async def test_all_servers(registry_path: str, env_vars: Dict[str, str] = None) -> bool:
    """Test all servers in the registry"""
    tester = MCPServerTester()
    path = Path(registry_path)
    
    try:
        results = await tester.test_all_servers(path, env_vars)
        tester.print_results(results)
        
        return results['summary']['failed_servers'] == 0
        
    except Exception as e:
        print(f"❌ Testing failed: {e}")
        return False


def parse_env_vars(env_string: str) -> Dict[str, str]:
    """Parse environment variables from string format KEY=value,KEY2=value2"""
    if not env_string:
        return {}
    
    env_vars = {}
    for pair in env_string.split(','):
        if '=' in pair:
            key, value = pair.split('=', 1)
            env_vars[key.strip()] = value.strip()
    
    return env_vars


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test MCP servers")
    parser.add_argument(
        'target',
        nargs='?',
        help='Server directory to test, or --all for all servers'
    )
    parser.add_argument(
        '--all', 
        action='store_true',
        help='Test all servers in the registry'
    )
    parser.add_argument(
        '--env',
        help='Environment variables in format KEY=value,KEY2=value2'
    )
    parser.add_argument(
        '--timeout',
        type=int,
        default=30,
        help='Timeout in seconds for server startup (default: 30)'
    )
    
    args = parser.parse_args()
    
    # Parse environment variables
    env_vars = parse_env_vars(args.env) if args.env else None
    
    if args.all or args.target == '--all':
        # Test all servers
        registry_path = Path(__file__).parent.parent
        success = asyncio.run(test_all_servers(str(registry_path), env_vars))
    elif args.target:
        # Test single server
        success = asyncio.run(test_single_server(args.target, env_vars))
    else:
        print("Usage:")
        print("  python test_server.py <server_directory>     # Test single server")
        print("  python test_server.py --all                  # Test all servers")
        print("  python test_server.py --env KEY=value        # Set environment variables")
        print("  python test_server.py servers/echo           # Test specific server")
        sys.exit(1)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()