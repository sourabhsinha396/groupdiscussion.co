import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from .base import *

if os.getenv("DEBUG") == "TRUE" or os.getenv("DEBUG") == "True":
    from .local import *
else:
    from .production import *