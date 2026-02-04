#!/usr/bin/env python3
"""
Apply progressive disclosure modifications to skillz.
This script safely patches the skillz codebase with minimal changes.
"""

import re
import shutil
from pathlib import Path
from datetime import datetime

SKILLZ_DIR = Path("/home/steven/skillz")
SERVER_FILE = SKILLZ_DIR / "src/skillz/_server.py"
VERSION_FILE = SKILLZ_DIR / "src/skillz/_version.py"


def create_backup():
    """Create timestamped backup of skillz directory."""
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = Path(f"/home/steven/skillz-backup-{timestamp}")
    print(f"📦 Creating backup at: {backup_dir}")
    shutil.copytree(SKILLZ_DIR, backup_dir)
    print(f"✅ Backup created\n")
    return backup_dir


def add_import():
    """Add progressive_disclosure import to _server.py."""
    print("Step 1: Adding import...")
    
    with open(SERVER_FILE, "r") as f:
        content = f.read()
    
    import_line = "\nfrom .progressive_disclosure import MetadataGenerator, register_progressive_disclosure_tools\n"
    
    if "from .progressive_disclosure import" in content:
        print("ℹ️  Import already present\n")
        return
    
    # Add after __version__ import
    content = content.replace(
        'from ._version import __version__',
        'from ._version import __version__' + import_line
    )
    
    with open(SERVER_FILE, "w") as f:
        f.write(content)
    
    print("✅ Import added\n")


def add_cli_arguments():
    """Add --generate-metadata and --format CLI arguments."""
    print("Step 2: Adding CLI arguments...")
    
    with open(SERVER_FILE, "r") as f:
        content = f.read()
    
    if "--generate-metadata" in content:
        print("ℹ️  CLI arguments already present\n")
        return
    
    # Add arguments before parse_args
    new_args = '''    parser.add_argument(
        "--generate-metadata",
        action="store_true",
        help="Generate skill metadata and exit (for system prompt integration)",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format for metadata (default: markdown)",
    )
    '''
    
    content = content.replace(
        '    args = parser.parse_args(argv)',
        new_args + '    args = parser.parse_args(argv)'
    )
    
    with open(SERVER_FILE, "w") as f:
        f.write(content)
    
    print("✅ CLI arguments added\n")


def add_metadata_generation():
    """Add metadata generation logic to main()."""
    print("Step 3: Adding metadata generation to main()...")
    
    with open(SERVER_FILE, "r") as f:
        content = f.read()
    
    if "if args.generate_metadata:" in content or "if hasattr(args, 'generate_metadata')" in content:
        print("ℹ️  Metadata generation already present\n")
        return
    
    # Add after registry.load() in main()
    metadata_code = '''
    # Handle metadata generation mode
    if hasattr(args, 'generate_metadata') and args.generate_metadata:
        generator = MetadataGenerator(registry)
        
        if hasattr(args, 'format') and args.format == "json":
            output = generator.generate_json_metadata()
        else:
            output = generator.generate_system_prompt_metadata()
        
        print(output)
        return
'''
    
    # Find main() function and insert after registry.load()
    pattern = r'(def main\([^)]*\):.*?registry\.load\(\))'
    
    def replacement(match):
        return match.group(0) + metadata_code
    
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(SERVER_FILE, "w") as f:
        f.write(content)
    
    print("✅ Metadata generation added\n")


def replace_tool_registration():
    """Replace per-skill tool registration with progressive disclosure."""
    print("Step 4: Switching to progressive disclosure tools...")
    
    with open(SERVER_FILE, "r") as f:
        content = f.read()
    
    if "register_progressive_disclosure_tools" in content and "register_skill_tool" not in content:
        print("ℹ️  Already using progressive disclosure\n")
        return
    
    # Find and replace the for loop that registers per-skill tools
    old_pattern = r'for skill in registry\.skills:.*?register_skill_tool\(mcp, skill, resources=resources\)'
    
    new_code = '''# Register progressive disclosure tools (3 universal tools)
    register_progressive_disclosure_tools(mcp, registry)
    
    LOGGER.info(
        "Registered 3 progressive disclosure tools for %d skills",
        len(registry.skills)
    )'''
    
    content = re.sub(old_pattern, new_code, content, flags=re.DOTALL)
    
    with open(SERVER_FILE, "w") as f:
        f.write(content)
    
    print("✅ Progressive disclosure tools enabled\n")


def update_version():
    """Update version to indicate modification."""
    print("Step 5: Updating version...")
    
    with open(VERSION_FILE, "r") as f:
        content = f.read()
    
    content = re.sub(
        r'__version__ = .*',
        '__version__ = "0.1.14-progressive-disclosure"',
        content
    )
    
    with open(VERSION_FILE, "w") as f:
        f.write(content)
    
    print("✅ Version updated\n")


def main():
    print("🔧 Applying Progressive Disclosure to Skillz")
    print("=" * 50)
    print()
    
    # Create backup first
    backup_dir = create_backup()
    
    try:
        # Apply all modifications
        add_import()
        add_cli_arguments()
        add_metadata_generation()
        replace_tool_registration()
        update_version()
        
        print("=" * 50)
        print("✨ Progressive Disclosure Applied Successfully!")
        print("=" * 50)
        print()
        print("📊 Changes Summary:")
        print("  - Added MetadataGenerator class")
        print("  - Created 3 universal tools (load_skill, read_skill_file, list_skill_files)")
        print("  - Added --generate-metadata CLI flag")
        print("  - Replaced per-skill tools with progressive disclosure")
        print()
        print("📝 Testing:")
        print(f"  1. Generate metadata:")
        print(f"     cd {SKILLZ_DIR} && uv run skillz --generate-metadata /home/steven/.skillz")
        print()
        print(f"  2. Test with MCP Inspector:")
        print(f"     npx @modelcontextprotocol/inspector -- uv run --directory {SKILLZ_DIR} skillz /home/steven/.skillz")
        print()
        print(f"💾 Backup location: {backup_dir}")
        print()
        print("🔄 To rollback if needed:")
        print(f"   rm -rf {SKILLZ_DIR} && cp -r {backup_dir} {SKILLZ_DIR}")
        
    except Exception as e:
        print(f"\n❌ Error during modification: {e}")
        print(f"\n🔄 Restoring from backup...")
        shutil.rmtree(SKILLZ_DIR)
        shutil.copytree(backup_dir, SKILLZ_DIR)
        print(f"✅ Restored from backup")
        raise


if __name__ == "__main__":
    main()
