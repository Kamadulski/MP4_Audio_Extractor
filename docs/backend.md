```markdown
# Backend Implementation Guide: MP4 Audio Extractor Tool

## 1. Document Header

Version: 1.0
Date: May 13, 2025

## 2. API Design (Internal Logic Interface)

This tool is a standalone application with a GUI, not a traditional client-server application. Therefore, the "API" refers to the interface that the GUI layer will use to interact with the core audio extraction logic. These functions will be called directly within the same Python process.

**Core Functions:**

1.  **`process_single_file(input_filepath: str, output_format: str, output_directory: str = None) -> bool`**
    *   **Description:** Processes a single MP4 file to extract its audio track.
    *   **Parameters:**
        *   `input_filepath`: Full path to the source .mp4 file.
        *   `output_format`: Target audio format (e.g., 'mp3', 'aac'). Determines the output file extension and encoding method.
        *   `output_directory` (Optional): Directory where the output file should be saved. If `None`, the output file is saved in the same directory as the input file.
    *   **Returns:** `True` if processing is successful, `False` otherwise (e.g., file not found, `ffmpeg` error). Could be extended to return a status dictionary or raise exceptions for detailed error handling.
    *   **Payload/Data:** File paths and format string.

2.  **`process_folder(input_folderpath: str, output_format: str, output_directory: str = None) -> dict`**
    *   **Description:** Scans a folder for .mp4 files and processes each one.
    *   **Parameters:**
        *   `input_folderpath`: Full path to the source folder.
        *   `output_format`: Target audio format ('mp3' or 'aac').
        *   `output_directory` (Optional): Base directory where output files should be saved. If `None`, each output file is saved in the same directory as its corresponding input file. Note: This doesn't recreate the input folder structure if processing subfolders (which is an optional extension).
    *   **Returns:** A dictionary containing processing statistics (e.g., `{'total_files': 5, 'successful': 4, 'failed': 1, 'errors': [...]}`).
    *   **Payload/Data:** Folder path and format string.

**Helper Functions (Internal):**

*   `_generate_output_path(input_filepath: str, output_format: str, output_directory: str = None) -> str`: Determines the full output file path based on input, format, and optional output directory.
*   `_execute_ffmpeg(input_filepath: str, output_filepath: str, output_format: str) -> bool`: Handles the actual `ffmpeg` command execution. This is the core worker function.

## 3. Data Models

As a standalone desktop application without a database or persistent state beyond user settings (which are not in scope for this backend logic), there are no complex data models or database tables required.

The primary data structures are:

*   **File Paths:** Standard string representations of file and directory paths.
*   **Processing Results:** Simple dictionaries or lists to report outcomes, as defined in the `process_folder` return type.

## 4. Business Logic

The core business logic revolves around identifying the input files, determining the output paths, and using `ffmpeg` to extract and convert the audio streams.

**Dependencies:**

1.  **Python 3.x:** The programming language.
2.  **`ffmpeg` executable:** The heavy lifting for media processing is done by `ffmpeg`. It must be installed separately on the Windows 11 system and accessible in the system's PATH.
3.  **`ffmpeg-python` library:** A Python wrapper for `ffmpeg` that makes it easier and safer to construct and execute `ffmpeg` commands programmatically. Install via `pip install ffmpeg-python`.
4.  **`os`, `pathlib`:** Standard Python libraries for path manipulation and file system interaction.

**Flow:**

1.  **Input Handling:**
    *   Receive input from the GUI: either a single file path or a folder path.
    *   Receive the desired output format ('mp3' or 'aac').
    *   Receive an optional output directory.

2.  **Processing Dispatch:**
    *   If a single file is selected, call `process_single_file`.
    *   If a folder is selected, call `process_folder`.

3.  **`process_single_file` Logic:**
    *   Validate that the input path exists and is a file.
    *   Generate the output file path using `_generate_output_path`.
    *   Call `_execute_ffmpeg` with the appropriate parameters.
    *   Return success or failure based on the result of `_execute_ffmpeg`.

4.  **`process_folder` Logic:**
    *   Validate that the input path exists and is a directory.
    *   Initialize statistics (count of files, successful, failed).
    *   Use `os.listdir()` or `pathlib.Path.glob()` to find all files ending with `.mp4` within the input folder.
    *   Iterate through the list of MP4 files:
        *   For each `.mp4` file, generate its corresponding output path.
        *   Call `process_single_file` for the current MP4 file.
        *   Update statistics based on the result.
        *   (Optional) Log errors or failed files.
    *   Return the final statistics dictionary.

5.  **`_generate_output_path` Logic:**
    *   Take input path, output format, and optional output directory.
    *   If `output_directory` is `None`, use the directory of the input file (`os.path.dirname(input_filepath)` or `pathlib.Path(input_filepath).parent`).
    *   Get the base name of the input file (without extension) (`os.path.splitext(os.path.basename(input_filepath))[0]` or `pathlib.Path(input_filepath).stem`).
    *   Combine the output directory, base name, and the new extension (`.mp3` or `.aac`).
    *   Handle potential edge cases (e.g., directory creation if `output_directory` is specified and doesn't exist - although saving in the source dir avoids this).

6.  **`_execute_ffmpeg` Logic:**
    *   Construct the `ffmpeg` command using `ffmpeg-python`.
    *   Key `ffmpeg` arguments:
        *   `-i <input_filepath>`: Specify the input file.
        *   `-map 0:a:0`: Select the first audio stream from the input file (assuming the desired audio is the first stream). This is important for files with multiple streams (video, multiple audio, subtitles).
        *   **Output format options:**
            *   If `output_format` is 'aac': `-c:a copy`. This is the most efficient method if the source audio (AAC) and target format (AAC) match, as it avoids re-encoding. It's lossless for the audio stream itself.
            *   If `output_format` is 'mp3': `-c:a libmp3lame -ab 320k`. Specify the MP3 encoder and a bitrate (320kbps matches the source bitrate, offering good quality, though slightly different from the source AAC).
        *   `-vn`: Disable video recording (we only want audio).
        *   `-f <output_format>`: Specify the output container format (e.g., `mp3`, `aac`). `ffmpeg-python` often infers this from the output filename extension, but being explicit can be clearer.
        *   `<output_filepath>`: Specify the output file path.
    *   Execute the command using `ffmpeg-python`'s `run()` method.
    *   Wrap the execution in a `try...except` block to catch errors (e.g., `ffmpeg.Error`).
    *   Return `True` on success, `False` on error.

**Handling Source Audio Format:**

The knowledge that the source audio is expected to be AAC 48000Hz stereo 320kbps informs the choice of output options:
*   Saving as **AAC** should ideally use `-c:a copy` to simply copy the existing audio stream without re-encoding. This is fast and preserves the original stream's quality.
*   Saving as **MP3** requires re-encoding. Choosing a bitrate like 320kbps (`-ab 320k`) aims to retain high quality, comparable to the source bitrate, although MP3 is a different lossy format than AAC.

## 5. Security

For a standalone desktop tool processing local files, the security concerns are different from a network service.

*   **Malicious Files:** Processing crafted malicious media files could potentially exploit vulnerabilities in `ffmpeg`. Keeping the `ffmpeg` executable updated is the primary mitigation. Using `ffmpeg-python` provides a layer of abstraction but doesn't eliminate this risk inherent in the media processing engine.
*   **Path Traversal:** Ensure that generated output paths are safe and within expected directories. Using standard Python path handling functions (`os.path`, `pathlib`) generally prevents trivial traversal issues, especially when dealing with paths relative to known input directories.
*   **Resource Consumption:** Processing media is computationally intensive. The tool could potentially be used to consume high CPU/disk resources if pointed to a large number of files. For a simple local tool, this is usually an operational concern rather than a security one, but it's worth noting.
*   **External Dependency (`ffmpeg`):** The reliance on an external executable (`ffmpeg`) means its security is critical. Ensure users obtain `ffmpeg` from official, trusted sources.

Authentication and Authorization are **not applicable** for this type of standalone, single-user tool. The user running the tool has full file system access within their user permissions.

## 6. Performance

Performance is primarily determined by the speed of the `ffmpeg` execution, especially the encoding process.

*   **Key Optimization: Audio Copying:** When the output format is AAC, use `ffmpeg`'s stream copy feature (`-c:a copy`). This avoids computationally expensive re-encoding and is significantly faster than re-encoding, limited only by disk I/O. Given the source format is AAC, this is the most efficient option for AAC output.
*   **Encoding Speed:** If converting to MP3 (or another format requiring re-encoding), the speed depends on the CPU and the complexity of the audio. Using a standard encoder like `libmp3lame` in `ffmpeg` is generally well-optimized.
*   **Parallel Processing (Advanced):** For processing multiple files in a folder, the current design is sequential. To improve performance on multi-core processors, consider using Python's `concurrent.futures.ThreadPoolExecutor` or `multiprocessing.Pool` to process multiple files concurrently. This adds complexity to the `process_folder` logic and error handling but can significantly reduce total processing time for large batches.
*   **Disk I/O:** Processing involves reading source files and writing target files. Using fast storage (SSD) can help, especially when copying streams.
*   **`ffmpeg` Installation:** Ensure `ffmpeg` is correctly installed and accessible. Incorrect installation or path issues can cause delays or failures.

## 7. Code Examples

```python
import os
import pathlib
import ffmpeg # Requires 'pip install ffmpeg-python'
import sys # To check for ffmpeg executable (optional but good practice)

