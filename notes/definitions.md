# Definitions

## Thread

- New path of execution that can run concurrently with the main program

```python
thread=threading.Thread(target=self._load_loop,daemon=True)
```

- target -> what to do when the thread starts
  notice how the function is just passed, and not called (_load_loop()), since we don't want it to execute it while defining the thread
  daemon -> kill thread when main program ends


```
```
