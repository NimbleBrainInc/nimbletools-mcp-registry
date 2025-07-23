# Contributing to NimbleTools Community MCP Registry

🎉 Thank you for your interest in contributing to the NimbleTools Community MCP Registry! This guide will help you add your MCP server to our community catalog.

## 🚀 Quick Start

1. **Fork** this repository
2. **Create** your server definition in `servers/YOUR_SERVER_NAME/server.yaml`
3. **Validate** your server: `uv run python tools/cli.py validate servers/YOUR_SERVER_NAME`
4. **Submit** a pull request

## 📋 Server Requirements

### ✅ Must Have

- **Unique Name**: No conflicts with existing servers
- **Valid Schema**: Passes `server-schema.yaml` validation
- **GitHub Repository**: Public repository with source code
- **Clear Documentation**: README with usage instructions
- **Working Examples**: Demonstrate key functionality
- **MCP Compliance**: Follows Model Context Protocol standards

### 🎯 Should Have

- **Comprehensive Tests**: Unit and integration tests
- **Health Checks**: Proper health endpoints (for HTTP servers)
- **Error Handling**: Graceful error responses
- **Logging**: Appropriate logging levels
- **Security**: No hardcoded secrets or credentials

## 📝 Server Specification Guide

### Complete Example

```yaml
name: my-awesome-server
version: 1.0.0
status: active

meta:
  category: utilities # See categories below
  tags: [api, integration, useful]
  license: MIT
  featured: false

about:
  displayName: "My Awesome Server"
  description: "A comprehensive MCP server that does awesome things with data"
  homepage: "https://github.com/yourusername/awesome-server"
  documentation: "https://github.com/yourusername/awesome-server#readme"
  icon: "https://your-site.com/icon.png" # Optional

maintainer:
  name: "Your Name"
  email: "you@example.com" # Optional for external contributors
  organization: "Your Organization" # Optional
  github: "yourusername"

source:
  repository: "https://github.com/yourusername/awesome-server"
  branch: "main"
  dockerfile: "Dockerfile"
  directory: "src" # Optional if server is in subdirectory

deployment:
  type: "http" # or "stdio"
  healthPath: "/health" # Required for http type

container: # Optional - for deployment metadata
  image: "yourusername/awesome-server:latest"
  port: 8080

capabilities:
  tools:
    - name: process_data
      description: "Processes input data and returns structured results"
      schema:
        type: object
        properties:
          data:
            type: string
            description: "Raw data to process"
          format:
            type: string
            description: "Output format (json, csv, xml)"
            default: "json"
        required: [data]
      examples:
        - input: { data: "hello world", format: "json" }
          output: { processed: "HELLO WORLD", format: "json", length: 11 }
        - input: { data: "test data" }
          output: { processed: "TEST DATA", format: "json", length: 9 }

    - name: validate_input
      description: "Validates input against predefined rules"
      schema:
        type: object
        properties:
          input:
            type: string
            description: "Input to validate"
          rules:
            type: array
            items:
              type: string
            description: "Validation rules to apply"
        required: [input, rules]
      examples:
        - input: { input: "test@example.com", rules: ["email"] }
          output: { valid: true, type: "email" }

  resources:
    - uri: "file://data/*"
      name: "Data Files"
      description: "Access to server data files"
      mimeType: "application/json"

  prompts:
    - name: analyze_data
      description: "Analyzes data with specific formatting requirements"
      arguments:
        - name: data_type
          description: "Type of data to analyze"
          required: true
        - name: output_format
          description: "Desired output format"
          required: false

credentials:
  - name: API_KEY
    description: "Required API key for external service integration"
    required: true
    example: "sk-1234567890abcdef"
    link: "https://service.com/api-keys"

  - name: LOG_LEVEL
    description: "Logging verbosity level"
    required: false
    example: "info"

changelog:
  - version: "1.0.0"
    date: "2025-08-04"
    changes:
      - "Initial release with data processing capabilities"
      - "Added input validation and formatting tools"
      - "Comprehensive error handling and logging"
```

### Field Descriptions

#### Required Fields

