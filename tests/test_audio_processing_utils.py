import ffmpeg
import pytest
import pathlib
import shutil
import subprocess
from unittest.mock import patch
from mp4_audio_extractor.AudioProcessingUtils import AudioProcessingUtils

# Define the path to the test media directory relative to the test file
TEST_MEDIA_DIR = pathlib.Path(__file__).parent / "test_media"

# Paths to specific test files
VALID_MP4_2S = TEST_MEDIA_DIR / "sample_base_2s.mp4"
VALID_MP4_5S = TEST_MEDIA_DIR / "sample_base_5s.mp4"
CORRUPTED_HEADER_MP4 = TEST_MEDIA_DIR / "sample_base_2s_corrupted_header.mp4"
CORRUPTED_MIDDLE_MP4 = TEST_MEDIA_DIR / "sample_base_2s_corrupted_middle.mp4"
NON_MP4_FILE = TEST_MEDIA_DIR / "dummy.txt" # Need to create this dummy file


# --- Fixtures (These remain outside the test class definition) ---
# Pytest discovers fixtures at the module level or within conftest.py

@pytest.fixture(scope="module", autouse=True)
def create_dummy_files():
    """Fixture to create necessary dummy files for tests."""
    NON_MP4_FILE.write_text("This is a dummy file.")
    yield
    if NON_MP4_FILE.exists():
        NON_MP4_FILE.unlink()

@pytest.fixture
def temp_output_dir(tmp_path):
    """Fixture to provide a temporary directory for test outputs."""
    return tmp_path

@pytest.fixture
def temp_test_media_folder(tmp_path):
    """Fixture to create a temporary folder structure mirroring test_media."""
    temp_media_dir = tmp_path / "test_media_temp"
    temp_media_dir.mkdir()

    # Copy relevant test files
    # Check if source files exist before copying (important if test media wasn't generated)
    if VALID_MP4_2S.exists():
        shutil.copy(VALID_MP4_2S, temp_media_dir)
    else:
         pytest.fail(f"Test media file not found: {VALID_MP4_2S}")

    if VALID_MP4_5S.exists():
         shutil.copy(VALID_MP4_5S, temp_media_dir)
    else:
         pytest.fail(f"Test media file not found: {VALID_MP4_5S}")

    # Ensure dummy non-mp4 file exists before copying
    if NON_MP4_FILE.exists():
        shutil.copy(NON_MP4_FILE, temp_media_dir) # Include non-mp4 to ensure it's skipped
    else:
         pytest.fail(f"Dummy file not found: {NON_MP4_FILE}")


    yield temp_media_dir

    # Clean up generated files within the temporary folder (Pytest tmp_path cleans up the folder itself)
    for item in temp_media_dir.iterdir():
        if item.suffix in ['.mp3', '.aac']:
            item.unlink()


# --- Test Class ---
# Pytest discovers classes that start with 'Test'

