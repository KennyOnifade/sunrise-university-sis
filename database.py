import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_connection():
    """Create and return a database connection."""
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def initialize_database():
    """Create all necessary tables if they don't exist."""
    conn = get_connection()
    cursor = conn.cursor()

    # Students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            age INTEGER CHECK (age >= 0),
            course VARCHAR(100),
            gpa NUMERIC(3,2) CHECK (gpa >= 0.0 AND gpa <= 4.0),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # Users table for authentication
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role VARCHAR(20) DEFAULT 'teacher'
        );
    """)

    # Audit log table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id SERIAL PRIMARY KEY,
            username VARCHAR(50),
            action VARCHAR(200),
            accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Student database tables created successfully!")

def log_action(username, action):
    """Record every user action for security auditing."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_log (username, action)
        VALUES (%s, %s);
    """, (username, action))
    conn.commit()
    cursor.close()
    conn.close()

# Test the connection when this file is run directly
if __name__ == "__main__":
    try:
        conn = get_connection()
        print("✅ Connected to student_sis_db successfully!")
        conn.close()
        initialize_database()
    except Exception as e:
        print(f"❌ Connection failed: {e}")