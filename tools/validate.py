#!/usr/bin/env python3
"""
Server validation tool for NimbleTools Community MCP Registry

Validates server.yaml files against the schema and performs additional checks.
"""

import json
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional
import jsonschema
import requests
from datetime import datetime
import re

class ServerValidator:
    """Validates MCP server definitions"""
    
    def __init__(self, schema_path: Optional[Path] = None):
        self.schema_path = schema_path or Path(__file__).parent.parent / "schemas" / "server-schema.yaml"
        self.schema = self._load_schema()
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def _load_schema(self) -> Dict[str, Any]:
        """Load the server schema"""
        try:
            with open(self.schema_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            raise RuntimeError(f"Failed to load schema from {self.schema_path}: {e}")
    
    def validate_server(self, server_path: Path) -> bool:
        """Validate a server directory"""
        self.errors.clear()
        self.warnings.clear()
        
        if not server_path.is_dir():
            self.errors.append(f"Server path {server_path} is not a directory")
            return False
        
        server_yaml_path = server_path / "server.yaml"
        
        # Check required files exist
        if not server_yaml_path.exists():
            self.errors.append("server.yaml file is missing")
            return False
        
        # Load and validate server.yaml
        try:
            with open(server_yaml_path, 'r') as f:
                server_data = yaml.safe_load(f)
        except Exception as e:
            self.errors.append(f"Failed to parse server.yaml: {e}")
            return False
        
        # Schema validation
        try:
            jsonschema.validate(server_data, self.schema)
        except jsonschema.ValidationError as e:
            self.errors.append(f"Schema validation failed: {e.message}")
            if e.absolute_path:
                self.errors.append(f"  at path: {' -> '.join(str(p) for p in e.absolute_path)}")
            return False
        except Exception as e:
            self.errors.append(f"Schema validation error: {e}")
            return False
        
        # Additional validation checks
        self._validate_server_name(server_data, server_path)
        self._validate_tools(server_data)
        self._validate_repository(server_data)
        self._validate_deployment(server_data)
        self._validate_changelog(server_data)
        
        return len(self.errors) == 0
    
    def _validate_server_name(self, server_data: Dict[str, Any], server_path: Path) -> None:
        """Validate server name matches directory name"""
        server_name = server_data.get('name', '')
        dir_name = server_path.name
        
        if server_name != dir_name:
            self.errors.append(f"Server name '{server_name}' doesn't match directory name '{dir_name}'")
    
    def _validate_tools(self, server_data: Dict[str, Any]) -> None:
        """Validate tool definitions"""
        capabilities = server_data.get('capabilities', {})
        tools = capabilities.get('tools', [])
        
        if not tools:
            self.errors.append("At least one tool must be defined")
            return
        
        tool_names = set()
        for i, tool in enumerate(tools):
            tool_name = tool.get('name', '')
            
            # Check for duplicate tool names
            if tool_name in tool_names:
                self.errors.append(f"Duplicate tool name '{tool_name}' at index {i}")
            tool_names.add(tool_name)
            
            # Validate tool name format
            if not re.match(r'^[a-z][a-z0-9_]*$', tool_name):
                self.errors.append(f"Tool name '{tool_name}' must start with lowercase letter and contain only lowercase letters, numbers, and underscores")
            
            # Validate schema structure
            schema = tool.get('schema', {})
            if schema.get('type') != 'object':
                self.errors.append(f"Tool '{tool_name}' schema must have type 'object'")
            
            if 'properties' not in schema:
                self.errors.append(f"Tool '{tool_name}' schema must have 'properties'")
    
    def _validate_repository(self, server_data: Dict[str, Any]) -> None:
        """Validate repository information"""
        source = server_data.get('source', {})
        repo_url = source.get('repository', '')
        
        if not repo_url.startswith('https://github.com/'):
            self.errors.append("Repository must be a GitHub HTTPS URL")
            return
        
        # Extract owner/repo from URL
        try:
            parts = repo_url.replace('https://github.com/', '').split('/')
            if len(parts) != 2:
                raise ValueError("Invalid format")
            owner, repo = parts
            
            # Basic validation of owner/repo names
            if not re.match(r'^[a-zA-Z0-9-_]+$', owner) or not re.match(r'^[a-zA-Z0-9-_]+$', repo):
                self.errors.append("Repository owner and name must contain only alphanumeric characters, hyphens, and underscores")
        except:
            self.errors.append("Invalid GitHub repository URL format")
    
    def _validate_deployment(self, server_data: Dict[str, Any]) -> None:
        """Validate deployment configuration"""
        deployment = server_data.get('deployment', {})
        deployment_type = deployment.get('type', 'http')
        
        if deployment_type == 'http':
            health_path = deployment.get('healthPath', '/health')
            if not health_path.startswith('/'):
                self.errors.append("Health path must start with '/'")
        elif deployment_type == 'stdio':
            if 'healthPath' in deployment:
                self.warnings.append("Health path not applicable for stdio deployment type")
    
    def _validate_changelog(self, server_data: Dict[str, Any]) -> None:
        """Validate changelog format"""
        changelog = server_data.get('changelog', [])
        
        if not changelog:
            self.warnings.append("Changelog is empty - consider adding version history")
            return
        
        current_version = server_data.get('version', '')
        
        # Check if current version is in changelog
        changelog_versions = [entry.get('version', '') for entry in changelog]
        if current_version not in changelog_versions:
            self.warnings.append(f"Current version '{current_version}' not found in changelog")
        
        # Validate changelog entry format
        for i, entry in enumerate(changelog):
            if not isinstance(entry.get('changes'), list):
                self.errors.append(f"Changelog entry {i} must have 'changes' as a list")
            
            # Validate date format
            date_str = entry.get('date', '')
            try:
                datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                self.errors.append(f"Changelog entry {i} has invalid date format '{date_str}' (expected YYYY-MM-DD)")


def validate_single_server(server_path: str) -> bool:
    """Validate a single server directory"""
    validator = ServerValidator()
    path = Path(server_path)
    
    print(f"Validating server: {path.name}")
    print("-" * 40)
    
    is_valid = validator.validate_server(path)
    
    # Print results
    if validator.errors:
        print("❌ ERRORS:")
        for error in validator.errors:
            print(f"  • {error}")
    
    if validator.warnings:
        print("⚠️  WARNINGS:")
        for warning in validator.warnings:
            print(f"  • {warning}")
    
    if is_valid and not validator.warnings:
        print("✅ Server validation passed!")
    elif is_valid:
        print("✅ Server validation passed with warnings")
    else:
        print("❌ Server validation failed")
    
    print()
    return is_valid


def validate_all_servers(registry_path: str) -> bool:
    """Validate all servers in the registry"""
    registry = Path(registry_path)
    servers_dir = registry / "servers"
    
    if not servers_dir.exists():
        print(f"❌ Servers directory not found: {servers_dir}")
        return False
    
    server_dirs = [d for d in servers_dir.iterdir() if d.is_dir()]
    
    if not server_dirs:
        print("❌ No server directories found")
        return False
    
    print(f"Validating {len(server_dirs)} servers...")
    print("=" * 50)
    
    all_valid = True
    results = []
    
    for server_dir in sorted(server_dirs):
        validator = ServerValidator()
        is_valid = validator.validate_server(server_dir)
        
        results.append({
            'name': server_dir.name,
            'valid': is_valid,
            'errors': len(validator.errors),
            'warnings': len(validator.warnings)
        })
        
        if not is_valid:
            all_valid = False
        
        # Print individual results
        status = "✅" if is_valid else "❌"
        warning_text = f" ({len(validator.warnings)} warnings)" if validator.warnings else ""
        print(f"{status} {server_dir.name}{warning_text}")
        
        if validator.errors:
            for error in validator.errors:
                print(f"     • {error}")
    
    # Print summary
    print("\n" + "=" * 50)
    print("VALIDATION SUMMARY")
    print("=" * 50)
    
    valid_count = sum(1 for r in results if r['valid'])
    total_errors = sum(r['errors'] for r in results)
    total_warnings = sum(r['warnings'] for r in results)
    
    print(f"Servers validated: {len(results)}")
    print(f"Valid servers: {valid_count}")
    print(f"Failed servers: {len(results) - valid_count}")
    print(f"Total errors: {total_errors}")
    print(f"Total warnings: {total_warnings}")
    
    if all_valid:
        print("\n🎉 All servers passed validation!")
    else:
        print("\n❌ Some servers failed validation")
    
    return all_valid


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python validate.py <server_directory>     # Validate single server")
        print("  python validate.py --all                  # Validate all servers")
        print("  python validate.py servers/echo           # Validate specific server")
        sys.exit(1)
    
    if sys.argv[1] == "--all":
        # Validate all servers
        registry_path = Path(__file__).parent.parent
        success = validate_all_servers(str(registry_path))
    else:
        # Validate single server
        server_path = sys.argv[1]
        success = validate_single_server(server_path)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()