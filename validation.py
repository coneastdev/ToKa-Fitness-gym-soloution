import re 
from datetime import datetime, timezone
from dotenv import load_dotenv
import os

from pwdlib import PasswordHash

load_dotenv()

# Uses adapated AI generated code from task 1 C
def validate_credentials(email: str, password: str) -> int: 
    """Check if email and password are valid"""
    email_valid = bool(re.fullmatch( 
        # contains text @ text . text
        r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+"
        r"@[A-Za-z0-9](?:[A-Za-z0-9]{0,61}[A-Za-z0-9])?" 
        r"(?:\.[A-Za-z0-9](?:[A-Za-z0-9]{0,61}[A-Za-z0-9])?)+", email,)
    ) 
    
    password_valid = ( 
        # contains lowercase, uppercase, number and special char
        isinstance(password, str) 
        and len(password) >= 8 
        and re.search(r"[A-Z]", password)
        and re.search(r"[a-z]", password) 
        and re.search(r"\d", password) 
        and re.search(r"[^A-Za-z0-9]", password) 
    ) is not False 

    if email_valid and password_valid: 
        return 0 
    if not email_valid and not password_valid: 
        return 1 
    if not email_valid: 
        return 2 
    return 4

# uses AI generated code from google gemini
def convert(date_time) -> datetime:
    return datetime.strptime(date_time, '%d/%m/%Y').replace(tzinfo=timezone.utc)

def hash(password: str, email: str) -> str:
    password_hash = PasswordHash.recommended()

    return password_hash.hash(password + email + str(os.environ.get("SALT")))