'''一个计时器'''
from abc import ABC, abstractmethod
import queue
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
#in abstract
class Thread_WAR(ABC,Thread):
    '''一个用于为线程提供参数与返回的类
    '''
    def __init__(self,sizeof_args,sizeof_res):
        Thread.__init__(self)
        self.__args=queue.Queue(sizeof_args) if sizeof_args>0 else None
        self.__res=queue.Queue(sizeof_res) if sizeof_res>0 else None
#public_method
    def start(self) -> None:
        if self.__args!=None and self.__args.empty():
            raise RuntimeError('start(): args queue is empty')
            return
        else:
            Thread.start(self)  
    # def get_args(self):
    #     return self.__args
    def get_res(self):
        if self.__res.full():
            return self.__res
        else:
            raise RuntimeError('get_res(): res queue is not full')
    def res_qsize(self):
        return self.__res.qsize()
    def add_args(self,arg,block=True,timeout=None):
        self.__args.put(arg,block,timeout)
#protected_method
    def _add_res(self,res,bool=True,timeout=None):
        self.__res.put(res,bool,timeout)
    def _res_full(self):
        return self.__res.full()
    def _res_empty(self):
        return self.__res.empty()

    def _args_exist(self):
        return self.__args!=None
    def _args_full(self):
        return self.__args.full()
    def _args_get(self,block=True,timeout=None):
        return self.__args.get(block,timeout)
    def _args_qsize(self):
        return self.__args.qsize()
#abstract_method
    @abstractmethod
    def set_args(self):
        pass
#the of class Thread_WAR

class Time_Butler(Thread_WAR):
    def __init__(self,end_time,cycle,sizeof_args,sizeof_res):
        Thread.__init__(self)
        Thread_WAR.__init__(self,sizeof_args,sizeof_res)
        self.__end_time=end_time
        self.__cycle=cycle
        self.__count=0
#public_method
    def run(self):
        if self._args_exist():
            if not self._args_full():
                raise RuntimeError('time_butler: args is empty')
                return
        start_time=time.time()
        next_time=start_time+self.__cycle
        end_time=self.__end_time+start_time
        while next_time<=end_time:
            self.fuc()
            sleep_time=next_time-time.time()
            time.sleep(sleep_time if sleep_time>0 else 0)
            next_time+=self.__cycle
            self.__count+=1
    def get_count(self):
        return self.__count
    def set_args(self):
        pass
#protected_method
    @abstractmethod
    def fuc(self):
        pass
#the end of class Time_Butler


#in real
class Study_Stock_Data(Thread_WAR):
    def set_args(self,args):
        for i in range(args.qsize()):
            self.add_args(args.get())
    def run(self):
        self.study_stock_data()
    def __init__(self, sizeof_args):
        Thread_WAR.__init__(self,sizeof_args, 0)
        self.study_stock_data=self.test
    #具体各数据处理的方法
    def test(self):
        for i in range(self._args_qsize()):
            print(self._args_get())

#the end of class Study_Stock_Data

import requests
class Get_Stock_Data(Time_Butler):
    #以下实现抽象的获取数据的过程
    def __init__(self,end_time,cycle,sizeof_res,stock_code):
        Time_Butler.__init__(self,end_time,cycle,0,sizeof_res)
        self.__stock_code=stock_code
        #通过下一行更改的数据获取方法
        self.__get_data_methods=self.test
    def fuc(self):
        if self._res_full():
            a=Study_Stock_Data(self.res_qsize())
            a.set_args(self.get_res())
            a.start()
        text=self.__get_data_methods()
        self._add_res(text)
#具体各网站数据获取的方法
    def get_tencent_stock_data(self):
        page=requests.get('http://qt.gtimg.cn/q=s_sh'+str(self.__stock_code))
        text=page.text
        return text
    def test(self):
        print(time.time())
        return  self.get_tencent_stock_data()

#the end of class Get_Stock_Data