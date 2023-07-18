# Twisted

## 基本概况

官网地址：https://twistedmatrix.com/trac/

github：https://github.com/twisted/twisted/

API：https://twistedmatrix.com/documents/current/api/twisted.html

Twisted 是Python 基于事件驱动实现的高性能异步网络编程框架，诞生于2000年初，支持Python2.7和3.3+。Twisted 是建立在 deferred object （通过异步架构实现的机制）之上。Twisted和django/ flask等web框架的定位不同，在开发中Twisted不适合编写常规的web应用，而是常用于物联网、游戏、爬虫甚至VoIP(基于IP的语音传输技术)等底层网络应用，其中像Scrapy和firefly等框架底层就是基于Twisted封装的。

Twisted利用不同的底层技术实现了高效能通信，支持很多协议，包括传输层的TCP、UDP、TLS，以及应用层的HTTP、FTP等。对所有这些协议，Twisted提供了客户端和服务器方面的开发工具，如：

-   twisted.web：HTTP客户端和服务端，HTML模板，和一个WSGI服务器
-   twisted.conch：基于SSHv2和Telnet协议的的客户端，服务器和终端模拟器
-   twisted.words：基于IRC，XMPP和其他IM协议的客户端和服务器
-   twisted.mail：基于IMAPv4，POP3，SMTP的客户端和服务器
-   twisted.positioning：和NMEA（国际海上电子协会）兼容的GPS接收者通信的工具
-   twisted.names：DNS客户端和工具可用于构建自己的DNS服务器
-   twisted.trial：和基于Twisted的代码高度整合的单元测试框架

twisted支持所有主流的事件轮询机制：select（所有平台）、poll（大部分POSIX平台）、epoll（Linux）、kqueue（FreeBSD,OSX）、OCP（Windows)和各种GUI事件轮询机制（GTK+2/3、QT、wxWidgets）。还提供了丰富的 特性来支持异步编程，如**Defer**、**Threading**等。

## 安装与版本

目前最新版本是21.x.x版本，但是我们接下来要使用的是firefly游戏引擎，所以后面安装的版本是19.x.x版本。

现在我们学习，直接用最新即可。

```bash
mkvirtualenv twdemo
pip install twisted
```



## 事件管理器(reactor)

reactor是学习Twisted框架的最核心概念。我们称之为反应堆[其实就是一个死循环，但是如果叫死循环就太low了]。

### 快速使用

```python
from twisted.internet import reactor

def main(message):
    print(message)
    reactor.stop() # 停止运行

if __name__ == '__main__':
    reactor.callWhenRunning(main,"twisted开始运行!") # 立即执行
    reactor.run()
```

### 基本原理

reactor，本质上就是一个基于基于select，poll或epoll的事件循环，在**单线程**中运行。在编程领域中，这种利用循环体来等待事件发生，然后处理发生的事件的模型非常常见，被设计成为一个设计模式，叫反应器模式或反应堆模式。因为它是等待事件的发生，然后才做出相应的反应的。

![img](assets\883080-20160407104404234-713718492.png)

reactor是twisted异步框架中的核心组件，是事件管理器，用于注册、注销事件，运行事件循环，当事件发生时调用回调函数处理。

在twisted框架运行的过程中，reactor是一个<mark>基于单例模式实现</mark>的对象，它会监听socket的状态，当socket状态有变化时（有新的连接请求，或接受到数据等）时，调用相应的组件来进行处理。reactor不断的循环扫描socket列表中监听对象的状态，当有特定事件发生时（socket状态变化）调用回调函数callback，来处理事件，这时候执行权限交给回调函数，当我们的代码处理完事件后，将执行权返回给reactor，继续进行循环监听。

![img](assets\1483773-20181102212712358-1568016773.png)



1.  在Twisted中，reactor默认是不启动的，只有通过调用reactor.run()才启动，一旦启动，reactor循环就会在其开始的线程(主线程)中一直运行下去，可以通过reactor.stop()或者Ctrl+C进行退出。
2.  在Twisted中，reactor基于单例模式，即在一个程序中只能有一个reactor，并且不需要创建reactor，只需要导入就可以使用。
3.  在Twisted中，reactor默认基于select循环实现的，同时也提供了其他模式，如：pollreactor，epollreactor，如果要使用其它的reactor，需要在引入twisted.internet.reactor前引入并安装它(调用install)。
4.  reactor并不会因为回调函数中出现失败（虽然它会报告异常）而停止运行。
5.  在每个通过Twisted搭建起来的程序中心处，不管你这个程序有多少层，总会有一个reactor循环在不停止地驱动程序的运行。
6.  在Twisted中所有事件的触发都会被reactor监控，然后它会开启服务（初始化factory，factory再初始化protocol）。在没有事件处理时，reactor循环并不会消耗任何CPU的资源。

#### 手动切换事件循环模型

server.py，代码：

```python
# 如果要切换到其他的事件循环模型,则必须在引入reactor之前,引入并调用install进行注册安装
from twisted.internet import epollreactor
epollreactor.install()

from twisted.internet import reactor

# 下面2行代码会报错,因为在reactor后面才引入调用,则无效,并程序报错
# from twisted.internet import selectreactor
# selectreactor.install()

def main(message):
    print(message)
    # reactor.stop() # 停止运行

if __name__ == '__main__':
    reactor.callWhenRunning(main,"twisted开始运行!") # 立即执行
    reactor.run()
```



### 定时调用

reactor.callLater 会将某个任务加入到事件循环，并设置好多少秒后开始执行，当然要将事件循环启动后才会有作用。

```python
# 设置延时调用
call = reactor.callLater(调用时间(单位：秒), 回调函数, 参数1,参数2.....)
# 取消延时调用
call.cancel()
```

代码：

```python
from twisted.internet import reactor

def main(message):
    print("main函数开始运行!")
    print(message)
    num = 10
    reactor.callLater(5, callback, "小明","你好!") # 定时异步调用一次
    print("main函数结束运行!")

def callback(user,message):
    print("callback: %s,%s" % (user, message))
    # reactor.stop()  # 停止程序，这句代码与案例无关

if __name__ == '__main__':
    # reactor.callWhenRunning(main,"twisted开始运行!") # 立即执行
    reactor.callLater(5, main, "调用main函数!")
    reactor.run()
```



