# FRAME LOADING

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


