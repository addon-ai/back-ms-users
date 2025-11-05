#!/bin/bash

# Code Generation Pipeline
# Complete pipeline for generating Java backends and JSON schemas from Smithy definitions

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Define paths
CONFIG_PATH="$PROJECT_ROOT/libs/config/params.json"
TEMPLATES_DIR="$PROJECT_ROOT/libs/pyjava-backend-codegen/templates"

# Get first project name from params.json array
if [ -f "$PROJECT_ROOT/libs/config/params.json" ]; then
    PROJECT_NAME=$(python3 -c "import json; config=json.load(open('$PROJECT_ROOT/libs/config/params.json')); print(config[0]['project']['general']['name'] if config else 'generated-project')")
else
    PROJECT_NAME="generated-project"
fi

OUTPUT_DIR="$PROJECT_ROOT"

echo "🚀 Starting Code Generation Pipeline"
echo "📋 Projects: Multiple projects from config array"
echo "⚙️  Config: $CONFIG_PATH"
echo "📁 Templates: $TEMPLATES_DIR"
echo "📂 Output: $OUTPUT_DIR"
echo ""

# Check if Python 3 is available
echo "🔍 Checking Python 3 availability..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi
echo "✅ Python 3 found"

# Install pystache if not available
echo "📦 Checking dependencies..."
if ! python3 -c "import pystache" 2>/dev/null; then
    echo "📥 Installing pystache..."
    pip3 install pystache
    echo "✅ Pystache installed"
else
    echo "✅ Dependencies satisfied"
fi

# Remove existing projects if they exist
echo "🗑️  Cleaning up existing projects..."
if [ -d "$PROJECT_ROOT/projects" ]; then
    rm -rf "$PROJECT_ROOT/projects"
fi
echo "✅ Cleanup complete"

echo ""
echo "🏗️  Step 1: Generating Java Backend projects with hexagonal architecture..."
echo ""

# Run the Java backend generator
python3 "$PROJECT_ROOT/libs/java-backend-generator.py" "$TEMPLATES_DIR"

echo ""
echo "📋 Step 2: Generating JSON Schemas from OpenAPI specifications..."
echo ""

# Run the JSON schema generator
python3 "$PROJECT_ROOT/libs/jsonschema-generator.py"

echo ""
echo "🎲 Step 3: Generating fake data for unit testing..."
echo ""

# Run the fake data generator
python3 "$PROJECT_ROOT/libs/fake-data-generator.py"

echo ""
echo "📚 Step 4: Generating OpenAPI documentation..."
echo ""

# Run the OpenAPI documentation generator
python3 "$PROJECT_ROOT/libs/openapi-docs-generator.py"

echo ""
echo "🏗️  Step 5: Generating architectural diagrams (components & sequences)..."
echo ""

# Run the architectural documentation generator
python3 "$PROJECT_ROOT/libs/architect-docs-generator.py"

echo ""
echo "🎉 Code Generation Pipeline complete!"
echo "📁 Generated outputs:"
echo "   • projects/ → Java Spring Boot applications with hexagonal architecture"
echo "   • schemas/ → JSON Schema files from OpenAPI specs"
echo "   • schemas/*/fake-data/ → Fake data"
echo "   • docs/puml/open-api/ → OpenAPI documentation (PlantUML, Markdown, TXT)"
echo "   • docs/puml/components/ → Architectural component diagrams (PlantUML)"
echo "   • docs/puml/sequences/ → CRUD sequence diagrams by service (PlantUML)"
echo "🚀 Ready to run: cd projects/[project-name] && mvn spring-boot:run"