#### 定时多次

使用上面的reactor.callLater进行定时多次调用，代码：

```python
from twisted.internet import reactor

def main():
    # print("main开始运行")
    # reactor.callLater(调用时间(单位：秒), 回调函数, 参数1,参数2.....)
    reactor.callLater(3, callback, "twisted", "你好!")  # 定时调用一次
    # print("main结束运行")

def callback(user,message):
    print("callback: %s,%s" % (user, message))
    main()

if __name__ == '__main__':
    reactor.callWhenRunning(main) # 立即执行
    reactor.run()
```



twisted还提供了task.LoopingCall对象，专用于实现定时任务的调用。

```python
from twisted.internet import task
# 创建定时器
loop = task.LoopingCall(回调函数, 参数1,参数2,....)
# 开启定时器(interval=时间: 秒, now=是否立即调用)
loop.start()
# 关闭定时器
loop.stop()
```

代码：

```python
from twisted.internet import reactor
from twisted.internet import task
def main():
    print("main开始运行")

    # 创建定时器,绑定回调函数
    loop = task.LoopingCall(callback, "twisted", "你好!")  # 定时调用多次
    # 启动定时器，interval=间隔时间,单位: 秒, now=是否先立即调用一次
    loop.start(interval=5,now=True)

    print("main结束运行")

def callback(user,message):
    print("callback: %s,%s" % (user, message))

if __name__ == '__main__':
    reactor.callWhenRunning(main) # 立即执行
    reactor.run()
```



## 异步回调对象（Defered）

对于异步编程来说，能否进行异步回调是非常关键的，如果没有办法获取到异步调用的结果，那么整个程序就会失控，不光维护起来复杂，性能可能也会受到很大的影响，异步编程也就没有意义了。

Deferred对象就是Twisted提供给我们专门用来管理异步回调的。有了deferred，即可对任务的执行过程进行监控管理。防止程序的运行过程中，由于等待某项任务的完成而陷入阻塞停滞，可以有效的提高程序整体运行的效率。

Defered对象的实现过程中并没有使用到reactor，所以可以不用在事件循环中使用Defered。

### 快速使用

接下来，我们快速使用下Deferred对象进行异步调用，代码：

```python
from twisted.internet import defer
def func1(num):
    """任务代码"""
    deferred = defer.Deferred()
    deferred.callback(num + 10) # 假设经过上面的处理以后得到结果了,传递给回调函数
    print("func1执行结束!")
    return deferred

def func1_callback(num):
    """结果的回调函数"""
    print(f"func1的执行结果，num={num}")

if __name__ == '__main__':
    # 假设我有一个任务: 完成一个数值的计算,
    # 但是这个过程可能耗时,所以我们使用Deferred对象来进行异步处理,让func1执行以后返回异步结果
    deferred = func1(1)
    print("代码已经执行到这里了!")
    # 在这里,我们注册一个回调函数,当结果有了以后,自动执行func1_callback，
    # 并把任务中callback的结果作为参数传递到func_callback
    deferred.addCallback(func1_callback)
```

当然，上面的例子没什么作用，开发中如果写这样的代码，分分钟让我们找下一家公司。改进下上面的例子。

```python
from twisted.internet import defer,reactor
def func1(num):
    deferred = defer.Deferred()
    # deferred.callback(num+1) # 假设经过上面的处理以后得到结果了,传递给回调函数
    # 定时4秒后调用d.callback回调方法,模拟真实任务的耗时
    reactor.callLater(4, deferred.callback, num + 1)
    print("func1执行结束!")
    return deferred

def func2(num):
    print("结果出来了,num=%s" % num)
    reactor.stop() # 这句代码没什么用,就是为了让程序停止下来而已

if __name__ == '__main__':
    # 假设我有一个任务: 完成一个数值的计算,
    # 但是这个过程可能耗时,所以我们使用Deferred对象来进行异步处理,让func1执行以后返回异步结果
    deferred = func1(1)
    # 在这里,我们注册一个回调函数,当结果有了以后,自动执行func2
    deferred.addCallback(func2)
    print("代码已经执行到这里了!")
    reactor.run()
```

#### 基于deferred实现http异步请求和异步回调

server.py，代码：

```python
from twisted.internet import defer,reactor
from twisted.web.client import Agent,readBody
from pprint import pformat
import json

def func1(num):
    """任务代码"""
    #　创建http请求代理对象
    agent = Agent(reactor)
    ip = "123.112.18.111"
    url = "http://ip-api.com/json/%s?lang=zh-CN" % ip
    # 发起请求(http请求动作，url地址，请求头，请求体)
    # 返回值就是一个deferred对象
    deferred = agent.request(
        b"GET",
        url.encode(),
        None,
        None,
    )
    return deferred

def func1_callback(defer):
    """结果的回调函数"""
    # 获取响应状态码
    print(defer.code)
    # 获取原始响应头
    print(pformat(list(defer.headers.getAllRawHeaders())))
    # 回调提取响应内容
    d = readBody(defer)
    d.addCallback(cbBody)

def cbBody(body):
    # 转换数据格式
    data = json.loads( body.decode() )
    print("国家：%s 省份: %s 城市: %s" % (data["country"], data["regionName"], data["city"]) )

if __name__ == '__main__':
    deferred = func1(1)
    # 在这里,我们注册一个回调函数,当结果有了以后,自动执行func1_callback，
    # 并把任务中callback的结果作为参数传递到func_callback
    deferred.addCallback(func1_callback)
    reactor.run()
```



### 回调异常

异步调用就是异步编程的核心，不管是成功的回调，还是失败的回调。上面我们都是使用 addCallback 注册成功回调，除开这个，我们还可以通过addErrback注册异常回调处理函数，实现异常处理。代码：

