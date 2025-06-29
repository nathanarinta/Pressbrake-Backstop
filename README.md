Press Brake Backstop GUI
This is still a work in progress. Soon i will have wiring documents, 3D models, and videos to go with this project!

A touchscreen application for Raspberry Pi that adds CNC-style backstop control to an existing press brake via a stepper motor and ball-screw assembly.

Overview

This GUI allows you to set a programmable backstop position on your press brake, manually jog the backstop in precise increments, and automate a sequence of bends for repeatable CNC-style operation.

Key Features

Manual Jog & Zeroing

Zero the backstop at any position

Jog forward/backward in selectable increments: 0.001″, 0.01″, 0.1″, 1″

Bend Sequence Automation

Load and save simple text-based bend sequences

Automatically move to each bend distance offset from zero

Highlight the current step in the sequence display

Hardware Requirements

Controller: Raspberry Pi 5 with 7″ Touchscreen v2

Interface PCB: Custom circuit board (schematic forthcoming)

Motion: Stepper motor + ball-screw assembly as press backstop

Driver: A4988, DM54T, or equivalent stepper driver

Power: 24 V power supply

Mounting: 3D‑printed components for integration

Software Prerequisites

OS: Raspberry Pi OS (formerly Raspbian)

Python: 3.11 or newer

Libraries:

gpiozero for GPIO control

tkinter for the GUI interface

Installation & Setup

Clone the repository

git clone https://github.com/yourusername/PressBrake-Backstop.git
cd PressBrake-Backstop

Install Python dependencies

sudo apt update && sudo apt install python3-pip python3-tk
pip3 install gpiozero

Configure assets and settings

Place all asset images under assets/ (the folder structure is already set up)

Create a settings.json in the project root with:

{
  "lead": 1.0,
  "steps_per_rev": 200,
  "micro_steps": 16
}

Adjust values to match your ball-screw lead, motor steps per revolution, and microstep setting.

Wiring

Connect STEP and DIR pins from your driver to the GPIO pins defined in hardware.py (default: GPIO 8 and 10).

Wire the driver’s ENABLE, GND, and V+ to your power supply and Raspberry Pi ground.

See the upcoming PCB schematic for detailed pinouts.

Usage

Launch the GUI

python3 app.py

Main Screen

Tap Zero to set your current backstop position as the new zero reference.

Use Forward and Backward buttons to jog in preselected increments.

Tap Bend Sequence to configure or run an automated sequence.

Tap Settings to adjust calibration values.

Bend Sequence

Create or load a sequence file (.txt) with two columns: step labels and distances.

Use Next / Prev to move the press to each programmed bend offset.

Exit returns you to the main manual control screen.

Settings

Modify lead, steps_per_rev, and micro_steps to match your hardware.

Save to persist calibration for future runs.

Contributing

Contributions, issues, and feature requests are welcome!

Fork the repository and create a new branch for your feature or bugfix.

Submit a pull request with a clear description of your changes.

License

This project is released under the MIT License. See LICENSE for details.
