#!/bin/bash
# Apply progressive disclosure modifications to skillz

set -e

SKILLZ_DIR="/home/steven/skillz"
BACKUP_DIR="/home/steven/skillz-backup-$(date +%Y%m%d-%H%M%S)"

echo "🔧 Applying Progressive Disclosure to Skillz"
echo "=============================================="
echo ""

# Create backup
echo "📦 Creating backup at: $BACKUP_DIR"
cp -r "$SKILLZ_DIR" "$BACKUP_DIR"
echo "✅ Backup created"
echo ""

cd "$SKILLZ_DIR"

# Step 1: Add import in _server.py
echo "Step 1: Adding imports..."
if ! grep -q "from .progressive_disclosure import" src/skillz/_server.py; then
    # Add after the existing imports (after "from ._version import __version__")
    sed -i '/from \._version import __version__/a\\nfrom .progressive_disclosure import MetadataGenerator, register_progressive_disclosure_tools' src/skillz/_server.py
    echo "✅ Imports added"
else
    echo "ℹ️  Imports already present"
fi

# Step 2: Add CLI arguments
echo ""
echo "Step 2: Adding CLI arguments..."
if ! grep -q "\-\-generate-metadata" src/skillz/_server.py; then
    # Find the parser section and add new arguments before parse_args
    cat > /tmp/skillz_cli_patch.txt << 'EOF'
    parser.add_argument(
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
EOF

    # Insert before "args = parser.parse_args"
    sed -i '/args = parser\.parse_args/i\    parser.add_argument(\n        "--generate-metadata",\n        action="store_true",\n        help="Generate skill metadata and exit (for system prompt integration)",\n    )\n    parser.add_argument(\n        "--format",\n        choices=["markdown", "json"],\n        default="markdown",\n        help="Output format for metadata (default: markdown)",\n    )' src/skillz/_server.py
    
    echo "✅ CLI arguments added"
else
    echo "ℹ️  CLI arguments already present"
fi

# Step 3: Modify main() to handle metadata generation
echo ""
echo "Step 3: Adding metadata generation to main()..."
if ! grep -q "if args.generate_metadata:" src/skillz/_server.py; then
    # Create a Python script to do the modification
    cat > /tmp/modify_main.py << 'PYEOF'
import re

with open("src/skillz/_server.py", "r") as f:
    content = f.read()

# Find the main function and add metadata generation after registry.load()
insertion = '''
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

# Insert after "registry.load()" in main()
pattern = r'(def main\(.*?\):.*?registry\.load\(\))'
content = re.sub(
    pattern,
    r'\1' + insertion,
    content,
    flags=re.DOTALL
)

with open("src/skillz/_server.py", "w") as f:
    f.write(content)
PYEOF
    
    python3 /tmp/modify_main.py
    echo "✅ Metadata generation added to main()"
else
    echo "ℹ️  Metadata generation already present"
fi

# Step 4: Modify build_server to use progressive disclosure
echo ""
echo "Step 4: Switching to progressive disclosure tools..."

# Create Python script to replace tool registration
cat > /tmp/modify_build_server.py << 'PYEOF'
import re

with open("src/skillz/_server.py", "r") as f:
    content = f.read()

# Find and replace the tool registration section in build_server
old_pattern = r'for skill in registry\.skills:.*?register_skill_tool\(mcp, skill, resources=resources\)'

new_code = '''# Register progressive disclosure tools (3 universal tools)
    register_progressive_disclosure_tools(mcp, registry)
    
    LOGGER.info(
        "Registered 3 progressive disclosure tools for %d skills",
        len(registry.skills)
    )'''

content = re.sub(
    old_pattern,
    new_code,
    content,
    flags=re.DOTALL
)

with open("src/skillz/_server.py", "w") as f:
    f.write(content)
PYEOF

if grep -q "register_skill_tool" src/skillz/_server.py; then
    python3 /tmp/modify_build_server.py
    echo "✅ Progressive disclosure tools enabled"
else
    echo "ℹ️  Already using progressive disclosure"
fi

# Step 5: Update version to indicate modification
echo ""
echo "Step 5: Updating version..."
sed -i 's/__version__ = .*/__version__ = "0.1.14-progressive-disclosure"/' src/skillz/_version.py
echo "✅ Version updated"

echo ""
echo "=============================================="
echo "✨ Progressive Disclosure Applied Successfully!"
echo "=============================================="
echo ""
echo "📊 Changes Summary:"
echo "  - Added MetadataGenerator class"
echo "  - Created 3 universal tools (load_skill, read_skill_file, list_skill_files)"
echo "  - Added --generate-metadata CLI flag"
echo "  - Replaced per-skill tools with progressive disclosure"
echo ""
echo "📝 Testing:"
echo "  1. Generate metadata:"
echo "     cd $SKILLZ_DIR && uv run skillz --generate-metadata /home/steven/.skillz"
echo ""
echo "  2. Run MCP server:"
echo "     cd $SKILLZ_DIR && uv run skillz /home/steven/.skillz"
echo ""
echo "💾 Backup location: $BACKUP_DIR"
echo ""
echo "🔄 To rollback if needed:"
echo "   rm -rf $SKILLZ_DIR && cp -r $BACKUP_DIR $SKILLZ_DIR"
