# CEN4020 InCollege Website

Member:
1. Umar Khan
2. Akmal Kurbanov
3. Quy An Le
4. Mukund Sharma
5. Carlos Otero Pena

## Installation
1. Create a virtual environment

**Windows**:
```bash
python -m venv venv
```
**MacOS/Linux**:
```bash
python3 -m venv venv
```

2. Activate the virtual environment

**MacOS/Linux**:
```bash
source venv/bin/activate
```

**Windows**:
```bash
venv\Scripts\activate
```

3. Install requirements
```bash
pip install -r requirements.txt
```

4. Run the server (for development only)
```bash
uvicorn app.main:app --reload
```

or
```bash
python3 server.py
```


## Run tests
```bash
pytest -v -s
```
