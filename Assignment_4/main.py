import bcrypt
import hashlib
import sqlite3
import sys
from Rockyou import Rockyou


def init_database():
    """Initialize the database if it doesn't exist"""
    conn = sqlite3.connect("test.db")
    cursor = conn.cursor()

    # Create user table (if it doesn't exist)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid VARCHAR(32) UNIQUE NOT NULL,
            password BLOB NOT NULL
        )
    """
    )

    # Create user256 table (if it doesn't exist)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user256 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid VARCHAR(32) UNIQUE NOT NULL,
            password BLOB NOT NULL,
            comments TEXT NOT NULL
        )
    """
    )

    conn.commit()
    conn.close()


def register(userid, password):
    """Register a new user with password validation (bcrypt)"""

    if not userid or not password:
        return "Error: Username and password are required"

    if len(password) < 8:
        return "Error: Password must be at least 8 characters long"

    # Check if password is in rockyou.txt
    rockyou = Rockyou()
    if rockyou.check_password(password):
        return "Not good enough, try again"

    try:
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        # Check if userid already exists
        cursor.execute("SELECT userid FROM user WHERE userid = ?", (userid,))
        if cursor.fetchone():
            conn.close()
            return "Error: Username already exists"

        # Hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

        # Insert the user into db
        cursor.execute(
            "INSERT INTO user (userid, password) VALUES (?, ?)", (userid, hashed)
        )
        conn.commit()
        conn.close()

        return "You chose wisely!"

    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def register_sha256(userid, password, comments=""):
    """Register a new user with password validation (sha256)"""

    if not userid or not password:
        return "Error: Username and password are required"

    if len(password) < 8:
        return "Error: Password must be at least 8 characters long"

    # Check if password is in rockyou.txt
    rockyou = Rockyou()
    if rockyou.check_password(password):
        return "Not good enough, try again"

    try:
        # Connect to database
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        # Check if userid already exists
        cursor.execute("SELECT userid FROM user256 WHERE userid = ?", (userid,))
        if cursor.fetchone():
            conn.close()
            return "Error: Username already exists"

        # Hash password using SHA256
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

        # Insert the user into db
        cursor.execute(
            "INSERT INTO user256 (userid, password, comments) VALUES (?, ?, ?)",
            (userid, password_hash, comments),
        )
        conn.commit()
        conn.close()

        return "You chose wisely!"

    except sqlite3.Error as e:
        return f"Database error: {str(e)}"
    except Exception as e:
        return f"Error: {str(e)}"


def login_bcrypt(userid, password):
    """Login with bcrypt password"""
    try:
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        # Get user data using parameterized query
        cursor.execute(
            "SELECT id, userid, password FROM user WHERE userid = ?", (userid,)
        )
        user = cursor.fetchone()

        if not user:
            conn.close()
            return "error"

        # Verify password
        stored_hash = user[2]
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
            return f"id: {user[0]}, userid: {user[1]}"
        else:
            return "error"

    except sqlite3.Error as e:
        return "error"
    finally:
        if conn:
            conn.close()


def login_sha256(userid, password):
    """Login with sha256 password"""
    try:
        conn = sqlite3.connect("test.db")
        cursor = conn.cursor()

        # Hash the provided password
        password_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

        # Get user data using parameterized query
        cursor.execute(
            "SELECT id, userid FROM user256 WHERE userid = ? AND password = ?",
            (userid, password_hash),
        )
        user = cursor.fetchone()

        if user:
            return f"id: {user[0]}, userid: {user[1]}"
        else:
            return "error"

    except sqlite3.Error as e:
        return "error"
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    init_database()

    if len(sys.argv) < 3:
        print("Usage:")
        print("Registration:")
        print("  python main.py register bcrypt <userid> <password>")
        print("  python main.py register sha256 <userid> <password> [comments]")
        print("Login:")
        print("  python main.py login bcrypt <userid> <password>")
        print("  python main.py login sha256 <userid> <password>")
        sys.exit(1)

    action = sys.argv[1]
    hash_type = sys.argv[2]

    if action == "register":
        if hash_type == "bcrypt":
            if len(sys.argv) != 5:
                print("Usage: python main.py register bcrypt <userid> <password>")
                sys.exit(1)
            result = register(sys.argv[3], sys.argv[4])
        elif hash_type == "sha256":
            if len(sys.argv) < 5:
                print(
                    "Usage: python main.py register sha256 <userid> <password> [comments]"
                )
                sys.exit(1)
            comments = sys.argv[5] if len(sys.argv) > 5 else ""
            result = register_sha256(sys.argv[3], sys.argv[4], comments)
    elif action == "login":
        if len(sys.argv) != 5:
            print("Usage: python main.py login <hash_type> <userid> <password>")
            sys.exit(1)
        if hash_type == "bcrypt":
            result = login_bcrypt(sys.argv[3], sys.argv[4])
        elif hash_type == "sha256":
            result = login_sha256(sys.argv[3], sys.argv[4])
        else:
            result = "Error: Invalid hash type. Use 'bcrypt' or 'sha256'"
    else:
        result = "Error: Invalid action. Use 'register' or 'login'"
    if result is None:
        result = "error, please make sure you have the correct number of arguments"
    else:
        print(result)
    if action == "register":
        print("Checked against {} passwords".format(len(Rockyou._bad_passwords)))
