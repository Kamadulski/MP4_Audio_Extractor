import subprocess
import pathlib
import sys # Import sys for platform-specific executable handling

class TestMediaGenerator:
    """Utility class for generating test media files using FFmpeg."""

    @staticmethod
    def generate_test_mp4_with_tone(
        output_filepath: str,
        duration: int = 5,
        audio_frequency: int = 440,
        video_size: str = '640x480',
        video_fps: int = 30,
        audio_sample_rate: int = 44100,
        overwrite: bool = False
    ) -> tuple[bool, str]:
        """
        Generates a test MP4 file with a visual test pattern and an audible tone.

        This file is suitable for testing audio extraction utilities.

        Args:
            output_filepath: The desired path for the output .mp4 file.
            duration: Duration of the generated file in seconds.
            audio_frequency: Frequency of the sine wave tone in Hz.
            video_size: Resolution of the test video pattern (e.g., '640x480').
            video_fps: Frame rate of the test video pattern.
            audio_sample_rate: Sample rate of the audio tone.
            overwrite: If True, overwrite the output file if it already exists.

        Returns:
            Tuple[bool, str]: (success, message) where success is True if generation
                             was successful, and message contains status or error information.
        """
        output_path = pathlib.Path(output_filepath)
        output_dir = output_path.parent

        # Ensure output directory exists (optional, but good for test setup)
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            return False, f"Error creating output directory {output_dir}: {e}"

        # Construct the FFmpeg command
        # Use 'ffmpeg' executable name, but check for platform specifics if necessary
        ffmpeg_cmd = ['ffmpeg']

        if overwrite:
            ffmpeg_cmd.append('-y') # Overwrite output files without asking

        ffmpeg_cmd.extend([
            '-f', 'lavfi', '-i', f'testsrc=duration={duration}:size={video_size}:rate={video_fps}', # Video input
            '-f', 'lavfi', '-i', f'sine=frequency={audio_frequency}:sample_rate={audio_sample_rate}:duration={duration}', # Audio input
            '-c:v', 'libx264',       # Video codec
            '-c:a', 'aac',           # Audio codec (standard for MP4)
            '-strict', 'experimental', # Sometimes needed for certain AAC encoders
            str(output_filepath)     # Output file path
        ])

        try:
            # Execute the FFmpeg command
            # Capture output but suppress it unless there's an error for quiet operation
            result = subprocess.run(
                ffmpeg_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True # Raise CalledProcessError if command returns non-zero exit code
            )
            return True, f"Successfully generated test file: {output_filepath}"

        except FileNotFoundError:
            return False, "Error: FFmpeg not found. Please ensure FFmpeg is installed and in your system's PATH."
        except subprocess.CalledProcessError as e:
            # FFmpeg command failed
            error_message = e.stderr.decode(sys.getfilesystemencoding(), errors='replace').strip()
            return False, f"Error generating test file '{output_path.name}': {error_message}\nCommand: {' '.join(e.cmd)}"
        except Exception as e:
            return False, f"An unexpected error occurred: {e}"
