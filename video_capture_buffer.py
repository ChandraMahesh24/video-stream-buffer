import cv2
import threading
import time
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class VideoCaptureBuffer:
    """
    Thread-safe video capture buffer that continuously reads frames
    from a video source (file, RTSP stream, webcam) in a background thread.

    Supports:
    - Real-time playback with delay adjustment for video files.
    - Automatic reconnection for RTSP streams or video files reaching EOF.
    """

    def __init__(self, video_source):
        """
        Initialize the video capture buffer.

        Args:
            video_source (str or int): Path to video file, RTSP URL, or camera index.
        """
        self.video_source = video_source
        self.cap = cv2.VideoCapture(video_source)
        self.buffer_frame = None
        self.stopped = False
        self.lock = threading.Lock()

        # Detect if source is RTSP stream
        self.is_rtsp = isinstance(video_source, str) and video_source.startswith("rtsp")
        # Detect if source is a video file by file extension
        self.is_file = isinstance(video_source, str) and Path(video_source).suffix.lower() in ['.mp4', '.avi', '.mov', '.mkv']

        if not self.cap.isOpened():
            logger.error(f"Unable to open video source: {video_source}")
            raise ValueError(f"Cannot open source: {video_source}")

        # Start background thread to read frames continuously
        self.thread = threading.Thread(target=self.update_frames, daemon=True)
        self.thread.start()

    def update_frames(self):
        """
        Background thread function to read frames continuously and store
        the latest frame in a buffer.
        """
        while not self.stopped:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    self.buffer_frame = frame

                # Simulate real-time playback delay for video files
                if self.is_file:
                    fps = self.cap.get(cv2.CAP_PROP_FPS)
                    time.sleep(0.60 / fps if fps > 0 else 0.01)  # Slightly slower than FPS
                else:
                    time.sleep(0.01)  # Short delay for RTSP or webcam
            else:
                # Handle errors or end-of-stream based on source type
                if self.is_rtsp:
                    logger.error("Failed to capture frame from RTSP, retrying...")
                    time.sleep(1)
                elif self.is_file:
                    logger.warning("End of video file reached or read failed. Reinitializing...")
                    self.cap.release()
                    self.cap = cv2.VideoCapture(self.video_source)
                    time.sleep(1)
                else:
                    logger.error("Unknown error reading frame.")
                    time.sleep(1)

    def read(self):
        """
        Retrieve the latest buffered frame.

        Returns:
            (bool, frame): Tuple indicating if frame is available and the frame itself.
        """
        with self.lock:
            frame = self.buffer_frame
        return frame is not None, frame

    def release(self):
        """
        Stop the background thread and release the video capture resource.
        """
        self.stopped = True
        if self.thread.is_alive():
            self.thread.join()
        if self.cap:
            self.cap.release()
