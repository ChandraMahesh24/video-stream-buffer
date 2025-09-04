# video-stream-buffer
A thread-safe Python video capture buffer that efficiently reads frames from video files, RTSP streams, or webcams using OpenCV. It uses a background thread to continuously fetch frames, providing smoother real-time playback and reconnection logic for stream interruptions       



# Video Stream Buffer

A thread-safe video capture buffer for OpenCV that continuously reads frames
from video files, RTSP streams, or webcams in a background thread. This helps
achieve smoother frame capture and real-time playback in applications that
consume video streams.

## Features

- Supports video files (`.mp4`, `.avi`, `.mov`, `.mkv`), RTSP streams, and webcams.
- Background thread fetches frames continuously to avoid lag.
- Automatic reconnection on stream interruptions or end-of-file for videos.
- Thread-safe access to the latest frame buffer.
- Simple API: `read()` and `release()`.

## Installation

This module requires:

- Python 3.6+
- OpenCV (`opencv-python`)
- `threading`, `time`, `pathlib`, `logging` (standard libs)

pip install opencv-pytho:

```bash

Using with RTSP Stream:

import cv2
from video_capture_buffer import VideoCaptureBuffer    #Import and Initialize

rtsp_url = "rtsp://username:password@ip_address:port/stream"     #Use with RTSP Stream
vcb = VideoCaptureBuffer(rtsp_url)

while True:
    success, frame = vcb.read()
    if success:
        cv2.imshow("Video Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vcb.release()
cv2.destroyAllWindows()


