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
✅ Use your own skills - no forking required!  

## Quick Start

### 1. Install the MCP Server

```bash
pip install progressive-skills-mcp
```

### 2. Add Your Skills

Put your skills in `~/.skillz/` or any directory you choose:

```bash
mkdir -p ~/.skillz
# Add skill directories or .zip files
```

**Or clone an existing skills repo:**

```bash
git clone https://github.com/Flowtrica/agent-skills.git ~/.skillz
```

### 3. Run the Server

```bash
# Use default location (~/.skillz)
progressive-skills-mcp

# Or specify custom directory
progressive-skills-mcp /path/to/your/skills
```

## Using with MCPHub

### Option 1: Local Skills Directory

If your skills are on the same machine as MCPHub:

```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": ["progressive-skills-mcp", "/path/to/skills"]
    }
  }
}
```

### Option 2: Clone Skills from Git

Skills cloned fresh each time MCPHub starts:

```json
{
  "mcpServers": {
    "skills": {
      "command": "sh",
      "args": [
        "-c",
        "cd /tmp && rm -rf skills && git clone https://github.com/YOUR_USERNAME/your-skills.git skills && uvx progressive-skills-mcp /tmp/skills"
      ]
    }
  }
}
```

### Option 3: Just the Server (Uses ~/.skillz)

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

## System Prompt Configuration

Progressive disclosure works by adding skill metadata to your LLM agent's system prompt. This tells the agent what skills are available **without** loading all the detailed instructions.

### Step 1: Generate Metadata

```bash
# Generate from default location
progressive-skills-mcp --generate-metadata

# Or from custom directory
progressive-skills-mcp --generate-metadata /path/to/skills
```

This outputs:

```markdown
## Available Skills

You have access to specialized skills that provide detailed instructions for specific tasks. When a task requires specialized knowledge or a specific workflow, use the `load_skill` tool to get the full instructions.

### How to Use Skills

1. Check if a skill is relevant to the user's request
2. Call `load_skill("skill-name")` to get detailed instructions
3. Follow the instructions in the skill
4. Use `read_skill_file()` if the skill references additional resources

**Available skills:**

- **context7-docs-lookup**: Look up documentation from Context7 for libraries and frameworks
```

### Step 2: Add to Agent System Prompt

Copy the metadata output and add it to your LLM agent's system prompt. For example, in **Onyx**, **LibreChat**, or **Open WebUI**:

```
You are a helpful AI assistant.

[... other system prompt content ...]

## Available Skills

You have access to specialized skills that provide detailed instructions for specific tasks...

- **context7-docs-lookup**: Look up documentation from Context7...
```

### Step 3: Agent Uses Skills

When relevant, the agent will:

1. **See skill in system prompt** → "context7-docs-lookup is available"
2. **Call load_skill** → `load_skill("context7-docs-lookup")`
3. **Receive full instructions** → Complete SKILL.md content
4. **Follow instructions** → Execute the skill workflow

### Example Conversation

**User:** "How do I use React hooks in Next.js?"

**Agent thinks:** *The context7-docs-lookup skill can help with documentation lookup*

**Agent calls:** `load_skill("context7-docs-lookup")`

**Agent receives:** Full skill instructions on how to use Context7 API

**Agent executes:** Follows skill instructions to look up Next.js documentation

**Agent responds:** "Here's how to use React hooks in Next.js..." (with accurate docs)

## Progressive Disclosure Explained

### Level 1: System Prompt (Once per conversation)
```markdown
## Available Skills
- **context7-docs-lookup**: Look up documentation
```
**Cost:** ~200 tokens, sent ONCE

### Level 2: On-Demand Instructions
```python
load_skill("context7-docs-lookup")  # Returns full SKILL.md
```
**Cost:** 0 tokens until loaded (only when needed!)

### Level 3: Referenced Resources  
```python
read_skill_file("context7-docs-lookup", "references/api.md")
```
**Cost:** 0 tokens until accessed (only when the skill needs it!)

## Three Universal Tools

These tools are available regardless of how many skills you have:

1. **`load_skill(skill_name)`** - Returns SKILL.md body without frontmatter
2. **`read_skill_file(skill_name, file_path)`** - Returns specific resource file
3. **`list_skill_files(skill_name, subdirectory?)`** - Lists available resources

## Usage Examples

```bash
# Run with default skills directory (~/.skillz)
progressive-skills-mcp

# Run with custom directory
progressive-skills-mcp /path/to/skills

# Generate metadata for system prompt
progressive-skills-mcp --generate-metadata

# Generate JSON metadata
progressive-skills-mcp --generate-metadata --format json

# List all discovered skills
progressive-skills-mcp --list-skills

# List skills in custom directory
progressive-skills-mcp --list-skills /path/to/skills
```

## Creating Your Own Skills

### Skill Structure

Skills can be:
- **Directories** with SKILL.md file
- **Zip archives** containing SKILL.md
- **.skill archives**

Example:
```
~/.skillz/
├── weather/
│   ├── SKILL.md
│   └── references/
│       └── api.md
├── pptx.zip
└── custom-skill/
    └── SKILL.md
```

### SKILL.md Format

```markdown
---
name: skill-name
description: Brief one-line description
---

# Skill Instructions

Detailed instructions for the AI agent to follow...

## Steps

1. First do this
2. Then do that
3. Finally, complete the task

## Resources

See references/api.md for API details.
```

### Example Skills Repo

Check out the example skills repo:
https://github.com/Flowtrica/agent-skills

You can:
- Clone it: `git clone https://github.com/Flowtrica/agent-skills.git ~/.skillz`
- Fork it and add your own skills
- Use it as a template for your own skills repo

## Token Efficiency Comparison

| Approach | Tools/Request | Tokens/Request | 20 Skills |
|----------|--------------|----------------|-----------|
| Original | 20 tools | ~100 each | 2000 tokens |
| **Progressive Skills MCP** | **3 tools** | **~50 each** | **150 tokens** |
| **Improvement** | | | **13x better!** 🎉 |

## For Skill Creators

Want to share your skills with others?

1. Create a GitHub repo with your skills
2. Users can clone it: `git clone YOUR_REPO ~/.skillz`
3. Or users can point MCPHub to it directly (see Option 2 above)

No need to publish anything to PyPI - just share your skills repo!

## License

MIT (same as original skillz)

## Credits

- Based on [skillz](https://github.com/intellectronica/skillz) by Eleanor Berger
- Progressive disclosure modifications by Flowtrica
- Inspired by Claude.ai's skills system

## Links

- GitHub: https://github.com/Flowtrica/skills-mcp
- PyPI: https://pypi.org/project/progressive-skills-mcp/
- Example skills: https://github.com/Flowtrica/agent-skills
