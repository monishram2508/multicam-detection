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
```
```
