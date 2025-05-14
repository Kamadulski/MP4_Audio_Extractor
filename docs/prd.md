Okay, here is a detailed PRD for the MP4 Audio Extractor tool, formatted in Markdown as requested.

# Document Header

**Product Name:** MP4 Audio Extractor
**Version:** 1.0
**Date:** May 13, 2025
**Author:** Your Name/Team Name
**Status:** Draft

# Executive Summary

The MP4 Audio Extractor is a simple, user-friendly Windows 11 desktop application built with Python. Its primary purpose is to allow users to easily extract the audio track from one or more MP4 video files and save them as standard audio files (MP3 or AAC). The tool focuses on a straightforward graphical user interface (GUI), offering options to select a single MP4 file or an entire folder containing multiple MP4 files for batch processing. The output files will be saved in the same directory as their source files, using the original base filename. This tool addresses the common need to isolate audio content from video without requiring technical command-line knowledge or complex video editing software.

# Product Vision

The vision for the MP4 Audio Extractor is to be the go-to simple, reliable, and free tool for Windows 11 users who need to quickly and effortlessly get audio files from their MP4 videos. We aim to provide a minimal, intuitive interface that makes the process accessible to anyone, regardless of technical skill. The core purpose is utility and convenience, solving a specific, frequent task efficiently. The target users are individuals who deal with video files (personal recordings, downloaded content, etc.) and need the audio component for listening on audio players, simple editing, or archiving. The success of the tool will be measured by its ease of use, reliability in handling the specified audio format, and positive user feedback (if distributed).

# User Personas

**Persona:** The Casual Converter

*   **Demographics:** Age 30-60, uses Windows 11 for personal tasks, moderate computer literacy.
*   **Goals:**
    *   Extract audio from MP4 videos quickly and without hassle.
    *   Save the audio in a widely compatible format (MP3).
    *   Process multiple files at once if needed (e.g., a folder of video recordings).
    *   Avoid complex software with many settings.
*   **Pain Points:**
    *   Finding and installing complex video conversion software.
    *   Command-line tools are intimidating.
    *   Online converters have privacy concerns or limitations.
    *   Not understanding audio/video codecs or conversion settings.
*   **Scenario:** Has a folder of family videos recorded on a phone (MP4 format). Wants to extract the audio tracks to listen to conversations or background sound on an MP3 player or phone music app without the video. Wants to select the whole folder and get the audio files automatically named and placed next to the videos.

# Feature Specifications

## 1. Feature: Core Audio Extraction & Conversion Engine

**Description:** The underlying mechanism that reads an MP4 file, identifies the primary audio track, extracts it, and converts/saves it to the target audio format (MP3 or AAC). This engine needs to be robust enough to handle the expected source audio format (AAC 48000Hz stereo 320kbps).

*   **User Story:** As a user, when I initiate a conversion, I expect the tool to accurately extract the audio from my MP4 file and create a usable audio file in the desired format.
*   **Acceptance Criteria:**
    *   Given a valid MP4 file containing an audio track (specifically in the format: AAC 48000Hz stereo 320kbps).
    *   When the core engine processes this file.
    *   Then an output audio file (either `.mp3` or `.aac`) is successfully created.
    *   The output audio file contains the complete audio track from the source MP4.
    *   The quality of the output audio should be reasonably preserved, considering the conversion to MP3 or re-muxing/conversion to AAC from the source AAC. (Note: Direct codec copy might be possible if output is AAC and input is compatible AAC, which is preferred for speed/quality if possible).
    *   The process completes without crashing for valid input files.
*   **Edge Cases:**
    *   Input MP4 file is corrupted or incomplete.
    *   Input MP4 file has no audio track.
    *   Input MP4 file has an audio track in a format significantly different from the expected AAC 48kHz stereo 320kbps.
    *   Input MP4 has multiple audio tracks (tool should default to the first audio track found).
    *   Errors during the conversion process itself (e.g., library issues).

## 2. Feature: GUI - Single File Selection

**Description:** A user interface element (button) that allows the user to open a standard Windows file browser dialog to select a single MP4 file for conversion. A display area (text field or label) shows the path of the selected file.

*   **User Story:** As a user, I want a clear way to pick just one MP4 file from my computer to convert its audio.
*   **Acceptance Criteria:**
    *   The main GUI window includes a clearly labeled button (e.g., "Select MP4 File").
    *   Clicking this button opens a standard Windows "Open File" dialog.
    *   The dialog should initially filter for `.mp4` files, but ideally allow the user to view "All Files".
    *   Selecting a file and confirming in the dialog populates a visible text field or label in the GUI with the full path of the selected file.
    *   Canceling the file selection dialog does not crash the application and leaves the file path display empty or unchanged.
    *   There is a separate, clear button to initiate the conversion once a file is selected (e.g., "Convert File").
