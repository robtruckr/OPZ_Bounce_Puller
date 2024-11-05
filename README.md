# OPZ_Bounce_Puller
This is a tool designed to automate the process of transferring .wav bounce files from a Teenage Engineering OPZ synth to a user-defined folder on your computer. It also offers options to delete the files from the OPZ after transfer. This program saves time by streamlining what would otherwise be a multi-step, manual file management task.

This is my first GitHub project, and I'm still learning, so feedback is welcome!

---

## Features

- **Automated File Transfer**: Easily transfer `.wav` bounce files from OP-Z to a selected folder on your computer.
- **File Renaming**: Files are renamed for organization, saving you time.
- **Optional Deletion**: Choose to delete files from the OP-Z after they’ve been transferred.
- **Configurable Settings**: Preferences are saved for future sessions.

---

## Installation Instructions

1. Download the installer (`OPZ_Bounce_Puller_Setup.exe`) from the **Releases** section of this repository.
2. Run the installer and follow the on-screen instructions.
3. After installation, launch the application to configure your settings.

---

## Getting Started

1. **Select OP-Z Drive**  
   - Click on "Select Drive" to locate the OP-Z’s main directory.

2. **Select Destination Folder**  
   - Choose the folder on your computer where you want the `.wav` files to be stored.

3. **Pull Bounces**  
   - Click "Pull Bounces" to transfer the files according to your configuration. If you selected "Delete After Transfer," the files will be removed from the OP-Z after they’re moved.

---

## Requirements

- **Operating System**: Windows 10 or later
- **Python Libraries**:  
   - `tkinter` for GUI  
   - `json` for configuration management  
   - `shutil` for file operations  
   - `uuid` for generating unique file names  
   - `send2trash` for safe deletion

---

## Known Issues and Feedback

As this is my first project, please report any issues or suggestions in the **Issues** section on GitHub. I’d appreciate any feedback that could help improve this tool or my GitHub skills!

---

Thank you for checking out OPZ Bounce Puller, and I hope it saves you time in managing your OP-Z bounces!
