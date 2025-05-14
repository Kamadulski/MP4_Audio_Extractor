# MP4 Audio Extractor - User Guide

## Introduction

MP4 Audio Extractor is a simple tool that allows you to extract audio tracks from MP4 video files. It is available in two versions:

1. **GUI Version** - Provides a user-friendly graphical interface
2. **CLI Version** - Command-line interface for systems without tkinter or for users who prefer a CLI

Both versions support single file and batch processing.

## Installation

### Prerequisites

Before using the MP4 Audio Extractor, you need to have the following installed:

1. **Python 3.6 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation
   - For the GUI version, you need tkinter, which is included with most Python installations but may need to be installed separately on some systems

2. **FFmpeg**
   - Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - Add FFmpeg to your system PATH:
     - Extract the downloaded FFmpeg archive
     - Copy the path to the bin folder (e.g., `C:\ffmpeg\bin`)
     - Add this path to your system's PATH environment variable

### Installing the Application

1. Download or clone the MP4 Audio Extractor repository
2. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

   This will install the ffmpeg-python package, which is used to interact with FFmpeg.

## Using the Application

### GUI Version

#### Starting the GUI Application

1. Navigate to the application directory
2. Run the application by executing:
   ```
   python mp4_audio_extractor_gui.py
   ```

   Or use the module directly:
   ```
   python -m mp4_audio_extractor
   ```

#### Extracting Audio from a Single File (GUI)

1. Click the "Select File" button
2. Browse to and select the MP4 file you want to process
3. Choose the desired output format (MP3 or AAC)
4. Select the audio bitrate using either the dropdown menu or by entering a custom value
5. Click the "Convert Audio" button
6. The application will process the file and save the extracted audio in the same directory as the input file

#### Batch Processing Multiple Files (GUI)

1. Click the "Select Folder" button
2. Browse to and select the folder containing MP4 files
3. Choose the desired output format (MP3 or AAC)
4. Select the audio bitrate using either the dropdown menu or by entering a custom value
5. Click the "Convert Audio" button
6. The application will process all MP4 files in the selected folder and save the extracted audio files in the same directory as each input file

### Command-Line Version

#### Using the CLI Application

1. Navigate to the application directory

2. Process a single file:
   ```
   python mp4_audio_extractor_cli.py path/to/video.mp4 [-f mp3|aac] [-b 128k|192k|320k] [--custom-bitrate BITRATE]
   ```

3. Process all MP4 files in a folder:
   ```
   python mp4_audio_extractor_cli.py path/to/folder [-f mp3|aac] [-b 128k|192k|320k] [--custom-bitrate BITRATE]
   ```

4. Get help:
   ```
   python mp4_audio_extractor_cli.py --help
   ```

Examples:
```
# Extract audio from a single file and save as MP3 (default)
python mp4_audio_extractor_cli.py C:\Videos\myvideo.mp4

# Extract audio from a single file and save as AAC
python mp4_audio_extractor_cli.py C:\Videos\myvideo.mp4 -f aac

# Extract audio with a specific bitrate
python mp4_audio_extractor_cli.py C:\Videos\myvideo.mp4 -b 192k

# Extract audio with a custom bitrate
python mp4_audio_extractor_cli.py C:\Videos\myvideo.mp4 --custom-bitrate 256k

# Process all MP4 files in a folder and save as MP3
python mp4_audio_extractor_cli.py C:\Videos
```

You can also use the module directly:
```
python -m mp4_audio_extractor --cli path/to/video.mp4 [-f mp3|aac] [-b 128k|192k|320k] [--custom-bitrate BITRATE]
```

### Understanding the Output

- The extracted audio files will have the same name as the input files but with a different extension (.mp3 or .aac)
- In the GUI version, the status area at the bottom of the application window shows the current operation and results
- In the CLI version, status messages are printed to the console

## Troubleshooting

### Common Issues

1. **"FFmpeg not found" error**
   - Make sure FFmpeg is installed correctly
   - Verify that FFmpeg is added to your system PATH
   - Try restarting the application after installing FFmpeg

2. **No MP4 files found in selected folder**
   - Verify that the selected folder contains files with the .mp4 extension
   - Note that the application does not search in subfolders

3. **Error processing a specific file**
   - The file might be corrupted or have an unsupported audio codec
   - Check the status message for more details about the error

## Technical Notes

- When extracting to AAC format, the application attempts to copy the audio stream without re-encoding (assuming the source audio is AAC)
- When extracting to MP3 format, the application uses the libmp3lame codec with the selected bitrate (default: 192kbps)
- The application allows selecting from standard bitrates (128k, 192k, 320k) or specifying a custom bitrate
- The application removes metadata from the output files
- The application uses the ffmpeg-python library to interact with FFmpeg, which provides a more reliable and maintainable interface than direct subprocess calls
- By default, output files are saved in the same directory as the input files, with the same filename but a different extension
