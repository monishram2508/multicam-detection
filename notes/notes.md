# NOTES 

## Frame Loading Process:

To my understanding, this is what [frame_loader.py](../src/frame_loader.py) does:
- Creates a class called frameloader which is an object basically reads a video path using a cv2 function (VideoCapture()), and returns frames according to the function call.
- There are two situations:
  1. Video files are in the hard drive, already pre-recorded (testing case; usually not the case in most real-life implementations)
  2. Live video feed from multiple cameras
- Implementation v1 encompasses the former of the above points, where pre-recorded videos are fed to the system pipeline.
- One frameloader object is created for each of the camera inputs. These frameloaders create a [thread](definitions.md#thread) which performs the queuing of frames without blocking inference.
- Multiple frameloader threads can be started to read frames from different video sources simultaneously.
- The multicamloader class accomodates multiple cameras, by just including multiple frameloader objects, and reading each camera sequentially, adding it to an empty dictionary if and only if all the frames are within the [timeout](definitions.md#timeout) duration of each other.

Now, this is not the case for a live feed scenario:

- If we loop through the frames sequentially, there will be timing issues in the case of actual camera-sourced video feeds. Since video files are processed and have technically the exact same FPS, the frames come in at zero offset.
- To solve this problem, we use a timestamp validation technique, i.e. if the frames' timestamps are within a certain threshold (e.g. 10ms), the batch is taken, else, dropped.

## Detection Pipeline

- We have a yolov8detector class, which opens the ONNX model using CPU providers. This object has the following methods:
1. preprocess() - carries out resizing, normalization (0-255 to 0-1), color format conversion (BGR to RGB), HWC to CHW conversion, and addition of batch dimension (CHW to BCHW)
2. _postprocess() - parses raw ONNX model output and extracts detections. 
  1. ONNX outputs shape (1,8400,84) which needs transposing. (1,8400,84) is a tensor shape of the format (batch dimension,number of predictions,values per prediction). So, this is the dimension of the output array.
  2. Looping through all 8400 predictions:
  - the first four elements of each subarray are the coordinates x,y,w, and h, where (x,y) represent the center of the bounding box and (w,h) represent the width and the height. 
  - output[4] gives the confidence of the model for that particular prediction.
  - output[5:] represent 80 COCO (common objects in context) class probabilities.
  3. The highest probable class is then found, and the final confidence is returned as the product of the class confidence and the detection confidence. 
  4. The detected object is recorded if the confidence exceeds a certain threshold.

