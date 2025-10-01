#!/usr/bin/env python3
"""
Railnation Autobot - Start Script
Launches the modern UI for the Railnation automation bot.
"""

import sys
import os

# Check if required packages are installed
try:
    import tkinter
except ImportError:
    print("ERROR: tkinter is not installed!")
    print("On Ubuntu/Debian, install with: sudo apt-get install python3-tk")
    sys.exit(1)

try:
    import pyautogui
except ImportError:
    print("WARNING: pyautogui is not installed!")
    print("Install with: pip install pyautogui")
    print("The UI will launch but bot functionality will be limited.")
    print()
    response = input("Continue anyway? (y/n): ")
    if response.lower() != 'y':
        sys.exit(0)

# Launch the UI
if __name__ == "__main__":
    from railnation_ui import main
    main()
