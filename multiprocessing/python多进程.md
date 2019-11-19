# 			python多进程

### 一、并发实现

```python
#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:Mei

import multiprocessing
from multiprocessing import Pool
from multiprocessing import Process
import os
import time

def f(x):
    return x*x

def info(title):
    print(title)
    print('module_name:',__name__)
    print('parent_process_id:',os.getppid())
    print('process id:',os.getpid())

def ff(name):
    info('function ff')
    print('hello',name)

#显示多进程并行工作状态
def work(x):
    time.sleep(5)
    print(time.ctime(),'这是子进程[{0}]  module_name:{1} parent_process_id:{2} process id:{3}'.format(x,__name__,os.getppid(),os.getpid()))

if __name__ == '__main__':
    '''
      with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
    
    info('main line')
    p=Process(target=ff,args=('mei',))
    p.start()
    print(p.name,p.pid)
    p.join()
    '''
    #产生多进程
    for i in range(5):
        p=Process(target=work,args=(i,))
        print('启动进程数:{0}'.format(i))
        p.start()
```

输出结果:

```bash
启动进程数:0
启动进程数:1
启动进程数:2
启动进程数:3
启动进程数:4
Tue Nov 19 12:18:15 2019 这是子进程[0]  module_name:__mp_main__ parent_process_id:4541 process id 4542
Tue Nov 19 12:18:15 2019 这是子进程[1]  module_name:__mp_main__ parent_process_id:4541 process id
4543
Tue Nov 19 12:18:15 2019 这是子进程[2]  module_name:__mp_main__ parent_process_id:4541 process id
4544
Tue Nov 19 12:18:15 2019 这是子进程[3]  module_name:__mp_main__ parent_process_id:4541 process id
4545
Tue Nov 19 12:18:15 2019 这是子进程[4]  module_name:__mp_main__ parent_process_id:4541 process id
4546

-- 多进程状态
[root@test1 ~]# ps -ef | grep mp
gdm       2153  2004  0 09:14 ?        00:00:00 /usr/libexec/ibus-engine-simple
root      4541  4326  1 12:23 pts/1    00:00:00 python mp.py
root      4542  4541  0 12:23 pts/1    00:00:00 python mp.py
root      4543  4541  0 12:23 pts/1    00:00:00 python mp.py
root      4544  4541  0 12:23 pts/1    00:00:00 python mp.py
root      4545  4541  0 12:23 pts/1    00:00:00 python mp.py
root      4546  4541  0 12:23 pts/1    00:00:00 python mp.py
```

### 二、进程间通信(IPC)

多进程支持两种进程间的通信通道 :Queues和Pipes

#### Queue模块

```python
#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:Mei
#父子进程之间的通信(没有涉及子进程间的通信)

from multiprocessing import Process,Queue
import os,time

def p_con(q,x):
    time.sleep(2)
    print(time.ctime(),'这是子进程[{0}]  module_name:{1} parent_process_id:{2} process id:{3}'.format(x, __name__, os.getppid(),os.getpid()))

def write(q):
    for x in range(0,5):
        q.put([x,'None','test'])

if __name__ == '__main__':
    q=Queue()
    write(q)
    for i in range(5):
        p=Process(target=p_con,args=(q,i))
        p.start()
        print(q.get(),q.qsize())
        p.join()
    # 队列消息读取完毕
    if(q.empty()):
        print('队列消息读取完毕')
    else:
        printf('还有队列消息未读取')
```

##### 实现效果

```
[0, 'None', 'test'] 4
Tue Nov 19 15:26:48 2019 这是子进程[0]  module_name:__mp_main__ parent_process_id:80388 process id:78172
[1, 'None', 'test'] 3
Tue Nov 19 15:26:51 2019 这是子进程[1]  module_name:__mp_main__ parent_process_id:80388 process id:66428
[2, 'None', 'test'] 2
Tue Nov 19 15:26:53 2019 这是子进程[2]  module_name:__mp_main__ parent_process_id:80388 process id:72412
[3, 'None', 'test'] 1
Tue Nov 19 15:26:55 2019 这是子进程[3]  module_name:__mp_main__ parent_process_id:80388 process id:80340
[4, 'None', 'test'] 0
Tue Nov 19 15:26:57 2019 这是子进程[4]  module_name:__mp_main__ parent_process_id:80388 process id:33812
队列消息读取完毕
```

##### 代码改进

```python
#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:Mei
#
from multiprocessing import Process,Queue
import os,time

def p_con(q,x):
    time.sleep(2)
    print(time.ctime(),'这是子进程[{0}]  module_name:{1} parent_process_id:{2} process id:{3}'.format(x, __name__, os.getppid(),os.getpid()))

def write(q):
    for x in range(0,2):
        q.put([x,'None','test'])

def read(q):
    print(q.get())

if __name__ == '__main__':
    q=Queue()
    #定义子进程:往消息队列中写数据
    p_writer=Process(target=write,args=(q,))
    p_writer.start()
    p_con(q,0)
    p_writer.join()
    for i in range(1,3):
        p=Process(target=read,args=(q,))
        p.start()
        p_con(q,i)
        print(q.qsize())
        p.join()
    # 队列消息读取完毕
    if(q.empty()):
        print('队列消息读取完毕')
    else:
        printf('还有队列消息未读取')
```

