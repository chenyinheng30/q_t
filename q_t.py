'''一个计时器'''
from queue import Queue
from threading import Thread
import time
def fun_time_butler(start_time,accuracy, func,args=None):
    delta_time=start_time-time.time()
    if delta_time>3*accuracy:
        sleep_time=delta_time-3*accuracy
        time.sleep(sleep_time)
    elif delta_time<-accuracy:
        raise RuntimeError('time_butler: outtime error:'+str(abs(delta_time)))
        return
    while(time.time()<start_time):
        pass
    # now_time=time.time()
    # if abs(now_time-start_time)>accuracy:
    #     raise RuntimeError('time_butler: outtime error:'+str(abs(now_time-start_time)))
    #     return
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
    def __init__(self,start_time,cycle,running_time,accuracy,func,args):
        Thread.__init__(self)
        self.__tasks_queue=Queue(maxsize=running_time/cycle)
        self.__result=Queue(maxsize=running_time/cycle)
        self.__is_result_ready=False
        self.__start_time=start_time
        for t in range(0,running_time,cycle):
            task=time_butler(start_time+t,accuracy,func,(self,)+args)
            self.__tasks_queue.put(task)
    def run(self):
        self.__is_result_ready=True
        for i in range(self.__tasks_queue.qsize()):
            task=self.__tasks_queue.get()
            task.start()
            task.join()
    def get_result(self):
        if self.__is_result_ready:
            return self.__result
        else:
            raise RuntimeError('running_by_cycle: result is not ready')
            return