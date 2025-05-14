"""
Audio processing utilities for the MP4 Audio Extractor.

This module contains utility functions for extracting audio from MP4 files.
"""

import pathlib
import ffmpeg
import subprocess
from typing import Dict, Tuple, Optional


class AudioProcessingUtils:
    """Utility class for handling audio extraction from MP4 files."""

    @staticmethod
    def check_ffmpeg() -> bool:
        """
        Check if FFmpeg is available in the system PATH.

        Returns:
            bool: True if FFmpeg is available, False otherwise.
        """
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

    @staticmethod
    def process_file(input_filepath: str, output_format: str, bitrate: str = '192k') -> Tuple[bool, str]:
        """
        Process a single MP4 file to extract its audio.

        Args:
            input_filepath: Path to the input MP4 file.
            output_format: Output audio format ('mp3' or 'aac').
            bitrate: Audio bitrate for the output file (e.g., '128k', '192k', '320k').
                    Only applies to MP3 format. Default is '192k'.
                    For MP3 format, the function will optimize the bitrate by using the lower value
                    between the source audio's bitrate and the provided bitrate parameter.

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

        # Process using ffmpeg-python based on output format
        try:
            # Create base input stream
            stream = ffmpeg.input(str(input_filepath))

            # For MP3 format, optimize the bitrate based on source audio
            optimal_bitrate = bitrate
            if output_format.lower() == 'mp3':
                try:
                    # Probe the input file to get audio information
                    probe_data = ffmpeg.probe(str(input_filepath))

                    # Find the audio stream
                    audio_stream = next((s for s in probe_data['streams']
                                        if s.get('codec_type') == 'audio'), None)

                    if audio_stream:
                        # Check if the audio stream has a bit_rate field
                        if 'bit_rate' in audio_stream:
                            # Get source bitrate in kbps (remove 'k' suffix from our bitrate parameter)
                            source_bitrate_bps = int(audio_stream['bit_rate'])
                            source_bitrate_kbps = source_bitrate_bps / 1000
                            target_bitrate_kbps = int(bitrate.rstrip('k'))

                            # Check if source has variable bitrate (VBR)
                            is_vbr = False
                            if 'tags' in audio_stream and 'encoder' in audio_stream['tags']:
                                # Some encoders indicate VBR in their tags
                                encoder_info = audio_stream['tags']['encoder'].lower()
                                is_vbr = 'vbr' in encoder_info

                            # Use the optimization logic
                            if is_vbr:
                                # For VBR, use the provided bitrate parameter
                                optimal_bitrate = bitrate
                            else:
                                # For CBR, use the lower value between source and target
                                if source_bitrate_kbps < target_bitrate_kbps:
                                    optimal_bitrate = f"{int(source_bitrate_kbps)}k"
                                else:
                                    optimal_bitrate = bitrate
                except Exception as probe_error:
                    # If probing fails, use the provided bitrate parameter
                    optimal_bitrate = bitrate

            # Configure output based on format
            if output_format.lower() == 'mp3':
                output = ffmpeg.output(
                    stream.audio,
                    str(output_filepath),
                    acodec='libmp3lame',
                    ab=optimal_bitrate,
                    map_metadata='-1',
                    vn=None  # No video
                )
            elif output_format.lower() == 'aac':
                output = ffmpeg.output(
                    stream.audio,
                    str(output_filepath),
                    acodec='copy',
                    map_metadata='-1',
                    vn=None  # No video
                )
            else:
                return False, f"Error: Unsupported output format '{output_format}'."

            # Run the FFmpeg command with overwrite enabled
            ffmpeg.run(output, overwrite_output=True, quiet=True)
            return True, f"Successfully extracted audio to {output_filepath}"

        except ffmpeg.Error as e:
            return False, f"Error processing {input_path.name}: {e.stderr.decode() if e.stderr else str(e)}"

    @staticmethod
    def process_folder(input_folderpath: str, output_format: str, bitrate: str = '192k',
                      progress_callback=None) -> Dict:
        """
        Process all MP4 files in a folder.

        Args:
            input_folderpath: Path to the folder containing MP4 files.
            output_format: Output audio format ('mp3' or 'aac').
            bitrate: Audio bitrate for the output file (e.g., '128k', '192k', '320k').
                    Only applies to MP3 format. Default is '192k'.
            progress_callback: Optional callback function to report progress.
                          Called with (current_file, current_index, total_files).

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
            # Call progress callback if provided
            if progress_callback:
                progress_callback(str(mp4_file), i + 1, len(mp4_files))
                
            success, message = AudioProcessingUtils.process_file(str(mp4_file), output_format, bitrate)

            if success:
                results['successful'] += 1
            else:
                results['failed'] += 1
                results['errors'].append(message)

        return results

    @staticmethod
    def get_output_filepath(input_filepath: str, output_format: str, output_directory: Optional[str] = None) -> str:
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

