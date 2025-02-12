# User Registration and Login System for Assignment in Data Security Class

A simple Python-based user registration and login system that checks passwords against the rockyou.txt list and supports both bcrypt and SHA256 hashing.

## Setup

1. Install required Python packages from the root folder
```bash
pip install -r ../requirements.txt 
```

2. Get rockyou.txt:
```bash
git clone https://gitlab.com/arosano/rockyou.git
unzip rockyou/rockyou.zip
```

3. Make sure rockyou.txt is in the same directory as your Python files

## Project Files

- `main.py` - Main program file containing registration and login functionality
- `Rockyou.py` - Singleton class for password checking against rockyou.txt
- `test.db` - SQLite database (created automatically on first run)

## Usage

### Registration

With bcrypt:
```bash
python main.py register bcrypt <userid> <password>
```

With SHA256:
```bash
python main.py register sha256 <userid> <password> [comments]
```

### Login

With bcrypt:
```bash
python main.py login bcrypt <userid> <password>
```

With SHA256:
```bash
python main.py login sha256 <userid> <password>
```

## Features

- Password strength validation against rockyou.txt
- Two hashing methods supported (bcrypt and SHA256)
- SQL injection prevention through parameterized queries
- Minimum password length requirement (8 characters)
- Duplicate username prevention
- Support for comments in SHA256 version

## Security Notes

- Uses parameterized SQL queries to prevent SQL injection
- Passwords are properly hashed before storage
- Basic input validation implemented
- Generic error messages to prevent information leakage