| Field                | Description              | Example                        |
| -------------------- | ------------------------ | ------------------------------ |
| `name`               | Unique server identifier | `awesome-server`               |
| `version`            | Semantic version         | `1.0.0`                        |
| `status`             | Current status           | `active`                       |
| `meta.category`      | Server category          | `utilities`                    |
| `meta.tags`          | Descriptive tags         | `[api, data, processing]`      |
| `meta.license`       | SPDX license ID          | `MIT`                          |
| `about.displayName`  | Human-readable name      | `Awesome Server`               |
| `about.description`  | Brief description        | `Does awesome things`          |
| `maintainer.name`    | Your name                | `John Doe`                     |
| `source.repository`  | GitHub repo URL          | `https://github.com/user/repo` |
| `source.branch`      | Default branch           | `main`                         |
| `deployment.type`    | Deployment type          | `http` or `stdio`              |
| `capabilities.tools` | Tool definitions         | See example above              |

#### Optional Fields

| Field                     | Description       | Default           |
| ------------------------- | ----------------- | ----------------- |
| `maintainer.email`        | Contact email     | None              |
| `maintainer.organization` | Organization name | None              |
| `maintainer.github`       | GitHub username   | None              |
| `about.homepage`          | Project website   | Repository URL    |
| `about.documentation`     | Docs URL          | Repository README |
| `about.icon`              | Icon URL          | None              |
| `source.dockerfile`       | Dockerfile path   | `Dockerfile`      |
| `source.directory`        | Source directory  | Root              |
| `container.image`         | Container image   | None              |
| `container.port`          | Container port    | 8080              |
| `credentials`             | Required env vars | `[]`              |
| `capabilities.resources`  | File resources    | `[]`              |
| `capabilities.prompts`    | Prompt templates  | `[]`              |

### Categories

Choose the most appropriate category:

| Category          | Description                   | Examples                         |
| ----------------- | ----------------------------- | -------------------------------- |
| `text-processing` | Text analysis, transformation | NLP, translation, formatting     |
| `financial`       | Financial data, markets       | Stock quotes, crypto, banking    |
| `utilities`       | General tools, helpers        | File processing, validation      |
| `communication`   | Messaging, notifications      | Email, Slack, webhooks           |
| `data-analytics`  | Data processing, analysis     | ETL, reporting, visualization    |
| `cloud-services`  | Cloud API integrations        | AWS, GCP, Azure services         |
| `media`           | Image, video, audio           | Processing, generation, analysis |
| `security`        | Security tools, auth          | Scanning, encryption, auth       |
| `testing`         | Testing, debugging            | Mock services, validators        |
| `experimental`    | Cutting-edge, research        | AI models, new protocols         |

### Status Values

| Status         | When to Use      | Description                         |
| -------------- | ---------------- | ----------------------------------- |
| `active`       | Production ready | Stable, tested, recommended for use |
| `experimental` | In development   | May have breaking changes           |
| `maintenance`  | Bug fixes only   | No new features planned             |
| `deprecated`   | End of life      | Use alternatives, will be removed   |
| `inactive`     | Temporarily down | Not currently working               |

## 🔍 Validation Process

### Local Validation

```bash
# Install dependencies
uv sync

# Validate your server
uv run python tools/cli.py validate servers/your-server-name

# Run full check
uv run python tools/cli.py check
```

### Common Validation Errors

#### Schema Validation

```
❌ Schema validation failed: 'example' does not match '^[a-z][a-z0-9_]*$'
```

**Fix**: Tool names must start with lowercase letter, contain only lowercase letters, numbers, and underscores.

```
❌ At least one tool must be defined
```

**Fix**: Add at least one tool to `capabilities.tools`.

#### Repository Validation

```
❌ Repository must be a GitHub HTTPS URL
```

**Fix**: Use format `https://github.com/owner/repo`.

#### Name Validation

```
❌ Server name 'MyServer' doesn't match directory name 'my-server'
```

**Fix**: Ensure server name matches directory name exactly.

## 📤 Submission Process

### 1. Prepare Your Submission

- [ ] Server code is in a public GitHub repository
- [ ] Repository has clear README with usage instructions
- [ ] Server passes local validation
- [ ] Examples demonstrate key functionality
- [ ] No secrets or credentials in code

### 2. Create Pull Request