```python
from twisted.internet import defer,reactor

def func1(num):
    print('func1开始执行了!')
    deferred = defer.Deferred()
    # 模拟异常的出现
    if isinstance(num, int):
        # reactor.callLater 模拟耗时的效果
        reactor.callLater(2, deferred.callback, num + 1)
    else:
        reactor.callLater(2, deferred.errback, ValueError('请输入整型!'))

    return deferred # 只要是异步任务,必须返回异步回调对象deferred

def func1_success(num):
    print('成功回调: num=%s' % num)

def func1_error(failure):
    print("异常回调.<%s> \n\t %s " % (
        failure.type.__name__,  # 异常类型
        failure.value,  # 异常信息
    ))
    print(failure.getBriefTraceback())  # 异常跟踪信息

if __name__ == '__main__':
    deferred = func1('2')
    # deferred.addCallback(callback=success) # 注册成功回调
    # deferred.addErrback(errback=error)     # 注册失败回调
    deferred.addCallback(callback=func1_success).addErrback(errback=func1_error)
    reactor.run()
```



### 回调链

从上面的使用中，可以看到，Deferred对象就是用来**管理回调函数**的，该对象定义了成功回调链和错误回调链（一个deferred对象就有一对callback/errback回调链，它们以添加到deferred中的顺序依次排列）。deferred只能被激活一次(通过Deferred对象的callback或errback激活)。

Deferred对象一共提供了4个方法让我们可以向实例对象中添加callback回调链/errback回调链：

-   addCallback(callback)：添加一个成功回调链
-   addErrback(errback)：添加一个错误回调链
-   addCallbacks(callback, errback)：添加一对回调链，分别是成功回调和错误回调
-   addBoth(anyback)：在成功回调链和错误回调链中都添加一个anyback回调。

![img](assets\v2-3ca4acca0e02309edf769b2d232a111e_720w.jpg)



#### 链式回调

代码：

```python
# coding=utf-8
from twisted.internet import reactor,defer

def cb1(res):
    print('步骤cb1: res=', res)
    return res+1

def cb2(res):
    print('步骤cb12: res=', res)
    return res+1

def cb3(res):
    print('步骤cb13: res=', res)
    return res+1

def main(deferred):
    print("main函数执行")
    reactor.callLater(3, deferred.callback,1) # 3秒后激活deferred

if __name__ == '__main__':
    d = defer.Deferred()
    d.addCallback(cb1).addCallback(cb2).addCallback(cb3)
    reactor.callWhenRunning(main,d)
    reactor.run()
```

代码2：

```python
# coding=utf-8
from twisted.internet import reactor,defer
from twisted.python.failure import Failure


def cb1(res):
    print('步骤cb1: res=', res)
    raise Exception("cb1发生异常!!!")
    return res+1

def cb2(res):
    print('步骤cb2: res=', res)
    if isinstance(res,Exception):
        deferred = defer.Deferred()
        raise deferred.errback(ValueError("cb1发生异常!!!"))
    else:
        return res+1

def cb3(res):
    print('步骤cb3: res=', res)
    return res+1

def eb1(res):
    print('步骤eb1: res=', res.type.__name__)
    return res

def eb2(res):
    print('步骤eb2: res=', res.type.__name__)
    if not isinstance(res,Failure):
        return res
    else:
        return 3

def eb3(res):
    print('步骤eb3: res=', res.type.__name__)
    return res

def main(deferred):
    print("main函数执行")
    reactor.callLater(1, deferred.callback,1) # 3秒后激活deferred

if __name__ == '__main__':
    d = defer.Deferred()
    d.addCallbacks(cb1,eb1).addCallbacks(cb2,eb2).addCallbacks(cb3,eb3)
    reactor.callWhenRunning(main,d)
    reactor.run()
```

上面的链式回调中，每一个成功回调的结果都是下个成功回调的输入，比如 cb1 的结果会是 cb2 的输入。

同时，如果我们有设置了错误回调，则同理，上一个错误回调的异常结果也会是下一个错误回调的输入。

当然，这里也有特殊情况，则是在成功回调链中任意一环如果出现了异常，则该异常则会被作为参数传递给下一个错误回调中进行处理，而且，错误回调中如果及时处理了异常并返回成功结果，那么也会把本次结果传递给下一个成功回调作为参数的。



根据上面的分析，那么开发中就可能存在以下情况了。代码：

```python
from twisted.internet import defer

def cb1(res):
    print('步骤1: res=', res)
    return res+1

def cb2(res):
    print('步骤2: res=', res)
    deferred2 = defer.Deferred() # 这种代码仅仅作为例子，不可能在开发中编写的。
    return deferred2

def cb3(res):
    print('步骤3: res=', res)
    return res+1
if __name__ == '__main__':
    d = defer.Deferred()
    d.addCallbacks(cb1).addCallback(cb2).addCallback(cb3)
    d.callback(0)
```



#### Deferredlist

如果不需要每个回调都作为上一个回调的基础的话，上面的执行结果也没有问题。但是如果是上一个回调作为下一个回调的基础的话，那么我们就必须要考虑好，保证多个回调结果都没有问题的情况了。此时，我们可以使用 DeferredList。

Deferredlist可以在列表中所有deferred对象就绪后执行指定回调函数，从本质上来说它返回了一个新的deferred对象

使用语法：

```python
from twisted.internet.defer import DeferredList
DeferredList(deferrlist, fireOnOneCallback， fireOnOneErrback, consumeErrors)
.addCallback(deferrlist_suc)
.addErrback(deferrlist_suc)
# deferrlist        等待的defer对象列表
# fireOnOneCallback 是否列表中任一deferred对象callback后，DeferredList就回调callback
# fireOnOneErrback  是否列表中任一deferred对象errback后，DeferredList就回调errback
# consumeErrors     是否列表中任一deferred对象执行过程中发生错误后，DeferredList就回调errback
```

代码：

```python
from twisted.internet import defer

def get_results(res):
    print('结果:', res)

def cb1(res):
    print("cb1,res=%s" % res)
    return cb1

def cb2(res):
    print("cb2,res=%s" % res)
    return cb2

d1 = defer.Deferred()
d1.addCallback(cb1)
d2 = defer.Deferred()
d2.addCallback(cb2)
d = defer.DeferredList([d1,d2])
# d = defer.DeferredList([d1,d2],1)
d.addCallback(get_results)
d1.callback('d1成功回调了')
# 下面这句代码注释掉，可以看到，DeferredList会在所有Deferred执行callback以后才回调.（前提是fireOnOneCallback=False）
# d2.callback("d2成功回调了")
```

