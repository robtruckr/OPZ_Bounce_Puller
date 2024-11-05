import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import shutil
import uuid
from pathlib import Path
from send2trash import send2trash

# Define the directory in LocalAppData and ensure it exists
def setup_config():
    try:
        app_data_dir = Path(os.getenv('LOCALAPPDATA')) / 'OPZ_Bounce_Puller'
        app_data_dir.mkdir(parents=True, exist_ok=True)  # Creates the directory if it doesn't exist
        config_file = app_data_dir / 'opz_config.json'
        # Attempt to create the config file if it doesn't exist
        if not config_file.exists():
            default_config = {"opz_drive": "", "destination_folder": "", "skip_confirmation": False, "delete_after_transfer": False}
            with open(config_file, 'w') as file:
                json.dump(default_config, file)
            print("Created config file at:", config_file)
        return config_file
    except PermissionError as e:
        messagebox.showerror("Permission Error", f"Cannot write to LocalAppData folder: {e}")
        exit(1)

# Config file path within LocalAppData\OPZ_Bounce_Puller
config_file = setup_config()

# Load configuration or set defaults
def load_config():
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
            config.setdefault("opz_drive", "")
            config.setdefault("destination_folder", "")
            config.setdefault("skip_confirmation", False)
            config.setdefault("delete_after_transfer", False)
            return config
    except Exception as e:
        print("Error loading config:", e)
        return {"opz_drive": "", "destination_folder": "", "skip_confirmation": False, "delete_after_transfer": False}

def save_config(opz_drive, destination_folder, skip_confirmation, delete_after_transfer):
    try:
        with open(config_file, 'w') as file:
            json.dump({"opz_drive": opz_drive, "destination_folder": destination_folder, "skip_confirmation": skip_confirmation, "delete_after_transfer": delete_after_transfer}, file)
        print("Config saved successfully.")
    except Exception as e:
        print("Error saving config:", e)

# Load existing configuration if it exists
config = load_config()

# GUI setup
root = tk.Tk()
root.title("OPZ Bounce Puller")
root.geometry("600x400")  # Set a larger initial window size for more padding
root.minsize(600, 400)     # Set minimum window size to prevent cut-off

# Functions for selecting the OPZ drive and updating configuration
def select_opz_drive():
    drive = filedialog.askdirectory(title="Select OPZ Drive (Root Directory)")
    if drive:
        config['opz_drive'] = drive
        opz_drive_var.set(drive)
        save_config(config['opz_drive'], config['destination_folder'], config['skip_confirmation'], config['delete_after_transfer'])

def select_destination_folder():
    folder = filedialog.askdirectory(title="Select Destination Folder")
    if folder:
        config['destination_folder'] = folder
        destination_folder_var.set(folder)
        save_config(config['opz_drive'], config['destination_folder'], config['skip_confirmation'], config['delete_after_transfer'])

# Pull bounces with conditional confirmation and deletion logic
def pull_bounces():
    # Check if the OPZ drive and destination folder are set
    if not config['opz_drive'] or not config['destination_folder']:
        messagebox.showwarning("Missing Paths", "Please select both the OPZ drive and the destination folder.")
        return
    # Verify the OPZ drive exists before proceeding
    if not os.path.exists(config['opz_drive']):
        messagebox.showwarning("OPZ Drive Not Found", "The configured OPZ drive was not found. Please select the correct drive.")
        select_opz_drive()
        return
    # Show confirmation message only if "Delete After Transfer" is selected
    if config.get("delete_after_transfer", False):
        confirm_message = "This action will move all bounces from your OPZ to the destination folder and delete the originals from the OPZ. Proceed?"
        response = messagebox.askyesno("Confirm Pull Bounces", confirm_message)
        if not response:
            return  # Exit if user cancels the action

    # Define the bounce folders based on the selected OPZ drive
    source_folders = [os.path.join(config['opz_drive'], "bounces", f"bounce{i:02}") for i in range(1, 6)]
    transferred_files = False  # Track if any files were transferred

    # Perform the file transfer for each bounce folder
    for folder in source_folders:
        if not os.path.exists(folder):
            print(f"Folder {folder} does not exist. Skipping.")
            continue  # Skip this folder if it doesn’t exist
        source_file = os.path.join(folder, "bounce.wav")

        # Check if the bounce file exists and transfer it
        if os.path.isfile(source_file):
            destination_file = os.path.join(config['destination_folder'], os.path.basename(folder) + ".wav")
            if os.path.exists(destination_file):
                unique_id = uuid.uuid4().hex[:8]
                destination_file = os.path.join(config['destination_folder'], f"{os.path.basename(folder)}_{unique_id}.wav")
            # Transfer the file
            try:
                shutil.move(source_file, destination_file)
                print(f"Moved {source_file} to {destination_file}")
                transferred_files = True  # Mark as successful transfer
                # Only delete the folder after successful transfer if option is selected
                if config.get("delete_after_transfer", False) and os.path.exists(folder):
                    shutil.rmtree(folder)  # Delete the folder on OPZ after transfer
                    print(f"Deleted folder {folder}.")

            except Exception as e:
                print(f"Failed to move {source_file} to {destination_file}: {e}")
        else:
            print(f"No bounce.wav found in {folder}, skipping transfer and deletion.")

    # Show appropriate message based on transfer status
    if transferred_files:
        messagebox.showinfo("Success", "All bounces have been transferred from your OPZ!")
    else:
        messagebox.showinfo("No Bounces Found", "No bounces found on the OPZ.")

# Update configuration settings
def toggle_skip_confirmation():
    config['skip_confirmation'] = skip_confirmation_var.get()
    save_config(config['opz_drive'], config['destination_folder'], config['skip_confirmation'], config['delete_after_transfer'])

def toggle_delete_after_transfer():
    config['delete_after_transfer'] = delete_after_transfer_var.get()
    save_config(config['opz_drive'], config['destination_folder'], config['skip_confirmation'], config['delete_after_transfer'])

# UI Elements
opz_drive_var = tk.StringVar(value=config['opz_drive'])
destination_folder_var = tk.StringVar(value=config['destination_folder'])
skip_confirmation_var = tk.BooleanVar(value=config.get('skip_confirmation', False))
delete_after_transfer_var = tk.BooleanVar(value=config.get('delete_after_transfer', False))

tk.Label(root, text="OPZ Drive").grid(row=0, column=0, padx=20, pady=20, sticky="w")
tk.Entry(root, textvariable=opz_drive_var, width=50).grid(row=0, column=1, padx=10, pady=20, sticky="w")
tk.Button(root, text="Select Drive", command=select_opz_drive).grid(row=0, column=2, padx=10, pady=20, sticky="w")
tk.Label(root, text="Destination Folder").grid(row=1, column=0, padx=20, pady=20, sticky="w")
tk.Entry(root, textvariable=destination_folder_var, width=50).grid(row=1, column=1, padx=10, pady=20, sticky="w")
tk.Button(root, text="Select Folder", command=select_destination_folder).grid(row=1, column=2, padx=10, pady=20, sticky="w")
tk.Button(root, text="Pull Bounces from OPZ", command=pull_bounces, width=25).grid(row=2, column=1, pady=30)
tk.Checkbutton(root, text="Remember my choice for future transfers", variable=skip_confirmation_var).grid(row=3, column=1, pady=10)

# Start the Tkinter event loop
root.mainloop()