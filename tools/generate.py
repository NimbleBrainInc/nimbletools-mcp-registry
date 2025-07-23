#!/usr/bin/env python3
"""
Registry generation tool for NimbleTools Community MCP Registry

Generates the unified registry.yaml file from individual server definitions.
"""

import yaml
import json
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, date
import sys

class RegistryGenerator:
    """Generates the unified registry from server definitions"""
    
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.servers_dir = registry_path / "servers"
        self.output_path = registry_path / "registry.yaml"
        
        # Predefined categories
        self.categories = {
            "text-processing": {
                "displayName": "Text Processing",
                "description": "Tools for text manipulation, analysis, and transformation",
                "icon": "text"
            },
            "financial": {
                "displayName": "Financial Services", 
                "description": "Market data, trading, and financial analysis tools",
                "icon": "chart-line"
            },
            "testing": {
                "displayName": "Testing & Development",
                "description": "Tools for testing and development workflows", 
                "icon": "code"
            },
            "utilities": {
                "displayName": "Utilities",
                "description": "General-purpose utility tools and services",
                "icon": "tools"
            },
            "communication": {
                "displayName": "Communication",
                "description": "Messaging, notifications, and communication tools",
                "icon": "message"
            },
            "data-analytics": {
                "displayName": "Data Analytics",
                "description": "Data processing, analysis, and visualization tools",
                "icon": "chart-bar"
            },
            "cloud-services": {
                "displayName": "Cloud Services", 
                "description": "Integration with cloud platforms and services",
                "icon": "cloud"
            },
            "media": {
                "displayName": "Media Processing",
                "description": "Image, video, and audio processing tools",
                "icon": "image"
            },
            "security": {
                "displayName": "Security",
                "description": "Security, encryption, and authentication tools",
                "icon": "shield"
            },
            "experimental": {
                "displayName": "Experimental",
                "description": "Experimental and cutting-edge MCP services",
                "icon": "flask"
            }
        }
    
    def load_server_definition(self, server_path: Path) -> Dict[str, Any]:
        """Load a server definition from server.yaml"""
        server_yaml_path = server_path / "server.yaml"
        
        if not server_yaml_path.exists():
            raise FileNotFoundError(f"server.yaml not found in {server_path}")
        
        with open(server_yaml_path, 'r') as f:
            return yaml.safe_load(f)
    
    def transform_server_definition(self, server_data: Dict[str, Any]) -> Dict[str, Any]:
        """Transform server definition to registry format"""
        
        # Extract basic information
        result = {
            "name": server_data["name"],
            "displayName": server_data["about"]["displayName"], 
            "description": server_data["about"]["description"],
            "category": server_data["meta"]["category"],
            "image": server_data["deployment"]["image"],
            "repository": {
                "url": server_data["source"]["repository"],
                "branch": server_data["source"]["branch"],
                "dockerfile": server_data["source"].get("dockerfile", "Dockerfile")
            },
            "maintainer": {
                "name": server_data["maintainer"]["name"],
                "email": server_data["maintainer"]["email"]
            },
            "status": server_data["status"],
            "version": server_data["version"],
            "tags": server_data["meta"]["tags"],
            "license": server_data["meta"]["license"],
            "featured": server_data["meta"].get("featured", False),
            "tools": []
        }
        
        # Add optional fields
        if "organization" in server_data["maintainer"]:
            result["maintainer"]["organization"] = server_data["maintainer"]["organization"]
        
        if "github" in server_data["maintainer"]:
            result["maintainer"]["github"] = server_data["maintainer"]["github"]
        
        if "directory" in server_data["source"]:
            result["repository"]["directory"] = server_data["source"]["directory"]
        
        # Transform tools
        for tool in server_data.get("tools", []):
            tool_entry = {
                "name": tool["name"],
                "description": tool["description"],
                "inputSchema": tool["schema"]
            }
            
            if "examples" in tool:
                tool_entry["examples"] = tool["examples"]
            
            result["tools"].append(tool_entry)
        
        # Add credentials if present
        if server_data.get("credentials"):
            result["credentials"] = server_data["credentials"]
        else:
            result["credentials"] = []
        
        # Add deployment information
        result["deployment"] = {
            "port": server_data["deployment"]["port"],
            "healthPath": server_data["deployment"]["healthPath"]
        }
        
        if "resources" in server_data["deployment"]:
            result["deployment"]["resources"] = server_data["deployment"]["resources"]
        
        if "scaling" in server_data["deployment"]:
            result["deployment"]["scaling"] = server_data["deployment"]["scaling"]
        
        # Add about information
        result["about"] = {}
        for field in ["icon", "homepage", "documentation"]:
            if field in server_data["about"]:
                result["about"][field] = server_data["about"][field]
        
        # Add dates
        today = date.today().isoformat()
        result["created"] = today  # TODO: Extract from git history or changelog
        result["updated"] = today
        
        return result
    
    def generate_category_stats(self, servers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate category statistics"""
        category_counts = {}
        
        for server in servers:
            category = server["category"]
            category_counts[category] = category_counts.get(category, 0) + 1
        
        # Build category list with counts
        categories = []
        for cat_id, cat_info in self.categories.items():
            categories.append({
                "name": cat_id,
                "displayName": cat_info["displayName"],
                "description": cat_info["description"], 
                "icon": cat_info["icon"],
                "serverCount": category_counts.get(cat_id, 0)
            })
        
        return categories
    
    def generate_statistics(self, servers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate registry statistics"""
        active_servers = sum(1 for s in servers if s["status"] == "active")
        
        category_stats = {}
        for server in servers:
            category = server["category"]
            category_stats[category] = category_stats.get(category, 0) + 1
        
        return {
            "totalServers": len(servers),
            "activeServers": active_servers,
            "categories": category_stats,
            "lastGenerated": datetime.now().isoformat()
        }
    
    def generate_registry(self) -> Dict[str, Any]:
        """Generate the complete registry"""
        
        if not self.servers_dir.exists():
            raise FileNotFoundError(f"Servers directory not found: {self.servers_dir}")
        
        # Load all server definitions
        servers = []
        server_dirs = [d for d in self.servers_dir.iterdir() if d.is_dir()]
        
        print(f"Loading {len(server_dirs)} server definitions...")
        
        for server_dir in sorted(server_dirs):
            try:
                server_data = self.load_server_definition(server_dir)
                transformed = self.transform_server_definition(server_data)
                servers.append(transformed)
                print(f"✅ Loaded: {server_data['name']}")
            except Exception as e:
                print(f"❌ Failed to load {server_dir.name}: {e}")
                continue
        
        if not servers:
            raise RuntimeError("No valid server definitions found")
        
        # Generate categories with stats
        categories = self.generate_category_stats(servers)
        
        # Generate statistics
        statistics = self.generate_statistics(servers)
        
        # Build complete registry
        registry = {
            "apiVersion": "registry.nimbletools.ai/v1",
            "kind": "MCPRegistry",
            "metadata": {
                "name": "community-servers",
                "description": "Community-contributed MCP servers for the NimbleTools runtime platform",
                "version": "1.0.0",
                "lastUpdated": date.today().isoformat(),
                "generatedBy": "mcp-registry/tools/generate.py",
                "serverCount": len(servers)
            },
            "spec": {
                "autoDiscovery": True,
                "refreshInterval": "24h",
                "servers": servers,
                "categories": categories,
                "statistics": statistics
            }
        }
        
        return registry
    
    def save_registry(self, registry: Dict[str, Any]) -> None:
        """Save the registry to YAML file"""
        
        # Add generation header
        header = f"""# NimbleTools Community MCP Registry
# Generated automatically - DO NOT EDIT MANUALLY
# Generated on: {datetime.now().isoformat()}
# Total servers: {len(registry['spec']['servers'])}
#
# This file is consumed by the NimbleTools runtime platform for
# dynamic MCP server discovery and deployment.

"""
        
        with open(self.output_path, 'w') as f:
            f.write(header)
            yaml.dump(registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"\n✅ Registry generated: {self.output_path}")
        print(f"   📊 {len(registry['spec']['servers'])} servers")
        print(f"   📂 {len(registry['spec']['categories'])} categories")
        print(f"   📈 {registry['spec']['statistics']['activeServers']} active servers")


def main():
    """Main entry point"""
    registry_path = Path(__file__).parent.parent
    
    print("NimbleTools Community MCP Registry Generator")
    print("=" * 50)
    
    try:
        generator = RegistryGenerator(registry_path)
        registry = generator.generate_registry()
        generator.save_registry(registry)
        
        print("\n🎉 Registry generation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Registry generation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()