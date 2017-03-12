
import queue
import select
import socket
import types
from system_call import SystemCall, GetTid, NewTask, KillTask, WaitFor, WaitRead

class Task(object):
    '''
    the wrapper of coroutine
    '''
    tid = 0
    def __init__(self,target):
        Task.tid += 1
        self.tid = Task.tid
        self.target = target
        self.sendval = None
        self.stack = []

    def run(self):
        return self.target.send(self.sendval)




class Scheduler(object):
    '''
    模拟的调度程序
    '''

    def __init__(self):
        self.task_map = {}
        self.ready = queue.Queue()
        self.wait_exit = {}
        self.read_waiting = {}
        self.write_waiting = {}

    def schedule(self,task):
        '''
        将某个task加入到调度序列中
        :param task:
        :return:
        '''
        self.ready.put(task)

    def new(self,target):
        '''
        新建一个task，并将其添加至调度序列中
        :param target:  一个generator对象
        :return:  新建task的tid
        '''
        task = Task(target)
        tid = task.tid
        self.task_map[tid] = task
        self.schedule(task)
        return tid

    def wait_for_task(self,wait_for_tid,waiting_task):
        '''
        设置一个task需要等待某个task结束后才能执行
        :param wait_for_tid:  后者的tid
        :param waiting_task:  前者
        :return:  设置是否成功
        '''
        if wait_for_tid in self.task_map:
            self.wait_exit.setdefault(wait_for_tid, []).append(waiting_task)
            return True
        return False

    def wait_for_read(self,fd,task):
        '''
        设置一个task需要等文件描述符可读才能执行
        :param fd:  文件描述符的fileno()
        :param task:  task对象
        :return:
        '''
        self.read_waiting[fd] = task

    def wait_for_write(self,fd,task):
        '''
        设置一个task需要等待文件描述符可写才能执行
        :param fd:  文件描述符的fileno()
        :param task:  task对象
        :return:
        '''
        self.write_waiting[fd] = task

    def io_loop(self, timeout):
        '''
        检测所有注册的文件描述符，如果某个文件描述符就绪后就将对应的task假如调度序列
        :param timeout:  设置select的timeout
        :return:
        '''
        if self.read_waiting or self.write_waiting:
            r, w, e = select.select(self.read_waiting, self.write_waiting, [], timeout)
            for fd in r:
                self.schedule(self.read_waiting.pop(fd))
            for fd in w:
                self.schedule(self.write_waiting.pop(fd))

    def task_loop(self):
        while True:
            if self.task_map:
                self.io_loop(0)
            else:
                self.io_loop(None)
            yield

    def exit(self,tid):
        '''
        结束某个task的执行
        :param tid:  想要结束的task的tid
        :return:
        '''
        task = self.task_map.get(tid,None)
        if task:
            task.target.close()
            del self.task_map[tid]
            for task in self.wait_exit.pop(tid,[]):
                self.schedule(task)
            return True

    def main_loop(self):
        '''
        一个loop，不断的从调度序列中取出task并执行
        :return:
        '''
        self.new(self.task_loop())
        while True:
            task = self.ready.get()
            try:
                result = task.run()
                if isinstance(result,SystemCall):
                    result.task = task
                    result.scheduler = self
                    result.handler()
                    continue
            except StopIteration:
                self.exit(task.tid)
                continue
            self.schedule(task)











