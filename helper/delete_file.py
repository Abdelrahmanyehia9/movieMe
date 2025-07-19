import os

def delete_file(path):
    if path and os.path.exists(path):
        try:
            os.remove(path)
            return True
        except Exception as e:
            print(f"Error deleting file {path}: {e}")
            return False
    return False
