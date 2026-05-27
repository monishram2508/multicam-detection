import time
from ultralytics import YOLO
from pathlib import Path
import numpy as np
import logging as lg
import onnxruntime as rt
import shutil

root=Path(__file__).parent.parent

lg.basicConfig(level=lg.INFO)
logger=lg.getLogger(__name__)

lg.info("step 1: get yolov8 and export to onnx")
model=YOLO("../models/yolov8n.pt")
exported_path=model.export(format="onnx",opset=20)
onnx_path=root/"models"/"yolov8n.onnx"
shutil.move(exported_path,onnx_path)

lg.info(f"onnx path:{onnx_path}")
lg.info(f"file size:{onnx_path.stat().st_size/1e6:.2f} MB")

lg.info("step 2: benchmarking onnx runtime (default)")

sesh=rt.InferenceSession(str(onnx_path),providers=['CPUExecutionProvider']) #onnx model to executable inference session
# run inference on cpu
# other providers:
# CUDAExecutionProvider
# TensorRTExecutionProvider

dummy=np.random.randn(1,3,640,640).astype(np.float32)
# convert numbers to 32 bit floating point
_=sesh.run(None,{"images":dummy}) # first run
# None -> return all outputs

times=[]
for i in range(10):
    st=time.perf_counter()
    _=sesh.run(None,{'images':dummy})
    runtime=time.perf_counter()-st
    times.append(runtime*1000)
onnx_time=sum(times)/len(times)

lg.info(f"onnx avg time per inference = {onnx_time:.2f} ms/frame and fps={1000/onnx_time:.1f}")

lg.info("step 3: benchmarking pytorch runtime")
dummy=np.zeros((640,640,3),dtype=np.uint8)
_=model(dummy,verbose=False)

times=[]
for i in range(10):
    st=time.perf_counter()
    _=model(dummy,verbose=False)
    runtime=time.perf_counter()-st
    times.append(runtime*1000)
pt_time=sum(times)/len(times)

lg.info(f"pytorch avg time per inference = {pt_time:.2f} ms/frame and fps={1000/pt_time:.1f}")

lg.info("step 4: onnx quantization to int8")
dummy = np.random.randn(1,3,640,640).astype(np.float32)
try:
    from onnxruntime.quantization import quantize_dynamic,QuantType
    quant_path=Path(root/"models"/"yolov8n_int8.onnx")
    quant_path.parent.mkdir(exist_ok=True)
    quantize_dynamic(
        str(onnx_path),
        str(quant_path),
        weight_type=QuantType.QUInt8
    )
    lg.info(f"quantized model: {quant_path}")
    lg.info(f"file size = {quant_path.stat().st_size/1e6:.2f} MB")

    sess_q = rt.InferenceSession(str(quant_path), providers=['CPUExecutionProvider'])
    times=[]
    for i in range(10):
        start = time.perf_counter()
        _ = sess_q.run(None, {'images': dummy})
        times.append((time.perf_counter() - start) * 1000)
    
    q_time=sum(times)/len(times)
    lg.info(f"quantized avg time per inference = {q_time:.2f} ms/frame and fps={1000/q_time:.1f}")
except Exception as e:
    lg.exception(e)
