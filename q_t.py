'''一个计时器'''
from queue import Queue
from threading import Thread
import time
def accuracy_sleep(next_time,accuracy):
    delta_time=next_time-time.time()
    if delta_time>accuracy:
        sleep_time=delta_time-accuracy
        time.sleep(sleep_time)
    elif delta_time<-accuracy:
        raise RuntimeError('time_butler: outtime error:'+str(abs(delta_time)))
        return
    while(time.time()<next_time):
        pass
    now_time=time.time()
    if now_time-next_time>accuracy:
        raise RuntimeError('time_butler: outtime error:'+str(abs(now_time-next_time)))
        return