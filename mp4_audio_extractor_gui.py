#!/usr/bin/env python3
"""
MP4 Audio Extractor GUI

A simple GUI application to extract audio from MP4 video files.
"""

import sys
from mp4_audio_extractor.controller import AudioExtractorController
from mp4_audio_extractor.view_gui import AudioExtractorGUI


def main():
    """Main entry point for the GUI application."""
    try:
        # Create the controller
        controller = AudioExtractorController()
        view = AudioExtractorGUI()

        # Connect the view and controller
        view.set_controller_callbacks(
            controller.handle_gui_convert,
            controller.check_ffmpeg
        )

        # Run the application
        view.run()
        return 0

    except ImportError:
        print("Error: Tkinter is not available. Please use the CLI version instead.")
        print("Run: python mp4_audio_extractor_cli.py --help")
        return 1


if __name__ == "__main__":
    sys.exit(main())
