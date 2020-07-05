import subprocess
from typing import Any, Dict, Optional


def extract_audio_from_video(input_file_path: str, output_file_path: str,
                             start_time: Optional[str] = None, stop_time: Optional[str] = None):
    input_args = [
        'ffmpeg',
        '-v', 'error',
        '-nostdin',
        '-y'  # to overwrite the output file
    ]
    if start_time:
        input_args.extend(['-ss', start_time])
    input_args.extend(['-i', input_file_path])

    output_args = [
        '-vn',
        '-acodec', 'copy'
    ]
    if stop_time:
        output_args.extend(['-to', stop_time])
    output_args.append(output_file_path)

    proc = subprocess.run(input_args + output_args, **_get_common_proc_run_args())
    if proc.stderr:
        raise Exception(f'There is error in calling ffmpeg: {proc.stderr}')


def _get_common_proc_run_args() -> Dict[str, Any]:
    return dict(universal_newlines=True,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                check=True)


def extract_audio_segment(input_file_path: str, output_file_path: str,
                          start_time: Optional[str] = None, stop_time: Optional[str] = None):
    input_args = [
        'ffmpeg',
        '-v', 'error',
        '-nostdin',
        '-y'  # to overwrite the output file
    ]
    if start_time:
        input_args.extend(['-ss', start_time])
    input_args.extend(['-i', input_file_path])

    output_args = [
        '-c', 'copy'
    ]
    if stop_time:
        output_args.extend(['-to', stop_time])
    output_args.append(output_file_path)

    proc = subprocess.run(input_args + output_args, **_get_common_proc_run_args())
    if proc.stderr:
        raise Exception(f'There is error in calling ffmpeg: {proc.stderr}')
