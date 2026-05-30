import cv2
import threading
import queue
import time
from config import get_logger
from utils import perfmetrics

logger=get_logger(__name__)

class frameloader():
    def __init__(self,video_path,cam_id,queue_size):
        self.video_path=video_path
        self.cam_id=cam_id
        self.frame_queue=queue.Queue(maxsize=queue_size)
        self.running=False
        self.thread=None # Only create thread when needed
        self.metrics=perfmetrics(f"frameloader - {cam_id}")
    
    def start(self):
        if self.running:
            logger.warning(msg=f"{self.cam_id} already running")
            return
        running=True
        self.thread=threading.Thread(target=self._load_loop,daemon=True)
        self.thread.start()
        logger.info(f"frameloader started: {self.cam_id}")
    
    def _load_loop(self):
        capture=cv2.VideoCapture(str(self.video_path))
        if not capture.isOpened():
            logger.error(f"Failed to open {self.video_path}")
            self.running=False
        frame_index=0
        try:
            while self.running:
                read,frame=capture.read()
                if not read:
                    logger.info(f"{self.cam_id} reached end of clip")
                    break
                try:
                    self.frame_queue.put_nowait({
                            "cam_id":self.cam_id,
                            "frame_index":frame_index,
                            "image":frame,
                            "timestamp":time.time()
                        })
                    self.metrics.record_frame(0)
                    frame_index+=1
                except queue.Full:
                    self.metrics.record_drop()
                    logger.debug(f"{self.camera_id} dropped frame {frame_idx}")
        finally:
            capture.release()
            self.running=False

    def get_frame(self,timeout=1):
        try:
            return self.frame_queue.get(timeout=timeout)
        except queue.Empty:
            return None

    def stop(self):
        self.running=False
        if self.thread:
            self.thread.join(timeout=2)
        logger.info(f"frameloader stopped: {self.cam_id}")
        self.metrics.log_stats()


class multicamloader():
    def __init__(self,video_paths): # creates one frameloader for each camera
        self.loaders={
            cam_id:frameloader(path,cam_id) for cam_id,path in video_paths.items()
        }
        self.sync_metrics=perfmetrics("multicamsync")

    def start(self):
        for loader in self.loaders.values():
            loader.start()

    def get_frame_batch(self,timeout):
        batch={}
        for cam_id,loader in self.loaders.items():
            frame=loader.get_frame(timeout=timeout)
            if frame is None:
                logger.warning(f"timeout waiting for {cam_id}")
                return None
            batch[cam_id]=frame
        self.sync_metrics.record_frame(0)
        return batch

    def stop(self):
        for loader in self.loaders.values():
            loader.stop()