class TestAudioProcessingUtils:
    """
    Tests for the AudioProcessingUtils static class.
    Organized in a class structure similar to other testing frameworks.
    """

    # --- Tests for check_ffmpeg ---

    def test_check_ffmpeg_available(self):
        """Test check_ffmpeg when ffmpeg is available."""
        # Assume ffmpeg is in the system PATH for this test environment
        # If not, you might need to mock subprocess.run
        if AudioProcessingUtils.check_ffmpeg():
            assert True # ffmpeg is found and executable
        else:
            # This case is for environments where ffmpeg might not be standard.
            # A proper CI setup should have ffmpeg. If this fails locally,
            # it might just mean ffmpeg isn't installed or in PATH.
            pytest.skip("FFmpeg not found in system PATH. Skipping check_ffmpeg_available test.")


    @patch('subprocess.run')
    def test_check_ffmpeg_not_available(self, mock_run):
        """Test check_ffmpeg when ffmpeg is not available (FileNotFoundError or SubprocessError)."""
        mock_run.side_effect = FileNotFoundError("ffmpeg not found")
        assert AudioProcessingUtils.check_ffmpeg() is False

    @patch('subprocess.run')
    def test_check_ffmpeg_subprocess_error(self, mock_run):
        """Test check_ffmpeg when subprocess returns an error."""
        mock_run.side_effect = subprocess.SubprocessError("some ffmpeg error")
        assert AudioProcessingUtils.check_ffmpeg() is False

    # --- Tests for process_file ---

    # Note: Fixtures like temp_output_dir are passed as arguments to test methods
    def test_process_file_mp4_to_mp3(self, temp_output_dir):
        """Test processing a valid MP4 to MP3."""
        # The AudioProcessingUtils saves output in the *input* file's directory by default
        output_filepath_in_input_dir = VALID_MP4_2S.parent / VALID_MP4_2S.with_suffix('.mp3').name
        success, message = AudioProcessingUtils.process_file(str(VALID_MP4_2S), 'mp3')

        assert success is True
        assert f"Successfully extracted audio to" in message
        # Check if the output file was created in the same directory as the input
        assert output_filepath_in_input_dir.exists()
        assert output_filepath_in_input_dir.stat().st_size > 0
        # Clean up the created file
        if output_filepath_in_input_dir.exists():
            output_filepath_in_input_dir.unlink()


    def test_process_file_mp4_to_aac(self, temp_output_dir):
        """Test processing a valid MP4 to AAC (copy codec)."""
        # The AudioProcessingUtils saves output in the *input* file's directory by default
        output_filepath_in_input_dir = VALID_MP4_2S.parent / VALID_MP4_2S.with_suffix('.aac').name
        success, message = AudioProcessingUtils.process_file(str(VALID_MP4_2S), 'aac')

        assert success is True
        assert f"Successfully extracted audio to" in message
        # Check if the output file was created in the same directory as the input
        assert output_filepath_in_input_dir.exists()
        assert output_filepath_in_input_dir.stat().st_size > 0
        # Clean up the created file
        if output_filepath_in_input_dir.exists():
            output_filepath_in_input_dir.unlink()

    # Note: Bitrate optimization logic is hard to test precisely without inspecting the output file properties,
    # but we can test that the function accepts and processes with the bitrate parameter.
    # A more advanced test might use ffprobe on the output file to verify bitrate/encoding properties.
    def test_process_file_with_bitrate_parameter(self, temp_output_dir):
        """Test processing MP4 to MP3 with a specific bitrate parameter."""
        # The AudioProcessingUtils saves output in the *input* file's directory by default
        output_filepath_in_input_dir = VALID_MP4_2S.parent / VALID_MP4_2S.with_suffix('.mp3').name
        bitrate = '128k'

        success, message = AudioProcessingUtils.process_file(str(VALID_MP4_2S), 'mp3', bitrate=bitrate)

        assert success is True
        assert f"Successfully extracted audio to" in message
        assert output_filepath_in_input_dir.exists()
        assert output_filepath_in_input_dir.stat().st_size > 0
        # Clean up
        if output_filepath_in_input_dir.exists():
            output_filepath_in_input_dir.unlink()


    def test_process_file_invalid_filepath(self):
        """Test processing with a non-existent file path."""
        invalid_path = "/path/to/nonexistent_file.mp4"
        success, message = AudioProcessingUtils.process_file(invalid_path, 'mp3')

        assert success is False
        assert f"Error: {pathlib.Path(invalid_path).name} is not a valid file." in message

    def test_process_file_non_mp4_file(self):
        """Test processing a file that is not an MP4."""
        # NON_MP4_FILE is created by the fixture
        success, message = AudioProcessingUtils.process_file(str(NON_MP4_FILE), 'mp3')

        assert success is False
        assert f"Error: {NON_MP4_FILE.name} is not an MP4 file." in message

    def test_process_file_unsupported_format(self):
        """Test processing with an unsupported output format."""
        success, message = AudioProcessingUtils.process_file(str(VALID_MP4_2S), 'wav')

        assert success is False
        assert "Error: Unsupported output format 'wav'." in message

    @patch('ffmpeg.run')
    def test_process_file_ffmpeg_error(self, mock_ffmpeg_run, temp_output_dir):
        """Test handling of ffmpeg.Error during processing."""
        # Simulate an FFmpeg error
        mock_ffmpeg_run.side_effect = ffmpeg.Error('cmd', 'stdout', b'stderr message')

        success, message = AudioProcessingUtils.process_file(str(VALID_MP4_2S), 'mp3')

        assert success is False
        assert f"Error processing {VALID_MP4_2S.name}: stderr message" in message
        # Ensure no output file was created (or is zero size, depending on ffmpeg behavior)
        output_filepath = VALID_MP4_2S.parent / VALID_MP4_2S.with_suffix('.mp3').name
        assert not output_filepath.exists() or output_filepath.stat().st_size == 0

    # Test corrupted files - FFmpeg should ideally fail gracefully
    def test_process_file_corrupted_header(self, temp_output_dir):
        """Test processing a file with a corrupted header."""
        # Check if the corrupted file exists before attempting to test
        if not CORRUPTED_HEADER_MP4.exists():
             pytest.skip(f"Corrupted test media file not found: {CORRUPTED_HEADER_MP4}")

        success, message = AudioProcessingUtils.process_file(str(CORRUPTED_HEADER_MP4), 'mp3')
        assert success is False
        # The error message might vary depending on FFmpeg version and corruption type,
        # but it should indicate a processing error related to the file.
        assert "Error processing" in message
        output_filepath = CORRUPTED_HEADER_MP4.parent / CORRUPTED_HEADER_MP4.with_suffix('.mp3').name
        assert not output_filepath.exists() or output_filepath.stat().st_size == 0

    def test_process_file_corrupted_middle(self, temp_output_dir):
        """Test processing a file with corruption in the middle."""
        # Check if the corrupted file exists before attempting to test
        if not CORRUPTED_MIDDLE_MP4.exists():
             pytest.skip(f"Corrupted test media file not found: {CORRUPTED_MIDDLE_MP4}")

        # FFmpeg might succeed partially or fail depending on the corruption.
        # We test for failure as a likely outcome for severe corruption impacting audio.
        success, message = AudioProcessingUtils.process_file(str(CORRUPTED_MIDDLE_MP4), 'mp3')
        assert success is True
        output_filepath = CORRUPTED_MIDDLE_MP4.parent / CORRUPTED_MIDDLE_MP4.with_suffix('.mp3').name
        assert output_filepath.exists()


    # --- Tests for process_folder ---

    # Uses the temp_test_media_folder fixture which copies files to a temporary location
    def test_process_folder_success(self, temp_test_media_folder):
        """Test processing a folder with valid MP4 files."""
        results = AudioProcessingUtils.process_folder(str(temp_test_media_folder), 'mp3')

        assert results['total_files'] == 2 # Only MP4 files are counted from the copied files
        assert results['successful'] == 2
        assert results['failed'] == 0
        assert results['errors'] == []

        # Verify output files exist in the temporary folder
        assert (temp_test_media_folder / VALID_MP4_2S.with_suffix('.mp3').name).exists()
        assert (temp_test_media_folder / VALID_MP4_5S.with_suffix('.mp3').name).exists()
        # Verify non-mp4 was not processed
        assert not (temp_test_media_folder / NON_MP4_FILE.with_suffix('.mp3').name).exists()


    def test_process_folder_empty(self, tmp_path):
        """Test processing an empty folder."""
        empty_folder = tmp_path / "empty_folder"
        empty_folder.mkdir()

        results = AudioProcessingUtils.process_folder(str(empty_folder), 'mp3')

        assert results['total_files'] == 0
        assert results['successful'] == 0
        assert results['failed'] == 0
        assert len(results['errors']) == 1
        assert "No MP4 files found" in results['errors'][0]


    def test_process_folder_non_existent(self, tmp_path):
        """Test processing a non-existent folder."""
        non_existent_folder = tmp_path / "non_existent_folder"

        results = AudioProcessingUtils.process_folder(str(non_existent_folder), 'mp3')

        assert results['total_files'] == 0
        assert results['successful'] == 0
        assert results['failed'] == 0
        assert len(results['errors']) == 1
        assert f"Invalid input directory: {non_existent_folder}" in results['errors'][0]

    # Patching a static method within a class requires specifying the class itself
    @patch('mp4_audio_extractor.AudioProcessingUtils.AudioProcessingUtils.process_file')
    def test_process_folder_with_errors(self, mock_process_file, temp_test_media_folder):
        """Test processing a folder where some files fail."""
        # Configure mock_process_file to succeed for one, fail for another
        def side_effect_mock(filepath, output_format, bitrate):
            filename = pathlib.Path(filepath).name
            if filename == VALID_MP4_2S.name:
                # Simulate success for one file
                return True, f"Successfully processed {filename}"
            elif filename == VALID_MP4_5S.name:
                 # Simulate failure for another file
                return False, f"Error processing {filename}: Mock error"
            else: # Should not happen for MP4 files, but good practice
                 return False, f"Unexpected file processed: {filename}"

        mock_process_file.side_effect = side_effect_mock

        results = AudioProcessingUtils.process_folder(str(temp_test_media_folder), 'mp3')

        assert results['total_files'] == 2 # Still counts both MP4s as total
        assert results['successful'] == 1
        assert results['failed'] == 1
        assert len(results['errors']) == 1 # Only one expected error message from the failed file
        assert f"Error processing {VALID_MP4_5S.name}: Mock error" in results['errors'][0]

        # Check that process_file was called for the two MP4 files within the temp folder
        # We need to check the actual paths passed to the mock
        called_files = {pathlib.Path(call.args[0]).name for call in mock_process_file.call_args_list}
        assert VALID_MP4_2S.name in called_files
        assert VALID_MP4_5S.name in called_files
        assert mock_process_file.call_count == 2 # Ensure it was called exactly twice for the two MP4s


    # --- Tests for get_output_filepath ---
    # These tests don't require file system interaction, so they are simpler

    def test_get_output_filepath_same_directory(self):
        """Test generating output path when output_directory is None."""
        input_path = "/path/to/input/video.mp4"
        output_format = "mp3"
        expected_output_path = str(pathlib.Path("/path/to/input/video.mp3")) # Convert to string for comparison if needed
        assert AudioProcessingUtils.get_output_filepath(input_path, output_format) == expected_output_path

    def test_get_output_filepath_specified_directory(self):
        """Test generating output path when output_directory is specified."""
        input_path = "/path/to/input/video.mp4"
        output_format = "aac"
        output_directory = "/path/to/output"
        expected_output_path = str(pathlib.Path("/path/to/output/video.aac"))
        assert AudioProcessingUtils.get_output_filepath(input_path, output_format, output_directory) == expected_output_path

    def test_get_output_filepath_different_formats(self):
        """Test generating output path with different output formats."""
        input_path = "/another/place/movie.mp4"
        output_directory = "/exports"

        # Test mp3 format
        output_format_mp3 = "mp3"
        expected_output_path_mp3 = str(pathlib.Path("/exports/movie.mp3"))
        assert AudioProcessingUtils.get_output_filepath(input_path, output_format_mp3, output_directory) == expected_output_path_mp3

        # Test aac format
        output_format_aac = "aac"
        expected_output_path_aac = str(pathlib.Path("/exports/movie.aac"))
        assert AudioProcessingUtils.get_output_filepath(input_path, output_format_aac, output_directory) == expected_output_path_aac

    def test_get_output_filepath_input_with_different_suffix_case(self):
        """Test handling input file suffix case."""
        input_path = "/path/to/input/VIDEO.MP4" # Uppercase suffix
        output_format = "mp3"
        expected_output_path = str(pathlib.Path("/path/to/input/VIDEO.mp3"))
        assert AudioProcessingUtils.get_output_filepath(input_path, output_format) == expected_output_path

    def test_get_output_filepath_output_dir_is_pathlib_object(self):
        """Test with output_directory provided as a pathlib.Path object."""
        input_path = "/path/to/input/video.mp4"
        output_format = "mp3"
        output_directory = pathlib.Path("/path/to/output")
        expected_output_path = str(pathlib.Path("/path/to/output/video.mp3"))
        assert AudioProcessingUtils.get_output_filepath(input_path, output_format, str(output_directory)) == expected_output_path
