"""
Controller component for the MP4 Audio Extractor.

This module connects the model and view components and handles the application logic.
"""

import os
from typing import Callable, Dict, Any

from mp4_audio_extractor.utils import AudioProcessingUtils


class AudioExtractorController:
    """Controller class for the MP4 Audio Extractor."""

    def __init__(self):
        """
        Initialize the controller.
        """
        self._ffmpeg_available = None

    def check_ffmpeg(self) -> bool:
        """
        Check if FFmpeg is available.

        Returns:
            bool: True if FFmpeg is available, False otherwise.
        """
        if self._ffmpeg_available is None:
            self._ffmpeg_available = AudioProcessingUtils.check_ffmpeg()
        return self._ffmpeg_available

    def process_file(self, input_filepath: str, output_format: str, bitrate: str = '192k') -> tuple:
        """
        Process a single MP4 file.

        Args:
            input_filepath: Path to the input MP4 file.
            output_format: Output audio format ('mp3' or 'aac').
            bitrate: Audio bitrate for the output file (e.g., '128k', '192k', '320k').
                    Only applies to MP3 format. Default is '192k'.

        Returns:
            tuple: (success, message) where success is True if processing was successful,
                  and message contains status or error information.
        """
        return AudioProcessingUtils.process_file(input_filepath, output_format, bitrate)

    def process_folder(self, input_folderpath: str, output_format: str, bitrate: str = '192k') -> Dict[str, Any]:
        """
        Process all MP4 files in a folder.

        Args:
            input_folderpath: Path to the folder containing MP4 files.
            output_format: Output audio format ('mp3' or 'aac').
            bitrate: Audio bitrate for the output file (e.g., '128k', '192k', '320k').
                    Only applies to MP3 format. Default is '192k'.

        Returns:
            Dict: A dictionary containing processing statistics.
        """
        return AudioProcessingUtils.process_folder(input_folderpath, output_format, bitrate)

    def handle_gui_convert(self, selected_path: str, output_format: str, bitrate: str,
                          update_status: Callable, set_processing_state: Callable):
        """
        Handle the convert button click event from the GUI.

        Args:
            selected_path: The selected file or folder path.
            output_format: The selected output format.
            bitrate: Audio bitrate for the output file (e.g., '128k', '192k', '320k').
            update_status: Callback function to update the status message.
            set_processing_state: Callback function to set the processing state.
        """
        try:
            if os.path.isfile(selected_path):
                # Process a single file
                update_status(f"Processing file: {os.path.basename(selected_path)}")
                success, message = AudioProcessingUtils.process_file(selected_path, output_format, bitrate)

                if success:
                    update_status(message)
                else:
                    update_status(f"Error: {message}")

            elif os.path.isdir(selected_path):
                # Process a folder
                update_status(f"Scanning folder: {selected_path} for MP4 files...")
                results = AudioProcessingUtils.process_folder(selected_path, output_format, bitrate)

                if results['total_files'] == 0:
                    update_status(f"No MP4 files found in {selected_path}")
                else:
                    update_status(
                        f"Processing complete. Total: {results['total_files']}, "
                        f"Successful: {results['successful']}, Failed: {results['failed']}"
                    )

            else:
                update_status("Error: Selected path is neither a file nor a folder.")

        except Exception as e:
            update_status(f"Error during conversion: {str(e)}")

        finally:
            # Re-enable the convert button
            set_processing_state(False)
