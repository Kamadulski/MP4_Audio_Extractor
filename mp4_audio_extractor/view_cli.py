"""
CLI View component for the MP4 Audio Extractor.

This module contains the command-line interface for the application.
"""

import argparse
import sys
from typing import Dict, Any

from mp4_audio_extractor.controller import AudioExtractorController


class AudioExtractorCLI:
    """CLI view class for the MP4 Audio Extractor."""

    def __init__(self, controller: AudioExtractorController):
        """Initialize the CLI view.

        Args:
            controller: The controller instance to use.
        """
        self.controller = controller
        self.parser = argparse.ArgumentParser(description='Extract audio from MP4 files.')
        self.parser.add_argument('input', help='Input MP4 file or folder containing MP4 files')
        self.parser.add_argument('-f', '--format', choices=['mp3', 'aac'], default='mp3',
                                help='Output audio format (default: mp3)')

        # Add bitrate options
        bitrate_group = self.parser.add_mutually_exclusive_group()
        bitrate_group.add_argument('-b', '--bitrate', choices=['128k', '192k', '320k'], default='192k',
                                  help='Audio bitrate for MP3 output (default: 192k)')
        bitrate_group.add_argument('--custom-bitrate', metavar='BITRATE',
                                  help='Custom audio bitrate for MP3 output (e.g., 256k)')

    def parse_args(self) -> argparse.Namespace:
        """
        Parse command-line arguments.

        Returns:
            argparse.Namespace: Parsed arguments.
        """
        return self.parser.parse_args()



    def display_message(self, message: str):
        """
        Display a message to the user.

        Args:
            message: The message to display.
        """
        print(message)

    def display_error(self, message: str):
        """
        Display an error message to the user.

        Args:
            message: The error message to display.
        """
        print(f"Error: {message}", file=sys.stderr)

    def get_bitrate_from_args(self, args):
        """
        Determine the bitrate to use based on command-line arguments.

        Args:
            args: Parsed command-line arguments.

        Returns:
            str: The bitrate to use (e.g., '128k', '192k', '320k', or a custom value).
        """
        if args.custom_bitrate:
            # If custom bitrate is provided, ensure it has the 'k' suffix
            custom_bitrate = args.custom_bitrate
            if not custom_bitrate.endswith('k'):
                try:
                    # Try to convert to int to validate it's a number
                    int(custom_bitrate)
                    custom_bitrate = f"{custom_bitrate}k"
                except ValueError:
                    # If not a valid number, use the default
                    self.display_error(f"Invalid custom bitrate: {custom_bitrate}. Using default 192k.")
                    return '192k'
            return custom_bitrate
        else:
            # Use the standard bitrate option
            return args.bitrate

    def display_folder_results(self, results: Dict[str, Any]):
        """
        Display the results of processing a folder.

        Args:
            results: Dictionary containing processing statistics.
        """
        print(f"\nProcessing complete.")
        print(f"Total files: {results['total_files']}")
        print(f"Successful: {results['successful']}")
        print(f"Failed: {results['failed']}")

        if results['errors']:
            print("\nErrors:")
            for error in results['errors']:
                print(f"- {error}")

    def run(self) -> int:
        """
        Run the CLI application.

        Returns:
            int: Exit code (0 for success, non-zero for failure).
        """
        args = self.parse_args()

        # Check if FFmpeg is available
        if not self.controller.check_ffmpeg():
            self.display_error("FFmpeg not found. Please install FFmpeg and make sure it's in your system PATH.")
            return 1

        import pathlib

        input_path = pathlib.Path(args.input)

        if input_path.is_file():
            # Process a single file
            self.display_message(f"Processing file: {input_path.name}")

            # Determine which bitrate to use
            bitrate = self.get_bitrate_from_args(args)

            success, message = self.controller.process_file(str(input_path), args.format, bitrate)

            if success:
                self.display_message(message)
                return 0
            else:
                self.display_error(message)
                return 1

        elif input_path.is_dir():
            # Process a folder
            self.display_message(f"Processing folder: {input_path}")

            # Determine which bitrate to use
            bitrate = self.get_bitrate_from_args(args)

            results = self.controller.process_folder(str(input_path), args.format, bitrate)
            self.display_folder_results(results)

            if results['failed'] == 0:
                return 0
            else:
                return 1

        else:
            self.display_error(f"Input path '{args.input}' is neither a file nor a folder.")
            return 1