#### gatherResults

gatherResults 和 DeferredList 类似，也是等待多个 deferred，不同的是gatherResults只要有 1 个 deferred 异常，就会触发gatherResults 整体的异常。可以保证deferred列表中所有的deferred对象都成功回调了，才会成功回调。

```python
from twisted.internet import defer
from twisted.internet.defer import FirstError
def get_results(res):
    print('结果:', res)

def get_fails(res):
    # print(res.type.__name__) # 异常类型
    # print(res.value.index)   # 获取索引,判断第几个deferred对象出现了异常回调
    print(res.value.subFailure.value) # 异常回调的错误内容[错误提示]

def cb1(res):
    print("cb1,res=%s" % res)
    return res

def cb2(res):
    print("cb2,res=%s" % res)
    return res

def cb3(res):
    print("cb3,res=%s" % res)
    return res

d1 = defer.Deferred()
d1.addCallback(cb1)

d2 = defer.Deferred()
d2.addCallback(cb2)

d3 = defer.Deferred()
d3.addCallback(cb3)

d = defer.gatherResults([d1,d2,d3])
# gatherResults会保证所有deferred对象成功回调以后才得到结果
# 所以gatherResults的成功回调是没有执行状态,只有执行结果
d.addCallback(get_results).addErrback(get_fails)

# d1.callback('d1成功回调!')
d1.errback(ValueError('d1.....失败回调!'))
d2.callback('d2成功回调!')
# d2.errback(ValueError('d2失败回调!'))
d3.callback("d3成功回调!")
```



#### 内联回调

inlineCallbacks，是一个装饰器，它总是装饰**生成器函数**，如那些使用 yield 语句的函数。inlineCallbacks 唯一的目的是将一个个生成器转化为一系列的异步回调，每个回调被yield分隔，yield的返回值会传到下一个回调。

当我们调用一个用 inlineCallbacks 装饰的函数时,不需要自己调用 send 或 throw 方法，修饰器内部会帮助我们处理细节，并确保生成器运行到结束(假设它不抛出异常)；

代码：

```python
from twisted.internet import reactor, defer

def callback(num):
    print('callback执行了!')
    deferred = defer.Deferred()
    reactor.callLater(8, deferred.callback, num+1)
    return deferred

@defer.inlineCallbacks
def main():
    result = yield callback(3)
    print(result)

if __name__ == '__main__':
    main()
    print("twisted开始运行 >>>> ")
    reactor.callLater(30, reactor.stop)
    reactor.run()
```



更加详细的例子：

```python
# coding:utf-8
from twisted.internet import defer,reactor

@defer.inlineCallbacks
def callback():
    result = 1
    print('第1个回调!')
    result = yield 1                        # 第一个回调结束
                                            # yiled后面的值就是第一个回调的返回值，这个返回值会赋值给result，实现原理就是：
                                            # 在inlineCallbacks装饰器中通过对生成器执行send操作，将yield的值又给send回到生成器了
    d = defer.Deferred()
    print('第2个回调,并得到结果,result=%s' % result)     #,result=1 2.第二个回调开始
    reactor.callLater(5, d.callback, 2)     # 5秒后激活Deferred对象，并将2传入Deferred的起始回调
    result = yield d                        # 当Deferred回调激活并执行完后，第二个回调结束，并将第二个回调的返回值2赋予变量result

    print('第3个回调,并得到结果,result=%s' % result)   #,result=2 3.第三个回调开始

    d = defer.Deferred()
    reactor.callLater(5, d.errback, Exception(3)) # 5秒后激活Deferred对象，并将Exception(3)传入Deferred的第一个错误回调

    try:
        yield d                             # 第三个回调抛出了异常
    except Exception as e:                    # 捕获异常
        result = e

    print('第4个回调,并得到结果,result=%s' % result) # result=3, 这里的result来自上面的异常Exception赋值
    reactor.stop()

if __name__ == '__main__':
    reactor.callWhenRunning(callback)
    reactor.run()

    # 输出
    # 第1个回调!
    # 第2个回调, 并得到结果, result = 1
    # 第3个回调, 并得到结果, result = 2
    # 第4个回调, 并得到结果, result = 3
```



### 实现同步非阻塞

deferToThread使用线程实现的,不推荐过多使用。

twisted.deferToThread返回一个deferred对象，把回调函数在另一个线程中进行处理，主要用于I/O操作，例如：数据库/文件读取操作。

扩展：callinThread和callfromThread

```python
# coding=utf-8
import time
from twisted.internet import defer, reactor
from twisted.internet.threads import deferToThread

# 耗时操作 这是一个同步阻塞函数
def sleep(result):
    print("阻塞开始!")
    time.sleep(3)
    print("阻塞结束!")
    return result

def callback(result):
    print("callback执行了,result=%s" % result)

if __name__ == '__main__':

    # d = defer.Deferred()
    # d.addCallback(sleep).addCallback(callback)
    # d.callback("hello")

    # # 如果函数附带了参数,可以使用 functools.partial 偏函数包装一下, 传递参数进去
    import functools
    sleep = functools.partial(sleep, 3)
    d = deferToThread(sleep)
    d.addCallback(callback)

    print("程序执行结束!")
    reactor.run()
```



## TCP编程

接口定义：`twisted.internet.interfaces.IReactorTCP`

**twisted**的TCP网络编程主要基于3个基础模块：`Protocol`, `ProtocolFactory`, `Transport`.这三个模块是构成twisted服务器端与客户端程序的TCP通信的基本。

| 模块      | 描述                                                         |
| --------- | ------------------------------------------------------------ |
| Protocol  | 顾名思义就是**twisted**提供给我们定义一个处理协议的类，这个类里面的代码就是写你这个协议要怎么处理通信过程中数据的发送和接收的。 |
| Factory   | 工厂模式的体现，在这里面生成协议，是生成协议的工厂           |
| Transport | 用来收发数据， 服务器端与客户端的数据收发与处理都是基于这个模块来完成 |

