import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    # "packages": ["tkinter"],
    "packages": ["tkinter", "random_word"],
    # "include_files": ["tkinter", "random_word"],
    "include_files": [("/Applications/XAMPP/xamppfiles/htdocs/python-typing-speed-test/venv/bin/python3.11", "python3.11")],
    "excludes": [],
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable("app.py", base=base)
]

setup(
    name="TypingTest",
    version="1.0",
    description="Test typing speed",
    options={"build_exe": build_exe_options},
    executables=executables,
)
