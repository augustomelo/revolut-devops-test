import re

_pattern_letters = re.compile("^[a-zA-Z]+$")

def is_username_valid(username: str) -> bool:

    if _pattern_letters.match(username):
        return True
    
    return False
