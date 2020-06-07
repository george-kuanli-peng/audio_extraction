# Contributing Notes

## Useful commands

To view basic media information of a file:

```bash
mediainfo source_file.mkv
```

or to use ffprobe that comes with ffmpeg:

```bash
ffprobe source_file.mkv
```

To scan internal streams of a file for errors:

```bash
ffmpeg -v error -i source_file.mkv -f null - 2>error.log
```

If there are errors found, `error.log` may contain error messages such as

```
[matroska,webm @ 0x55d02d3088c0] Read error
```

The same information may also be captured in standard error stream by converting media files through ffmpeg, but remember to use verbose level no less than `error` (the default settings are ok) commandline option.

`ffmpeg` seems to exit with 0 even on errors, so to reliable detect errors in file, check wheter there are any contents in standard error.

To extra audio without re-encoding:

```bash
ffmpeg -i source.mkv -vn -acodec copy output.aac
```

it assumes the audio stream contained in the source video files is encoded by AAC.

## References

1. [using ffmpeg to extract audio from video files](https://gist.github.com/protrolium/e0dbd4bb0f1a396fcb55)