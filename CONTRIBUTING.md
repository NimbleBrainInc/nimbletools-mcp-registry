# Contributing to NimbleTools Community MCP Registry

We welcome community contributions to expand and improve the NimbleTools Community MCP Registry! This guide will help you contribute servers, improvements, and fixes to the registry that powers the NimbleTools runtime platform.

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) for dependency management
- Docker (for server testing)
- Git

## Development Setup

1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/YourUsername/mcp-registry.git
   cd mcp-registry
   ```

2. **Set up development environment:**
   ```bash
   make dev-setup
   ```

## Contributing a New Server

### Option 1: Interactive Wizard (Recommended)

```bash
# Create a new server interactively
uv run python tools/wizard.py --create-server

# Follow the prompts to configure your server
```

### Option 2: Manual Creation

1. **Create server directory:**
   ```bash
   mkdir servers/my-server
   ```

2. **Create `server.yaml`:**
   ```yaml
   # See schemas/server-schema.yaml for full specification
   name: my-server
   version: 1.0.0
   status: active
   
   meta:
     category: utilities
     tags: [utility, example]
     license: MIT
   
   about:
     displayName: "My Server"
     description: "Description of what this server does"
   
   # ... rest of configuration
   ```

3. **Add documentation:**
   ```bash
   # Create servers/my-server/README.md with:
   # - Server purpose and functionality
   # - Usage examples
   # - Configuration requirements
   # - License information
   ```

### Validation and Testing

```bash
# Validate your server definition
make validate

# Test specific server
uv run python tools/validate.py servers/my-server/

# Generate and check registry output
make generate
```

## Server Requirements

All servers must meet these requirements:

### ✅ Technical Requirements

- **Containerized**: Must include a working Dockerfile
- **Health Checks**: Implement `/health` endpoint
- **MCP Compliance**: Follow MCP protocol specification
- **Error Handling**: Proper error responses and logging
- **Documentation**: Complete README and tool descriptions

### ✅ Security Requirements

- **Non-root user**: Container runs as non-root user
- **Minimal attack surface**: Only necessary dependencies
- **Secure defaults**: No hardcoded secrets or credentials
- **Updated base images**: Use recent, patched base images

### ✅ Quality Requirements

- **Testing**: Include automated tests
- **Validation**: Pass schema validation
- **License**: Clear licensing (preferably MIT or Apache 2.0)
- **Maintenance**: Active maintainer contact information

## Server Schema

Your `server.yaml` must follow this structure:

```yaml
# Basic identification
name: string               # Unique server identifier
version: string           # Semantic version (1.0.0)
status: active|deprecated # Server status

# Metadata for discovery
meta:
  category: string        # One of predefined categories
  tags: [string]         # Descriptive tags
  license: string        # License identifier (MIT, Apache-2.0, etc.)
  featured: boolean      # Whether to feature in marketplace

# Display information
about:
  displayName: string    # Human-readable name
  description: string    # Detailed description
  icon: string          # Optional icon URL

# Maintainer information
maintainer:
  name: string          # Maintainer name
  email: string         # Contact email
  organization: string  # Optional organization

# Source code information
source:
  repository: string    # GitHub repository URL
  branch: string       # Default branch (usually 'main')
  dockerfile: string   # Path to Dockerfile

# Deployment configuration
deployment:
  image: string        # Docker image name
  port: number        # Container port
  healthPath: string  # Health check endpoint

# Tool definitions
tools:
  - name: string           # Tool identifier
    description: string    # Tool description
    schema: object        # JSON Schema for parameters

# Required credentials (if any)
credentials: []          # List of required environment variables
```

See `schemas/server-schema.yaml` for the complete specification.

## Categories

Choose from these predefined categories:

- `text-processing` - Text manipulation and analysis
- `financial` - Market data and financial tools
- `testing` - Testing and development tools
- `utilities` - General-purpose utilities
- `communication` - Messaging and notifications
- `data-analytics` - Data processing and visualization
- `cloud-services` - Cloud platform integrations
- `media` - Image, video, and audio processing
- `security` - Security and authentication tools
- `experimental` - Experimental and cutting-edge tools

## Pull Request Process

1. **Create a feature branch:**
   ```bash
   git checkout -b add-my-server
   ```

2. **Make your changes:**
   - Add server definition in `servers/my-server/`
   - Ensure all validation passes
   - Update documentation if needed

3. **Test thoroughly:**
   ```bash
   make test
   make validate
   make check-servers
   ```

4. **Commit with clear messages:**
   ```bash
   git add .
   git commit -m "Add my-server: Brief description of functionality"
   ```

5. **Submit pull request:**
   - Clear title and description
   - Link to any related issues
   - Include testing evidence
   - Follow the PR template

## Review Process

1. **Automated Checks**: CI will validate schema, run tests, and check security
2. **Maintainer Review**: NimbleTools team reviews for quality and compatibility
3. **Community Feedback**: Open for community input and suggestions
4. **Approval & Merge**: Once approved, changes are merged and deployed

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## Getting Help

- **Documentation**: Check existing servers for examples
- **Issues**: [Create an issue](https://github.com/NimbleBrainInc/mcp-registry/issues) for questions
- **Discussions**: [Join discussions](https://github.com/NimbleBrainInc/mcp-registry/discussions)
- **Email**: hello@nimblebrain.ai

## Recognition

Contributors will be:
- Listed in server metadata as maintainers
- Recognized in release notes
- Invited to join the contributor community

Thank you for helping make the NimbleTools community and MCP ecosystem better! 🚀