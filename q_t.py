'''一个计时器'''

from concurrent.futures import ThreadPoolExecutor
from itertools import cycle
from threading import Thread
import time
def fun_time_butler(start_time,accuracy, func,args=None):
    #print('fun_time_butler::'+start_time)
    delta_time=start_time-time.time()
    if delta_time>0:
        sleep_time=delta_time-3*accuracy
        time.sleep(sleep_time)
        while(time.time()<start_time):
            pass
        now_time=time.time()
        if abs(now_time-start_time)>accuracy:
            raise RuntimeError('time_butler: outtime error:'+str(abs(now_time-start_time)))
            return
    elif delta_time<-accuracy:
        raise RuntimeError('time_butler: outtime error:'+str(abs(delta_time)))
        return
    func(*args)
class time_butler(Thread):
    def __init__(self,start_time,accuracy, func,args=None):
        Thread.__init__(self)
        self.__start_time=start_time
        self.__accuracy=accuracy
        self.__func = func
        self.__args = args
    def run(self):
        fun_time_butler(self.__start_time,self.__accuracy,self.__func,self.__args)
class running_by_cycle(Thread):
    def __init__(self,start_time,cycle,running_time,accuracy,func,args=None) -> None:
        self.__start_time=start_time
        self.__cycle=cycle
        self.__running_time=running_time
        self.__accuracy=accuracy
        self.__func=func
        self.__args=args