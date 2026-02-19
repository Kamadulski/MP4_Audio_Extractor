# MP4 Audio Extractor 🎵

![GitHub release](https://img.shields.io/github/release/Kamadulski/MP4_Audio_Extractor.svg) ![GitHub issues](https://img.shields.io/github/issues/Kamadulski/MP4_Audio_Extractor.svg) ![GitHub forks](https://img.shields.io/github/forks/Kamadulski/MP4_Audio_Extractor.svg) ![GitHub stars](https://img.shields.io/github/stars/Kamadulski/MP4_Audio_Extractor.svg)

## Overview

Welcome to the **MP4 Audio Extractor**! This simple Python application allows you to extract audio tracks from MP4 video files. Whether you need MP3 or AAC formats, this tool has you covered. It supports both single file and batch processing, making it easy to convert multiple files at once. You can choose between a graphical user interface (GUI) or a command-line interface (CLI) based on your preference.

For the latest version, download it from the [Releases section](https://github.com/Kamadulski/MP4_Audio_Extractor/releases) and follow the instructions to get started.

## Features

- **Audio Formats**: Extract audio in MP3 or AAC formats.
- **Single and Batch Processing**: Handle one file or multiple files at once.
- **User-Friendly Interfaces**: Choose between a GUI for ease of use or a CLI for advanced users.
- **Cross-Platform**: Works on Windows, macOS, and Linux.
- **FFmpeg Integration**: Utilizes FFmpeg for high-quality audio extraction.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Graphical User Interface](#graphical-user-interface)
  - [Command-Line Interface](#command-line-interface)
- [Supported Formats](#supported-formats)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Installation

To install the MP4 Audio Extractor, follow these steps:

1. **Download**: Go to the [Releases section](https://github.com/Kamadulski/MP4_Audio_Extractor/releases) and download the latest version.
2. **Extract**: Unzip the downloaded file to your desired location.
3. **Install Dependencies**: Ensure you have Python installed on your machine. Install the required packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **FFmpeg**: Make sure FFmpeg is installed and accessible from your command line. You can download it from [FFmpeg's official site](https://ffmpeg.org/download.html).

## Usage

### Graphical User Interface

1. Launch the application by running `main.py` in your terminal or by double-clicking the file.
2. Use the "Select File" button to choose your MP4 video.
3. Choose your desired audio format (MP3 or AAC).
4. Select the output directory.
5. Click "Extract" to start the process.

### Command-Line Interface

To use the CLI, open your terminal and navigate to the folder where the application is located. Use the following command:

```bash
python main.py --input <path_to_mp4_file> --output <output_directory> --format <mp3|aac>
```

#### Example

```bash
python main.py --input video.mp4 --output ./audio --format mp3
```

This command will extract the audio from `video.mp4` and save it as an MP3 file in the `./audio` directory.

## Supported Formats

- **Input**: MP4
- **Output**: MP3, AAC

## Contributing

We welcome contributions! If you want to improve the MP4 Audio Extractor, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeature`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

Please ensure your code follows the existing style and includes appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or feedback, feel free to reach out:

- **Email**: kamadulski@example.com
- **GitHub**: [Kamadulski](https://github.com/Kamadulski)

For more updates, check the [Releases section](https://github.com/Kamadulski/MP4_Audio_Extractor/releases).

---

We hope you find the MP4 Audio Extractor useful! Happy extracting! 🎶