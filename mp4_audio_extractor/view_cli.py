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
            success, message = self.controller.process_file(str(input_path), args.format)

            if success:
                self.display_message(message)
                return 0
            else:
                self.display_error(message)
                return 1

        elif input_path.is_dir():
            # Process a folder
            self.display_message(f"Processing folder: {input_path}")
            results = self.controller.process_folder(str(input_path), args.format)
            self.display_folder_results(results)

            if results['failed'] == 0:
                return 0
            else:
                return 1

        else:
            self.display_error(f"Input path '{args.input}' is neither a file nor a folder.")
            return 1
