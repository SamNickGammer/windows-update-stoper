# Windows Update Control

## Overview
Windows Update Control is a simple tool that allows users to enable or disable Windows Updates easily through a graphical interface. This tool modifies Windows services, group policies, scheduled tasks, and the hosts file to ensure complete control over Windows updates.

## Features
- **Disable Windows Updates**: Stops and disables relevant services, policies, and tasks.
- **Enable Windows Updates**: Restores Windows Update functionality to its default settings.
- **GUI-based**: Easy-to-use graphical interface built with Tkinter.
- **Automated Execution**: Background execution using threading to avoid UI freezing.
- **One-click Control**: Enable or disable updates with a single button press.

## Download
Download the latest version from the [GitHub Releases](https://github.com/SamNickGammer/windows-update-stoper/releases/tag/Release).

## Installation & Usage
1. **Run as Administrator**: The tool requires administrator privileges to modify system settings.
2. **Execute the EXE File**: Download and run the provided EXE file.
3. **Disable/Enable Updates**: Click the respective button to disable or restore Windows Updates.

## Requirements
- Windows 10 or Windows 11
- Python 3.x (for running from source)
- Required dependencies: `tkinter`, `winreg`, `ctypes`, `subprocess`, `threading`

## Running from Source
To run the script manually:
```sh
python windows_update_control.py
```

## Release Notes
### v1.0.0 - Initial Release
- Added functionality to disable Windows Update services.
- Implemented Group Policy modifications.
- Scheduled tasks related to Windows Updates can now be disabled.
- Added domain blocking in the hosts file.
- Implemented an option to restore Windows Update functionality.

## License
This project is open-source under the MIT License.

## Disclaimer
Use this tool at your own risk. Disabling Windows Updates may prevent security patches and system updates from being applied.

