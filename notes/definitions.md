# Definitions

## Thread

- New path of execution that can run concurrently with the main program

```python
thread=threading.Thread(target=self._load_loop,daemon=True)
```

- target -> what to do when the thread starts
  (notice how the function is just passed, and not called (_load_loop()), since we don't want it to execute it while defining the thread)
- daemon -> kill thread when main program ends

## Timeout

- Maximum duration in seconds to wait before giving up
- For example:
```python
get_frame_batch(self,timeout)
```

will loop through each camera and get a frame from each one; if any camera does NOT return a frame within *timeout* seconds, the whole batch will be dropped.

## ONNX

- Open Neural Network Exchange
- PyTorch carries all the training infrastructure that we don't need during inference; the problem arises when we train a model in PyTorch and deploy somewhere else, resulting in a crash if the system doesn't have the hardware power for running the required framework.
- ONNX is a standardized model format that converts the model weights (filters, biases, layer weights), operator implementation (convolution, matrix multiplication, normalization, activation, etc.), and tensor execution engine, into a universal format for all systems to access.
- Converts a typical PyTorch model into a standardized computation graph, operator descriptions, and serialized weights.

## Codec

- Software that compresses/decompresses video.
- Fourcc - four character code used to identify a codec. (mp4v, XVID, MJPG, H264, etc.)