# --- Configuration ---
# Check if ffmpeg executable is available (basic check)
# More robust checks might use subprocess to run `ffmpeg -version`
try:
    # This command will fail if ffmpeg is not in PATH
    ffmpeg.run('ffmpeg -version', capture_stdout=True, capture_stderr=True, overwrite_output=True, quiet=True)
    FFMPEG_AVAILABLE = True
except ffmpeg.Error:
    print("Error: FFmpeg executable not found. Please ensure FFmpeg is installed and in your system's PATH.", file=sys.stderr)
    FFMPEG_AVAILABLE = False
except FileNotFoundError:
     print("Error: FFmpeg executable not found. Please ensure FFmpeg is installed and in your system's PATH.", file=sys.stderr)
     FFMPEG_AVAILABLE = False


# --- Helper Functions ---

def _generate_output_path(input_filepath: str, output_format: str, output_directory: str = None) -> str:
    """Generates the target output file path."""
    input_path = pathlib.Path(input_filepath)

    if output_directory:
        output_dir_path = pathlib.Path(output_directory)
    else:
        # Default: save in the same directory as the input file
        output_dir_path = input_path.parent

    # Ensure the output directory exists
    output_dir_path.mkdir(parents=True, exist_ok=True)

    output_filename = f"{input_path.stem}.{output_format.lower()}"
    output_filepath = output_dir_path / output_filename

    return str(output_filepath)

