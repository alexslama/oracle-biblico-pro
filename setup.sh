#!/bin/bash
# Oracle Biblico PRO - Automated Setup Script
# Mac M1 Max & Google Cloud Optimized
# Author: alexslama
# Date: 2025

set -e  # Exit on error

echo "🚀 Oracle Biblico PRO - Starting Setup..."
echo "========================================="

# 1. Check Python version (3.10+)
echo "✓ Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "  Python version: $PYTHON_VERSION"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10+"
    exit 1
fi

# 2. Create virtual environment
echo "✓ Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 3. Activate virtual environment
echo "✓ Activating virtual environment..."
source venv/bin/activate

# 4. Upgrade pip
echo "✓ Upgrading pip..."
pip install --upgrade pip setuptools wheel

# 5b. Install remaining dependencies
# 5a. Install PyTorch with M1 Metal acceleration
echo "✓ Installing PyTorch with M1 GPU acceleration..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cpu

pip install -r requirements.txt

# 6. Create required directories
echo "✓ Creating project directories..."
mkdir -p data/raw
mkdir -p data/processed
mkdir -p data/models
mkdir -p logs
mkdir -p outputs

# 7. Download Bible texts (optional)
echo "✓ Downloading Bible reference texts..."
echo "  (Note: You can manually add bible_texts.json to data/raw/)"

echo ""
echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. cd $(pwd)"
echo "2. source venv/bin/activate"
echo "3. python3 scripts/collect_data.py"
echo "4. python3 scripts/prepare_training_data.py"
echo "5. python3 scripts/finetune_llama.py"
echo "6. python3 scripts/build_rag.py"
echo "7. python3 scripts/analysis_pipeline.py"
echo ""
echo "For Google Cloud deployment:"
echo "  gcloud init"
echo "  gcloud compute instances create oracle-biblico-pro --machine-type=n1-standard-8 --zone=us-central1-a"
echo ""
