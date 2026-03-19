# Environment Setup Guide

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, Ubuntu 18.04+
- **Python Version**: 3.10 or higher (3.11 recommended)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 500MB for code and data, plus space for job data
- **Network**: Stable internet connection for API calls

### Recommended Setup
- **Python 3.11** with virtual environment
- **VS Code** with Python extension for development
- **Git** for version control and collaboration

## Python Environment Setup

### 1. Install Python 3.10+

#### Windows
```powershell
# Download from python.org or use winget
winget install Python.Python.3.11

# Verify installation
python --version
pip --version
```

#### macOS
```bash
# Using Homebrew
brew install python@3.11

# Or download from python.org
# Verify installation
python3 --version
pip3 --version
```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt update

# Install Python 3.11
sudo apt install python3.11 python3.11-venv python3-pip

# Verify installation
python3 --version
pip3 --version
```

### 2. Create Virtual Environment

#### Windows
```powershell
# Navigate to project directory
cd C:\Core_Workspace\02_Projects\SOC-Job-Task-Analyzer

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Verify activation (should show (venv) in prompt)
python --version
```

#### macOS/Linux
```bash
# Navigate to project directory
cd /path/to/SOC-Job-Task-Analyzer

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation
which python
```

### 3. Install Dependencies

```bash
# Ensure virtual environment is activated
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(requests|pandas|python-dotenv|fuzzywuzzy)"
```

## API Configuration

### SerpAPI Setup

1. **Get API Key**
   - Visit [SerpAPI](https://serpapi.com/)
   - Create free account (100 searches/month)
   - Copy your API key from dashboard

2. **Configure Environment Variables**
   ```bash
   # Create .env file in project root
   echo "SERPAPI_KEY=your_api_key_here" > .env
   ```

3. **Verify Configuration**
   ```python
   # Test environment loading
   python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key loaded:', bool(os.getenv('SERPAPI_KEY')))"
   ```

## Development Environment

### VS Code Setup (Recommended)

1. **Install VS Code**
   - Download from [code.visualstudio.com](https://code.visualstudio.com/)

2. **Install Python Extension**
   - Open VS Code
   - Go to Extensions (Ctrl+Shift+X)
   - Search for "Python" by Microsoft
   - Install and reload

3. **Configure Workspace**
   - Open project folder in VS Code
   - Python extension should auto-detect virtual environment
   - Select interpreter: `Python 3.11.x ('venv': venv)`

### Alternative IDEs

#### PyCharm
- Install PyCharm Professional or Community
- Open project directory
- Configure interpreter to use virtual environment

#### Jupyter Notebook (Optional)
```bash
# Install Jupyter
pip install jupyter

# Launch notebook server
jupyter notebook
```

## Project Structure Verification

After setup, verify your project structure:

```
SOC-Job-Task-Analyzer/
├── venv/                    # Virtual environment (created)
├── .env                     # Environment variables (created)
├── src/                     # Source code
│   ├── soc_scrapper_API.py
│   ├── data_analyzer.py
│   ├── task_aggregator.py
│   ├── task_thematic_clusterer.py
│   └── job_run.py
├── configs/
│   └── rules.json
├── data/
│   ├── raw/
│   └── processed/
├── docs/                    # Documentation
├── requirements.txt
├── README.md
└── .gitignore
```

## Testing Installation

### Basic Functionality Test

```python
# Test 1: Import verification
python -c "
import sys
print('Python version:', sys.version)
import pandas as pd
import requests
from dotenv import load_dotenv
print('All imports successful')
"
```

### API Connectivity Test

```python
# Test 2: API key validation
python -c "
from dotenv import load_dotenv
import os
load_dotenv()
api_key = os.getenv('SERPAPI_KEY')
if api_key:
    print('API key loaded successfully')
    print('Key length:', len(api_key))
else:
    print('ERROR: API key not found')
"
```

### Pipeline Dry Run

```bash
# Test 3: Pipeline import test
python -c "
import sys
sys.path.append('src')
try:
    import soc_scrapper_API
    import data_analyzer
    import task_aggregator
    import task_thematic_clusterer
    import job_run
    print('All modules imported successfully')
except ImportError as e:
    print('Import error:', e)
"
```

## Troubleshooting Common Issues

### Virtual Environment Issues

**Problem**: `python` command not found after activation
**Solution**: Use `python` on Windows, `python3` on macOS/Linux

**Problem**: Virtual environment not activating
**Solution**: Check execution policy on Windows:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Package Installation Issues

**Problem**: Permission denied during pip install
**Solution**: Ensure virtual environment is activated, or use:
```bash
pip install --user -r requirements.txt
```

**Problem**: Package conflicts or version issues
**Solution**: Recreate virtual environment:
```bash
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### API Key Issues

**Problem**: API key not loading
**Solution**: Check .env file encoding:
```python
# Test encoding
with open('.env', 'rb') as f:
    content = f.read()
    print('BOM detected:', content.startswith(b'\xef\xbb\xbf'))
```

If BOM detected, recreate .env without BOM:
```bash
rm .env
echo "SERPAPI_KEY=your_key_here" > .env
```

### Path Issues

**Problem**: Module import errors
**Solution**: Ensure you're running from project root:
```bash
cd /path/to/SOC-Job-Task-Analyzer
python src/job_run.py
```

## Performance Optimization

### Memory Management
- Close unnecessary applications during large data processing
- Monitor memory usage with Task Manager/Activity Monitor
- Consider upgrading RAM for processing >1000 job postings

### Network Optimization
- Use stable internet connection for API calls
- SerpAPI has rate limits; implement delays if needed
- Cache API responses for development/testing

### Storage Optimization
- Raw data: ~50MB per 1000 jobs
- Processed data: ~10MB for consolidated outputs
- Ensure adequate disk space for data growth

## Security Considerations

### API Key Management
- Never commit .env file to version control
- Use environment-specific keys for development/production
- Rotate keys periodically for security

### Data Privacy
- Job posting data may contain personal information
- Implement data retention policies
- Comply with data protection regulations (GDPR, CCPA)

### Code Security
- Keep dependencies updated
- Scan for vulnerabilities: `pip audit`
- Use virtual environments to isolate project dependencies

## Next Steps

After successful environment setup:

1. **Run Quick Start Tutorial**: Follow [QUICK_START.md](../01_GETTING_STARTED/QUICK_START.md)
2. **Review Architecture**: Read [ARCHITECTURE.md](../01_GETTING_STARTED/ARCHITECTURE.md)
3. **Customize Configuration**: Modify `configs/rules.json` for your research needs
4. **Execute Full Pipeline**: Run `python src/job_run.py` for complete analysis

## Support

If you encounter issues:

1. Check this troubleshooting section
2. Review [COMMON_ISSUES.md](../05_TROUBLESHOOTING/COMMON_ISSUES.md)
3. Check GitHub issues for similar problems
4. Create new issue with:
   - Python version
   - Operating system
   - Error messages
   - Steps to reproduce

---

**Last Updated:** December 2024
**Version:** 1.0.0