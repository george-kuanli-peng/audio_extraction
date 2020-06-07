import subprocess


def extract_audio_from_video(input_file_path: str, output_file_path: str):
    proc = subprocess.run(
        ['ffmpeg',
         '-v', 'error',
         '-y',  # to overwrite the output file
         '-i', input_file_path,
         '-vn', '-acodec', 'copy',
         output_file_path],
        universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    if proc.stderr:
        raise Exception(f'There is error in calling ffmpeg: {proc.stderr}')
