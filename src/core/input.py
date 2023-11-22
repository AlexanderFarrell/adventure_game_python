# Keeps track of what key is down
keys_down = set()

def is_key_pressed(key):
    return key in keys_down