#!/usr/bin/env python3
"""
Interactive wizard for creating new MCP server definitions
"""

import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List
import re
from datetime import date

class ServerWizard:
    """Interactive wizard for creating server definitions"""
    
    def __init__(self):
        self.registry_path = Path(__file__).parent.parent
        self.servers_dir = self.registry_path / "servers"
        
        # Predefined categories
        self.categories = {
            "text-processing": "Text Processing - Text manipulation, analysis, and transformation",
            "financial": "Financial Services - Market data, trading, and financial analysis",
            "testing": "Testing & Development - Tools for testing and development workflows",
            "utilities": "Utilities - General-purpose utility tools and services", 
            "communication": "Communication - Messaging, notifications, and communication tools",
            "data-analytics": "Data Analytics - Data processing, analysis, and visualization",
            "cloud-services": "Cloud Services - Integration with cloud platforms and services",
            "media": "Media Processing - Image, video, and audio processing tools",
            "security": "Security - Security, encryption, and authentication tools",
            "experimental": "Experimental - Experimental and cutting-edge MCP services"
        }
    
    def prompt_input(self, question: str, default: str = None, validator=None) -> str:
        """Prompt for user input with validation"""
        while True:
            if default:
                response = input(f"{question} [{default}]: ").strip()
                if not response:
                    response = default
            else:
                response = input(f"{question}: ").strip()
            
            if not response:
                print("❌ This field is required. Please enter a value.")
                continue
            
            if validator:
                error = validator(response)
                if error:
                    print(f"❌ {error}")
                    continue
            
            return response
    
    def prompt_choice(self, question: str, choices: Dict[str, str]) -> str:
        """Prompt for choice from options"""
        print(f"\n{question}")
        for i, (key, desc) in enumerate(choices.items(), 1):
            print(f"  {i}. {key} - {desc}")
        
        while True:
            try:
                choice = int(input("\nEnter choice number: ").strip())
                if 1 <= choice <= len(choices):
                    return list(choices.keys())[choice - 1]
                else:
                    print(f"❌ Please enter a number between 1 and {len(choices)}")
            except ValueError:
                print("❌ Please enter a valid number")
    
    def prompt_yes_no(self, question: str, default: bool = False) -> bool:
        """Prompt for yes/no answer"""
        default_text = "y/N" if not default else "Y/n"
        response = input(f"{question} [{default_text}]: ").strip().lower()
        
        if not response:
            return default
        
        return response in ['y', 'yes', 'true', '1']
    
    def prompt_list(self, question: str, example: str = None) -> List[str]:
        """Prompt for comma-separated list"""
        example_text = f" (example: {example})" if example else ""
        response = input(f"{question}{example_text}: ").strip()
        
        if not response:
            return []
        
        return [item.strip() for item in response.split(',') if item.strip()]
    
    def validate_server_name(self, name: str) -> str:
        """Validate server name format"""
        if not re.match(r'^[a-z][a-z0-9-]*[a-z0-9]$', name):
            return "Server name must start with lowercase letter, contain only lowercase letters, numbers, and hyphens, and end with alphanumeric character"
        
        if len(name) < 2 or len(name) > 50:
            return "Server name must be between 2 and 50 characters"
        
        # Check if directory already exists
        server_dir = self.servers_dir / name
        if server_dir.exists():
            return f"Server directory '{name}' already exists"
        
        return None
    
    def validate_version(self, version: str) -> str:
        """Validate semantic version"""
        if not re.match(r'^\d+\.\d+\.\d+(-[a-zA-Z0-9.-]+)?(\+[a-zA-Z0-9.-]+)?$', version):
            return "Version must follow semantic versioning (e.g., 1.0.0, 1.2.3-beta.1)"
        return None
    
    def validate_email(self, email: str) -> str:
        """Validate email format"""
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            return "Please enter a valid email address"
        return None
    
    def validate_github_url(self, url: str) -> str:
        """Validate GitHub repository URL"""
        if not url.startswith('https://github.com/'):
            return "Repository must be a GitHub HTTPS URL (https://github.com/owner/repo)"
        
        try:
            parts = url.replace('https://github.com/', '').split('/')
            if len(parts) != 2:
                raise ValueError("Invalid format")
            owner, repo = parts
            
            if not re.match(r'^[a-zA-Z0-9-_]+$', owner) or not re.match(r'^[a-zA-Z0-9-_]+$', repo):
                return "Repository owner and name must contain only alphanumeric characters, hyphens, and underscores"
        except:
            return "Invalid GitHub repository URL format (expected: https://github.com/owner/repo)"
        
        return None
    
    def validate_docker_image(self, image: str) -> str:
        """Validate Docker image format"""
        if not re.match(r'^[a-z0-9-_./]+:[a-zA-Z0-9-_.]+$', image):
            return "Invalid Docker image format (expected: registry/image:tag)"
        return None
    
    def validate_tool_name(self, name: str) -> str:
        """Validate tool name format"""
        if not re.match(r'^[a-z][a-z0-9_]*$', name):
            return "Tool name must start with lowercase letter and contain only lowercase letters, numbers, and underscores"
        return None
    
    def collect_basic_info(self) -> Dict[str, Any]:
        """Collect basic server information"""
        print("\n🚀 Creating new MCP server definition")
        print("=" * 40)
        
        name = self.prompt_input("Server name", validator=self.validate_server_name)
        version = self.prompt_input("Version", "1.0.0", self.validate_version)
        
        # Status
        status_choices = {
            "active": "Ready for production use",
            "experimental": "In development, may change",
            "maintenance": "Maintenance mode only"
        }
        status = self.prompt_choice("Server status", status_choices)
        
        return {
            "name": name,
            "version": version,
            "status": status
        }
    
    def collect_metadata(self) -> Dict[str, Any]:
        """Collect server metadata"""
        print("\n📋 Server Metadata")
        print("-" * 20)
        
        category = self.prompt_choice("Category", self.categories)
        tags = self.prompt_list("Tags (comma-separated)", "api, data, analysis")
        
        if not tags:
            tags = [category.replace("-", "")]
        
        license = self.prompt_input("License", "MIT")
        featured = self.prompt_yes_no("Featured in marketplace?", False)
        
        return {
            "category": category,
            "tags": tags,
            "license": license,
            "featured": featured
        }
    
    def collect_about_info(self) -> Dict[str, Any]:
        """Collect display information"""
        print("\n📝 Display Information")
        print("-" * 20)
        
        display_name = self.prompt_input("Display name")
        description = self.prompt_input("Description")
        
        # Optional fields
        homepage = input("Homepage URL (optional): ").strip()
        documentation = input("Documentation URL (optional): ").strip()
        icon = input("Icon URL (optional): ").strip()
        
        about = {
            "displayName": display_name,
            "description": description
        }
        
        if homepage:
            about["homepage"] = homepage
        if documentation:
            about["documentation"] = documentation
        if icon:
            about["icon"] = icon
        
        return about
    
    def collect_maintainer_info(self) -> Dict[str, Any]:
        """Collect maintainer information"""
        print("\n👤 Maintainer Information")
        print("-" * 25)
        
        name = self.prompt_input("Maintainer name")
        email = self.prompt_input("Email", validator=self.validate_email)
        
        # Optional fields
        organization = input("Organization (optional): ").strip()
        github = input("GitHub username (optional): ").strip()
        
        maintainer = {
            "name": name,
            "email": email
        }
        
        if organization:
            maintainer["organization"] = organization
        if github:
            maintainer["github"] = github
        
        return maintainer
    
    def collect_source_info(self) -> Dict[str, Any]:
        """Collect source code information"""
        print("\n📦 Source Code")
        print("-" * 15)
        
        repository = self.prompt_input("GitHub repository URL", validator=self.validate_github_url)
        branch = self.prompt_input("Branch", "main")
        dockerfile = self.prompt_input("Dockerfile path", "Dockerfile")
        
        source = {
            "repository": repository,
            "branch": branch,
            "dockerfile": dockerfile
        }
        
        directory = input("Source directory (optional): ").strip()
        if directory:
            source["directory"] = directory
        
        return source
    
    def collect_deployment_info(self) -> Dict[str, Any]:
        """Collect deployment configuration"""
        print("\n🚀 Deployment Configuration")
        print("-" * 28)
        
        image = self.prompt_input("Docker image", validator=self.validate_docker_image)
        port = int(self.prompt_input("Port", "8000"))
        health_path = self.prompt_input("Health check path", "/health")
        
        deployment = {
            "image": image,
            "port": port,
            "healthPath": health_path
        }
        
        # Optional resource configuration
        if self.prompt_yes_no("Configure resource limits?", False):
            print("\nResource requests:")
            cpu_request = input("CPU request (e.g., 25m): ").strip()
            memory_request = input("Memory request (e.g., 32Mi): ").strip()
            
            print("\nResource limits:")
            cpu_limit = input("CPU limit (e.g., 100m): ").strip()
            memory_limit = input("Memory limit (e.g., 64Mi): ").strip()
            
            if any([cpu_request, memory_request, cpu_limit, memory_limit]):
                resources = {}
                if cpu_request or memory_request:
                    requests = {}
                    if cpu_request:
                        requests["cpu"] = cpu_request
                    if memory_request:
                        requests["memory"] = memory_request
                    resources["requests"] = requests
                
                if cpu_limit or memory_limit:
                    limits = {}
                    if cpu_limit:
                        limits["cpu"] = cpu_limit
                    if memory_limit:
                        limits["memory"] = memory_limit
                    resources["limits"] = limits
                
                deployment["resources"] = resources
        
        # Optional scaling configuration
        if self.prompt_yes_no("Configure auto-scaling?", False):
            min_replicas = int(self.prompt_input("Minimum replicas", "0"))
            max_replicas = int(self.prompt_input("Maximum replicas", "3"))
            target_concurrency = int(self.prompt_input("Target concurrency", "10"))
            
            deployment["scaling"] = {
                "minReplicas": min_replicas,
                "maxReplicas": max_replicas,
                "targetConcurrency": target_concurrency
            }
        
        return deployment
    
    def collect_tools(self) -> List[Dict[str, Any]]:
        """Collect tool definitions"""
        print("\n🔧 Tool Definitions")
        print("-" * 18)
        
        tools = []
        
        while True:
            tool_name = self.prompt_input("Tool name", validator=self.validate_tool_name)
            tool_description = self.prompt_input("Tool description")
            
            # Simple schema creation
            print("\nTool parameters (press Enter when done):")
            properties = {}
            required = []
            
            while True:
                param_name = input("Parameter name (or Enter to finish): ").strip()
                if not param_name:
                    break
                
                param_type = self.prompt_choice(f"Type for '{param_name}'", {
                    "string": "Text string",
                    "number": "Numeric value",
                    "boolean": "True/false value",
                    "object": "JSON object",
                    "array": "List of values"
                })
                
                param_desc = self.prompt_input(f"Description for '{param_name}'")
                is_required = self.prompt_yes_no(f"Is '{param_name}' required?", True)
                
                properties[param_name] = {
                    "type": param_type,
                    "description": param_desc
                }
                
                if is_required:
                    required.append(param_name)
            
            tool = {
                "name": tool_name,
                "description": tool_description,
                "schema": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
            
            tools.append(tool)
            
            if not self.prompt_yes_no("Add another tool?", False):
                break
        
        return tools
    
    def collect_credentials(self) -> List[Dict[str, Any]]:
        """Collect credential requirements"""
        if not self.prompt_yes_no("\nDoes this server require credentials/API keys?", False):
            return []
        
        print("\n🔐 Credential Requirements")
        print("-" * 26)
        
        credentials = []
        
        while True:
            name = self.prompt_input("Environment variable name (e.g., API_KEY)")
            description = self.prompt_input("Description")
            required = self.prompt_yes_no("Required?", True)
            
            credential = {
                "name": name,
                "description": description,
                "required": required
            }
            
            example = input("Example value format (optional): ").strip()
            if example:
                credential["example"] = example
            
            link = input("Link to obtain credential (optional): ").strip()
            if link:
                credential["link"] = link
            
            credentials.append(credential)
            
            if not self.prompt_yes_no("Add another credential?", False):
                break
        
        return credentials
    
    def create_server_definition(self) -> Dict[str, Any]:
        """Create complete server definition"""
        print("🎯 NimbleTools Community MCP Registry - Server Creation Wizard")
        print("=" * 65)
        
        # Collect all information
        basic = self.collect_basic_info()
        meta = self.collect_metadata()
        about = self.collect_about_info()
        maintainer = self.collect_maintainer_info()
        source = self.collect_source_info()
        deployment = self.collect_deployment_info()
        tools = self.collect_tools()
        credentials = self.collect_credentials()
        
        # Build complete definition
        server_def = {
            **basic,
            "meta": meta,
            "about": about,
            "maintainer": maintainer,
            "source": source,
            "deployment": deployment,
            "tools": tools,
            "credentials": credentials,
            "changelog": [
                {
                    "version": basic["version"],
                    "date": date.today().isoformat(),
                    "changes": [
                        "Initial server definition created"
                    ]
                }
            ]
        }
        
        return server_def
    
    def save_server_definition(self, server_def: Dict[str, Any]) -> None:
        """Save server definition to file"""
        server_name = server_def["name"]
        server_dir = self.servers_dir / server_name
        
        # Create directory
        server_dir.mkdir(parents=True, exist_ok=True)
        
        # Save server.yaml
        server_yaml_path = server_dir / "server.yaml"
        with open(server_yaml_path, 'w') as f:
            yaml.dump(server_def, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"\n✅ Server definition saved: {server_yaml_path}")
        print(f"📁 Server directory: {server_dir}")
        
        # Next steps
        print("\n📋 Next Steps:")
        print("1. Review and edit the generated server.yaml if needed")
        print("2. Validate your server definition:")
        print(f"   python tools/validate.py servers/{server_name}")
        print("3. Test the server locally with Docker")
        print("4. Submit a pull request to add your server to the registry")


def main():
    """Main entry point"""
    if len(sys.argv) > 1 and sys.argv[1] == "--create-server":
        wizard = ServerWizard()
        
        try:
            server_def = wizard.create_server_definition()
            wizard.save_server_definition(server_def)
            
            print("\n🎉 Server definition created successfully!")
            
        except KeyboardInterrupt:
            print("\n\n👋 Server creation cancelled")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Error creating server: {e}")
            sys.exit(1)
    else:
        print("Usage: python wizard.py --create-server")
        sys.exit(1)


if __name__ == "__main__":
    main()