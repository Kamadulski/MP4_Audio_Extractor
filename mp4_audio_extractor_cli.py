#!/usr/bin/env python3
"""
MP4 Audio Extractor CLI

A simple command-line application to extract audio from MP4 video files.
"""

import sys
from mp4_audio_extractor.__main__ import main_cli

if __name__ == "__main__":
    sys.exit(main_cli())
