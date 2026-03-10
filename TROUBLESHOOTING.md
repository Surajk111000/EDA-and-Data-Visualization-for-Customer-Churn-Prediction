# Troubleshooting Guide

Common issues and their solutions.

## Installation Issues

### Issue: "Python is not installed"
**Error**: `python: command not found` or `'python' is not recognized`

**Solutions**:
1. Install Python from [python.org](https://www.python.org)
2. During installation, check "Add Python to PATH"
3. Restart your terminal/command prompt
4. Verify: `python --version`

---

### Issue: "pip is not recognized"
**Error**: `'pip' is not recognized as an internal or external command`

**Solutions**:
1. Ensure Python is installed correctly
2. Try `python -m pip --version`
3. Update pip: `python -m pip install --upgrade pip`
4. Use `python -m pip` instead of `pip` if issues persist

---

### Issue: "Permission denied" on macOS/Linux
**Error**: `Permission denied` when running `./run.sh`

**Solution**:
```bash
chmod +x run.sh
./run.sh
```

---

## Dependency Issues

### Issue: "ModuleNotFoundError: No module named 'streamlit'"
**Error**: `ModuleNotFoundError: No module named 'streamlit'`

**Solutions**:
1. Install all requirements:
   ```bash
   pip install -r requirements.txt
   ```
2. Verify installation:
   ```bash
   pip list | grep streamlit
   ```
3. If still not found, reinstall:
   ```bash
   pip uninstall streamlit
   pip install streamlit==1.31.1
   ```

---

### Issue: "No module named 'venv'"
**Error**: `Error: the following arguments are required: ENV_DIR`

**Solution**:
```bash
# Use python3 explicitly
python3 -m venv venv

# On Windows, try:
python -m venv venv
```

---

### Issue: "Conflicting package versions"
**Error**: Version conflict during `pip install -r requirements.txt`

**Solutions**:
1. Upgrade pip, setuptools, and wheel:
   ```bash
   pip install --upgrade pip setuptools wheel
   ```
2. Install in a fresh virtual environment
3. Use specific Python version:
   ```bash
   python3.9 -m venv venv  # For Python 3.9
   ```

---

## Runtime Issues

### Issue: "FileNotFoundError: 'client_data.csv' not found"
**Error**: `FileNotFoundError: File not found: ./client_data.csv`

**Solutions**:
1. Ensure CSV files are in the same directory as `app.py`
2. Check file names are exactly correct (case-sensitive on Linux/macOS)
3. Verify files exist:
   ```bash
   # Windows
   dir *.csv
   
   # macOS/Linux
   ls -la *.csv
   ```
4. Update file paths in code if files are elsewhere

---

### Issue: "Port 8501 is already in use"
**Error**: `Address already in use` or `Port 8501 already running`

**Solutions**:
1. Run on a different port:
   ```bash
   streamlit run app.py --server.port 8502
   ```
2. Kill the existing process:
   ```bash
   # Windows
   netstat -ano | findstr :8501
   taskkill /PID <PID> /F
   
   # macOS/Linux
   lsof -i :8501
   kill -9 <PID>
   ```
3. Wait a moment and try again

---

### Issue: "ValueError: File is empty"
**Error**: `ValueError: File is empty: ./client_data.csv`

**Solutions**:
1. Check file size:
   ```bash
   # Windows
   dir client_data.csv
   
   # macOS/Linux
   ls -lh client_data.csv
   ```
2. Ensure CSV files have data (not empty)
3. Verify files weren't corrupted during download

---

### Issue: "UnicodeDecodeError" when loading CSV
**Error**: `UnicodeDecodeError: 'utf-8' codec can't decode...`

**Solutions**:
1. The CSV might have different encoding
2. Try specifying encoding in config:
   ```python
   # In utils.py, modify DataLoader.load_data():
   df = pd.read_csv(filepath, encoding='latin-1')
   ```
3. Common encodings: 'utf-8', 'latin-1', 'iso-8859-1', 'cp1252'

---

## Application Issues

### Issue: "No visualizations appear"
**Error**: Plots don't show in Streamlit

**Solutions**:
1. Check that matplotlib/seaborn installed:
   ```bash
   pip list | grep -E "matplotlib|seaborn"
   ```
2. Ensure proper imports at top of `app.py`:
   ```python
   import matplotlib.pyplot as plt
   import seaborn as sns
   ```
3. For Streamlit, use `st.pyplot()`:
   ```python
   st.pyplot(fig)
   ```

---

### Issue: Application runs but page is blank
**Error**: Streamlit loads but shows no content

**Solutions**:
1. Check browser console for errors (F12)
2. Check terminal for error messages
3. Restart the app
4. Clear browser cache: Ctrl+Shift+Delete
5. Try a different browser

---

### Issue: Slow data loading
**Problem**: App takes long time to load

**Solutions**:
1. Enable caching in `config.py`:
   ```python
   STREAMLIT_CONFIG["enable_caching"] = True
   ```
2. Sample data for testing:
   ```python
   STREAMLIT_CONFIG["sample_data"] = True
   STREAMLIT_CONFIG["sample_size"] = 10000
   ```
3. Restart the app to clear cache
4. Reduce number of columns being analyzed

---

### Issue: "Memory Error" or "Out of Memory"
**Error**: Application crashes due to insufficient memory

**Solutions**:
1. Enable data sampling in `config.py`:
   ```python
   DATA_CONFIG["sample_data"] = True
   DATA_CONFIG["sample_size"] = 50000
   ```
2. Close other applications to free memory
3. Split analysis into smaller chunks
4. Use a machine with more RAM

---

## Data Issues

### Issue: "Missing values not detected"
**Problem**: Missing values appear in data but not detected

**Solutions**:
1. Check missing value representations:
   - NaN, None, "N/A", "", "null", -999
2. Update data cleaning logic to handle these
3. Add custom handling in `DataProcessor`

---

### Issue: "Incorrect data types detected"
**Problem**: Columns detected as wrong type (e.g., number as string)

**Solutions**:
1. Check raw data with `head()`:
   ```python
   df.head()
   ```
2. Verify data types:
   ```python
   df.dtypes
   ```
3. Force type conversion:
   ```python
   df['column'] = pd.to_numeric(df['column'], errors='coerce')
   ```

---

### Issue: "Datetime parsing fails"
**Error**: `ValueError: time data does not match format`

**Solutions**:
1. Check actual date format in data
2. Update date format in `utils.py`:
   ```python
   # Change from '%Y-%m-%d' to actual format
   df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')
   ```
3. Use `infer_datetime_format=True`:
   ```python
   df['date'] = pd.to_datetime(df['date'], infer_datetime_format=True)
   ```

---

## Deployment Issues

### Issue: "Can't connect to Streamlit Cloud"
**Error**: Deployment to Streamlit Cloud fails

**Solutions**:
1. Ensure all files pushed to GitHub
2. Update `requirements.txt` with all dependencies
3. Check that `app.py` is in repository root
4. Verify GitHub credentials and permissions

---

### Issue: "Docker build fails"
**Error**: Docker container fails to build

**Solutions**:
1. Check Docker is installed: `docker --version`
2. Verify Dockerfile syntax
3. Build with verbose output:
   ```bash
   docker build -t app . --progress=plain
   ```
4. Check Dockerfile paths are correct

---

## Debugging Tips

### Enable debug logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
```

### Check data at each step
```python
print(f"Shape: {df.shape}")
print(f"Columns: {df.columns.tolist()}")
print(f"Types: {df.dtypes}")
print(df.head())
```

### Use assertions for validation
```python
assert len(df) > 0, "DataFrame is empty"
assert 'id' in df.columns, "Missing 'id' column"
```

### Test in development mode
```bash
streamlit run app.py --logger.level=debug
```

---

## Getting Help

1. **Check existing errors**
   - Scroll terminal/console for red error messages
   - Copy-paste error into Google

2. **Common resources**
   - [Streamlit Docs](https://docs.streamlit.io)
   - [Pandas Docs](https://pandas.pydata.org/docs/)
   - [Python Docs](https://docs.python.org/3/)
   - Stack Overflow (tag with language)

3. **Debug yourself**
   - Run code in Python REPL
   - Add print statements
   - Check data expectations
   - Verify file paths

4. **Check configuration**
   - Review `config.py` settings
   - Ensure CSV columns match expectations
   - Verify datetime formats

---

## Reset Everything (Nuclear Option)

If nothing works, start fresh:

```bash
# 1. Delete virtual environment
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# 2. Delete Python cache
find . -type d -name __pycache__ -exec rm -r {} +  # macOS/Linux
// Windows: manually delete __pycache__ folders

# 3. Reinstall everything
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install fresh
pip install -r requirements.txt

# Run
streamlit run app.py
```

---

**Still stuck?** Check these in order:
1. ✅ Python installed? `python --version`
2. ✅ Virtual environment activated? Check terminal prompt
3. ✅ Dependencies installed? `pip list`
4. ✅ CSV files present? `ls -la *.csv`
5. ✅ Correct directory? `pwd` or `cd`
6. ✅ Ports available? `netstat -ano | findstr :8501`

**Last Updated**: March 2026  
**Version**: 1.0
