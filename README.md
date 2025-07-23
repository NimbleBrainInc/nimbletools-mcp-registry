# 🌟 NimbleTools Community MCP Registry

[![Servers](https://img.shields.io/badge/servers-4-blue)](#available-servers) [![License](https://img.shields.io/badge/license-MIT-green)](LICENSE) [![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](#-contributing)

> A curated, community-driven registry of Model Context Protocol (MCP) servers for the NimbleTools ecosystem. Discover, share, and deploy MCP servers with clean separation of functionality and infrastructure.

## 🎯 What is this?

The NimbleTools Community MCP Registry is the **central catalog** for community-contributed MCP servers. It provides:

- 🔍 **Discoverable** - Browse available MCP servers and their capabilities
- 🛡️ **Validated** - All servers pass schema validation and quality checks
- 🚀 **Deploy-Ready** - Clean specs ready for any deployment platform
- 🌍 **Community-Driven** - Open source contributions from developers worldwide

## 🚀 Quick Start

### 🔧 For Users

Browse available servers in our [registry](registry.yaml) or see the [Available Servers](#available-servers) section below.

### 👩‍💻 For Contributors

Ready to add your MCP server? It's easy!

1. **Fork this repository**
2. **Add your server** (see [Contributing Guide](#-contributing))
3. **Submit a pull request**

We welcome servers for:

- 📝 Text processing and analysis
- 💰 Financial data and market information
- 🌐 Web APIs and integrations
- 🛠️ Developer tools and utilities
- 📊 Data analytics and visualization
- 🎮 Games and entertainment
- 🔒 Security and authentication
- 🤖 AI and machine learning tools

## 📦 Available Servers

| Name                                                | Category        | Description                                                | Status    | Maintainer      |
| --------------------------------------------------- | --------------- | ---------------------------------------------------------- | --------- | --------------- |
| **[echo](servers/echo/)**                           | Testing         | Simple echo service for testing MCP protocol functionality | ✅ Active | NimbleBrain Inc |
| **[reverse-text](servers/reverse-text/)**           | Text Processing | Text manipulation with reverse and analysis tools          | ✅ Active | NimbleBrain Inc |
| **[finnhub](servers/finnhub/)**                     | Financial       | Real-time stock quotes, market data, and financial news    | ✅ Active | NimbleBrain Inc |
| **[nationalparks-mcp](servers/nationalparks-mcp/)** | Utilities       | U.S. National Parks information and data                   | ✅ Active | Tang Sheng      |

**Want to see your server here?** [Add it to the registry!](#-contributing)

## 🏗️ Architecture

### Core Principles

- **🎯 Functionality First**: Server specs focus purely on capabilities (tools, resources, prompts)
- **🏗️ Infrastructure Agnostic**: No Docker images, resource limits, or deployment configs
- **📋 Schema Driven**: Strong validation ensures consistency and quality
- **🔗 GitHub Based**: Server definitions reference source repositories
- **📦 Self-Contained**: Complete specs with no external dependencies

### Repository Structure

```
nimbletools-mcp-registry/
├── 📁 servers/                  # Server definitions
│   ├── 📁 echo/
│   │   └── 📄 server.yaml       # Echo server spec
│   ├── 📁 reverse-text/
│   │   └── 📄 server.yaml       # Text processing server spec
│   └── 📁 finnhub/
│       └── 📄 server.yaml       # Financial data server spec
├── 📁 schemas/                  # Validation schemas
│   ├── 📄 server-schema.yaml    # Server specification schema
│   └── 📄 registry-schema.yaml  # Registry format schema
├── 📁 tools/                    # Registry management CLI
│   ├── 📄 cli.py               # Main CLI interface
│   ├── 📄 validate.py          # Validation engine
│   └── 📄 generate.py          # Registry generator
├── 📄 registry.yaml            # 🎯 Generated registry (DO NOT EDIT)
├── 📄 README.md                # You are here!
└── 📄 CONTRIBUTING.md          # Contribution guidelines
```

## 📋 Server Specification

Here's what a minimal server specification looks like:

```yaml
name: my-awesome-server
version: 1.0.0
status: active

meta:
  category: utilities
  tags: [api, integration, awesome]
  license: MIT
  featured: false

about:
  displayName: "My Awesome Server"
  description: "Does awesome things with the MCP protocol"

maintainer:
  name: "Your Name"
  email: "you@example.com" # Optional for external contributors
  github: "yourusername"

source:
  repository: "https://github.com/yourusername/your-mcp-server"
  branch: "main"
  dockerfile: "Dockerfile"

deployment:
  type: "http" # or "stdio"
  healthPath: "/health"

capabilities:
  tools:
    - name: awesome_tool
      description: "Does something awesome"
      schema:
        type: object
        properties:
          input:
            type: string
            description: "What to make awesome"
        required: [input]
      examples:
        - input: { input: "hello" }
          output: { result: "✨ hello ✨" }

  resources: [] # File resources (optional)
  prompts: [] # Prompt templates (optional)

credentials:
  - name: API_KEY
    description: "Your awesome API key"
    required: true
    example: "sk-..."
    link: "https://awesome-api.com/keys"

changelog:
  - version: "1.0.0"
    date: "2025-08-04"
    changes:
      - "Initial release"
      - "Added awesome_tool"
```

### Server Status Options

| Status         | Description         | When to Use                     |
| -------------- | ------------------- | ------------------------------- |
| `active`       | ✅ Production ready | Stable, tested, recommended     |
| `experimental` | 🧪 In development   | New features, may change        |
| `maintenance`  | 🔧 Maintenance only | No new features, bug fixes only |
| `deprecated`   | ⚠️ End of life      | Use alternatives                |
| `inactive`     | ❌ Not working      | Temporarily unavailable         |

## 🛠️ Development Tools

### Prerequisites

```bash
# Install uv (modern Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/nimblebrain/nimbletools-mcp-registry.git
cd nimbletools-mcp-registry

# Install dependencies
uv sync
```

### Registry Management Commands

```bash
# 🔍 Validate all servers
uv run python tools/cli.py validate --all

# ✅ Validate specific server
uv run python tools/cli.py validate servers/my-server

# 🏗️ Generate registry
uv run python tools/cli.py generate

# 🎯 Full check (validate + generate)
uv run python tools/cli.py check

# 📊 Show statistics
uv run python tools/cli.py stats
```

## 🤝 Contributing

We **love** community contributions! Here's how to get involved:

### 🎉 Adding Your Server

1. **Fork** this repository
2. **Create** a new directory: `servers/your-server-name/`
3. **Add** your `server.yaml` specification
4. **Validate** your server: `uv run python tools/cli.py validate servers/your-server-name`
5. **Submit** a pull request

### 📝 Contribution Checklist

- [ ] Server name is unique and descriptive
- [ ] `server.yaml` follows the [schema](schemas/server-schema.yaml)
- [ ] Server passes validation: `uv run python tools/cli.py validate servers/your-server`
- [ ] GitHub repository exists and is public
- [ ] Documentation is clear and helpful
- [ ] Examples demonstrate key functionality
- [ ] Changelog includes version history

### 🎯 What We're Looking For

**High-Quality Servers** that:

- ✅ Solve real problems
- ✅ Have clear documentation
- ✅ Include usage examples
- ✅ Follow MCP protocol standards
- ✅ Are actively maintained

**Popular Categories**:

- 🔧 Developer tools and utilities
- 🌐 API integrations and web services
- 📊 Data processing and analysis
- 💰 Financial and business tools
- 🎨 Creative and media tools
- 🔒 Security and authentication
- 🤖 AI and machine learning

### 🚫 What We Don't Accept

- ❌ Servers that require proprietary software
- ❌ Malicious or harmful functionality
- ❌ Duplicate functionality without improvement
- ❌ Servers without proper documentation
- ❌ Abandoned or unmaintained projects

### 📞 Getting Help

- 💬 **Questions?** Open a [Discussion](https://github.com/nimblebrain/nimbletools-mcp-registry/discussions)
- 🐛 **Bug Reports?** Create an [Issue](https://github.com/nimblebrain/nimbletools-mcp-registry/issues)
- 💡 **Feature Ideas?** Start a [Discussion](https://github.com/nimblebrain/nimbletools-mcp-registry/discussions)

## 🌟 Community

### 🏆 Featured Contributors

Thanks to our amazing contributors who make this registry possible:

- **NimbleBrain Inc** - Core platform servers
- **[Your name here]** - [Add your server!](#-contributing)

### 📈 Registry Stats

- **Total Servers**: 4
- **Active Servers**: 4
- **Categories**: 4 (Testing, Text Processing, Financial, Utilities)
- **Community Contributors**: 2

## 🔮 Roadmap

### Coming Soon

- 🔍 **Enhanced Discovery** - Better search and filtering
- 📊 **Usage Analytics** - Track popular servers
- 🏷️ **Tagging System** - Improved categorization
- 🤖 **Auto-Updates** - Sync with source repositories
- 📝 **Server Templates** - Quick-start templates

### Future Vision

- 🌍 **Global Registry** - Federated registry network
- 🔐 **Signed Packages** - Cryptographic verification
- 📦 **Binary Distribution** - Pre-built server packages
- 🎯 **Smart Recommendations** - AI-powered server suggestions

## 🔗 Integration

This registry is designed for consumption by:

- **🚀 NimbleTools Runtime** - Dynamic server deployment
- **💻 Platform UI** - Server browser and management
- **⚙️ CLI Tools** - Command-line server management
- **🔄 CI/CD Systems** - Automated testing and deployment

## 📜 License

This registry is open source under the [MIT License](LICENSE). Individual servers may have their own licenses as specified in their metadata.

## 🙏 Acknowledgments

- **Model Context Protocol** - For the amazing MCP standard
- **Community Contributors** - For sharing their awesome servers
- **Open Source Community** - For making collaboration possible

---

<div align="center">

**Ready to contribute?** [Add your server now!](#-contributing) 🚀

**Questions?** [Join the discussion](https://github.com/nimblebrain/nimbletools-mcp-registry/discussions) 💬

</div>
