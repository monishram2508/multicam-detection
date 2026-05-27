import time
from config import get_logger
from contextlib import contextmanager

logger=get_logger(__name__)

@contextmanager
def timer(name):
    start=time.perf_counter()
    try:
        yield
    finally:
        runtime=(time.perf_counter()-start)*1000
        logger.info(f"[TIMER] - {name}:{runtime:.2f} ms")


# creates a timing contextmanager which we use as below:
# with timer("inference"):
#   model(dummy)
#
# output: [TIMER] - inference: 42.32 ms 

class perfmetrics:
    def __init__(self,name):
        self.name=name
        self.frame_count=0
        self.dropped_frames=0
        self.times=[]
        self.st_time=time.time()

    def record_frame(self,latency):
        "record a frame's latency"
        self.frame_count+=1
        self.times.append(latency)

    def record_drop(self):
        self.dropped_frames+=1

    def get_stats(self):
        if not self.times:
            return {}
        runtime=time.time()-self.st_time
        avg_latency=sum(self.times)/len(self.times)
        fps=self.frame_count/runtime if runtime>0 else 0
        return {
            "name":self.name,
            "fps":round(fps,2),
            "avg_latency":round(avg_latency,2),
            "frames_processed":self.frame_count,
            "frames_dropped":self.dropped_frames,
            "elapsed":round(runtime,1)
        }

    def log_stats(self):
        stats=self.get_stats()
        logger.info(f"[METRICS] - {self.name}:{stats}")

