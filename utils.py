import string
import random
import logging
from typing import Optional

logger = logging.getLogger(__name__)


def generate_unique_code(prefix: str = "CODIRO", length: int = 6) -> str:
    characters = string.ascii_uppercase + string.digits
    random_part = "".join(random.choices(characters, k=length))
    code = f"{prefix}-{random_part}"
    logger.info(f"Generated unique code: {code}")
    return code


def validate_phone_number(phone: str) -> bool:
    if not phone:
        return False
    
    phone_digits = "".join(filter(str.isdigit, phone))
    
    if len(phone_digits) < 10 or len(phone_digits) > 15:
        return False
    
    return True


def validate_fullname(name: str) -> bool:
    if not name or len(name.strip()) < 2:
        return False
    
    if len(name) > 100:
        return False
    
    return True


def validate_skills(skills: str) -> bool:
    if not skills or len(skills.strip()) < 3:
        return False
    
    if len(skills) > 500:
        return False
    
    return True


def format_user_info(user: dict) -> str:
    info = f"""
📋 User Information:
━━━━━━━━━━━━━━━━━━━━━
👤 Full Name: {user.get('fullname', 'N/A')}
📱 Phone: {user.get('phone', 'N/A')}
💼 Skills: {user.get('skills', 'N/A')}
🆔 Telegram ID: {user.get('telegram_id', 'N/A')}
📊 Status: {user.get('status', 'N/A').upper()}
🔐 Code: {user.get('unique_code', 'Pending')}
"""
    return info.strip()


def format_user_list(users: list) -> str:
    if not users:
        return "No users found."
    
    formatted = "👥 Users Found:\n" + "━" * 30 + "\n"
    
    for idx, user in enumerate(users, 1):
        formatted += f"""
{idx}. {user.get('fullname', 'Unknown')}
   ID: {user.get('telegram_id')}
   Phone: {user.get('phone')}
   Status: {user.get('status', 'unknown').upper()}
"""
    
    return formatted.strip()


def sanitize_input(text: str) -> Optional[str]:
    if not text:
        return None
    
    sanitized = text.strip()
    
    if len(sanitized) == 0 or len(sanitized) > 500:
        return None
    
    return sanitized