##### 改进后效果

```
Tue Nov 19 15:43:37 2019 这是子进程[0]  module_name:__main__ parent_process_id:25184 process id:81332
[0, 'None', 'test']
Tue Nov 19 15:43:39 2019 这是子进程[1]  module_name:__main__ parent_process_id:25184 process id:81332
1
[1, 'None', 'test']
Tue Nov 19 15:43:41 2019 这是子进程[2]  module_name:__main__ parent_process_id:25184 process id:81332
0
队列消息读取完毕
```

#### Pipe模块

```python
#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:Mei
#python中的pipe默认是半双工的
#父子进程或者子进程间可以是发送或者接收链接，但是同一时刻只能是其中的一种
#多个链接同时在同一端口写数据或者读数据会造成数据损坏

from multiprocessing import Process,Pipe
import os,time

#管道链接写数据
def pipe_send(conn):
    for x in range(0,4):
        conn.send([x,'None','IPC_pipe_test'])
    conn.close()
#管道链接读数据
def pipe_recev(conn):
    for x in range(0,2):
        print(conn.recv())
    conn.close()


if __name__ == '__main__':
    #获取管道链接对象
    parent_conn,chlid_conn=Pipe()
    p=Process(target=pipe_send,args=(chlid_conn,))
    #子进程消费
    p1 = Process(target=pipe_recev, args=(parent_conn,))
    p.start()
    p1.start()
    p.join()
    p1.join()
    #父进程消费
    pipe_recev(parent_conn)
```

##### 实现效果

```
[0, 'None', 'IPC_pipe_test']
[1, 'None', 'IPC_pipe_test']
[2, 'None', 'IPC_pipe_test']
[3, 'None', 'IPC_pipe_test']
```

### 三、进程同步

```python
#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:Mei
#确保并发进程不会产生混乱(同时读写数据时，可能造成数据混乱，需要使用锁来控制并发)

from multiprocessing import Process,Pipe,Lock
import os,time

def con_control(lock,x):
    lock.acquire()
    try:
        print('test',x)
    finally:
        lock.release()

if __name__ == '__main__':
    lock=Lock()
    for i in range(10):
        p=Process(target=con_control,args=(lock,i))
        p.start()
```

### 四、进程间共享状态

#### 共享内存

数据可以使用Value或者Array存储在共享内存映射中

```python
#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:Mei
#共享内存
#Value(typecode_or_type, *args, lock=True)可以看到其实也加了锁

from multiprocessing import Process,Value,Array
import os,time

def shared_buffer(n,a):
    n.value=3.1415926
    for i in range(len(a)):
        a[i]=-a[i]

if __name__ == '__main__':
    num=Value('d',0.0)
    num.value=1.1
    arr=Array('i',range(10))

    p=Process(target=shared_buffer,args=(num,arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
```

##### 实现效果

```
3.1415926
[0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
```

#### 服务器进程

服务器进程管理器比使用共享内存对象更灵活，因为它们可以支持任意对象类型。 此外，单个管理器可以通过网络由不同计算机上的进程共享。 然而，它们比使用共享内存要慢。 

```python
#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:Mei
#服务器进程管理器


from multiprocessing import Process, Manager

def f(d,l):
    d[1] = '1'
    d[2] = 2
    d[3] = None
    l.reverse()

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))

        p = Process(target=f, args=(d, l))
        p.start()
        p.join() #等待进程结束后往下执行
        print (d,'\n',l[:])
```

### 五、工作进程池pool

```python
from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return x*x

if __name__ == '__main__':
    # start 4 worker processes
    with Pool(processes=4) as pool:
        print(pool.map(f, range(10)))
        for i in pool.imap_unordered(f, range(10)):
            print(i)
        res = pool.apply_async(f, (20,))      # runs in *only* one process
        print(res.get(timeout=1))             # prints "400"

        res = pool.apply_async(os.getpid, ()) # runs in *only* one process
        print(res.get(timeout=1))             # prints the PID of that process

        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        print([res.get(timeout=1) for res in multiple_results])

        res = pool.apply_async(time.sleep, (10,))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")

        print("For the moment, the pool remains available for more work")

    # exiting the 'with'-block has stopped the pool
    print("Now the pool is closed and no longer available")
    
    
#pool使用案例(缓存进程连接)
#!/usr/bin/python
# -*- coding:utf-8 -*-
# Author:Mei

import multiprocessing
import os,time,random

def run_time(x):
    start_time = time.time()
    time.sleep(random.random())
    print(x,os.getpid(),os.getppid(),time.time()-start_time)


if __name__ == '__main__':
    pool = multiprocessing.Pool(4)
    for i in range(10):
        pool.apply_async(func=run_time,args=(i,))
    pool.close()
    pool.join()
    print("结束标志")
```