def _execute_ffmpeg(input_filepath: str, output_filepath: str, output_format: str) -> bool:
    """Executes the ffmpeg command to extract and convert audio."""
    if not FFMPEG_AVAILABLE:
        print(f"Skipping {input_filepath}: FFmpeg is not available.")
        return False

    input_path = pathlib.Path(input_filepath)
    output_path = pathlib.Path(output_filepath)

    if not input_path.exists():
        print(f"Error: Input file not found - {input_filepath}")
        return False

    try:
        stream = ffmpeg.input(str(input_path))

        # Select the first audio stream (-map 0:a:0)
        # -vn disables video
        # Output format options depend on the desired format
        if output_format.lower() == 'aac':
            # Copy audio stream if source is AAC (most efficient)
            # Assuming source is AAC as per requirements.
            # If source could be something else, may need conditional encoding
            # ffmpeg -i input.mp4 -vn -c:a copy output.aac
            print(f"Processing {input_filepath} -> {output_filepath} (AAC copy)")
            stream = stream.output(str(output_path), format='aac', acodec='copy', vn=None, overwrite_output=True)
        elif output_format.lower() == 'mp3':
            # Re-encode to MP3 320kbps
            # ffmpeg -i input.mp4 -vn -c:a libmp3lame -ab 320k output.mp3
            print(f"Processing {input_filepath} -> {output_filepath} (MP3 320k)")
            stream = stream.output(str(output_path), format='mp3', acodec='libmp3lame', audio_bitrate='320k', vn=None, overwrite_output=True)
        else:
            print(f"Error: Unsupported output format '{output_format}'.")
            return False

        # Run the ffmpeg command
        # capture_stdout/stderr=True prevents ffmpeg from printing to console directly
        # quiet=True suppresses progress output, handle progress externally if needed
        ffmpeg.run(stream, capture_stdout=True, capture_stderr=True, overwrite_output=True, quiet=True)

        print(f"Successfully created {output_filepath}")
        return True

    except ffmpeg.Error as e:
        print(f"Error processing {input_filepath}:")
        print(f"  Stderr: {e.stderr.decode('utf8')}")
        # print(f"  Stdout: {e.stdout.decode('utf8')}") # Often less useful than stderr for errors
        return False
    except Exception as e:
        print(f"An unexpected error occurred processing {input_filepath}: {e}")
        return False

# --- Core Logic Functions (API Interface) ---

def process_single_file(input_filepath: str, output_format: str, output_directory: str = None) -> bool:
    """
    Processes a single MP4 file to extract its audio track.
    Called by the GUI when a single file is selected.
    """
    input_path = pathlib.Path(input_filepath)
    if not input_path.is_file() or not input_path.suffix.lower() == '.mp4':
        print(f"Error: Invalid input file selected: {input_filepath}")
        return False

    output_filepath = _generate_output_path(input_filepath, output_format, output_directory)

    print(f"Starting processing for single file: {input_filepath}")
    success = _execute_ffmpeg(input_filepath, output_filepath, output_format)

    return success

