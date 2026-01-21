import sys
import os

# Path where pip installs user packages
USER_SITE = os.path.expanduser("~/.local/lib/python3.11/site-packages")

# Force user site-packages to take precedence over system site-packages
if USER_SITE not in sys.path:
    sys.path.insert(0, USER_SITE)

# Optional: print for debugging (safe to remove)
# print("sitecustomize loaded, sys.path:", sys.path)