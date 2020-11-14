# audio_extraction
It contains tools for converting video clips to audio files and for extracting a part of audio file.

# Requirements

1. Python 3.6+
1. ffmpeg

# Setup

1. (Optional) Set up a Python virtual-env and activate virtual-env.
1. Install the dependent Python packages.
     ```
     pip install -r requirements.txt
     ```
1. Set up a configuration file:
   1. Copy from the template `config-example.ini` file and name it `config.ini` under the same directory.
   1. Fill up all related fields in `config.ini` with the actual settings.

# Usage

1. (Optional) Activate virtual-env.
1. Run the program.
     ```
     ./cmd.py
     ```
   - To specify a certain recording date (rather than a latest recording date),
     add the `--rec_date=YYYY-MM-DD` option (E.g., `--rec_date=2020-11-07`)