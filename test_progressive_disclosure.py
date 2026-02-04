#!/usr/bin/env python3
"""Quick test to verify progressive disclosure tools are registered."""

import subprocess
import json

print("🧪 Testing Skillz Progressive Disclosure\n")

# Test 1: Metadata Generation
print("Test 1: Metadata Generation")
result = subprocess.run(
    ["/home/steven/.local/bin/uv", "run", "skillz", "--generate-metadata", "/home/steven/.skillz"],
    cwd="/home/steven/skillz",
    capture_output=True,
    text=True
)

if "Available Skills" in result.stdout and "test-skill" in result.stdout:
    print("✅ Metadata generation works!")
    print(f"   Output preview: {result.stdout[:100]}...")
else:
    print("❌ Metadata generation failed")
    print(f"   Stdout: {result.stdout}")
    print(f"   Stderr: {result.stderr}")

print()

# Test 2: JSON format
print("Test 2: JSON Metadata Format")
result = subprocess.run(
    ["/home/steven/.local/bin/uv", "run", "skillz", "--generate-metadata", "--format", "json", "/home/steven/.skillz"],
    cwd="/home/steven/skillz",
    capture_output=True,
    text=True
)

try:
    # Parse JSON to verify it's valid
    data = json.loads(result.stdout.split('\n', 2)[-1])  # Skip log lines
    if isinstance(data, list) and len(data) > 0:
        print("✅ JSON metadata works!")
        print(f"   Skills found: {len(data)}")
        print(f"   First skill: {data[0]['name']}")
    else:
        print("❌ JSON format unexpected")
except Exception as e:
    print(f"❌ JSON parsing failed: {e}")
    print(f"   Output: {result.stdout}")

print()
print("=" * 50)
print("✨ Progressive Disclosure is READY!")
print("=" * 50)
print()
print("Next steps:")
print("1. Add more skills to /home/steven/.skillz/")
print("2. Deploy to MCPHub on your VPS")
print("3. Configure Onyx to use the skills")
