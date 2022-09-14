import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": [
    "selenium", "omegaconf", "pandas", "asyncio", "plotly", "httpx",
    "anyio._backends._asyncio",
]}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "main",
    version = "1.0",
    description = "Download price data and plot as background image on Linkedin",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base=base)],
)