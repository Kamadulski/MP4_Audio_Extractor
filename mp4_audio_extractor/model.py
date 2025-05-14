"""
Model component for the MP4 Audio Extractor.

This module contains the core business logic for extracting audio from MP4 files.
"""

import subprocess
import pathlib
from typing import Dict, Tuple, Optional


class AudioExtractorModel:
    """Model class for handling audio extraction from MP4 files."""
    
    def __init__(self):
        """Initialize the model."""
        self._ffmpeg_available = None
    
    def check_ffmpeg(self) -> bool:
        """
        Check if FFmpeg is available in the system PATH.
        
        Returns:
            bool: True if FFmpeg is available, False otherwise.
        """
        if self._ffmpeg_available is None:
            try:
                subprocess.run(
                    ["ffmpeg", "-version"], 
                    stdout=subprocess.PIPE, 
                    stderr=subprocess.PIPE,
                    check=True
                )
                self._ffmpeg_available = True
            except (subprocess.SubprocessError, FileNotFoundError):
                self._ffmpeg_available = False
        
        return self._ffmpeg_available
    
    def process_file(self, input_filepath: str, output_format: str) -> Tuple[bool, str]:
        """
        Process a single MP4 file to extract its audio.
        
        Args:
            input_filepath: Path to the input MP4 file.
            output_format: Output audio format ('mp3' or 'aac').
            
        Returns:
            Tuple[bool, str]: (success, message) where success is True if processing was successful,
                             and message contains status or error information.
        """
        input_path = pathlib.Path(input_filepath)
        
        # Validate input file
        if not input_path.is_file():
            return False, f"Error: {input_path.name} is not a valid file."
        
        if input_path.suffix.lower() != '.mp4':
            return False, f"Error: {input_path.name} is not an MP4 file."
        
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
            return False, f"Error: Unsupported output format '{output_format}'."
        
        # Execute FFmpeg command
        try:
            process = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            return True, f"Successfully extracted audio to {output_filepath}"
        
        except subprocess.CalledProcessError as e:
            return False, f"Error processing {input_path.name}: {e.stderr}"
    
    def process_folder(self, input_folderpath: str, output_format: str) -> Dict:
        """
        Process all MP4 files in a folder.
        
        Args:
            input_folderpath: Path to the folder containing MP4 files.
            output_format: Output audio format ('mp3' or 'aac').
            
        Returns:
            Dict: A dictionary containing processing statistics.
        """
        input_path = pathlib.Path(input_folderpath)
        
        # Validate input folder
        if not input_path.is_dir():
            return {
                'total_files': 0,
                'successful': 0,
                'failed': 0,
                'errors': [f"Invalid input directory: {input_folderpath}"]
            }
        
        # Find all MP4 files in the folder
        mp4_files = list(input_path.glob('*.mp4'))
        
        results = {
            'total_files': len(mp4_files),
            'successful': 0,
            'failed': 0,
            'errors': []
        }
        
        if not mp4_files:
            results['errors'].append(f"No MP4 files found in {input_folderpath}")
            return results
        
        # Process each file
        for i, mp4_file in enumerate(mp4_files):
            success, message = self.process_file(str(mp4_file), output_format)
            
            if success:
                results['successful'] += 1
            else:
                results['failed'] += 1
                results['errors'].append(message)
        
        return results
    
    def get_output_filepath(self, input_filepath: str, output_format: str, output_directory: Optional[str] = None) -> str:
        """
        Generate the output file path based on the input file path and output format.
        
        Args:
            input_filepath: Path to the input MP4 file.
            output_format: Output audio format ('mp3' or 'aac').
            output_directory: Optional directory to save the output file. If None, the output file
                             is saved in the same directory as the input file.
                             
        Returns:
            str: Path to the output file.
        """
        input_path = pathlib.Path(input_filepath)
        
        if output_directory:
            output_dir = pathlib.Path(output_directory)
        else:
            output_dir = input_path.parent
        
        output_name = f"{input_path.stem}.{output_format}"
        output_filepath = output_dir / output_name
        
        return str(output_filepath)
