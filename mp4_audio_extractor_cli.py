#!/usr/bin/env python3
"""
MP4 Audio Extractor Tool (CLI Version)

A simple command-line application to extract audio from MP4 video files.
Supports both single file and folder (batch) processing.
"""

import subprocess
import os
import pathlib
import sys
import argparse
import time

def check_ffmpeg():
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

def process_file(input_filepath, output_format):
    """Process a single MP4 file to extract its audio."""
    input_path = pathlib.Path(input_filepath)
    
    # Validate input file
    if not input_path.is_file() or input_path.suffix.lower() != '.mp4':
        print(f"Error: {input_path.name} is not a valid MP4 file.")
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
        print(f"Error: Unsupported output format '{output_format}'.")
        return False
    
    # Execute FFmpeg command
    try:
        print(f"Extracting audio from {input_path.name}...")
        process = subprocess.run(
            ffmpeg_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print(f"Successfully extracted audio to {output_filepath}")
        return True
    
    except subprocess.CalledProcessError as e:
        print(f"Error processing {input_path.name}: {e.stderr}")
        return False

def process_folder(input_folderpath, output_format):
    """Process all MP4 files in a folder."""
    input_path = pathlib.Path(input_folderpath)
    
    # Validate input folder
    if not input_path.is_dir():
        print(f"Error: Invalid input directory: {input_folderpath}")
        return
    
    # Find all MP4 files in the folder
    print(f"Scanning folder: {input_folderpath} for MP4 files...")
    mp4_files = list(input_path.glob('*.mp4'))
    
    if not mp4_files:
        print(f"No MP4 files found in {input_folderpath}")
        return
    
    # Process each file
    total_files = len(mp4_files)
    successful = 0
    failed = 0
    
    print(f"Found {total_files} MP4 files. Starting processing...")
    
    for i, mp4_file in enumerate(mp4_files):
        print(f"[{i+1}/{total_files}] Processing: {mp4_file.name}")
        
        if process_file(str(mp4_file), output_format):
            successful += 1
        else:
            failed += 1
    
    # Show final results
    print(f"Processing complete. Total: {total_files}, Successful: {successful}, Failed: {failed}")

def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(description='Extract audio from MP4 files.')
    parser.add_argument('input', help='Input MP4 file or folder containing MP4 files')
    parser.add_argument('-f', '--format', choices=['mp3', 'aac'], default='mp3',
                        help='Output audio format (default: mp3)')
    
    args = parser.parse_args()
    
    # Check if FFmpeg is available
    if not check_ffmpeg():
        print("Error: FFmpeg not found. Please install FFmpeg and make sure it's in your system PATH.")
        return 1
    
    input_path = pathlib.Path(args.input)
    
    if input_path.is_file():
        # Process a single file
        if process_file(str(input_path), args.format):
            return 0
        else:
            return 1
    
    elif input_path.is_dir():
        # Process a folder
        process_folder(str(input_path), args.format)
        return 0
    
    else:
        print(f"Error: Input path '{args.input}' is neither a file nor a folder.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