*   **Edge Cases:**
    *   User cancels the file selection dialog.
    *   User attempts to select a file type other than MP4 (the GUI should ideally guide but the core engine handles the eventual error).
    *   The selected file path is extremely long or contains unusual characters.
    *   The selected file no longer exists or is inaccessible by the time conversion is attempted (handled by the core engine, but GUI should display an error).

## 3. Feature: GUI - Folder Selection

**Description:** A user interface element (button) that allows the user to open a standard Windows folder browser dialog to select a directory. The tool will then identify all MP4 files *directly within* that selected folder for batch processing. A display area shows the path of the selected folder.

*   **User Story:** As a user, I want a quick way to convert the audio for all the MP4 files located in a specific folder.
*   **Acceptance Criteria:**
    *   The main GUI window includes a clearly labeled button (e.g., "Select Folder").
    *   Clicking this button opens a standard Windows "Browse For Folder" dialog.
    *   Selecting a folder and confirming in the dialog populates a visible text field or label in the GUI with the full path of the selected folder.
    *   Canceling the folder selection dialog does not crash the application and leaves the folder path display empty or unchanged.
    *   There is a separate, clear button to initiate the conversion once a folder is selected (e.g., "Convert Folder").
    *   Initiating folder conversion triggers the core engine for *each* file ending with `.mp4` found directly within the selected folder path (non-recursive).
    *   The GUI should provide some feedback during batch processing (e.g., processing file X of N, or displaying the current file being processed). *Minimal feature might omit detailed progress, but indicating activity is good.*
*   **Edge Cases:**
    *   User cancels the folder selection dialog.
    *   The selected folder contains no `.mp4` files.
    *   The selected folder contains many files, some of which are not `.mp4`.
    *   Permissions issues preventing the tool from listing files in the folder or reading specific files.
    *   Errors occurring for individual files during a batch process (should ideally skip the problematic file and continue with the next, logging the error).

## 4. Feature: Default Output Location and Naming

**Description:** The converted audio file(s) will be saved in the *exact same directory* as the original MP4 source file(s). The base filename will be preserved, with only the extension changed to `.mp3` or `.aac`.