![img](assets\1562659162037-22424146-af29-4204-9ea2-7a791485e98d.png)

要学习上面3个模块的使用，我们先使用一个基本的echo服务器例子，来看下他们三种在代码中的基本使用。

### echo服务器

服务端，`echo_server.py`，代码：

```python
# coding=utf-8
from twisted.internet import protocol, reactor

class EchoServerProtocol(protocol.Protocol):
    def connectionMade(self):
        self.client = self.transport.getPeer().host
        print('客户端连接成功！: %s' % self.client)

    def dataReceived(self, data):
        data = data.decode()
        print("客户端：%s" % data)
        self.transport.write(data.encode())

class EchoServerFactory(protocol.ServerFactory):
    protocol = EchoServerProtocol

if __name__ == '__main__':
    print('服务端启动，等待连接...')
    reactor.listenTCP(10003, EchoServerFactory())
    reactor.run()
```

客户端，`echo_client.py`，代码：

```python
# coding=utf-8
from twisted.internet import protocol, reactor

class EchoClientProtocol(protocol.Protocol):
    def sendData(self):
        data = input('> ')
        if data:
            self.transport.write(data.encode())
        else:
            self.transport.loseConnection()

    def connectionMade(self):
        self.sendData()

    def dataReceived(self, data):
        data = data.decode()
        print("服务端: %s" % data)
        self.sendData()


class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClientProtocol
    def clientConnectionLost(self, connector, reason):
        reactor.stop()

if __name__ == '__main__':
    reactor.connectTCP('localhost', 10003, EchoClientFactory())
    reactor.run()
```

根据端口关闭指定进程： 

```bash
kill -9 `lsof -t -i:端口号`
```



### Transports

Transports代表网络中两个通信结点之间的连接。Transports负责描述连接的细节，比如连接是面向流式的还是面向数据报的，流控以及可靠性。Transports实现了ITransports接口：

```
write                   以非阻塞的方式按顺序依次将数据写到物理连接上
writeSequence           将一个字符串列表写到物理连接上
loseConnection          将所有挂起的数据写入，然后主动断开连接
getPeer                 取得连接中对端的地址信息
	host                对端的地址
	port                对端的端口
getHost                 取得连接中本端的地址信息
    host                本端的地址
    port                本端的端口
```

### Protocols

Protocols描述了如何以异步的方式处理网络中的事件。HTTP、DNS以及IMAP是应用层协议中的例子。Protocols实现了IProtocol接口，它包含如下的方法：

```
factory                      默认为None，协议工厂实例对象，需要在构建协议对象时进行赋值
connected                    连接状态，默认为0，连接以后状态为True
transport                    

makeConnection               在transport对象和服务器之间建立一条连接
dataReceived                 接收数据时调用
connectionLost               关闭连接时调用
connectionMade               连接建立起来后调用
```

### Factory

协议工厂，用于实例化protocol协议对象并保存持久的公共信息（配置，状态），负责连接、通信时建立连接、以及连接中断的处理。服务器端使用protocol.Factory（别名：protocol.ServerFactory），客户端使用protocol.ClientFactory(ClientFactory是Factory的子类)。

在程序运行过程中，每次有对端连接本端，Factory都会针对对端实例化一个protocol协议处理对象来与对端进行通信的！！

```
Factory：
    protocol                     Protocol协议类[一般不使用，一般使用buildProtocol方法来代替它]
    buildProtocol                创建Protocol协议实例对象
    startFactory                 实例化协议对象时，会自动调用这个方法
    stopFactory                  协议对象被销毁时，会自动调用这个方法

客户端 ClientFactory:
    clientConnectionFailed       客户端连接服务端失败的回调
    clientConnectionLost         客户端连接服务端断开的回调
```



## UDP编程

相对于TCP编程来说，Twisted提供的UDP编程相对简单许多，我们不需要定义协议工厂Factory类，仅需要实现DatagramProtocol协议类即可。

udp服务器，代码：

```python
import socket
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class UDPServerProtocol(DatagramProtocol):
    def datagramReceived(self, data, addr):
        """接收数据"""
        message = data.decode()
        print(f"接收 {message} 来自于{addr}")
        data = ("服务端的"+message).encode()
        self.transport.write(data, addr)

if __name__ == '__main__':
    portSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    portSocket.setblocking(False)
    portSocket.bind(("127.0.0.1", 10004))

    reactor.adoptDatagramPort(portSocket.fileno(), socket.AF_INET, UDPServerProtocol())
    portSocket.close()
    reactor.run()
```

udp客户端，代码：

```python
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

class UDPClientProtocol(DatagramProtocol):
    def startProtocol(self):
        """协议对象被创建时自动"""
        self.transport.connect("127.0.0.1", 10004)
        self.transport.write("hello".encode())

    def datagramReceived(self, data, addr):
        message = data.decode()
        print(f"接收 {message} 来自于 {addr}")

    def connectionRefused(self):
        """连接断开...."""
        print("No one listening")

if __name__ == '__main__':
    reactor.listenUDP(0, UDPClientProtocol())
    reactor.run()
```



## 私有化协议

我们在前面已经使用了twisted提供的模块进行TCP编程，但是TCP是基于字节流的协议，所以只要是TCP通信都会遇到消息边界的处理问题（这就是面试过程中经常被问到的粘包和分包问题）。

```
粘包：发送方发送两个消息过来，例如："hello"+"world"，接收方却一次性接收到了"helloworld"
分包：发送方发送字符串"helloworld"，接收方却接收到了两个字符串"hellowo"和"rld"
```

消息发送方发送了三个字符串：

![img](assets\20140821134046402.png)

但是接收方收到的可能是这样的：

![img](assets\20140821134131782.png)

一般解决的方案无非以下几种：

1.  使用固定长度的消息。比如每个长度4字节，那么接收的时候按每条4字节拆分就可以了。
2.  使用请求头+请求体格式。其中请求头中指定请求头+请求体的总长度（字节数），将信息的内容放在请求体中。
3.  使用分隔符。例如许多文本内容的传输协议就是在每条消息后面加上换行符（CR LF，即"\r\n"），也就是一行一条消息。

