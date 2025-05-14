#!/usr/bin/env python3
"""
Setup script for the MP4 Audio Extractor package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mp4_audio_extractor",
    version="1.0.0",
    author="MP4 Audio Extractor Team",
    author_email="example@example.com",
    description="A simple application to extract audio tracks from MP4 video files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mp4_audio_extractor",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "mp4-audio-extractor=mp4_audio_extractor.__main__:main",
            "mp4-audio-extractor-cli=mp4_audio_extractor.__main__:main_cli",
        ],
    },
)
