
class SystemCall(object):
    '''
    模拟系统调用
    '''
    def __init__(self):
        self.task = None
        self.scheduler = None

    def handler(self):
        '''
        当某个task调用了系统调用，调度器会执行该系统调用的handler方法
        :return:
        '''
        pass

class GetTid(SystemCall):
    '''
    获取该task的tid
    '''

    def __init__(self):
        super().__init__()

    def handler(self):
        self.task.senval = self.task.tid
        self.scheduler.schedule(self.task)

class NewTask(SystemCall):
    '''
    新建一个task
    '''

    def __init__(self,target):
        super().__init__()
        self.target = target

    def handler(self):
        self.task.sendval = self.scheduler.new(self.target)
        self.scheduler.schedule(self.task)

class KillTask(SystemCall):
    '''
    结束某个task的执行
    '''

    def __init__(self,kill_tid):
        super().__init__()
        self.kill_tid = kill_tid

    def handler(self):
        self.task.sendval = self.scheduler.exit(self.kill_tid)
        self.scheduler.schedule(self.task)

class WaitFor(SystemCall):
    '''
    等待某个task执行完成后才执行
    '''

    def __init__(self,tid):
        super().__init__()
        self.tid = tid

    def handler(self):
        self.scheduler.wait_for_task(self.tid, self.task)

class WaitRead(SystemCall):
    '''
    等待某个文件描述符可读后才执行
    '''

    def __init__(self,fd):
        super().__init__()
        self.fd = fd.fileno() or fd

    def handler(self):
        self.scheduler.wait_for_read(self.fd, self.task)

class WaitWrite(SystemCall):
    '''
        等待某个文件描述符可写后才执行
    '''

    def __init__(self,fd):
        super().__init__()
        self.fd = fd.fileno() or fd

    def handler(self):
        self.scheduler.wait_for_write(self.fd, self.task)

