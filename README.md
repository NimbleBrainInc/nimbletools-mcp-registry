# NimbleTools Community MCP Registry

A curated registry of community-contributed Model Context Protocol (MCP) servers for the NimbleTools runtime platform, providing secure, scalable, and enterprise-ready AI tool integration.

## Overview

This registry serves as the central catalog for community MCP servers that can be dynamically deployed and executed within the NimbleTools runtime. NimbleTools is the MCP server runtime and SaaS platform offered by NimbleBrain, enabling organizations to securely integrate and scale AI tools. Each server is containerized, validated, and maintained following enterprise security standards.

## Repository Structure

```
mcp-registry/
├── servers/                     # Individual server definitions
│   ├── ...
│   │   └── server.yaml          # Server metadata and configuration
├── schemas/                     # Schema definitions
│   ├── server-schema.yaml       # Server definition schema
│   └── registry-schema.yaml     # Registry format schema
├── tools/                       # Registry management tools
│   ├── validate.py              # Schema validation
│   ├── generate.py              # Registry generation
│   └── wizard.py                # Interactive server creation
├── .github/workflows/           # CI/CD automation
├── docs/                        # Documentation
├── registry.yaml                # Generated registry (DO NOT EDIT)
└── CONTRIBUTING.md              # Contribution guidelines
```

## Quick Start

### For Server Maintainers

1. **Create a new server entry:**

   ```bash
   python tools/wizard.py --create-server my-server
   ```

2. **Validate your server definition:**

   ```bash
   python tools/validate.py servers/my-server/
   ```

3. **Submit via pull request** following our [contribution guidelines](CONTRIBUTING.md)

### For NimbleTools Platform Integration

The registry automatically generates `registry.yaml` from individual server definitions for consumption by the NimbleTools runtime:

```bash
python tools/generate.py
```

## Server Categories

- **Text Processing**: Text manipulation, analysis, and transformation
- **Financial**: Market data, trading, and financial analysis tools
- **Testing & Development**: Testing and development workflow tools
- **Utilities**: General-purpose utility tools and services
- **Communication**: Messaging, notifications, and communication tools
- **Data Analytics**: Data processing, analysis, and visualization
- **Cloud Services**: Integration with cloud platforms and services
- **Media**: Image, video, and audio processing tools
- **Security**: Security, encryption, and authentication tools
- **Experimental**: Cutting-edge and experimental MCP services

## Quality Standards

All servers in this registry must meet:

- ✅ **Security**: Container security best practices
- ✅ **Documentation**: Comprehensive README and tool descriptions
- ✅ **Testing**: Automated tests and validation
- ✅ **MCP Compliance**: Full MCP protocol compatibility
- ✅ **Containerization**: Docker-based deployment
- ✅ **Health Checks**: Proper health and readiness endpoints

## Migration Status

This registry is actively migrating from the monolithic `community-registry.yaml` format to the new distributed structure:

- ✅ **Phase 1**: Repository structure and tooling
- 🔄 **Phase 2**: Server migration and automation
- ⏳ **Phase 3**: Community contribution process
- ⏳ **Phase 4**: Security and governance enhancements

## Contributing

We welcome community contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- Adding new servers
- Updating existing servers
- Reporting issues
- Development workflow

## License

This registry is licensed under the MIT License. Individual servers may have their own licenses as specified in their metadata.

## Support

- **Issues**: [GitHub Issues](https://github.com/NimbleBrainInc/mcp-registry/issues)
- **Discussions**: [GitHub Discussions](https://github.com/NimbleBrainInc/mcp-registry/discussions)
- **NimbleTools Platform**: [nimbletools.ai](https://nimbletools.ai)
- **Email**: hello@nimblebrain.ai
