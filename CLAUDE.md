# CLAUDE.md - NimbleTools MCP Registry

This file provides comprehensive guidance for Claude when working with the NimbleTools Community MCP Registry, which provides a clean, infrastructure-agnostic approach to MCP server management.

## 🎯 Core Understanding

### Registry Purpose
The NimbleTools MCP Registry is a **curated catalog** of Model Context Protocol (MCP) servers that can be dynamically deployed within the NimbleTools runtime platform. It serves as the single source of truth for available MCP servers and their capabilities.

### Key Architectural Principles
1. **Clean Separation**: Server functionality is completely separated from infrastructure concerns
2. **Self-Contained**: Registry contains complete server specs with no external dependencies
3. **GitHub-Based**: Server definitions reference remote GitHub repositories
4. **Schema-Driven**: Strong validation ensures consistency and prevents infrastructure leakage

## 🏗️ Registry Architecture

### Directory Structure
```
nimbletools-mcp-registry/
├── servers/                     # Individual server definitions
│   ├── echo/server.yaml         # Server spec for mcp-echo
│   ├── reverse-text/server.yaml # Server spec for mcp-reverse-text
│   ├── finnhub/server.yaml      # Server spec for mcp-finnhub
│   ├── nationalparks-mcp/       # External server definition
│   └── ref-tools-mcp/           # External server definition
├── schemas/
│   ├── server-schema.yaml       # Clean server spec schema (NO infrastructure)
│   └── registry-schema.yaml     # Registry format schema
├── tools/                       # Lean toolset (4 files only)
│   ├── cli.py                   # Main CLI interface
│   ├── validate.py              # Schema validation
│   ├── generate.py              # Registry generation
│   └── __init__.py              # Package init
├── registry.yaml                # Generated registry (DO NOT EDIT)
├── README.md                    # Public documentation
└── CLAUDE.md                    # This file
```

### Server Types
1. **Core Servers**: Primary MCP servers maintained by NimbleBrain
   - `servers/echo/server.yaml` - References https://github.com/nimblebrain/mcp-echo
   - `servers/reverse-text/server.yaml` - References https://github.com/nimblebrain/mcp-reverse-text
   - `servers/finnhub/server.yaml` - References https://github.com/nimblebrain/mcp-finnhub

2. **Community Servers**: External server definitions
   - `servers/nationalparks-mcp/server.yaml`
   - `servers/ref-tools-mcp/server.yaml`

## 📋 Server Specification Format

### Complete Example
```yaml
name: example-server
version: 1.0.0
status: active  # active, inactive, deprecated, experimental, maintenance

meta:
  category: utilities  # text-processing, financial, testing, utilities, etc.
  tags: [example, demo, api]
  license: MIT
  featured: false

about:
  displayName: "Example Server"
  description: "Comprehensive example of the new server format"
  homepage: "https://github.com/owner/repo"
  documentation: "https://github.com/owner/repo#readme"
  icon: "https://example.com/icon.png"  # Optional

maintainer:
  name: "Maintainer Name"
  email: "maintainer@example.com"
  organization: "Organization Name"  # Optional
  github: "github-username"          # Optional

source:
  repository: "https://github.com/owner/repo"
  branch: "main"
  dockerfile: "Dockerfile"
  directory: "subdirectory"  # Optional if server is in subdirectory

deployment:
  type: "http"  # or "stdio"
  healthPath: "/health"  # Only for http type

capabilities:
  tools:
    - name: example_tool
      description: "Does something useful with the input"
      schema:
        type: object
        properties:
          input:
            type: string
            description: "Input text to process"
          options:
            type: object
            description: "Optional processing options"
        required: [input]
      examples:
        - input: {input: "test", options: {format: "json"}}
          output: {result: "processed test", format: "json"}
  
  resources:
    - uri: "file://data/*"
      name: "Data Files"
      description: "Access to server data files"
      mimeType: "text/plain"
  
  prompts:
    - name: analyze_data
      description: "Analyzes data with specific formatting"
      arguments:
        - name: data_type
          description: "Type of data to analyze"
          required: true
        - name: format
          description: "Output format preference"
          required: false

credentials:
  - name: API_KEY
    description: "Required API key for external service access"
    required: true
    example: "sk-1234567890abcdef"
    link: "https://service.com/api-keys"
  - name: LOG_LEVEL
    description: "Logging verbosity level"
    required: false
    example: "info"

# Legacy tools field for backwards compatibility
tools:
  - name: example_tool
    description: "Does something useful with the input"
    schema:
      type: object
      properties:
        input:
          type: string
          description: "Input text to process"
      required: [input]

changelog:
  - version: "1.0.0"
    date: "2025-07-27"
    changes:
      - "Initial release with example_tool"
      - "Added comprehensive examples and documentation"
```

### Field Explanations

#### Required Fields
- **`name`**: Unique identifier (lowercase, hyphens allowed)
- **`version`**: Semantic version (e.g., "1.0.0")
- **`status`**: Current status (active, inactive, deprecated, experimental, maintenance)
- **`meta`**: Category, tags, license, featured flag
- **`about`**: Display name and description
- **`maintainer`**: Name and email (minimum)
- **`source`**: Repository, branch, dockerfile
- **`deployment`**: Type and health path
- **`capabilities`** OR **`tools`**: At least one capability definition

#### Status Values
- **`active`**: Ready for production use
- **`inactive`**: Not currently available/functioning
- **`deprecated`**: No longer maintained, use alternatives
- **`experimental`**: In development, may change
- **`maintenance`**: Maintenance mode only

#### Deployment Types
- **`http`**: Web service expecting REST API calls
- **`stdio`**: Process-based communication via stdin/stdout

