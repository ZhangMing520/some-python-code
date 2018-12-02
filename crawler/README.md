1. handler处理器和自定义opener
- opener是urllib2.OpenerDirector的实例，我们之前一直使用urlopen，他是一个特殊的opener（也是模块帮我们构建好的）
- 但是基本的urlopen()方法不支持代理、cookie等其他的http/https高级功能。所以要支持这些功能：
    1. 使用相关的handler处理器来创建特定动能的处理器对象；
    2. 然后通过urllib2.build_opener()方法使用这些处理器对象，来创建自定义opener对象；
    3. 使用自定义的opener对象，调用open()方法发送请求
- 如果程序所有的请求都使用自定义的opener，可以使用urllib2.install_opener()将自定义的opener对象定义为全局opener，表示如果之后凡是调用urlopen，都将使用这个opener（根据自定的需求来选择）

2. cookielib库和 HTTPCookieProcesser 处理器
- cookielib模块：朱啊哟作用是提供用于存储cookie的对象
- HTTPCookieProcesser 处理器：主要作用是处理这些 cookie 对象，并构建 handler 对象

3. cookielib 主要包含对象有 CookieJar,FileCookieJar,MozillaCookieJar,LWPCookieJar
- CookieJar：管理http cookie 值，存储http请求生成的cookie，向传出的http请求添加cookie的对象。整个cookie都存储在内存中，对CookieJar实例进行垃圾回收后cookie也将丢失
- FileCookieJar(filename=None, delayload=False, policy=None)：从CookieJar派生而来，用来创建FileCookieJar实例，检索cookie信息并将cookie存储到文件中。filename是存储cookie的文件名。delayload为True时支持延迟访问文件，即只有在需要时才读取文件或在文件中存储数据
- MozillaCookieJar(filename, ignore_discard, ignore_expires)：从FileCookieJar派生而来，创建于 Mozilla 浏览器 cookie.txt 兼容的FileCookieJar实例
- LWPCookieJar(filename, ignore_discard, ignore_expires)：从FileCookieJar派生而来，创建于 libwww-perl标准的 Set-Cookie3 文件格式兼容的FileCookieJar实例
```
    大多数情况下，我们只用 CookieJar() , 如果需要和本地文件交互，就用 LWPCookieJar(),MozillaCookieJar()
```

3. json
- json.loads()  把json格式字符串解码成python对象，数据类型对照

| json  | python |
| ----- | ----- |
|object |dict|
|array  |list|
|string |unicode|
|number(int)|int,long|
|number(real)|float|
|true   |True|
|false  |False|
|null   |None|
- json.dumps() 实现python类型转化为json类型，返回str对象 ，使用的时候禁用 ascii 编码，ensure_ascii=False

| python| json   |
| ----- | ----- |
|dict   |object |
|list   |array |
|unicode|string |
|int,long |number(int)|
|float  |number(real)|
|True   |true|
|False  |false|
|None   | null |

- json.dump() python转化为json对象之后写入文件
- json.load() 读取文件中json对象转化为python类型

4. JsonPath

| xpath| jsonpath  | 描述 |
| ----- | ----- | ----- |
|   /   |$ | 根节点 |
|   .   |@ | 现行节点 |
|   /   |. or [] | 取子节点 |
|   ..   |无 | 取父节点 |
|   //   |.. | 选取所有符合条件的 |
|   *   |*| 匹配所有元素节点 |
|   @   |无 | 根据属性访问 |
|   []  |[] | 迭代器标示（可以在里面做简单的迭代操作，如数组下标，根据内容选值等） |
|   &#124;（竖线）   |[,] | 支持迭代器中做多选 |
|   []   |?() | 支持过滤操作 |
|   无   |() | 支持表达式计算 |
|   ()   |无 | 分组 |


5. scrapy 
- scrapy engine（引擎）：负责 spider 、downloader、scheduler中间的通讯，信号，数据传递等
- scheduler（调度器）：它负责接收 engine 发送过来的Request请求，并按照一定的方式进行排列，入队，当 engine 需要时，还给 engine
- downloader（下载器）：负责下载 engine 发送过来的Request请求，并将其获取到的Response交还给 engine，由 engine 交个 spider 处理
- spider（爬虫）：负责处理所有的Response，从中分析提取数据，获取 Item 字段需要的数据，并将需要跟进的 URL 提交给 engine，再次进入 scheduler（调度器）
- Item Pipeline（管道）：负责处理 spider 中获取到的 Item，并进行后期处理（详细分析，过滤，存储的等）
- Downloader Middlewares（下载中间件）：可以当做是一个可以自定义扩展下载功能的组件
- spider Middlewares（spider中间件）：可以理解是一个自定义扩展和操作 engine 和 spider 中间通信功能的组件（比如进入 spider的Response，从spider出去的Request）

- 制作爬虫的4步
    - 新建一个爬虫项目（scrapy startproject xxx）
    - 明确目标（编写items.py）：明确你想要爬取的目标
    - 制作爬虫（spiders/xxspider.py）:制作爬虫开始爬取网页
    - 内容存储（pipelines.py）:设计管道存储爬取内容
