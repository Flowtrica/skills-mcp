# Progressive Skills MCP

MCP server for SKILL.md files with **progressive disclosure** - achieving **13x token efficiency** over traditional approaches.

Based on [intellectronica/skillz](https://github.com/intellectronica/skillz) with progressive disclosure modifications inspired by Claude.ai's approach.

## What's Different?

**Original skillz:**
- Creates 1 tool per skill
- 20 skills = 20 tools × ~100 tokens = **2000 tokens/request**

**Progressive Skills MCP:**
- Creates 3 universal tools (`load_skill`, `read_skill_file`, `list_skill_files`)
- 20 skills = 3 tools × ~50 tokens = **150 tokens/request**
- **13x improvement!** 🎉

## Features

✅ Progressive disclosure (3-level token efficiency)  
✅ Metadata generation for system prompts  
✅ Compatible with all SKILL.md format files  
✅ Supports .zip and .skill archives  
✅ Bundled skills ready to use  

## Quick Start

### Using uvx (Recommended)

```bash
uvx progressive-skills-mcp
```

### With MCPHub

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": ["progressive-skills-mcp"]
    }
  }
}
```

### Using pip

```bash
pip install progressive-skills-mcp
progressive-skills-mcp
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

## Three Universal Tools

1. **`load_skill(skill_name)`** - Returns SKILL.md body without frontmatter
2. **`read_skill_file(skill_name, file_path)`** - Returns specific resource file
3. **`list_skill_files(skill_name, subdirectory?)`** - Lists available resources

## Generate Metadata

For Onyx or other MCP clients that support system prompts:

```bash
progressive-skills-mcp --generate-metadata
```

Output:
```markdown
## Available Skills

You have access to specialized skills...

- **context7-docs-lookup**: Look up documentation from Context7
```

## Usage

```bash
# Run MCP server with bundled skills
progressive-skills-mcp

# Run with custom skills directory
progressive-skills-mcp /path/to/skills

# Generate metadata
progressive-skills-mcp --generate-metadata

# Generate JSON metadata
progressive-skills-mcp --generate-metadata --format json

# List discovered skills
progressive-skills-mcp --list-skills
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

## Token Efficiency Comparison

| Approach | Tools/Request | Tokens/Request | 20 Skills |
|----------|--------------|----------------|-----------|
| Original | 20 tools | ~100 each | 2000 tokens |
| **Progressive Skills MCP** | **3 tools** | **~50 each** | **150 tokens** |
| **Improvement** | | | **13x better!** 🎉 |

## License

MIT (same as original skillz)

## Credits

- Based on [skillz](https://github.com/intellectronica/skillz) by Eleanor Berger
- Progressive disclosure modifications by Flowtrica
- Inspired by Claude.ai's skills system

## Links

- GitHub: https://github.com/Flowtrica/skills-mcp
- PyPI: https://pypi.org/project/progressive-skills-mcp/
- Skills repo: https://github.com/Flowtrica/agent-skills
