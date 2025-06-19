from fastapi.templating import Jinja2Templates
import os

base_dir = os.path.dirname(__file__)
templates = Jinja2Templates(directory=base_dir)
