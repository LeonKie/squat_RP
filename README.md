
# Steps to get it running
```
python3 main_loop.py
```

# Introduction

I am using a *face-detection* model to detect the position of any face. When the detected face moves blow a certain threshold in the video frame a **squard** is detected and a counter keeps track.

The ```main_loop.py``` script is connecting to the Vision AI Camera and uses *Face-detection* to find any faces in the video. 

After 5 squats the the raspberry outputs a signal to pin ```GPIOD```

You can trigger any event you want. In our case we decided to trigger a coffee machine, rewarding you with a free coffee after a small work out.


## what requirements you need to run the script??

### hardware
-  AIY Vision Kit
### software
- python3