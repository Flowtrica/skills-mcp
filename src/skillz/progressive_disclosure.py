"""Progressive disclosure implementation for skillz.

Add this code to _server.py to enable progressive disclosure.
"""

from typing import Optional, Any
from fastmcp import Context
from fastmcp.exceptions import ToolError
import base64


class MetadataGenerator:
    """Generate system prompt metadata for all skills."""
    
    def __init__(self, registry):
        self.registry = registry
    
    def generate_system_prompt_metadata(self) -> str:
        """Generate markdown-formatted skill metadata for system prompts."""
        skills = sorted(self.registry.skills, key=lambda s: s.slug)
        
        if not skills:
            return "No skills available."
        
        lines = [
            "## Available Skills",
            "",
            "You have access to specialized skills. To use a skill, call the `load_skill` tool with the skill name.",
            "",
        ]
        
        for skill in skills:
            lines.append(f"- **{skill.slug}**: {skill.metadata.description}")
        
        return "\n".join(lines)
    
    def generate_json_metadata(self) -> str:
        """Generate JSON metadata for programmatic use."""
        import json
        metadata = [
            {
                "name": skill.slug,
                "description": skill.metadata.description,
                "allowed_tools": list(skill.metadata.allowed_tools),
            }
            for skill in self.registry.skills
        ]
        return json.dumps(metadata, indent=2)


def register_progressive_disclosure_tools(mcp, registry) -> None:
    """Register 3 universal tools for progressive disclosure."""
    
    @mcp.tool(
        name="load_skill",
        description=(
            "Load the complete instructions for a skill. "
            "Use this when you've decided a skill is relevant based on "
            "the skill metadata in your system prompt. "
            "Returns the full SKILL.md content without frontmatter."
        )
    )
    async def load_skill_tool(
        skill_name: str,
        ctx: Optional[Context] = None,
    ) -> str:
        """Load full skill instructions (Level 2 progressive disclosure)."""
        try:
            skill = registry.get(skill_name)
            LOGGER.info("Loaded skill: %s", skill_name)
            return skill.read_body()
        except Exception as exc:
            raise ToolError(
                f"Skill '{skill_name}' not found. "
                f"Available skills can be seen in your system prompt."
            ) from exc
    
    @mcp.tool(
        name="read_skill_file",
        description=(
            "Read a specific file from a skill's directory. "
            "Use this when skill instructions reference a file "
            "(e.g., 'See references/api_reference.md'). "
            "Provide the skill name and relative file path."
        )
    )
    async def read_skill_file_tool(
        skill_name: str,
        file_path: str,
        ctx: Optional[Context] = None,
    ) -> str:
        """Read a specific file from skill directory (Level 3 progressive disclosure)."""
        try:
            skill = registry.get(skill_name)
            
            # Validate path doesn't traverse upward
            if ".." in file_path or file_path.startswith("/"):
                raise ToolError("Invalid path: path traversal not allowed")
            
            if not skill.exists(file_path):
                raise ToolError(
                    f"File '{file_path}' not found in skill '{skill_name}'"
                )
            
            # Read content
            data = skill.open_bytes(file_path)
            
            # Try to decode as UTF-8, fallback to base64 for binary
            try:
                content = data.decode("utf-8")
            except UnicodeDecodeError:
                content = f"[Binary file - base64 encoded]\n{base64.b64encode(data).decode('ascii')}"
            
            LOGGER.info("Read file: %s/%s", skill_name, file_path)
            return content
            
        except Exception as exc:
            raise ToolError(str(exc)) from exc
    
    @mcp.tool(
        name="list_skill_files",
        description=(
            "List files available in a skill's directory. "
            "Use this to discover what reference files, scripts, or resources "
            "a skill provides. Optionally specify a subdirectory like "
            "'references' or 'scripts'."
        )
    )
    async def list_skill_files_tool(
        skill_name: str,
        subdirectory: Optional[str] = None,
        ctx: Optional[Context] = None,
    ) -> str:
        """List available files in a skill directory."""
        try:
            skill = registry.get(skill_name)
            
            # Get all resource paths
            all_paths = list(skill.iter_resource_paths())
            
            # Filter by subdirectory if specified
            if subdirectory:
                # Normalize subdirectory path
                subdir_prefix = subdirectory.rstrip("/") + "/"
                filtered_paths = [
                    path for path in all_paths
                    if path.startswith(subdir_prefix)
                ]
            else:
                filtered_paths = all_paths
            
            if not filtered_paths:
                subdir_msg = f" in subdirectory '{subdirectory}'" if subdirectory else ""
                return f"No files found in skill '{skill_name}'{subdir_msg}"
            
            # Format output
            subdir_msg = f" in '{subdirectory}'" if subdirectory else ""
            lines = [f"Files in skill '{skill_name}'{subdir_msg}:"]
            lines.extend(f"  - {path}" for path in sorted(filtered_paths))
            
            return "\n".join(lines)
            
        except Exception as exc:
            raise ToolError(str(exc)) from exc
