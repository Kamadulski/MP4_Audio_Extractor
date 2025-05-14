#!/usr/bin/env python3
"""
MP4 Audio Extractor CLI

A simple command-line application to extract audio from MP4 video files.
"""

import sys
from mp4_audio_extractor.model import AudioExtractorModel
from mp4_audio_extractor.controller import AudioExtractorController
from mp4_audio_extractor.view_cli import AudioExtractorCLI


def main():
    """Main entry point for the CLI application."""
    # Create the model, view, and controller
    model = AudioExtractorModel()
    controller = AudioExtractorController(model)
    view = AudioExtractorCLI()

    # Connect the view and controller
    view.set_controller_callbacks(
        controller.process_file,
        controller.process_folder,
        controller.check_ffmpeg
    )

    # Run the application
    return view.run()

if __name__ == "__main__":
    sys.exit(main())
