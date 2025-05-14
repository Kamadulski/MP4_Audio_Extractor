import os
import sys
import shutil
import subprocess
import random # Import random for generating corrupted bytes

# Add the root directory to the sys.path to import from tests
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..')) # Go up one level to project root
sys.path.insert(0, PROJECT_ROOT)

from tests.test_utils.TestMediaGenerator import TestMediaGenerator

TEST_MEDIA_DIR = os.path.join(PROJECT_ROOT, 'tests', 'test_media')

def check_ffmpeg():
    """Check if FFmpeg is available."""
    try:
        # Use Popen instead of run with timeout for better compatibility
        process = subprocess.Popen(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = process.communicate(timeout=5) # Add a timeout
        return process.returncode == 0
    except (subprocess.SubprocessError, FileNotFoundError, TimeoutError):
        return False

def corrupt_file(filepath: str, corruption_type: str, num_bytes: int = 1024) -> tuple[bool, str]:
    """
    Intentionally corrupts a portion of a file.

    Args:
        filepath: The path to the file to corrupt.
        corruption_type: Type of corruption ('header', 'middle', 'random').
        num_bytes: The number of bytes to overwrite.

    Returns:
        Tuple[bool, str]: (success, message).
    """
    try:
        file_size = os.path.getsize(filepath)
        if file_size == 0:
            return False, f"File is empty, cannot corrupt: {filepath}"
        if file_size < num_bytes:
             # If file is smaller than num_bytes, just corrupt the whole file
             bytes_to_corrupt = file_size
        else:
             bytes_to_corrupt = num_bytes

        position = 0
        if corruption_type == 'middle':
            # Corrupt around the middle of the file
            position = max(0, (file_size // 2) - (bytes_to_corrupt // 2))
        elif corruption_type == 'random':
            # Corrupt at a random position, ensuring we don't go past file end
            position = random.randint(0, max(0, file_size - bytes_to_corrupt))
        # 'header' case defaults to position 0

        # Generate random bytes for corruption
        random_data = os.urandom(bytes_to_corrupt)

        # Open the file in binary read/write mode
        with open(filepath, 'rb+') as f:
            f.seek(position)
            f.write(random_data)

        return True, f"Successfully corrupted {bytes_to_corrupt} bytes at position {position} ({corruption_type}) in {os.path.basename(filepath)}"

    except FileNotFoundError:
        return False, f"Error: File not found for corruption: {filepath}"
    except OSError as e2:
        return False, f"Error corrupting file {filepath}: {e2}"
    except Exception as e2:
        return False, f"An unexpected error occurred during corruption: {e2}"


def generate_all_test_files():
    """Generates all required test media files, including corrupted ones."""
    print(f"Ensuring directory exists: {TEST_MEDIA_DIR}")
    os.makedirs(TEST_MEDIA_DIR, exist_ok=True)

    # --- Generate Base Valid Files ---
    print("\n--- Generating Base Valid Files ---")
    base_files_to_generate = [
        ("sample_base_2s.mp4", 2, 300, {}), # A basic 2s file with E3 tone
        ("sample_base_5s.mp4", 5, 200, {}), # A 5s file with A2 tone
    ]

    generated_base_count = 0
    failed_base_count = 0
    failed_base_files = []
    generated_base_filepaths = {} # Store paths for corruption

    for filename, duration, frequency, params in base_files_to_generate:
        filepath = os.path.join(TEST_MEDIA_DIR, filename)
        print(f"  Generating base file: {filename}...")
        success, message = TestMediaGenerator.generate_test_mp4_with_tone(
            output_filepath=filepath,
            duration=duration,
            audio_frequency=frequency,
            overwrite=True, # Always overwrite base files
            **params # Pass other optional parameters
        )

        if success:
            print(f"    Success: {message}")
            generated_base_count += 1
            generated_base_filepaths[filename] = filepath
        else:
            print(f"    Failed: {message}")
            failed_base_count += 1
            failed_base_files.append(filename)

    if failed_base_count > 0:
         print("\n--- Base Generation Summary ---")
         print(f"Failed to generate {failed_base_count} base files: {', '.join(failed_base_files)}")
         print("Cannot proceed with corrupting files if base files failed.")
         sys.exit(1) # Exit if base generation failed

    print("\nAll base files generated successfully.")

    # --- Generate Corrupted Files ---
    print("\n--- Generating Corrupted Files ---")
    corrupted_files_specs = [
        # (base_filename, corruption_type, output_suffix, num_bytes)
        ("sample_base_2s.mp4", "header", "_corrupted_header.mp4", 20), # Corrupt first 20 bytes (header)
        ("sample_base_2s.mp4", "middle", "_corrupted_middle.mp4", 1024), # Corrupt 1KB in the middle
    ]

    generated_corrupted_count = 0
    failed_corrupted_count = 0
    failed_corrupted_files = []

    for base_filename, corruption_type, output_suffix, num_bytes in corrupted_files_specs:
        if base_filename not in generated_base_filepaths:
            print(f"  Skipping corruption for '{base_filename}' as base file was not generated successfully.")
            failed_corrupted_count += 1
            failed_corrupted_files.append(base_filename + output_suffix)
            continue

        base_filepath = generated_base_filepaths[base_filename]
        output_filename = base_filename.replace('.mp4', output_suffix)
        output_filepath = os.path.join(TEST_MEDIA_DIR, output_filename)

        print(f"  Corrupting from '{base_filename}' ({corruption_type}) to '{output_filename}'...")

        try:
            # Copy the base file first
            shutil.copy2(base_filepath, output_filepath)

            # Now corrupt the copied file
            success, message = corrupt_file(output_filepath, corruption_type, num_bytes)

            if success:
                print(f"    Success: {message}")
                generated_corrupted_count += 1
            else:
                print(f"    Failed: {message}")
                failed_corrupted_count += 1
                failed_corrupted_files.append(output_filename)

        except FileNotFoundError:
             print(f"    Failed: Base file not found for copying: {base_filepath}")
             failed_corrupted_count += 1
             failed_corrupted_files.append(output_filename)
        except Exception as e2:
            print(f"    Failed: An error occurred during copying or corruption setup: {e2}")
            failed_corrupted_count += 1
            failed_corrupted_files.append(output_filename)


    print("\n--- Generation Summary ---")
    print(f"Base files intended: {len(base_files_to_generate)}")
    print(f"Base files generated successfully: {generated_base_count}")
    print(f"Corrupted files intended: {len(corrupted_files_specs)}")
    print(f"Corrupted files generated successfully: {generated_corrupted_count}")
    print(f"Total files failed (base or corrupted): {failed_base_count + failed_corrupted_count}")

    if failed_base_files or failed_corrupted_files:
        print("\n--- Failed Files ---")
        if failed_base_files:
            print(f"Base files: {', '.join(failed_base_files)}")
        if failed_corrupted_files:
             print(f"Corrupted files: {', '.join(failed_corrupted_files)}")
        sys.exit(1) # Indicate failure if any file didn't generate/corrupt
    else:
        print("\nAll specified test files (base and corrupted) generated successfully.")
        sys.exit(0) # Indicate success


if __name__ == "__main__":
    if not check_ffmpeg():
        print("Error: FFmpeg is not found in your system's PATH.")
        print("Please install FFmpeg before running this script.")
        sys.exit(1)

    # Optional: Clean up existing test_media directory before generating
    if os.path.exists(TEST_MEDIA_DIR):
         print(f"Removing existing test media directory: {TEST_MEDIA_DIR}")
         try:
             shutil.rmtree(TEST_MEDIA_DIR)
             print("Directory removed.")
         except OSError as e:
             print(f"Error removing directory: {e}")
             print("Proceeding with generation, but existing files might interfere.")

    generate_all_test_files()