"""
Main entry point for the MP4 Audio Extractor package.

This module allows the package to be run as a module:
python -m mp4_audio_extractor
"""

import sys
from mp4_audio_extractor.AudioExtractorController import AudioExtractorController


def main_cli():
    """Entry point for the CLI application."""
    # Create the controller
    controller = AudioExtractorController()

    # Use the CLI view
    from mp4_audio_extractor.view_cli import AudioExtractorCLI

    # Create the view with the controller
    view = AudioExtractorCLI(controller)

    # Run the CLI application
    return view.run()


def main():
    """Main entry point for the application."""
    # Create the controller
    controller = AudioExtractorController()

    # Determine which view to use based on command-line arguments
    if len(sys.argv) > 1 and sys.argv[1] == '--cli':
        # Use the CLI view
        return main_cli()

    else:
        # Use the GUI view
        try:
            from mp4_audio_extractor.view_gui import AudioExtractorGUI

            # Create the view with the controller
            view = AudioExtractorGUI(controller)

            # Run the GUI application
            view.run()
            return 0

        except ImportError:
            print("Error: Tkinter is not available. Using CLI mode instead.")
            print("To use the GUI, please install Tkinter.")
            print("To use CLI mode explicitly, run: python -m mp4_audio_extractor --cli")

            # Fall back to CLI mode
            return main_cli()


if __name__ == "__main__":
    sys.exit(main())
