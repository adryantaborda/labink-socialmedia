import re

''' THIS FUNCTION WILL CHECK THE STRENGTH OF YOUR PASSWORD BEFORE SAVING '''

def check_strength(password):
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"[a-zA-Z]", password):
        return False, "Password must contain letters"
    if not re.search(r"\d", password):
        return False, "Password must contain at least one number."
    
    return True, "Password is strong."

def clean_username(username):
    cleanspaces = username.replace(" ","")
    cleanusername = cleanspaces.lower()
    return cleanusername
