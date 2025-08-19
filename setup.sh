#!/bin/bash

echo "🧬 EGFR Docking Project Setup (macOS)"
echo "====================================="

# Update system via Homebrew
echo "📦 Updating system packages..."
brew update

# Install system dependencies
echo "🔧 Installing system dependencies..."
brew install python cmake boost open-babel autodock-vina wget curl unzip || true

# Optional: install PyMOL (karena tidak ada di PyPI)
echo "🧪 Installing PyMOL (open-source)..."
brew install brewsci/bio/pymol || true

# Create project structure
echo "📁 Creating project structure..."
mkdir -p data/{proteins,ligands,results}
mkdir -p scripts notebooks

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
python3 -m venv egfr_docking_env
source egfr_docking_env/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python packages (skip pymol-open-source, handled by brew)
echo "📚 Installing Python packages..."
pip install -r requirements.txt

# Make main.py executable if exists
if [ -f "main.py" ]; then
    chmod +x main.py
fi

echo "✅ Setup completed successfully!"
echo ""
echo "👉 To run the docking simulation:"
echo "   source egfr_docking_env/bin/activate"
echo "   python main.py"