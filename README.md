# Progressive Skills MCP

MCP server for SKILL.md files with **progressive disclosure** - achieving **13x token efficiency** over traditional MCP approaches.

Based on [intellectronica/skillz](https://github.com/intellectronica/skillz) with progressive disclosure modifications inspired by Claude.ai's skills system.

## Why Progressive Disclosure?

Many MCP servers load all their information upfront - every tool description, parameter, and instruction is included in each request. This consumes significant tokens even when most information isn't needed.

**Traditional MCP Approach:**
- Creates 1 tool per skill/capability
- All tool descriptions sent with every request
- 20 skills = 20 tools × ~100 tokens = **~2000 tokens/request**
- Information sent whether needed or not

**Progressive Skills MCP:**
- Creates 3 universal tools that load skills on-demand
- Only skill names/descriptions sent initially
- Full instructions loaded only when needed
- 20 skills = 3 tools × ~50 tokens + skill list = **~150 tokens/request**
- **13x more efficient!** 🎉

**The Three Levels:**
1. **System Prompt**: Brief skill list (~200 tokens, sent once)
2. **On-Demand Loading**: Full skill instructions (0 tokens until requested)
3. **Referenced Resources**: Additional files (0 tokens until accessed)

This approach is especially valuable when working with many skills or limited context windows.

## Features

✅ Progressive disclosure (3-level token efficiency)  
✅ Compatible with all SKILL.md format files  
✅ Supports .zip and .skill archives  
✅ Flexible skills source (local directories, VPS volumes)  
✅ Simple `uvx` installation - works with any MCP client  

## Installation

**Important:** Before installing, you must create a skills directory and optionally add some skills to it. The server will not start without a valid skills directory.

### Setup Steps

**Step 1: Create Your Skills Directory**

Choose where to store your skills:

**Local (Linux/Mac):**
```bash
mkdir -p ~/.skills
# Or any other location you prefer
mkdir -p /home/username/skills
```

**Local (Windows):**
```powershell
mkdir C:\Users\YourName\skills
```

**VPS/Container:**
- Create a volume or persistent directory on your host
- Mount it to your container (e.g., `/mnt/data/skills` → `/app/skills`)

**Step 2: Add Skills (Optional)**

You can start with an empty directory, but you'll need to add skills before the MCP server can do anything useful:

```bash
# Clone example skills
git clone https://github.com/Flowtrica/agent-skills.git ~/.skills

# Or create your own
mkdir -p ~/.skills/my-skill
# (See "Creating Your Own Skills" section below)
```

**Step 3: Configure Your MCP Client**

### Option 1: Local Installation (PC/Laptop)

For local development or personal use:

**Linux/Mac:**
```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": ["progressive-skills-mcp"],
      "env": {
        "SKILLS_SOURCE": "/home/username/skills"
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

### Option 2: VPS with Mounted Volume

For server deployments with persistent storage:

**First, mount the volume in your container:**
- In Docker: Mount host directory to container path
- Example: Host `/mnt/data/skills` → Container `/app/skills`

**Then configure:**
```json
{
  "mcpServers": {
    "skills": {
      "command": "uvx",
      "args": ["progressive-skills-mcp"],
      "env": {
        "SKILLS_SOURCE": "/app/skills"
      }
    }
  }
}
```

## Adding More Skills Later

You can add skills to your directory at any time:

**Method 1: Clone a skills repository**
```bash
cd ~/.skills  # Or your skills directory
git clone https://github.com/Flowtrica/agent-skills.git . # Your own skills repository or aone you have found that contains skills.
```

**Method 2: Create individual skills**

```bash
# Example: Adding a weather skill
mkdir -p ~/.skills/weather
cat > ~/.skills/weather/SKILL.md << 'EOF'
---
name: weather
description: Get weather forecasts for any location
---

# Weather Skill

This skill helps you get weather information...
EOF
```

The server will find it automatically when restarted.

## System Prompt Configuration

Progressive disclosure works by adding skill metadata to your LLM agent's system prompt. This tells the agent what skills are available **without** loading all the detailed instructions upfront.

### System Prompt Template

Copy this template and add it to your agent's system prompt. Update the skill list with your actual skills:

```markdown
## Available Skills

You have access to specialized skills that provide detailed instructions for specific tasks.

### How to Use Skills

**Before responding to each user message:**
1. Review the available skills list below
2. Determine if any skill would improve your response quality
3. If a skill is relevant, call `load_skill("skill-name")` to get detailed instructions
4. Follow the skill's instructions to complete the task

**Important:** Proactively use skills based on message context - don't wait for the user to explicitly request a skill. For example, if the user asks "What's the weather like?", immediately use the weather skill without asking.

**When you load a skill:**
- Follow its instructions exactly
- Use `read_skill_file("skill-name", "path/to/file")` if the skill references additional resources
- Use `list_skill_files("skill-name")` to see what resources are available

**MCP Tool Skills:** Some skills provide guidance for other MCP tools. Before using an MCP tool, check if a corresponding skill exists and load it first for usage instructions.

### Available Skills:

- **skill-name-1**: Brief description of what this skill does
- **skill-name-2**: Instructions for how to use the [MCP Tool Name]. Brief description of what the MCP tool does
- **skill-name-3**: Brief description of what this skill does

[Add more skills as needed...]

**Note:** For skills that provide instructions for other MCP tools, always start the description with "Instructions for how to use the [MCP Tool Name]" followed by what the tool does. This helps the agent recognize when to use the skill before calling the MCP tool.
```

### Example (Filled In)

```markdown
## Available Skills

You have access to specialized skills that provide detailed instructions for specific tasks.

### How to Use Skills

**Before responding to each user message:**
1. Review the available skills list below
2. Determine if any skill would improve your response quality
3. If a skill is relevant, call `load_skill("skill-name")` to get detailed instructions
4. Follow the skill's instructions to complete the task

**Important:** Proactively use skills based on message context - don't wait for the user to explicitly request a skill. For example, if the user asks "What's the weather like?", immediately use the weather skill without asking.

**When you load a skill:**
- Follow its instructions exactly
- Use `read_skill_file("skill-name", "path/to/file")` if the skill references additional resources
- Use `list_skill_files("skill-name")` to see what resources are available

**MCP Tool Skills:** Some skills provide guidance for other MCP tools. Before using an MCP tool, check if a corresponding skill exists and load it first for usage instructions.

### Available Skills:

- **weather**: Get weather forecasts and conditions for any location
- **pptx**: Create professional PowerPoint presentations
- **context7**: Instructions for how to use the Context7 MCP which pulls up-to-date, version-specific documentation and code examples straight from the source
- **docx**: Create and edit Word documents with formatting
```

### Adding Skills for MCP Tools

If you're adding a skill that provides instructions for another MCP tool, use this format in the system prompt;
```markdown
---
skill name: context7
description: Instructions for how to use the Context7 MCP which pulls up-to-date, version-specific documentation and code examples straight from the source
---
```

**Why this format matters:** Starting the description with "Instructions for how to use the [MCP Tool Name]" is critical. It tells the agent this skill should be loaded *before* using that MCP tool. Without this pattern, the agent won't consistently recognize when to use the skill.


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

You can clone it to your local machine or VPS to use as a starting point.

## Sharing Skills

Want to share your skills with others?

1. Create a public GitHub repository with your skills
2. Share the repository URL
3. Others can clone it to their local directory or VPS volume
4. Point `SKILLS_SOURCE` to the cloned directory

## Token Efficiency Comparison

| Approach | Tools/Request | Tokens/Request | 20 Skills |
|----------|--------------|----------------|-----------|
| Traditional MCP (one tool per skill) | 20 tools | ~100 each | ~2000 tokens |
| **Progressive Disclosure** | **3 tools** | **~50 each** | **~150 tokens** |
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

### Skills not loading

1. Check that `SKILLS_SOURCE` points to the correct directory
2. Verify the directory contains valid SKILL.md files
3. Check server logs for specific errors
4. Ensure the path is accessible to the MCP server

### Environment variable not recognized

Some MCP clients may require specific formatting for environment variables. Check your client's documentation for the correct syntax.

### Path issues on Windows

Windows paths need double backslashes in JSON:
```json
"SKILLS_SOURCE": "C:\\Users\\YourName\\skills"
```

Or use forward slashes:
```json
"SKILLS_SOURCE": "C:/Users/YourName/skills"
```

## License

MIT (same as original skillz)

## Credits

- Based on [skillz](https://github.com/intellectronica/skillz) by Eleanor Berger
- Progressive disclosure modifications by Flowtrica
- Inspired by Claude.ai's skills system

## Links

- **GitHub:** https://github.com/Flowtrica/progressive-skills-mcp
- **PyPI:** https://pypi.org/project/progressive-skills-mcp/
- **Example Skills:** https://github.com/Flowtrica/agent-skills
