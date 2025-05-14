#!/usr/bin/env python3
"""
MP4 Audio Extractor Tool

A simple GUI application to extract audio from MP4 video files.
Supports both single file and folder (batch) processing.
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import threading
import os
import pathlib

class MP4AudioExtractor(tk.Tk):
    """Main application class for the MP4 Audio Extractor tool."""
    
    def __init__(self):
        """Initialize the application window and components."""
        super().__init__()

        # Set up the main window
        self.title("MP4 Audio Extractor")
        self.geometry("550x325")
        self.resizable(False, False)
        
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
        self.convert_btn = ttk.Button(main_frame, text="Convert Audio", command=self.start_conversion)
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
    
    def update_status_safe(self, message):
        """Thread-safe method to update the status message."""
        self.after(0, lambda: self.status_message.set(message))
    
    def start_conversion(self):
        """Start the conversion process in a separate thread."""
        if not self.selected_path.get():
            messagebox.showerror("Error", "Please select a file or folder first.")
            return
        
        # Check if ffmpeg is available
        if not self.check_ffmpeg():
            messagebox.showerror(
                "Error", 
                "FFmpeg not found. Please install FFmpeg and make sure it's in your system PATH."
            )
            return
        
        # Disable the convert button during processing
        self.is_processing = True
        self.update_button_state()
        
        # Start processing in a separate thread to keep the GUI responsive
        threading.Thread(target=self.process_conversion, daemon=True).start()
    
    def process_conversion(self):
        """Process the selected file or folder."""
        try:
            selected_path = self.selected_path.get()
            output_format = self.output_format.get()
            
            if os.path.isfile(selected_path):
                # Process a single file
                self.update_status_safe(f"Processing file: {os.path.basename(selected_path)}")
                success = self.process_file(selected_path, output_format)
                
                if success:
                    self.update_status_safe(f"Successfully extracted audio from {os.path.basename(selected_path)}")
                else:
                    self.update_status_safe(f"Failed to process {os.path.basename(selected_path)}")
            
            elif os.path.isdir(selected_path):
                # Process a folder
                self.process_folder(selected_path, output_format)
            
            else:
                self.update_status_safe("Error: Selected path is neither a file nor a folder.")
        
        except Exception as e:
            self.update_status_safe(f"Error during conversion: {str(e)}")
        
        finally:
            # Re-enable the convert button
            self.is_processing = False
            self.after(0, self.update_button_state)
    
    def check_ffmpeg(self):
        """Check if FFmpeg is available in the system PATH."""
        try:
            subprocess.run(
                ["ffmpeg", "-version"], 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                check=True
            )
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            return False
    
    def process_file(self, input_filepath, output_format):
        """Process a single MP4 file to extract its audio."""
        input_path = pathlib.Path(input_filepath)
        
        # Validate input file
        if not input_path.is_file() or input_path.suffix.lower() != '.mp4':
            self.update_status_safe(f"Error: {input_path.name} is not a valid MP4 file.")
            return False
        
        # Determine output path
        output_dir = input_path.parent
        output_name = f"{input_path.stem}.{output_format}"
        output_filepath = output_dir / output_name
        
        # Construct FFmpeg command based on output format
        if output_format.lower() == 'mp3':
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", str(input_filepath),
                "-vn",                   # No video
                "-acodec", "libmp3lame", # MP3 codec
                "-ab", "320k",           # Audio bitrate
                "-map_metadata", "-1",   # Remove metadata
                "-y",                    # Overwrite output file without asking
                str(output_filepath)
            ]
        elif output_format.lower() == 'aac':
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", str(input_filepath),
                "-vn",                   # No video
                "-acodec", "copy",       # Copy audio codec (assuming AAC)
                "-map_metadata", "-1",   # Remove metadata
                "-y",                    # Overwrite output file without asking
                str(output_filepath)
            ]
        else:
            self.update_status_safe(f"Error: Unsupported output format '{output_format}'.")
            return False
        
        # Execute FFmpeg command
        try:
            self.update_status_safe(f"Extracting audio from {input_path.name}...")
            process = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return True
        
        except subprocess.CalledProcessError as e:
            self.update_status_safe(f"Error processing {input_path.name}: {e.stderr}")
            return False
    
    def process_folder(self, input_folderpath, output_format):
        """Process all MP4 files in a folder."""
        input_path = pathlib.Path(input_folderpath)
        
        # Validate input folder
        if not input_path.is_dir():
            self.update_status_safe(f"Error: Invalid input directory: {input_folderpath}")
            return
        
        # Find all MP4 files in the folder
        self.update_status_safe(f"Scanning folder: {input_folderpath} for MP4 files...")
        mp4_files = list(input_path.glob('*.mp4'))
        
        if not mp4_files:
            self.update_status_safe(f"No MP4 files found in {input_folderpath}")
            return
        
        # Process each file
        total_files = len(mp4_files)
        successful = 0
        failed = 0
        
        self.update_status_safe(f"Found {total_files} MP4 files. Starting processing...")
        
        for i, mp4_file in enumerate(mp4_files):
            self.update_status_safe(f"[{i+1}/{total_files}] Processing: {mp4_file.name}")
            
            if self.process_file(str(mp4_file), output_format):
                successful += 1
            else:
                failed += 1
        
        # Show final results
        self.update_status_safe(
            f"Processing complete. Total: {total_files}, Successful: {successful}, Failed: {failed}"
        )


def main():
    """Main entry point for the application."""
    app = MP4AudioExtractor()
    app.mainloop()


if __name__ == "__main__":
    main()
