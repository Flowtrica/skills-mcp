# Skills MCP

MCP server for SKILL.md files with **progressive disclosure** - achieving **13x token efficiency** over traditional approaches.

Based on [intellectronica/skillz](https://github.com/intellectronica/skillz) with progressive disclosure modifications inspired by Claude.ai's approach.

## What's Different?

**Original skillz:**
- Creates 1 tool per skill
- 20 skills = 20 tools × ~100 tokens = **2000 tokens/request**

**Skills MCP (this fork):**
- Creates 3 universal tools (`load_skill`, `read_skill_file`, `list_skill_files`)
- 20 skills = 3 tools × ~50 tokens = **150 tokens/request**
- **13x improvement!** 🎉

## Features

✅ Progressive disclosure (3-level token efficiency)  
✅ Metadata generation for system prompts  
✅ Compatible with all SKILL.md format files  
✅ Supports .zip and .skill archives  
✅ Docker image available  

## Quick Start

### Using Docker

```bash
docker run -i --rm \
  -v /path/to/skills:/skills \
  flowtrica/skills-mcp:latest \
  /skills
```

### Using uvx

```bash
uvx skills-mcp@latest /path/to/skills
```

### With MCPHub

```json
{
  "mcpServers": {
    "skills": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "--entrypoint", "sh",
        "flowtrica/skills-mcp:latest",
        "-c",
        "git clone https://github.com/YOUR_USERNAME/your-skills.git /tmp/skills && skills-mcp /tmp/skills"
      ]
    }
  }
}
```

## Progressive Disclosure

### Level 1: System Prompt (Once per conversation)
```markdown
## Available Skills
- **weather**: Get weather forecasts
- **pptx**: Create presentations
```
**Cost:** ~200 tokens, sent ONCE

### Level 2: On-Demand Instructions
```python
load_skill("pptx")  # Returns full SKILL.md
```
**Cost:** 0 tokens until loaded

### Level 3: Referenced Resources  
```python
read_skill_file("pptx", "references/api.md")
```
**Cost:** 0 tokens until accessed

## Generate Metadata

For Onyx or other MCP clients that support system prompts:

```bash
skills-mcp --generate-metadata /path/to/skills
```

Output:
```markdown
## Available Skills

You have access to specialized skills...

- **test-skill**: A simple test skill
- **weather**: Get weather forecasts
```

## Installation

```bash
pip install skills-mcp
```

Or use with `uv`:
```bash
uv tool install skills-mcp
```

## Usage

```bash
# Run MCP server
skills-mcp /path/to/skills

# Generate metadata
skills-mcp --generate-metadata /path/to/skills

# Generate JSON metadata
skills-mcp --generate-metadata --format json /path/to/skills

# List discovered skills
skills-mcp --list-skills /path/to/skills
```

## Skill Format

Skills can be:
- **Directories** with SKILL.md file
- **Zip archives** containing SKILL.md
- **.skill archives**

Example structure:
```
skills/
├── weather/
│   ├── SKILL.md
│   └── references/
│       └── api.md
└── pptx.zip
```

SKILL.md format:
```markdown
---
name: skill-name
description: Brief description
---

# Full Instructions

Detailed skill instructions here...
```

## Building Docker Image

```bash
docker build -t flowtrica/skills-mcp:latest .
docker push flowtrica/skills-mcp:latest
```

## Token Efficiency Comparison

| Approach | Tools/Request | Tokens/Request | 20 Skills |
|----------|--------------|----------------|-----------|
| Original | 20 tools | ~100 each | 2000 tokens |
| **Skills MCP** | **3 tools** | **~50 each** | **150 tokens** |
| **Improvement** | | | **13x better!** 🎉 |

## License

MIT (same as original skillz)

## Credits

- Based on [skillz](https://github.com/intellectronica/skillz) by Eleanor Berger
- Progressive disclosure modifications by Flowtrica
- Inspired by Claude.ai's skills system

## Links

- Original skillz: https://github.com/intellectronica/skillz
- Skills repo: https://github.com/Flowtrica/agent-skills
- Docker Hub: https://hub.docker.com/r/flowtrica/skills-mcp
