import logging as lg
from pathlib import Path
from ultralytics import YOLO

root=Path(__file__).parent.parent
data_path=root/"data"
models_path=root/"models"
logs_path=root/"logs"
outputs_path=root/"outputs"
for path in [data_path,models_path,logs_path,outputs_path]:
    path.mkdir(parents=True,exist_ok=True)

model_name="yolov8n"
conf_thresh=0.5
iou_thresh=0.45

input_size=640
batch_size=1
max_threads=2

target_fps=10
target_latency=100

log_level=lg.INFO
log_format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"

def get_logger(name):
    logger=lg.getLogger(name)
    logger.setLevel(log_level)
    
    fh=lg.FileHandler(logs_path/f'{name}.log')
    fh.setLevel(log_level)
    fh.setFormatter(lg.Formatter(log_format))

    ch=lg.StreamHandler()
    ch.setLevel(log_level)
    ch.setFormatter(lg.Formatter(log_format))

    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger
