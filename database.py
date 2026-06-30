import sqlite3
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)

DB_FILE = "codiro_bot.db"


def init_database() -> None:
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                fullname TEXT NOT NULL,
                phone TEXT NOT NULL,
                skills TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                unique_code TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization error: {e}")
        raise


def user_exists(telegram_id: int) -> bool:
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,))
        result = cursor.fetchone()
        
        conn.close()
        return result is not None
    except sqlite3.Error as e:
        logger.error(f"Error checking user existence: {e}")
        return False


def save_user(
    telegram_id: int,
    fullname: str,
    phone: str,
    skills: str,
    username: Optional[str] = None,
) -> bool:
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO users (telegram_id, username, fullname, phone, skills, status)
            VALUES (?, ?, ?, ?, ?, 'pending')
        """, (telegram_id, username, fullname, phone, skills))
        
        conn.commit()
        conn.close()
        logger.info(f"User {telegram_id} saved successfully")
        return True
    except sqlite3.IntegrityError as e:
        logger.warning(f"Duplicate user registration attempt: {telegram_id}")
        return False
    except sqlite3.Error as e:
        logger.error(f"Error saving user: {e}")
        return False


def get_user(telegram_id: int) -> Optional[Dict[str, Any]]:
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT telegram_id, username, fullname, phone, skills, status, unique_code, created_at
            FROM users
            WHERE telegram_id = ?
        """, (telegram_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    except sqlite3.Error as e:
        logger.error(f"Error retrieving user: {e}")
        return None


def get_pending_users() -> List[Dict[str, Any]]:
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT telegram_id, username, fullname, phone, skills, created_at
            FROM users
            WHERE status = 'pending'
            ORDER BY created_at ASC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error retrieving pending users: {e}")
        return []


def search_users(query: str) -> List[Dict[str, Any]]:
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        search_term = f"%{query}%"
        cursor.execute("""
            SELECT telegram_id, username, fullname, phone, skills, status, created_at
            FROM users
            WHERE fullname LIKE ? OR phone LIKE ? OR CAST(telegram_id AS TEXT) LIKE ?
            ORDER BY created_at DESC
        """, (search_term, search_term, search_term))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    except sqlite3.Error as e:
        logger.error(f"Error searching users: {e}")
        return []


def approve_user(telegram_id: int, unique_code: str) -> bool:
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users
            SET status = 'approved', unique_code = ?
            WHERE telegram_id = ?
        """, (unique_code, telegram_id))
        
        conn.commit()
        conn.close()
        logger.info(f"User {telegram_id} approved with code {unique_code}")
        return True
    except sqlite3.Error as e:
        logger.error(f"Error approving user: {e}")
        return False


def reject_user(telegram_id: int) -> bool:
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE users
            SET status = 'rejected'
            WHERE telegram_id = ?
        """, (telegram_id,))
        
        conn.commit()
        conn.close()
        logger.info(f"User {telegram_id} rejected")
        return True
    except sqlite3.Error as e:
        logger.error(f"Error rejecting user: {e}")
        return False


def get_statistics() -> Dict[str, int]:
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM users")
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'pending'")
        pending = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'approved'")
        approved = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE status = 'rejected'")
        rejected = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total": total,
            "pending": pending,
            "approved": approved,
            "rejected": rejected,
        }
    except sqlite3.Error as e:
        logger.error(f"Error retrieving statistics: {e}")
        return {"total": 0, "pending": 0, "approved": 0, "rejected": 0}


def get_approved_user_by_phone(phone: str) -> Optional[Dict[str, Any]]:
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT telegram_id, username, fullname, phone, skills, status, unique_code
            FROM users
            WHERE phone = ? AND status = 'approved'
        """, (phone,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    except sqlite3.Error as e:
        logger.error(f"Error retrieving approved user: {e}")
        return None
