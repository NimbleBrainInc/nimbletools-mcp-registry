#!/usr/bin/env python3
"""
CLI tool for NimbleTools Community MCP Registry management
"""

import click
import sys
from pathlib import Path

# Import our tools
from .validate import validate_single_server, validate_all_servers
from .generate import RegistryGenerator


@click.group()
@click.version_option()
def cli():
    """NimbleTools Community MCP Registry management CLI"""
    pass


@cli.command()
@click.argument('server_path', required=False)
@click.option('--all', 'validate_all', is_flag=True, help='Validate all servers')
def validate(server_path, validate_all):
    """Validate server definitions"""
    if validate_all:
        registry_path = Path(__file__).parent.parent
        success = validate_all_servers(str(registry_path))
    elif server_path:
        success = validate_single_server(server_path)
    else:
        click.echo("Error: Must specify server path or --all flag")
        click.echo("Usage: mcp-registry validate <server_path>")
        click.echo("       mcp-registry validate --all")
        sys.exit(1)
    
    sys.exit(0 if success else 1)


@cli.command()
@click.option('--output', '-o', help='Output file (default: registry.yaml)')
def generate(output):
    """Generate registry.yaml from server definitions"""
    registry_path = Path(__file__).parent.parent
    
    try:
        generator = RegistryGenerator(registry_path)
        
        if output:
            generator.output_path = Path(output)
        
        registry = generator.generate_registry()
        generator.save_registry(registry)
        
        click.echo("✅ Registry generation completed successfully!")
        
    except Exception as e:
        click.echo(f"❌ Registry generation failed: {e}")
        sys.exit(1)


@cli.command()
def check():
    """Run full validation and generation check"""
    registry_path = Path(__file__).parent.parent
    
    click.echo("🔍 Running full registry check...")
    click.echo("=" * 50)
    
    # Step 1: Validate all servers
    click.echo("Step 1: Validating all servers...")
    validation_success = validate_all_servers(str(registry_path))
    
    if not validation_success:
        click.echo("\n❌ Validation failed - aborting check")
        sys.exit(1)
    
    # Step 2: Generate registry
    click.echo("\nStep 2: Generating registry...")
    try:
        generator = RegistryGenerator(registry_path)
        registry = generator.generate_registry()
        generator.save_registry(registry)
    except Exception as e:
        click.echo(f"❌ Registry generation failed: {e}")
        sys.exit(1)
    
    click.echo("\n🎉 Full registry check completed successfully!")


@cli.command()
@click.argument('server_path', required=False)
@click.option('--all', 'test_all', is_flag=True, help='Test all servers')
@click.option('--env', help='Environment variables (KEY=value,KEY2=value2)')
def test(server_path, test_all, env):
    """Test server functionality with Docker"""
    import asyncio
    from .test_server import test_single_server, test_all_servers, parse_env_vars
    
    # Parse environment variables
    env_vars = parse_env_vars(env) if env else None
    
    if test_all:
        registry_path = Path(__file__).parent.parent
        success = asyncio.run(test_all_servers(str(registry_path), env_vars))
    elif server_path:
        success = asyncio.run(test_single_server(server_path, env_vars))
    else:
        click.echo("Error: Must specify server path or --all flag")
        click.echo("Usage: mcp-registry test <server_path>")
        click.echo("       mcp-registry test --all")
        sys.exit(1)
    
    sys.exit(0 if success else 1)

@cli.command()
def stats():
    """Show registry statistics"""
    registry_path = Path(__file__).parent.parent
    servers_dir = registry_path / "servers"
    
    if not servers_dir.exists():
        click.echo("❌ Servers directory not found")
        sys.exit(1)
    
    server_dirs = [d for d in servers_dir.iterdir() if d.is_dir()]
    
    click.echo("📊 Registry Statistics")
    click.echo("=" * 30)
    click.echo(f"Total servers: {len(server_dirs)}")
    
    if server_dirs:
        click.echo("\nServers:")
        for server_dir in sorted(server_dirs):
            click.echo(f"  • {server_dir.name}")


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()