上面几种方案就是开发中比较常见的解决方案，当然，有的协议也可能会同时用到上面多种方案。例如HTTP协议，Header部分用的是CR LF换行来区分每一条Header，而Header中用Content-Length来指定Body字节数。

在twisted中就提供了对应的模块方便我们解决开发中遇到的TCP粘包和分包问题，其中LineReCeiver 是以换行符为分隔符的协议。当然，除了LineReceiver以外，twisted还提供了其他几个基于分隔符的类来解决这个问题。

```python
from twisted.protocols.basic import LineReceiver
from twisted.protocols.basic import Int8StringReceiver,Int16StringReceiver,Int32StringReceiver
```

Python中解决分包和粘包问题的相关文档：https://blog.csdn.net/yannanxiu/article/details/52096465



### LineReceiver

LineReceiver继承于`protocol.Protocol`。

为了让大家对内容更加感兴趣，我这里的例子引入了一个外接接口：图灵机器人。开发中，这个图灵机器人一般用于在微信群聊，或者自动应答客服的系统的机器人。

服务端，代码：

```python
# coding=utf-8
import requests,json
from twisted.internet import  reactor,defer,protocol
from twisted.protocols.basic import LineReceiver,Int8StringReceiver,Int16StringReceiver,Int32StringReceiver

# 应答服务器
class Answer(LineReceiver):
    def lineReceived(self, line):
        line = line.decode()
        print(f"客户端:{line}")
        deferred = robot(line)
        deferred.addCallback(self.get_answer)

    def get_answer(self, result):
        data = json.loads(result.text)
        message = data["results"][0]["values"]["text"]
        self.sendLine(message.encode())

@defer.inlineCallbacks
def robot(text):
    url = "http://openapi.tuling123.com/openapi/api/v2"
    data = {
        "perception": {
            "inputText": {
                "text": text
            }
        },
        "userInfo": {
            "apiKey": "b84264cc645c7a78f7c71b68af24b773",
            "userId": "1"
        }
    }
    deferred = yield requests.post(url, json.dumps(data))
    return deferred

class AnswerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Answer()

if __name__ == '__main__':
    reactor.listenTCP(8000, AnswerFactory())
    reactor.run()
```

客户端，代码：

```python
# coding=utf-8
from twisted.internet import  reactor,protocol
from twisted.protocols.basic import LineReceiver

# 应答服务器
class Question(LineReceiver):
    def connectionMade(self):
        print("连接服务器成功!")
        self.sendData()

    def sendData(self):
        message = input(">")
        self.sendLine(message.encode())

    def lineReceived(self, line):
        print(line.decode())
        self.sendData()

class QuestionFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Question()

if __name__ == '__main__':
    reactor.connectTCP("localhost",8000,QuestionFactory())
    reactor.run()
```

### Int32StringReceiver

服务端，代码：

```python
# coding=utf-8
import requests,json
from twisted.internet import  reactor,defer
from twisted.internet import protocol
from twisted.protocols.basic import Int32StringReceiver

# 应答服务器
class Answer(Int32StringReceiver):
    def dataReceived(self, string):
        string = string.decode()
        print(f"客户端:{string}")
        deferred = robot(string)
        deferred.addCallback(self.get_answer)

    def get_answer(self, result):
        data = json.loads(result.text)
        message = data["results"][0]["values"]["text"]
        self.sendString(message.encode())

@defer.inlineCallbacks
def robot(text):
    url = "http://openapi.tuling123.com/openapi/api/v2"
    data = {
        "perception": {
            "inputText": {
                "text": text
            }
        },
        "userInfo": {
            "apiKey": "b84264cc645c7a78f7c71b68af24b773",
            "userId": "1"
        }
    }
    deferred = yield requests.post(url, json.dumps(data))
    return deferred

class AnswerFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Answer()

if __name__ == '__main__':
    reactor.listenTCP(8000, AnswerFactory())
    reactor.run()
```

客户端，代码：

```python
# coding=utf-8
from twisted.internet import  reactor
from twisted.internet import protocol
from twisted.protocols.basic import Int32StringReceiver

# 应答服务器
class Question(Int32StringReceiver):
    def connectionMade(self):
        print("连接服务器成功!")
        self.sendData()

    def sendData(self):
        message = input(">")
        self.sendString(message.encode())

    def dataReceived(self, string):
        print(string.decode())
        self.sendData()

class QuestionFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return Question()

if __name__ == '__main__':
    reactor.connectTCP("localhost",8000,QuestionFactory())
    reactor.run()
```



### 私有化协议

实际开发中，我们可以直接应用twisted提供的内置协议来解决通信问题，当然类似部分网络软件或者游戏则更多的是采⽤纯私有化协议来解决。在服务端和客户端之间发送数据时，根据指定的消息格式对消息进⾏打包，接收数据时进⾏数据解包。

#### Struct

在python中，由于没有提供数据类型的定义方式，所以一般消息的打包解包都是struct模块来解决。

struct常用方法：

```
普通数据基本方法：
	pack     打包
	unpack   解包
二进制数据打包：
	pack_into()       打包
	unpack_from()     解包
```

##### 快速使用

普通数据打包和解包，代码：

```python
import struct
import binascii

data = (1, 'abcabc'.encode(), 2.7)
print("源数据:", data)

# (函数式)打包
packed_data = struct.pack('i3sf',*data) # 3s表示3个字节长度的字符串，abcabc是6个字节长度了，会存在丢失的情况。
# (对象式)打包
s1 = struct.Struct('i3sf')
# packed_data = s1.pack(*data)

print("打包后数据格式", type(packed_data))
print("打包后数据 :", packed_data)
print("打包后数据 :", binascii.hexlify(packed_data))

# (函数式)解包
unpacked_data = struct.unpack('i3sf',packed_data)
# (对象式)解包
# unpacked_data = s1.unpack(packed_data)
print("解包后数据格式:", type(unpacked_data))
print("解包后数据: ",unpacked_data)

# 使用struct打包数据,和解包数据的格式必须一致.
# 使用struct打包和解包数据的过程中,针对数值都会出现精度丢失的问题
# 使用struct打包和解包数据时,如果字符串超过格式指定的长度,则会出现内容丢失的情况
```

