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
2. No additional Python packages are required beyond the standard library

## Using the Application

### GUI Version

#### Starting the GUI Application

1. Navigate to the application directory
2. Run the application by executing:
   ```
   python mp4_audio_extractor.py
   ```

#### Extracting Audio from a Single File (GUI)

1. Click the "Select File" button
2. Browse to and select the MP4 file you want to process
3. Choose the desired output format (MP3 or AAC)
4. Click the "Convert Audio" button
5. The application will process the file and save the extracted audio in the same directory as the input file

#### Batch Processing Multiple Files (GUI)

1. Click the "Select Folder" button
2. Browse to and select the folder containing MP4 files
3. Choose the desired output format (MP3 or AAC)
4. Click the "Convert Audio" button
5. The application will process all MP4 files in the selected folder and save the extracted audio files in the same directory as each input file

### Command-Line Version

#### Using the CLI Application

1. Navigate to the application directory

2. Process a single file:
   ```
   python mp4_audio_extractor_cli.py path/to/video.mp4 [--format mp3|aac]
   ```

3. Process all MP4 files in a folder:
   ```
   python mp4_audio_extractor_cli.py path/to/folder [--format mp3|aac]
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
python mp4_audio_extractor_cli.py C:\Videos\myvideo.mp4 --format aac

# Process all MP4 files in a folder and save as MP3
python mp4_audio_extractor_cli.py C:\Videos
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
- When extracting to MP3 format, the application uses the libmp3lame codec with a bitrate of 320kbps
- The application removes metadata from the output files