## 🔄 Registry Generation

### How It Works
1. **Loading**: `generate.py` loads all server definitions from `servers/*/server.yaml` files
2. **Validation**: Ensures all specs pass schema validation
3. **Registry Generation**: Creates self-contained `registry.yaml` with complete server specs
4. **GitHub References**: All servers reference their remote GitHub repositories

### Adding New Server
To add a new server to the registry:
1. Create directory: `servers/new-server/`
2. Create `servers/new-server/server.yaml` following the schema
3. Include GitHub repository URL in the `source.repository` field
4. Run `uv run python tools/cli.py validate servers/new-server`
5. Run `uv run python tools/cli.py generate`

### Current Server References
- `servers/echo/server.yaml` - References https://github.com/nimblebrain/mcp-echo
- `servers/reverse-text/server.yaml` - References https://github.com/nimblebrain/mcp-reverse-text
- `servers/finnhub/server.yaml` - References https://github.com/nimblebrain/mcp-finnhub

## 🛠️ Development Commands

### Registry Management
```bash
# Full validation and regeneration (recommended)
uv run python tools/cli.py check

# Validate all servers
uv run python tools/cli.py validate --all

# Validate specific server
uv run python tools/cli.py validate servers/echo

# Generate registry from server definitions
uv run python tools/cli.py generate

# Show registry statistics
uv run python tools/cli.py stats
```

### Working with Servers

#### Adding New Server
1. Create directory: `servers/new-server/`
2. Create `servers/new-server/server.yaml` following the schema
3. Include GitHub repository URL in `source.repository` field
4. Validate: `uv run python tools/cli.py validate servers/new-server`
5. Generate: `uv run python tools/cli.py generate`

#### Updating Existing Server
1. Edit the appropriate `servers/{server}/server.yaml` file
2. Update version number and changelog if needed
3. Validate: `uv run python tools/cli.py validate servers/{server}`
4. Regenerate: `uv run python tools/cli.py generate`

## 📊 Registry Output

### Generated Registry Structure
```yaml
apiVersion: registry.nimbletools.ai/v1
kind: MCPRegistry
metadata:
  name: community-servers
  description: Community-contributed MCP servers for the NimbleTools runtime platform
  version: 2.0.0
  lastUpdated: '2025-07-27'
  generatedBy: mcp-registry/tools/generate.py

servers:
  - name: echo
    version: 1.0.0
    status: active
    capabilities:
      tools: [...]
      resources: []
      prompts: []
    tools: [...]  # Legacy field
    # ... complete server specification
  - name: reverse-text
    # ... complete server specification
  # ... all other servers with complete specs
```

### Key Characteristics
- **Self-Contained**: No external references or dependencies
- **Complete Specs**: All server metadata and capabilities inline
- **No Infrastructure**: No Docker images, resource limits, or Kubernetes configs
- **Schema Compliant**: Validates against `registry-schema.yaml`

## 🚨 Important Rules & Constraints

### What NOT to Include
- **Docker Images**: No `image:` fields in server specs
- **Resource Limits**: No CPU/memory requests or limits
- **Scaling Config**: No replica counts or auto-scaling settings
- **Kubernetes Configs**: No namespaces, services, or ingress rules
- **Port Mappings**: No container port specifications (except health check path)

### Schema Validation
- All servers MUST validate against `schemas/server-schema.yaml`
- Required fields are enforced
- Invalid status values are rejected
- Tool names must follow naming conventions (`^[a-z][a-z0-9_]*$`)

### File Management
- **DO NOT EDIT** `registry.yaml` directly (auto-generated)
- **DO EDIT** server definitions in `servers/*/server.yaml` files
- **DO ENSURE** GitHub repository URLs are correct in `source.repository` fields
- **DO UPDATE** version numbers and changelogs when making changes

## 🎯 Common Tasks

### Task: Add New Server
1. Create `servers/{name}/server.yaml` with complete server specification
2. Include correct GitHub repository URL in `source.repository` field
3. Run `uv run python tools/cli.py validate servers/{name}`
4. Run `uv run python tools/cli.py generate`
5. Verify with `uv run python tools/cli.py validate --all`

### Task: Update Server Capabilities
1. Edit the appropriate `servers/{server}/server.yaml` file
2. Update the `capabilities` section with new tools, resources, or prompts
3. Increment version number and add changelog entry
4. Run `uv run python tools/cli.py validate servers/{server}`
5. Run `uv run python tools/cli.py generate`

### Task: Change Server Status
1. Edit the `servers/{server}/server.yaml` file
2. Change `status:` to one of: active, inactive, deprecated, experimental, maintenance
3. Add changelog entry explaining the status change
4. Run `uv run python tools/cli.py generate`

### Task: Fix Validation Errors
1. Run `uv run python tools/cli.py validate --all` to see errors
2. Check error messages for specific field issues
3. Compare against `schemas/server-schema.yaml` for requirements
4. Fix issues and re-validate

## 📈 Integration Points

### NimbleTools Runtime
- Reads `registry.yaml` to discover available servers
- Uses `capabilities` to understand what each server offers
- Deploys servers based on `deployment.type` (http vs stdio)
- Injects `credentials` as environment variables

### Platform UI
- Displays servers from registry with categories and tags
- Shows tool descriptions and examples for user discovery
- Filters by status (active, experimental, etc.)

### CLI Tools
- Discovery: Find available servers and their capabilities
- Validation: Ensure server specs are correct before deployment
- Management: Add, update, and remove servers from registry

This registry architecture ensures a clean separation between server functionality and infrastructure concerns, making it portable, maintainable, and easy to extend.