二进制数据打包和解包，代码：

```python
import struct,binascii,ctypes

values1 = (1, 'abc'.encode(), 2.7)
s1 = struct.Struct('I3sf') # I 表示int，3s表示三个字符长度的字符串，f 表示 float

values2 = ('defg'.encode(), 101)
s2 = struct.Struct('4sI')

prebuffer = ctypes.create_string_buffer(s1.size+s2.size)
print('Before :', binascii.hexlify(prebuffer)) # Before : b'0000000000000000000000000000000000000000'
# 数据打包
s1.pack_into(prebuffer, 0, *values1)
s2.pack_into(prebuffer, s1.size, *values2) # s1.size 因为前面数据位已经被第一段数据占用了,此处要空出s1.size的长度

print('After pack:', binascii.hexlify(prebuffer))
print(s1.unpack_from(prebuffer, 0))
print(s2.unpack_from(prebuffer, s1.size)) # s1.size 因为前面数据位已经被第一段数据占用了,此处要空出s1.size的长度
```

##### 打包格式

struct模块的常⻅的格式符意义如下：

| Format | C Type             | Python             | 字节数 |
| ------ | ------------------ | ------------------ | ------ |
| x      | pad byte           | no value           | 1      |
| c      | char               | string of length 1 | 1      |
| b      | signed char        | integer            | 1      |
| B      | unsigned char      | integer            | 1      |
| ?      | _Bool              | bool               | 1      |
| h      | short              | integer            | 2      |
| H      | unsigned short     | integer            | 2      |
| i      | int                | integer            | 4      |
| I      | unsigned int       | integer or long    | 4      |
| l      | long               | integer            | 4      |
| L      | unsigned long      | long               | 4      |
| q      | long long          | long               | 8      |
| Q      | unsigned long long | long               | 8      |
| f      | float              | float              | 4      |
| d      | double             | float              | 8      |
| s      | char[]             | string             |        |
| p      | char[]             | string             |        |
| P      | void *             | long               |        |
|        |                    |                    |        |



#### 消息头

消息头部不一定非要像twisted那样只能是一个字节比如`0xAA`什么的，也可以包含协议的其他信息，例如：协议版本号，指令等，当然**也可以把消息长度合并到消息头部里**，唯一的要求是包头长度必须是固定的（否则无法准确解包），包体则可变长。接下来我们自定义的一个**包头**：

| 版本号（ver） | 消息长度（bodySize） | 指令（cmd） |
| ------------- | -------------------- | ----------- |
|               |                      |             |

版本号，消息长度，指令数据类型都是无符号32位整型变量，于是这个消息长度固定为3*4=12字节。示例代码：

```python
import struct,json

if __name__ == '__main__':
    # 假设version就是版本号,body就是数据包,cmd就是终端执行[当然,这里除了body以外,都是举例而已,可有可无.]
    version = 1
    body = json.dumps({"company": "oldboyedu"})
    print(body)
    cmd = 101
    header = [version, body.__len__(), cmd]
    print(header)
    headPack = struct.pack("iii", *header)
    print(headPack) # b'\x01\x00\x00\x00\x18\x00\x00\x00e\x00\x00\x00'
    print(len(headPack)) # 12

    version, body_length, cmd = struct.unpack('iii', headPack)
    print(f"version={version}, body_length={body_length}, cmd={cmd}")
```



#### 消息体的打包和解包

服务端，代码：

```python
# coding=utf-8
from twisted.internet import protocol,reactor
import struct
import json
class MyProtocol(protocol.Protocol):
    _data_buffer = bytes()
    version = 1

    def dataPack(self,data,cmd):
        data = json.dumps(data)
        header = [self.version, data.__len__(), cmd]
        headPack = struct.pack("iii", *header)
        sendData1 = headPack + data.encode("utf-8")
        return sendData1

    def dataReceived(self,data):
        self._data_buffer += data
        headerSize = 12

        while True:
            if len(self._data_buffer) < headerSize:
                return

            # 读取消息头部
            # 定义消息格式iii表示三个int数据
            headPack = struct.unpack('iii', self._data_buffer[:headerSize])
            # 获取消息正文长度
            bodySize = headPack[1]

            # 分包情况处理
            if len(self._data_buffer) < headerSize + bodySize:
                return

            # 读取消息正文的内容
            body = self._data_buffer[headerSize:headerSize + bodySize]
            # 处理数据
            self.mydataReceived(headPack, body)
            # 粘包情况的处理
            self._data_buffer = self._data_buffer[headerSize + bodySize:]

    def mydataReceived(self, header,data):
        print(f"客户端: header={header}, data={data.decode('utf-8')}")
        senddata = self.dataPack("我收到你的信息了!", 1001)
        self.transport.write(senddata)

class MyFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return MyProtocol()

if __name__ == '__main__':
    reactor.listenTCP(8000, MyFactory())
    reactor.run()
```

客户端，代码：

```python
# coding=utf-8
from twisted.internet import protocol,reactor
import struct
import json
class MyProtocol(protocol.Protocol):
    _data_buffer = bytes()
    version = 1

    def connectionMade(self):
        senddata = self.dataPack({"company":"oldboyedu"},1100)
        self.transport.write(senddata)

    def dataPack(self,data,cmd):
        data = json.dumps(data)
        header = [self.version, data.__len__(), cmd]
        headPack = struct.pack("iii", *header)
        sendData1 = headPack + data.encode()
        return sendData1

    def dataReceived(self,data):
        self._data_buffer += data
        headerSize = 12

        while True:
            if len(self._data_buffer) < headerSize:
                return

            # 读取消息头部
            # 定义消息格式iii表示三个int数据
            headPack = struct.unpack('iii', self._data_buffer[:headerSize])
            # 获取消息正文长度
            bodySize = headPack[1]

            # 分包情况处理
            if len(self._data_buffer) < headerSize + bodySize:
                return

            # 读取消息正文的内容
            body = self._data_buffer[headerSize:headerSize + bodySize]
            # 处理数据
            self.mydataReceived(headPack, body)
            # 粘包情况的处理
            self._data_buffer = self._data_buffer[headerSize + bodySize:]

    def mydataReceived(self, header,data):
        data = data.decode('unicode_escape')
        print(f"服务端: header={header}, data={data}")

class MyFactory(protocol.ClientFactory):
    def buildProtocol(self, addr):
        return MyProtocol()

if __name__ == '__main__':
    reactor.connectTCP("localhost",8000, MyFactory())
    reactor.run()
```



