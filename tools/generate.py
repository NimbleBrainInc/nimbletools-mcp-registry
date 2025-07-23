#!/usr/bin/env python3
"""
Registry generation tool for NimbleTools Community MCP Registry

Generates the simplified registry.yaml file and handles nimbletools.yaml ingestion.
"""

import yaml
import json
import os
import shutil
from pathlib import Path
from typing import Dict, Any, List
from datetime import datetime, date
import sys

class RegistryGenerator:
    """Generates the unified registry from server definitions and ingests nimbletools.yaml files"""
    
    def __init__(self, registry_path: Path):
        self.registry_path = registry_path
        self.servers_dir = registry_path / "servers"
        self.output_path = registry_path / "registry.yaml"
        
        # Note: Auto-ingestion removed - servers should be added manually
        # External contributors create server.yaml files directly
        pass

    def load_server_definition(self, server_path: Path) -> Dict[str, Any]:
        """Load a server definition from server.yaml"""
        server_yaml_path = server_path / "server.yaml"
        
        if not server_yaml_path.exists():
            raise FileNotFoundError(f"server.yaml not found in {server_path}")
        
        with open(server_yaml_path, 'r') as f:
            return yaml.safe_load(f)
    
    def generate_registry(self) -> Dict[str, Any]:
        """Generate the complete registry with full server specs"""
        
        if not self.servers_dir.exists():
            raise FileNotFoundError(f"Servers directory not found: {self.servers_dir}")
        
        # Load all server definitions (complete specs)
        servers = []
        server_dirs = [d for d in self.servers_dir.iterdir() if d.is_dir()]
        
        print(f"Loading {len(server_dirs)} server definitions...")
        
        for server_dir in sorted(server_dirs):
            try:
                server_data = self.load_server_definition(server_dir)
                servers.append(server_data)  # Use complete server spec, no transformation
                print(f"✅ Loaded: {server_data['name']}")
            except Exception as e:
                print(f"❌ Failed to load {server_dir.name}: {e}")
                continue
        
        if not servers:
            raise RuntimeError("No valid server definitions found")
        
        # Build simplified registry with complete server specs
        registry = {
            "apiVersion": "registry.nimbletools.ai/v1",
            "kind": "MCPRegistry",
            "metadata": {
                "name": "community-servers",
                "description": "Community-contributed MCP servers for the NimbleTools runtime platform",
                "version": "2.0.0",
                "lastUpdated": date.today().isoformat(),
                "generatedBy": "mcp-registry/tools/generate.py"
            },
            "servers": servers  # Full server specs directly in registry
        }
        
        return registry
    
    def save_registry(self, registry: Dict[str, Any]) -> None:
        """Save the registry to YAML file"""
        
        # Add generation header
        header = f"""# NimbleTools Community MCP Registry
# Contains complete server specifications - no external dependencies
# Generated automatically - DO NOT EDIT MANUALLY
# Generated on: {datetime.now().isoformat()}
# Total servers: {len(registry['servers'])}

"""
        
        with open(self.output_path, 'w') as f:
            f.write(header)
            yaml.dump(registry, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
        
        print(f"\n✅ Registry generated: {self.output_path}")
        print(f"   📊 {len(registry['servers'])} servers")
        
        # Show server summary
        active_count = sum(1 for s in registry['servers'] if s.get('status') == 'active')
        print(f"   📈 {active_count} active servers")


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