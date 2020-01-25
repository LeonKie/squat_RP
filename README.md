
# Steps to get it running
```
python3 main_loop.py

```

# Introduction

We are using a model for detecting the different poses (Teachable Machine) and running it in a browser. The stream of data is transfered over a localhost

The ```main_loop.py``` script is connecting to the ```localhost:2601``` and is detecting the squats.

After 10 squats the the raspberry outputs a signal to pin ```GPIOD```

You can trigger any event you want. In our case we decided to trigger a coffee Machine, rewarding you with a free coffee after a small work out.


## what requirements you need to run the script??

### hardware
-  raspberry pie
-  raspberry pie camera
- ...
### software
- python3
- tensorflow