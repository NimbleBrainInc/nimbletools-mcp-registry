# NimbleTools Community MCP Registry

A curated registry of community-contributed Model Context Protocol (MCP) servers for the NimbleTools runtime platform, providing a clean, infrastructure-agnostic approach to MCP server definitions.

## 🎯 Core Purpose

This registry serves as the **central catalog** for community MCP servers that can be dynamically deployed within the NimbleTools runtime. The registry focuses purely on **server functionality** (tools, resources, prompts) while keeping infrastructure concerns separate.

## 🏗️ Architecture Overview

### Clean Separation of Concerns
- **Server Specs**: Define functionality, capabilities, and metadata
- **Infrastructure**: Handled separately by the deployment platform
- **Registry**: Self-contained with complete server definitions (no external dependencies)

### Key Design Principles
1. **No Infrastructure Leakage**: Server specs contain no Docker images, resource limits, or Kubernetes configs
2. **GitHub-Based**: Server definitions reference remote GitHub repositories
3. **Schema-Driven**: Strong validation ensures consistency and quality
4. **Capabilities-First**: MCP structure with tools, resources, and prompts

## 📁 Repository Structure

```
nimbletools-mcp-registry/
├── servers/                     # Individual server definitions
│   ├── echo/
│   │   └── server.yaml          # Server spec
│   ├── reverse-text/
│   │   └── server.yaml          # Server spec
│   └── finnhub/
│       └── server.yaml          # Server spec
├── schemas/                     # Schema definitions
│   ├── server-schema.yaml       # Server spec schema (NO infrastructure)
│   └── registry-schema.yaml     # Registry format schema
├── tools/                       # Registry management tools
│   ├── cli.py                   # Main CLI interface
│   ├── validate.py              # Schema validation
│   └── generate.py              # Registry generation + nimbletools.yaml ingestion
├── registry.yaml                # Generated registry with complete server specs
└── CONTRIBUTING.md              # Contribution guidelines
```

## 🚀 Quick Start

### For NimbleBrain Server Maintainers

NimbleBrain-maintained servers (mcp-echo, mcp-reverse-text, mcp-finnhub) use automatic ingestion:

1. **Add `nimbletools.yaml` to your MCP server repo**:
   ```yaml
   name: my-server
   version: 1.0.0
   status: active
   
   capabilities:
     tools:
       - name: my_tool
         description: "Does something useful"
         schema:
           type: object
           properties:
             input:
               type: string
           required: [input]
     resources: []
     prompts: []
   
   # ... other metadata
   ```

2. **Regenerate registry** (auto-detects and ingests):
   ```bash
   cd nimbletools-mcp-registry
   uv run python tools/cli.py generate
   ```

### For External Contributors

1. **Create server definition directly**:
   ```bash
   # Create servers/my-server/server.yaml manually
   uv run python tools/cli.py validate servers/my-server
   ```

2. **Submit pull request** with the server definition

### Registry Management Commands

```bash
# Validate all servers
uv run python tools/cli.py validate --all

# Validate specific server  
uv run python tools/cli.py validate servers/echo

# Generate registry (with auto-ingestion)
uv run python tools/cli.py generate

# Full check (validate + generate)
uv run python tools/cli.py check

# Show statistics
uv run python tools/cli.py stats
```

## 📋 Server Specification Format

### Capabilities Structure
Servers use a **capabilities** structure that mirrors the MCP protocol:

```yaml
name: example-server
version: 1.0.0
status: active  # active, inactive, deprecated, experimental, maintenance

meta:
  category: utilities
  tags: [example, demo]
  license: MIT
  featured: false

about:
  displayName: "Example Server"
  description: "Demonstrates the new server format"

maintainer:
  name: "Your Name"
  email: "you@example.com"

source:
  repository: "https://github.com/owner/repo"
  branch: "main"
  dockerfile: "Dockerfile"

deployment:
  type: "http"  # or "stdio"
  healthPath: "/health"

capabilities:
  tools:
    - name: example_tool
      description: "Does something useful"
      schema:
        type: object
        properties:
          input:
            type: string
            description: "Input parameter"
        required: [input]
      examples:
        - input: {input: "test"}
          output: {result: "processed"}
  
  resources:
    - uri: "file://data/*"
      name: "Data Files"
      description: "Access to data files"
      mimeType: "text/plain"
  
  prompts:
    - name: analyze_data
      description: "Analyzes data with specific format"
      arguments:
        - name: data_type
          description: "Type of data to analyze"
          required: true

credentials:
  - name: API_KEY
    description: "Required API key for external service"
    required: true
    example: "sk-..."
    link: "https://service.com/api-keys"

# Legacy tools field maintained for backwards compatibility
tools: [...] # Same as capabilities.tools
```

### Server Status Options
- **`active`**: Ready for production use
- **`inactive`**: Not currently available/functioning  
- **`deprecated`**: No longer maintained, use alternatives
- **`experimental`**: In development, may change
- **`maintenance`**: Maintenance mode only

### Deployment Types
- **`http`**: Web service with REST API endpoints
- **`stdio`**: Process-based communication via stdin/stdout

## 🔄 Auto-Ingestion System

The registry automatically ingests server definitions from NimbleBrain repositories:

### How It Works
1. **Detection**: `generate.py` scans for `nimbletools.yaml` files in `../mcp-*` directories
2. **Ingestion**: Copies `nimbletools.yaml` → `servers/{name}/server.yaml`
3. **Registry Generation**: Creates self-contained `registry.yaml` with complete specs

### Monitored Repositories
- `../mcp-echo` → `servers/echo/server.yaml`
- `../mcp-reverse-text` → `servers/reverse-text/server.yaml`  
- `../mcp-finnhub` → `servers/finnhub/server.yaml`

## 📊 Registry Output

The generated `registry.yaml` contains:
- **Complete server specifications** (no external references)
- **All server metadata** inline
- **Full capability definitions** (tools, resources, prompts)
- **No infrastructure details** (Docker images, resource limits, etc.)

Example registry structure:
```yaml
apiVersion: registry.nimbletools.ai/v1
kind: MCPRegistry
metadata:
  name: community-servers
  version: 2.0.0
  lastUpdated: '2025-07-27'

servers:
  - name: echo
    version: 1.0.0
    status: active
    capabilities:
      tools: [...]
    # ... complete server spec
  - name: reverse-text
    # ... complete server spec
```

## 🛠️ Development Workflow

### Adding a New NimbleBrain Server
1. Create MCP server repository with `nimbletools.yaml`
2. Add repo path to `generate.py` in `nimblebrain_repos` list
3. Run `uv run python tools/cli.py generate`

### Adding External Server
1. Create `servers/{name}/server.yaml` manually
2. Run `uv run python tools/cli.py validate servers/{name}`
3. Submit pull request

### Registry Maintenance
```bash
# Full validation and regeneration
uv run python tools/cli.py check

# Just validate
uv run python tools/cli.py validate --all

# Just regenerate
uv run python tools/cli.py generate
```

## 🎯 Future Integration

This registry is designed for consumption by:

1. **NimbleTools Runtime**: Deploys servers based on registry specs
2. **Platform UI**: Displays available servers and capabilities  
3. **CLI Tools**: Discovers and manages MCP servers
4. **CI/CD Systems**: Automated deployment and testing

The clean separation ensures infrastructure concerns don't pollute server definitions, making the registry portable across deployment platforms.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding servers and making changes.

## License

MIT License. Individual servers may have their own licenses as specified in their metadata.
