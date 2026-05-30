# FRAME LOADING

To my understanding, this is what [frame_loader.py](../src/frame_loader.py) does:
- creates a class called frameloader which is an object basically reads a video path using a cv2 function (VideoCapture()), and returns frames according to the function call.
- There are two situations:
  1. Video files are in the hard drive, already pre-recorded (testing case; usually not the case in most real-life implementations)
  2. Live video feed from multiple cameras
- implementation v1 encompasses the former of the above points, where pre-recorded videos are fed to the system pipeline.
- now, one frameloader object is created for each of the camera inputs. these frameloaders create a [thread](/definitions.md#thread) which performs the queuing of frames without blocking inference.