*   **User Story:** As a user, I want the converted audio files to appear right next to my original video files, automatically named correctly, so I can easily find them.
*   **Acceptance Criteria:**
    *   Given a source file located at `C:\Videos\MyMovie.mp4`.
    *   When converted, the output file is saved at `C:\Videos\MyMovie.mp3` (or `C:\Videos\MyMovie.aac`).
    *   Given a folder selection `D:\Recordings\` containing `Clip1.mp4` and `Clip2.mp4`.
    *   When processed, two output files are created: `D:\Recordings\Clip1.mp3` (or `.aac`) and `D:\Recordings\Clip2.mp3` (or `.aac`).
    *   The output file extension is consistently `.mp3` or consistently `.aac` for all conversions in a given run (or based on internal logic/default). For simplicity and compatibility, `.mp3` is the preferred default target format, though `.aac` might be technically simpler given the source codec. The tool should commit to one primary output format or make the logic clear (e.g., "Output as MP3 unless conversion fails, then try AAC"). Let's prioritize `.mp3` as the primary output goal for broad compatibility, but `.aac` is acceptable if technically much easier/more reliable from the source format.
*   **Edge Cases:**
    *   An output file with the exact target name already exists (`MyMovie.mp3` already exists). The tool should handle this (e.g., overwrite without warning, prompt the user, or skip). *Minimum viable product could simply attempt to write, potentially causing an error or overwriting depending on the library/OS behavior. A slightly better approach would be to prompt or add a number.* Let's define this as an edge case the *developer* needs to consider handling gracefully (e.g., with a simple overwrite confirmation dialog or a skip option if implementing more than minimum).
    *   Permissions issues preventing the tool from writing files to the source directory.
    *   The source directory no longer exists or is inaccessible by the time of saving.

# Technical Requirements

*   **Minimum Tech Stack:** Python
*   **Operating System:** Windows 11 (desktop application)
*   **GUI Framework:** A Python-compatible GUI library that works on Windows 11. Standard options include `tkinter` (built-in), `PyQt`, `PySide`, `PySimpleGUI`. `tkinter` is the most "minimum tech stack" as it requires no external installs *for the GUI framework itself*.
*   **Audio/Video Processing Library:** A robust library capable of reading MP4 containers, extracting audio streams (specifically AAC 48kHz stereo 320kbps), decoding if necessary, and encoding to MP3 or AAC.
    *   **Recommendation:** `ffmpeg`. This industry-standard tool is highly capable. The Python application would likely interface with `ffmpeg` either via `subprocess` calls or a Python wrapper library like `ffmpeg-python`. The `ffmpeg` executable would need to be bundled with the application or the user instructed to install it and add it to their PATH. Bundling `ffmpeg` simplifies user experience.
*   **File System Interaction:** Standard Python libraries (`os`, `pathlib`, `tkinter.filedialog`) for file and directory selection, path manipulation, and file writing.
*   **Data Storage:**
    *   **No Persistent Database:** The tool does not require a database.
    *   **Temporary Data:** May need temporary storage for audio streams during processing. `ffmpeg` handles this internally for most operations.
    *   **Configuration (Optional):** Could optionally store the last used directory in a simple config file (`.ini`, `.json`) or Windows Registry, but this is not a minimum requirement.

# Implementation Roadmap

This roadmap outlines the key phases for developing the MP4 Audio Extractor Minimum Viable Product (MVP).

1.  **Phase 1: Core Engine Proof of Concept (CLI)** (Estimated Time: 1-2 days)
    *   Goal: Verify the ability to extract and convert audio from the specified MP4 format using Python and a backend library (like `ffmpeg`).
    *   Tasks:
        *   Research and select the specific Python approach for interacting with `ffmpeg` (subprocess vs. wrapper).
        *   Develop a simple Python script that takes hardcoded or command-line input paths for a source MP4 (with the target audio format) and an output MP3/AAC file.
        *   Implement the logic to call `ffmpeg` (or equivalent) to perform the extraction and conversion.
        *   Test with sample MP4 files matching the specified AAC format.
        *   Ensure error handling for basic issues (file not found, invalid command).
    *   Outcome: A working command-line script that reliably converts a single, known MP4 file to MP3/AAC.

2.  **Phase 2: Basic GUI with Single File Functionality** (Estimated Time: 2-3 days)
    *   Goal: Create the fundamental GUI structure and hook up the single-file conversion capability.
    *   Tasks:
        *   Choose a Python GUI framework (`tkinter` recommended for minimum dependencies).
        *   Design and implement the basic GUI layout (title, file selection area, folder selection area, status message area, convert button).
        *   Add the "Select MP4 File" button and integrate the file dialog.
        *   Implement displaying the selected file path.
        *   Integrate the Phase 1 core logic to be triggered by a "Convert File" button when a single file is selected.
        *   Display basic status/completion messages in the GUI.
    *   Outcome: A functional GUI application that can select one MP4 file and convert it, showing basic progress or completion.

3.  **Phase 3: Add Folder Selection and Batch Processing** (Estimated Time: 2-3 days)
    *   Goal: Implement the folder selection feature and logic for iterating and processing multiple files.
    *   Tasks:
        *   Add the "Select Folder" button and integrate the folder dialog.
        *   Implement displaying the selected folder path.
        *   Add a "Convert Folder" button.
        *   Implement the logic triggered by "Convert Folder" to find all `.mp4` files in the selected directory.
        *   Loop through found `.mp4` files, calling the core conversion logic for each.
        *   Implement basic feedback for batch processing (e.g., processing file name, total count).
        *   Improve error handling to continue batch processing even if one file fails.
    *   Outcome: A GUI application that supports both single file and folder selection for conversion.

4.  **Phase 4: Refinement, Error Handling, and Packaging** (Estimated Time: 2-3 days)
    *   Goal: Improve robustness, user feedback, and prepare for potential distribution.
    *   Tasks:
        *   Enhance error handling and display more informative messages to the user in the GUI (e.g., "No audio track found", "File already exists", "Conversion failed: [details]").
        *   Implement specific handling for the "output file already exists" edge case (e.g., simple overwrite confirmation or automatic renaming/skipping option, defaulting to overwrite for MVP simplicity).
        *   Refine the GUI layout and user experience based on testing.
        *   Consider adding a simple progress bar (optional but helpful).
        *   Prepare the application for potential distribution (e.g., using PyInstaller to create an executable for Windows 11, including bundling `ffmpeg` if required).
        *   Write basic user instructions or documentation.
    *   Outcome: A more robust, user-friendly application ready for testing or limited distribution, handling common errors gracefully.

**Total Estimated Time (MVP):** 7-11 days (This is a rough estimate and depends heavily on developer experience with Python, GUI frameworks, and `ffmpeg` integration).

Further iterations (Version 1.1, etc.) could include features like:
*   Choosing the output format (MP3 or AAC).
*   Selecting a different output directory.
*   Configuring output quality/bitrate.
*   Handling MP4s with unexpected audio formats more gracefully or providing options.
*   Recursively processing subfolders.
*   More detailed progress indicators.
*   Option to handle multiple audio tracks.

