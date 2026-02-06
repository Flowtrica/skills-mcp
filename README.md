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
✅ Compatible with all SKILL.md format files  
✅ Supports .zip and .skill archives  
✅ Flexible skills source (GitHub repos, local directories, VPS volumes)  
✅ Simple `uvx` installation - works with any MCP client  

## Installation

### Option 1: Using a GitHub Repository

Perfect for sharing skills across machines or teams:

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": ["progressive-skills-mcp"],
      "env": {
        "SKILLS_SOURCE": "https://github.com/YOUR_USERNAME/your-skills.git"
      }
    }
  }
}
```

The server will clone the repository on startup.

### Option 2: Local Installation (PC/Laptop)

For local development or personal use:

**Linux/Mac:**
```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": ["progressive-skills-mcp"],
      "env": {
        "SKILLS_SOURCE": "/home/username/.skillz"
      }
    }
  }
}
```

**Windows:**
```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": ["progressive-skills-mcp"],
      "env": {
        "SKILLS_SOURCE": "C:\\Users\\YourName\\skills"
      }
    }
  }
}
```

### Option 3: VPS with Mounted Volume

For server deployments with persistent storage:

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": ["progressive-skills-mcp"],
      "env": {
        "SKILLS_SOURCE": "/mnt/data/skills"
      }
    }
  }
}
```

## System Prompt Configuration

Progressive disclosure works by adding skill metadata to your LLM agent's system prompt. This tells the agent what skills are available **without** loading all the detailed instructions upfront.

### System Prompt Template

Copy this template and add it to your agent's system prompt. Update the skill list with your actual skills:

```markdown
## Available Skills

You have access to specialized skills that provide detailed instructions for specific tasks. When a task requires specialized knowledge or a specific workflow, use the `load_skill` tool to get the full instructions.

### How to Use Skills

1. Check if a skill is relevant to the user's request
2. Call `load_skill("skill-name")` to get detailed instructions
3. Follow the instructions in the skill
4. Use `read_skill_file()` and `list_skill_files()` if the skill references additional resources

### Available Skills:

- **skill-name-1**: Brief description of what this skill does
- **skill-name-2**: Brief description of what this skill does
- **skill-name-3**: Brief description of what this skill does

[Add more skills as needed...]
```

### Example (Filled In)

```markdown
## Available Skills

You have access to specialized skills that provide detailed instructions for specific tasks. When a task requires specialized knowledge or a specific workflow, use the `load_skill` tool to get the full instructions.

### How to Use Skills

1. Check if a skill is relevant to the user's request
2. Call `load_skill("skill-name")` to get detailed instructions
3. Follow the instructions in the skill
4. Use `read_skill_file()` and `list_skill_files()` if the skill references additional resources

### Available Skills:

- **weather**: Get weather forecasts and conditions for any location
- **pptx**: Create professional PowerPoint presentations
- **docx**: Create and edit Word documents with formatting
- **context7-docs**: Look up technical documentation for libraries and frameworks
```

### When to Update the System Prompt

Update your system prompt whenever you:
- Add a new skill to your skills directory
- Remove a skill
- Change a skill's name or description

Simply edit the skill list in your agent's system prompt - no need to restart the MCP server.

## Progressive Disclosure Explained

### Level 1: System Prompt (Once per conversation)
```markdown
## Available Skills
- **context7-docs**: Look up technical documentation
```
**Cost:** ~200 tokens, sent ONCE at the start of conversation

### Level 2: On-Demand Instructions
```python
load_skill("context7-docs")  # Returns full SKILL.md
```
**Cost:** 0 tokens until the agent actually needs it!

### Level 3: Referenced Resources  
```python
read_skill_file("context7-docs", "references/api-guide.md")
```
**Cost:** 0 tokens until the skill specifically references it!

## Three Universal Tools

These tools are available regardless of how many skills you have:

1. **`load_skill(skill_name)`** - Returns the complete SKILL.md instructions
2. **`read_skill_file(skill_name, file_path)`** - Returns a specific resource file from the skill
3. **`list_skill_files(skill_name, subdirectory?)`** - Lists all available resources in a skill

## Creating Your Own Skills

### Skill Structure

Skills can be:
- **Directories** with a SKILL.md file
- **Zip archives** containing SKILL.md
- **.skill archives**

Example directory structure:
```
my-skills/
├── weather/
│   ├── SKILL.md
│   └── references/
│       └── api-docs.md
├── pptx/
│   ├── SKILL.md
│   └── templates/
│       └── example.pptx
└── custom-skill.zip
```

### SKILL.md Format

```markdown
---
name: skill-name
description: Brief one-line description shown in system prompt
---

# Skill Instructions

Detailed instructions for the AI agent to follow when using this skill.

## Purpose

Explain what this skill does and when to use it.

## Steps

1. First, do this...
2. Then, do that...
3. Finally, complete the task...

## Resources

You can reference additional files:
- See `references/api-docs.md` for API details
- Use `templates/example.pptx` as a template

## Notes

Any additional tips or warnings for using this skill.
```

### Example Skills Repository

Check out the example skills repo to get started:
- **Repository:** https://github.com/Flowtrica/agent-skills
- **What's included:** Sample skills demonstrating best practices

You can:
- Clone it as a starting point
- Fork it and add your own skills
- Use it as a reference for creating skills

## Sharing Skills

Want to share your skills with others?

1. Create a public GitHub repository with your skills
2. Share the repository URL
3. Others can use it by setting `SKILLS_SOURCE` to your repo URL

No PyPI publishing needed - just share the GitHub repo!

## Token Efficiency Comparison

| Approach | Tools/Request | Tokens/Request | 20 Skills |
|----------|--------------|----------------|-----------|
| Original Skillz | 20 tools | ~100 each | ~2000 tokens |
| **Progressive Skills MCP** | **3 tools** | **~50 each** | **~150 tokens** |
| **Improvement** | **-85%** | **-85%** | **13x better!** 🎉 |

## Supported MCP Clients

Progressive Skills MCP works with any MCP-compatible client:
- Claude Desktop
- Cherry Studio  
- Cline
- Zed
- And any other client supporting the MCP protocol

Configuration is similar across all clients - just adjust the JSON format to match your client's requirements.

## Troubleshooting

### "git command not found" error

If you're using a GitHub repository URL and get this error:

1. Install git on your system
2. Or use a local directory instead of a repository URL

### Skills not loading

1. Check that `SKILLS_SOURCE` points to the correct directory or repository
2. Verify the directory contains valid SKILL.md files
3. Check server logs for specific errors

### Environment variable not recognized

Some MCP clients may require specific formatting for environment variables. Check your client's documentation for the correct syntax.

## License

MIT (same as original skillz)

## Credits

- Based on [skillz](https://github.com/intellectronica/skillz) by Eleanor Berger
- Progressive disclosure modifications by Flowtrica
- Inspired by Claude.ai's skills system

## Links

- **GitHub:** https://github.com/Flowtrica/skills-mcp
- **PyPI:** https://pypi.org/project/progressive-skills-mcp/
- **Example Skills:** https://github.com/Flowtrica/agent-skills
