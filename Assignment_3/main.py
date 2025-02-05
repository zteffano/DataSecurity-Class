import bcrypt
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
    conn.commit()
    conn.close()


def register(userid, password):
    """Register a new user with password validation"""

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


if __name__ == "__main__":
    init_database()

    if len(sys.argv) != 3:
        print("Usage: python main.py <userid> <password>")
        sys.exit(1)

    # Process registration if arguments are provided
    result = register(sys.argv[1], sys.argv[2])
    print("Checked against {} passwords".format(len(Rockyou._bad_passwords)))
    print(result)
