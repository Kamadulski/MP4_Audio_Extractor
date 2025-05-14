"""
GUI View component for the MP4 Audio Extractor.

This module contains the graphical user interface for the application.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os

from mp4_audio_extractor.controller import AudioExtractorController


class AudioExtractorGUI(tk.Tk):
    """GUI view class for the MP4 Audio Extractor."""

    def __init__(self, controller: AudioExtractorController):
        """Initialize the GUI window and components.

        Args:
            controller: The controller instance to use.
        """
        super().__init__()

        # Set up the main window
        self.title("MP4 Audio Extractor")
        self.geometry("525x325")
        self.resizable(False, False)

        # Store the controller
        self.controller = controller

        # Application state variables
        self.selected_path = tk.StringVar()
        self.status_message = tk.StringVar()
        self.status_message.set("Select a file or folder to get started.")
        self.is_processing = False
        self.output_format = tk.StringVar(value="mp3")  # Default output format

        # Create the GUI components
        self.create_widgets()
        self.update_button_state()

    def create_widgets(self):
        """Create and arrange all GUI widgets."""
        # Main frame with padding
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Path selection section
        path_frame = ttk.LabelFrame(main_frame, text="Input Selection", padding="5")
        path_frame.pack(fill=tk.X, pady=5)

        path_entry = ttk.Entry(path_frame, textvariable=self.selected_path, width=50, state="readonly")
        path_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)

        button_frame = ttk.Frame(path_frame)
        button_frame.pack(side=tk.RIGHT, padx=5)

        select_file_btn = ttk.Button(button_frame, text="Select File", command=self.select_file)
        select_file_btn.pack(side=tk.LEFT, padx=2)

        select_folder_btn = ttk.Button(button_frame, text="Select Folder", command=self.select_folder)
        select_folder_btn.pack(side=tk.LEFT, padx=2)

        # Output format selection
        format_frame = ttk.LabelFrame(main_frame, text="Output Format", padding="5")
        format_frame.pack(fill=tk.X, pady=5)

        mp3_radio = ttk.Radiobutton(format_frame, text="MP3", variable=self.output_format, value="mp3")
        mp3_radio.pack(side=tk.LEFT, padx=20, pady=5)

        aac_radio = ttk.Radiobutton(format_frame, text="AAC", variable=self.output_format, value="aac")
        aac_radio.pack(side=tk.LEFT, padx=20, pady=5)

        # Convert button
        self.convert_btn = ttk.Button(main_frame, text="Convert Audio", command=self.on_convert_clicked)
        self.convert_btn.pack(pady=10)

        # Status display
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="5")
        status_frame.pack(fill=tk.X, pady=5)

        status_label = ttk.Label(status_frame, textvariable=self.status_message, wraplength=450)
        status_label.pack(padx=5, pady=5, fill=tk.X)

    def select_file(self):
        """Open a file dialog to select a single MP4 file."""
        filepath = filedialog.askopenfilename(
            title="Select MP4 File",
            filetypes=[("MP4 Files", "*.mp4"), ("All Files", "*.*")]
        )

        if filepath:
            self.selected_path.set(filepath)
            self.status_message.set(f"Selected file: {os.path.basename(filepath)}")
            self.update_button_state()

    def select_folder(self):
        """Open a folder dialog to select a directory containing MP4 files."""
        folderpath = filedialog.askdirectory(title="Select Folder Containing MP4 Files")

        if folderpath:
            self.selected_path.set(folderpath)
            self.status_message.set(f"Selected folder: {os.path.basename(folderpath)}")
            self.update_button_state()

    def update_button_state(self):
        """Update the state of the convert button based on current application state."""
        if self.is_processing:
            self.convert_btn.config(state=tk.DISABLED)
        elif self.selected_path.get():
            self.convert_btn.config(state=tk.NORMAL)
        else:
            self.convert_btn.config(state=tk.DISABLED)

    def update_status(self, message):
        """Update the status message."""
        self.status_message.set(message)

    def update_status_safe(self, message):
        """Thread-safe method to update the status message."""
        self.after(0, lambda: self.status_message.set(message))

    def set_processing_state(self, is_processing):
        """Set the processing state and update the UI accordingly."""
        self.is_processing = is_processing
        self.after(0, self.update_button_state)

    def on_convert_clicked(self):
        """Handle the convert button click event."""
        if not self.selected_path.get():
            messagebox.showerror("Error", "Please select a file or folder first.")
            return

        # Check if ffmpeg is available
        if not self.controller.check_ffmpeg():
            messagebox.showerror(
                "Error",
                "FFmpeg not found. Please install FFmpeg and make sure it's in your system PATH."
            )
            return

        # Disable the convert button during processing
        self.set_processing_state(True)

        # Get the selected path and output format
        selected_path = self.selected_path.get()
        output_format = self.output_format.get()

        # Start processing in a separate thread to keep the GUI responsive
        threading.Thread(
            target=self.controller.handle_gui_convert,
            args=(selected_path, output_format, self.update_status_safe, self.set_processing_state),
            daemon=True
        ).start()



    def run(self):
        """Run the GUI application."""
        self.mainloop()
