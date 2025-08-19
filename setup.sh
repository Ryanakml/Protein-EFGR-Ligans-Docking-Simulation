#!/bin/bash

echo "🧬 EGFR Docking Project Setup (macOS)"
echo "====================================="

# Update system via Homebrew
echo "📦 Updating system packages..."
brew update

# Install system dependencies
echo "🔧 Installing system dependencies..."
brew install python cmake boost open-babel autodock-vina wget curl unzip || true

# Create project structure
echo "📁 Creating project structure..."
mkdir -p data/{proteins,ligands,results}
mkdir -p scripts notebooks

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv egfr_docking_env
source egfr_docking_env/bin/activate

# Install Python packages (skip pymol-open-source on Mac)
echo "📚 Installing Python packages..."
pip install --upgrade pip
grep -v "pymol-open-source" requirements.txt > temp_reqs.txt
pip install -r temp_reqs.txt
rm temp_reqs.txt

# Make scripts executable
chmod +x main.py

echo "✅ Setup completed successfully!"
echo ""
echo "To run the docking simulation:"
echo "1. source egfr_docking_env/bin/activate"
echo "2. python main.py"