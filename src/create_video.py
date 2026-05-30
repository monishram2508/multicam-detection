from os.path import exists
import cv2
from cv2.gapi import video
import numpy as np
from pathlib import Path
from config import data_path,get_logger

logger = get_logger(__name__)

def create_simple_vid(filename,duration=10,fps=30):
    w,h=640,480
    video_path=data_path/"videos"/filename
    video_path.parent.mkdir(exist_ok=True)

    fourcc=cv2.VideoWriter_fourcc(*"mp4v")
    out=cv2.VideoWriter(str(video_path),fourcc,fps,(w,h))
    total_frames=duration*fps
    logger.info(f"Creating {filename} ({total_frames} frames)...")
    for index in range(total_frames):
        frame=np.ones((h,w,3),dtype=np.uint8)*200
        x=int((index%total_frames)/total_frames*w)
        cv2.rectangle(frame,(x,100),(x+50,150),(0,255,0),-1)
        cv2.putText(frame, f"Camera: {filename[:-4]}", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),2)
        cv2.putText(frame, f"Frame: {index}", (10, 70),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0),2)
        out.write(frame)
    out.release()
    logger.info(f"{filename} created, ({video_path.stat().st_size/1e6:.2f} MB)")


def main():
    create_simple_vid("cam_1.mp4")
    create_simple_vid("cam_2.mp4")
    logger.info(f"\n Test videos ready at data/videos/")

if __name__=="__main__":
    main()
