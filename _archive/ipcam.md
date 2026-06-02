# Record Video from IP Camera Using FFmpeg

> **Archived** — Instructions for recording an RTSP stream from an IP camera using FFmpeg.

## Record RTSP Stream to Segmented MP4 Files

The command below connects to an RTSP stream over TCP and saves the output as 60-second MP4 segments:

```bash
ffmpeg \
    -rtsp_transport tcp \
    -i rtsp://admin:888888@192.168.88.254:10554/tcp/av0_0 \
    -flags +global_header \
    -f segment \
    -segment_time 60 \
    -segment_format mp4 \
    -segment_format_options movflags=+faststart \
    -reset_timestamps 1 \
    "out%03d.mp4"
```

### Flag Explanation

| Flag                                          | Description                                         |
| --------------------------------------------- | --------------------------------------------------- |
| `-rtsp_transport tcp`                         | Use TCP for RTSP transport (more reliable than UDP) |
| `-flags +global_header`                       | Write global headers required for segmented output  |
| `-f segment`                                  | Use the segment muxer to split output into files    |
| `-segment_time 60`                            | Create a new segment every 60 seconds               |
| `-segment_format mp4`                         | Output format for each segment                      |
| `-segment_format_options movflags=+faststart` | Move MP4 index to the beginning for fast playback   |
| `-reset_timestamps 1`                         | Reset timestamps at the start of each segment       |

## VStarCam IP Camera

Default connection details for the VStarCam camera model:

| Field    | Value                                                  |
| -------- | ------------------------------------------------------ |
| RTSP URL | `rtsp://admin:888888@192.168.88.254:10554/tcp/av0_0`   |
| Username | `admin`                                                |
| Password | `888888`                                               |

> **Warning:** Change the default credentials immediately after setup to avoid unauthorized access.

## Test Stream Playback

```bash
ffplay rtsp://admin:888888@192.168.88.254:10554/tcp/av0_0
```

## References

- [FFmpeg Documentation](https://ffmpeg.org/documentation.html)
- [FFmpeg Segment Muxer](https://ffmpeg.org/ffmpeg-formats.html#segment_002c-stream_005fsegment_002c-ssegment)