1. **Fork** this repository
2. **Create** branch: `git checkout -b add-server-name`
3. **Add** server definition: `servers/your-server-name/server.yaml`
4. **Commit** changes: `git commit -m "Add your-server-name MCP server"`
5. **Push** branch: `git push origin add-server-name`
6. **Open** pull request with description:

```markdown
## Adding [Your Server Name]

### Description

Brief description of what your server does.

### Key Features

- Feature 1
- Feature 2
- Feature 3

### Testing

- [ ] Passes validation: `uv run python tools/cli.py validate servers/your-server`
- [ ] Manual testing completed
- [ ] Examples work as documented

### Checklist

- [ ] Server name is unique
- [ ] Repository is public
- [ ] Documentation is complete
- [ ] No hardcoded secrets
- [ ] Follows MCP protocol standards
```

### 3. Review Process

1. **Automated Checks**: CI validates your server
2. **Manual Review**: Maintainers review functionality and quality
3. **Feedback**: Address any requested changes
4. **Approval**: Server is merged and added to registry

## 🛠️ Development Best Practices

### Code Quality

- **Follow Standards**: Adhere to MCP protocol specifications
- **Error Handling**: Provide helpful error messages
- **Logging**: Use appropriate log levels
- **Documentation**: Include clear usage examples
- **Testing**: Write comprehensive tests

### Security

- **No Hardcoded Secrets**: Use environment variables
- **Input Validation**: Validate all user inputs
- **Safe Defaults**: Use secure default configurations
- **Dependency Security**: Keep dependencies updated

### Performance

- **Resource Efficient**: Minimize memory and CPU usage
- **Fast Startup**: Quick initialization times
- **Concurrent Safe**: Handle multiple requests safely
- **Graceful Shutdown**: Clean resource cleanup

## 🚫 What We Don't Accept

- **Malicious Software**: Any harmful or destructive functionality
- **Proprietary Dependencies**: Servers requiring paid/closed software
- **Duplicate Functionality**: Near-identical servers without improvement
- **Poor Documentation**: Servers without clear usage instructions
- **Unmaintained Code**: Abandoned or outdated projects
- **License Violations**: Code without proper licensing
- **Security Issues**: Servers with known vulnerabilities

## 🔧 Testing Your Server

### Manual Testing

1. **Start your server** locally
2. **Test each tool** with example inputs
3. **Verify outputs** match expected results
4. **Check error handling** with invalid inputs
5. **Test resource access** (if applicable)
6. **Validate health endpoints** (HTTP servers)

### Integration Testing

```bash
# Test with MCP client
mcp-client connect your-server

# List available tools
mcp-client tools list

# Call specific tool
mcp-client tools call your_tool_name '{"param": "value"}'
```

## 📞 Getting Help

### Questions & Support

- 💬 **General Questions**: [GitHub Discussions](https://github.com/nimblebrain/nimbletools-mcp-registry/discussions)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/nimblebrain/nimbletools-mcp-registry/issues)
- 📧 **Private Inquiries**: hello@nimblebrain.ai

### Common Issues

**Q: My server validation fails with schema errors**
A: Check the [server specification guide](#-server-specification-guide) and ensure all required fields are present and correctly formatted.

**Q: Can I include servers that require API keys?**
A: Yes! Use the `credentials` section to document required environment variables. Never include actual API keys in your code.

**Q: How do I update my server after it's accepted?**
A: Submit a new pull request with your changes. Update the version number and changelog.

**Q: Can I submit servers in languages other than Python?**
A: Absolutely! As long as your server follows the MCP protocol and can be containerized, any language is welcome.

## 🎉 Recognition

### Contributor Benefits

- **Attribution**: Your name and GitHub profile linked in the registry
- **Showcase**: Featured in our community servers list
- **Feedback**: Direct user feedback on your MCP server
- **Network**: Connect with other MCP developers
- **Learning**: Contribute to the growing MCP ecosystem

### Featured Contributors

Outstanding contributors may be featured in:

- README.md contributors section
- Community blog posts
- Conference presentations
- Social media recognition

---

**Ready to contribute?** Start by exploring our [server examples](servers/) and then create your own! 🚀

**Questions?** Join our [community discussions](https://github.com/nimblebrain/nimbletools-mcp-registry/discussions) 💬
