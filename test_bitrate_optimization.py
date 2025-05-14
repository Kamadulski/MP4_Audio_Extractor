#!/usr/bin/env python3
"""
Test script for the MP4 Audio Extractor's bitrate optimization feature.

This script tests the process_file function in the AudioProcessingUtils class
to verify that it correctly optimizes the bitrate based on the source audio.
"""

import os
import sys
from mp4_audio_extractor.utils import AudioProcessingUtils

def test_process_file():
    """Test the process_file function with different bitrate scenarios."""
    
    # Check if a test file was provided as a command-line argument
    if len(sys.argv) > 1:
        test_file = sys.argv[1]
        if not os.path.exists(test_file):
            print(f"Error: Test file '{test_file}' not found.")
            return
    else:
        print("Usage: python test_bitrate_optimization.py path/to/test.mp4")
        return
    
    print(f"Testing bitrate optimization with file: {test_file}")
    
    # Test with different bitrate values
    bitrates = ['128k', '192k', '320k']
    
    for bitrate in bitrates:
        print(f"\nTesting with bitrate: {bitrate}")
        success, message = AudioProcessingUtils.process_file(test_file, 'mp3', bitrate)
        
        if success:
            print(f"Success: {message}")
        else:
            print(f"Error: {message}")

if __name__ == "__main__":
    test_process_file()
