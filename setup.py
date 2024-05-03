from cx_Freeze import setup, Executable

# Dépendances supplémentaires éventuelles
build_exe_options = {
    "packages": ["os", "mido", "pynput"],
    "excludes": ["tkinter"],
    "includes": ["python-rtmidi"],
}

base = None

setup(
    name="MIDI Keyboard FF14",
    version="0.1",
    description="Simulate keyboard presses from MIDI input.",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)],
)
