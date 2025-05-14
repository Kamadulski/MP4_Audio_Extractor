# MP4 Audio Extractor

A simple application to extract audio tracks from MP4 video files. Available in both GUI and command-line versions. Built using the Model-View-Controller (MVC) architecture for better modularity and maintainability.

## Features

- Extract audio from a single MP4 file or batch process an entire folder
- Save as MP3 or AAC format
- Simple, user-friendly interface
- Output files are saved in the same location as the input files

## Requirements

- Python 3.6 or higher
- FFmpeg installed and available in the system PATH

## Installation

1. Ensure you have Python 3.6+ installed
2. Download and install FFmpeg from [ffmpeg.org](https://ffmpeg.org/)
3. Add FFmpeg to your system PATH
4. Clone or download this repository

## Architecture

The application is built using the Model-View-Controller (MVC) architecture:

- **Model**: Handles the core audio extraction logic and FFmpeg interaction
- **View**: Provides the user interface (both GUI and CLI versions)
- **Controller**: Connects the model and views, handling the application logic

## Usage

### GUI Version

**Note:** The GUI version requires tkinter, which is included with most Python installations but may need to be installed separately on some systems.

1. Run the GUI application:
   ```
   python mp4_audio_extractor_gui.py
   ```

   Or use the module directly:
   ```
   python -m mp4_audio_extractor
   ```

2. Use the "Select File" button to choose a single MP4 file, or "Select Folder" to select a directory containing MP4 files.

3. Choose the desired output format (MP3 or AAC).

4. Click "Convert Audio" to start the extraction process.

5. The status of the conversion will be displayed in the status area.

### Command-Line Version

The command-line version is available for systems without tkinter or for users who prefer a CLI.

1. Process a single file:
   ```
   python mp4_audio_extractor_cli.py path/to/video.mp4 [--format mp3|aac]
   ```

   Or use the module directly:
   ```
   python -m mp4_audio_extractor --cli path/to/video.mp4 [--format mp3|aac]
   ```

2. Process all MP4 files in a folder:
   ```
   python mp4_audio_extractor_cli.py path/to/folder [--format mp3|aac]
   ```

3. Get help:
   ```
   python mp4_audio_extractor_cli.py --help
   ```

## Notes

- The application requires FFmpeg to be installed and available in the system PATH.
- When extracting to AAC format, the application attempts to copy the audio stream without re-encoding (assuming the source audio is AAC).
- When extracting to MP3 format, the application uses the libmp3lame codec with a bitrate of 320kbps.
- The application will automatically fall back to CLI mode if tkinter is not available.

## Project Structure

```
mp4_audio_extractor/
├── __init__.py         # Package initialization
├── __main__.py         # Entry point when run as a module
├── model.py            # Core audio extraction logic
├── view_gui.py         # GUI interface
├── view_cli.py         # CLI interface
├── controller.py       # Application logic
├── utils.py            # Utility functions
mp4_audio_extractor_gui.py  # Thin wrapper for GUI entry point
mp4_audio_extractor_cli.py  # Thin wrapper for CLI entry point
```

The standalone scripts (`mp4_audio_extractor_gui.py` and `mp4_audio_extractor_cli.py`) are thin wrappers around the module functionality, ensuring consistent behavior regardless of how the application is launched.

## License

[MIT License](LICENSE)