## 数据库操作

异步操作MySQL数据库

```python
from twisted.internet import reactor
from twisted.enterprise import adbapi
import pymysql

def read(cursor,sql):
    cursor.execute(sql)
    return cursor.fetchall()
    # return cursor.fetchone()

def write(cursor,sql):
    cursor.execute(sql)
    return cursor.rowcount

def get_result(data):
    print("异步读取数据")
    for item in data:
        print(item)

def get_result2(data):
    print("受影响的行数: ", data)

if __name__ == '__main__':

    sql = "SELECT user_name,nick_name,password,modified_date FROM mj_user"
    # db = pymysql.connect(
    #     db="mahjong",
    #     user="root",
    #     password="123",
    #     host="127.0.0.1",
    #     port=3306,
    #     charset="utf8",
    #     cursorclass=pymysql.cursors.DictCursor
    # )
    #
    # cursor = db.cursor()
    # cursor.execute(sql)
    # data = cursor.fetchall()
    # for item in data:
    #     print(item)

    dbpool = adbapi.ConnectionPool(
       dbapiName="pymysql",
       db="mahjong",
       user="root",
       password="123",
       host="127.0.0.1",
       port=3306,
       charset="utf8",
       cursorclass=pymysql.cursors.DictCursor
    )

    # deferred = dbpool.runInteraction(read, sql)
    # deferred.addCallback(get_result)

    from datetime import datetime
    sql = 'INSERT INTO `mj_user` (`created_date`, `modified_date`, `bsfb_id`, `nick_name`, `user_name`, `password`, `salt`, `sex`,`avater_url`,`status`, `skey`, `register_time`, `login_time`, `logout_time`, `register_ip`, `login_ip`, `is_visitor`, `is_vip`, `is_robot`) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"),("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")' % (( '2021-03-13 15:37:3', '2021-03-13 15:37:03', 1, '测试用户11', 'oldboy1', 'd2d1558f08bb4ae0ed081344903021c5', 'YhgU9czInS3laFWcpYz14nkabuG2irb14GesZfQK9V8ClPIRqoX0qLBh38nPk', 1, 'https://mahjongbucket.oss-cn-beijing.aliyuncs.com/6.jpg', 1, '73fc14139c15989b25ca4bc199410192', 1615621023, 1615621023, 1615621023, '127.0.0.1', '127.0.0.1', 1, 0, 0)+( '2021-03-13 15:37:3', '2021-03-13 15:37:03', 1, '测试用户11', 'oldboy1', 'd2d1558f08bb4ae0ed081344903021c5', 'YhgU9czInS3laFWcpYz14nkabuG2irb14GesZfQK9V8ClPIRqoX0qLBh38nPk', 1, 'https://mahjongbucket.oss-cn-beijing.aliyuncs.com/6.jpg', 1, '73fc14139c15989b25ca4bc199410192', 1615621023, 1615621023, 1615621023, '127.0.0.1', '127.0.0.1', 1, 0, 0))
    deferred = dbpool.runInteraction(write, sql)
    deferred.addCallback(get_result2)
    reactor.run()
```



## 透明代理

透明代理(PB, Perspective Broker)是用于远程方法调用和对象交换协议，该协议是异步和对称的。

使用PB， 客户端就可以直接调用服务器的函数并得到函数的返回结果。

Twisted提供了一个pb模块，针对服务端和客户端分别提供了pb.PBServerFactory和pb.PBClientFactory供开发者使用。其中，服务端的透明代理协议工厂Factory中必须设置root对象属性，且该root对象必须直接或间接继承于pb.Referenceable类。pb.Referenceable有个子类pb.Root，也比较常用。

服务端中提供的远程调用方法的方法名必须以`remote_`开头，在客户端调用远程方法时，通过callRemote指定，此时，不需要指定`remote_`前缀。

服务端，代码：

```python
# coding=utf-8
from twisted.internet import reactor
from twisted.spread import pb

class ServerRoot(pb.Root):
    def remote_get_main(self,message0,message1): # get_main 就是将来提供给客户端进行调用的方法名
        print(message0)
        print(message1)

        server2 = Server2Root()
        message2 = f"2. 服务端: remote_get_main方法正在执行中...."
        message3 = f"3. 服务端: 返回新的远程调用对象给客户端: {server2}"
        print(message2)
        print(message3)
        return [message2, message3, server2]

class Server2Root(pb.Root):
    def remote_server2_main(self,message):
        print(message)
        message5 = f"5. 服务端: remote_server2_main方法正在执行中...."
        print(message5)

if __name__ == '__main__':
    reactor.listenTCP(8800, pb.PBServerFactory(ServerRoot()))
    reactor.run()
```



客户端，代码：

```python
# coding=utf-8
from twisted.internet import reactor
from twisted.spread import pb
def get_main(server_obj):
    message0 = "0. 客户端: 连接服务端, 获取第1个远程服务对象...."
    message1 = "1. 客户端: 请求调用remote_get_main方法"
    print(message0)
    print(message1)
    # 如果远程服务端有提供返回只,则可以通过deferred对象来设置回调方法进行获取
    deferred = server_obj.callRemote("get_main",message0,message1)
    deferred.addCallbacks(get_server_main,errback)

def get_server_main(data):
    message2 = data[0]
    message3 = data[1]
    print(message2)
    print(message3)
    server_obj = data[2]
    message4 = f"4. 客户端: 请求调用remote_server2_main方法"
    print(message4)
    server_obj.callRemote("server2_main", message4)

def errback(failure):
    print("操作错误: ", failure.value)


if __name__ == '__main__':
    factory = pb.PBClientFactory()
    reactor.connectTCP("localhost", 8800, factory)
    deferred1 = factory.getRootObject() # 获取pk连接操作的回调对象
    deferred1.addCallbacks(get_main, errback)
    reactor.run()
```
