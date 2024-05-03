import time

import mido
import mido.backends.rtmidi  # Explicitly import rtmidi for pyinstaller to include it
from pynput.keyboard import Controller

keyboard = Controller()

# Keys to press on the keyboard
keys = [
    "a",
    "b",
    "c",
    "d",
    "e",
    "f",
    "g",
    "h",
    "i",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "q",
    "r",
    "s",
    "t",
    "u",
    "v",
    "w",
    "x",
    "y",
    "z",
    "é",
    '"',
    "'",
    "(",
    "-",
    "è",
    "_",
    "ç",
    "à",
    ")",
    "=",
]

# Latency fake duration to simulate key press
LATENCY = 0.009  # 9ms


def get_midi_ports():
    """Retrieve all available MIDI input ports."""
    return mido.get_input_names()


def list_midi_ports(inputs):
    """List all available MIDI input ports."""
    print("MIDI ports available:")
    for index, name in enumerate(inputs):
        print(f"{index + 1}: {name}")


def choose_midi_port(inputs):
    """Ask the user to choose a MIDI input port from a list of input ports."""
    while True:
        try:
            choice = int(input("Enter the number of the MIDI port you want to use: "))
            if 1 <= choice <= len(inputs):
                return inputs[choice - 1]
            else:
                print(f"Please enter a number between 1 and {len(inputs)}.")
        except ValueError:
            print("Please enter a valid number.")


def get_corresponding_key(note):
    """Return the corresponding key on the keyboard for the given MIDI note."""
    # We use the MIDI note number to determine which key to press

    # 12 notes correspond to an octave in the MIDI standard
    key_index = (note - 12) % len(keys)  # We shift by one octave

    if key_index < 0:
        key_index += len(keys)  # Adjustment to avoid negative index
    return keys[key_index]


def handle_note_on(note):
    """Press the corresponding key on the keyboard for the given MIDI note."""
    key = get_corresponding_key(note)
    keyboard.press(key)
    print(f"Pressed {key}, MIDI note: {note}")
    time.sleep(LATENCY)  # Attendre un peu avant de permettre la prochaine note


def handle_note_off(note):
    """Release the corresponding key on the keyboard for the given MIDI note."""
    key = get_corresponding_key(note)
    keyboard.release(key)
    print(f"Released {key}, MIDI note: {note}")


def process_message(message):
    """Process the MIDI message."""
    if message.type == "note_on":
        handle_note_on(message.note)
    elif message.type == "note_off":
        handle_note_off(message.note)


def midi_callback(message):
    """Callback function to handle MIDI messages."""
    if message.type in ["note_on", "note_off"]:
        process_message(message)
    else:
        # Ignore unsupported message types
        print(f"Ignoring unsupported message type: {message.type}")


def main():
    """Main function to listen for MIDI input and press corresponding keys on the keyboard."""

    midi_ports = get_midi_ports()  # Get all available MIDI input ports

    if not midi_ports:
        # If no MIDI input ports are detected, wait for 5 seconds and try again
        print("No MIDI input ports detected. Please connect a MIDI device.")
        print("Waiting for 5 seconds before retrying...")
        time.sleep(5)
        return main()

    list_midi_ports(midi_ports)  # List all available MIDI input ports
    port_name = choose_midi_port(midi_ports)  # Ask the user to choose a MIDI input port

    with mido.open_input(port_name) as inport:
        # Open the MIDI input port
        print("Listening for MIDI input on", port_name)

        for message in inport:
            # Process each MIDI message
            midi_callback(message)


if __name__ == "__main__":
    main()