def process_folder(input_folderpath: str, output_format: str, output_directory: str = None) -> dict:
    """
    Scans a folder for .mp4 files and processes each one.
    Called by the GUI when a folder is selected.
    """
    input_path = pathlib.Path(input_folderpath)
    if not input_path.is_dir():
        print(f"Error: Invalid input directory selected: {input_folderpath}")
        return {'total_files': 0, 'successful': 0, 'failed': 0, 'errors': [f"Invalid input directory: {input_folderpath}"]}

    print(f"Scanning folder: {input_folderpath} for MP4 files...")
    mp4_files = list(input_path.glob('*.mp4')) # Finds files ending with .mp4 (case-insensitive search might be needed on case-sensitive file systems)

    results = {
        'total_files': len(mp4_files),
        'successful': 0,
        'failed': 0,
        'errors': []
    }

    print(f"Found {len(mp4_files)} MP4 files.")
    if not mp4_files:
        print("No MP4 files found in the selected directory.")
        return results

    for input_filepath in mp4_files:
        # input_filepath is a Path object here, convert to string for functions
        input_filepath_str = str(input_filepath)
        output_filepath = _generate_output_path(input_filepath_str, output_format, output_directory)

        print(f"Processing file: {input_filepath_str}")
        success = _execute_ffmpeg(input_filepath_str, output_filepath, output_format)

        if success:
            results['successful'] += 1
        else:
            results['failed'] += 1
            # Note: _execute_ffmpeg prints its own errors, but you could capture them here
            results['errors'].append(f"Failed to process {input_filepath_str}")

    print(f"Folder processing complete. Successful: {results['successful']}, Failed: {results['failed']}")
    return results

# --- Example Usage (for testing the backend logic) ---

if __name__ == "__main__":
    # This block is for testing the backend functions directly without a GUI
    # You would replace 'path/to/your/test.mp4' and 'path/to/your/test_folder'
    # with actual paths on your Windows 11 system for testing.
    # Ensure you have ffmpeg installed and in your system's PATH.

    # --- Test Case 1: Single File (MP3 output) ---
    print("\n--- Testing Single File (MP3) ---")
    test_mp4_file = "path/to/your/test_video.mp4" # Replace with a valid MP4 file path

    if os.path.exists(test_mp4_file):
        success = process_single_file(test_mp4_file, 'mp3')
        if success:
            print(f"Single file processing (MP3) successful for {test_mp4_file}")
        else:
            print(f"Single file processing (MP3) failed for {test_mp4_file}")
    else:
        print(f"Test file not found: {test_mp4_file}. Skipping single file test.")


    # --- Test Case 2: Single File (AAC output - copy) ---
    print("\n--- Testing Single File (AAC copy) ---")
    # Use the same test file, save as .aac
    if os.path.exists(test_mp4_file):
         success = process_single_file(test_mp4_file, 'aac')
         if success:
             print(f"Single file processing (AAC) successful for {test_mp4_file}")
         else:
             print(f"Single file processing (AAC) failed for {test_mp4_file}")
    else:
         print(f"Test file not found: {test_mp4_file}. Skipping single file AAC test.")


    # --- Test Case 3: Folder Processing (MP3 output) ---
    print("\n--- Testing Folder Processing (MP3) ---")
    test_folder = "path/to/your/test_folder" # Replace with a valid folder path containing MP4s

    if os.path.isdir(test_folder):
        results = process_folder(test_folder, 'mp3')
        print(f"\nFolder processing (MP3) results: {results}")
    else:
        print(f"Test folder not found: {test_folder}. Skipping folder test.")

    # --- Test Case 4: Folder Processing (AAC output) ---
    print("\n--- Testing Folder Processing (AAC) ---")
    if os.path.isdir(test_folder):
        results = process_folder(test_folder, 'aac')
        print(f"\nFolder processing (AAC) results: {results}")
    else:
        print(f"Test folder not found: {test_folder}. Skipping folder AAC test.")

```

**Integration with GUI:**

The GUI layer (using Tkinter, PyQt, or similar) will:
1.  Provide buttons/widgets for the user to select a file or a folder (using `filedialog`).
2.  Provide options (e.g., radio buttons) for the user to select the output format (MP3 or AAC).
3.  (Optional) Provide an option to specify a different output directory.
4.  On button click (e.g., "Convert"), call the appropriate backend function (`process_single_file` or `process_folder`) with the user's selections.
5.  Display feedback to the user based on the return values or exceptions from the backend functions (e.g., "Processing complete", "Error converting file X"). For folder processing, show the summary from the returned dictionary.
6.  Consider running the processing in a separate thread to prevent the GUI from freezing during long operations.
