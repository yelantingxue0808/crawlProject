代码实现方案链接：https://github.com/yelantingxue0808/crawlProject/tree/main/js%E9%80%86%E5%90%91%E4%B8%93%E9%A2%98%E9%A1%B9%E7%9B%AE/mazhangqu_gov
网页链接：[http://www.zjmazhang.gov.cn/hdjlpt/published?via=pc](http://www.zjmazhang.gov.cn/hdjlpt/published?via=pc)

通过网络抓包工具可以看到  `http://www.zjmazhang.gov.cn/hdjlpt/letter/pubList`
这个是请求数据的接口

![](asset/Pasted%20image%2020260923231648.png)

![](asset/Pasted%20image%2020260923231718.png)

连续多次请求观察到它的cookie是不断变化的，通过`https://curlconverter.com/python/`工具复制粘贴到python中观察请求数据
![](asset/Pasted%20image%2020260923232222.png)

携带着cookie是可以获取到数据的，注释掉cookie或者注释掉X-CSRF-TOKEN令牌的值都会出现异常

![](asset/Pasted%20image%2020260923232338.png)

![](asset/Pasted%20image%2020260923232610.png)

观察请求cookie中的HttpOnly是打勾的可以判断这个cookie是服务器生成的，也就是网页首页加载的时候浏览器向服务器发送请求，服务器返回一个响应数据`set-cookie`给到客户端/浏览器，后续当请求`http://www.zjmazhang.gov.cn/hdjlpt/letter/pubList`这个接口的时候会携带着这个cookie向服务器发送请求，服务器对这个cookie进行身份、期限等数据校验，校验通过即而返回数据；

此时我们需要寻找到请求头的cookie是从哪个包（请求对象）来的，复制`szxx_session`或者它的键对应的值`eyJpdiI6InZlcUh6K2tCck9kYmdpOVdSbUEzY3c9PSIsInZhbHVlIjoibkRPVzFZMEZxT3NaQzQ2VUhTVU1tV0JkNEdPZ1ZyN1R4bFBhSmpnVnNndXdTeldsRWQ2bE83ZGZGZlNzTUJ2ViIsIm1hYyI6ImYzMGVmODJhMzdkZmU0YjU0YWM3YmY5MzJjNGEwYjhiMGQxNjJhMzI5NmVhYWQ1Mjg4ZTc0Mzg3NTA1MGQ2OGQifQ`

![](asset/Pasted%20image%2020260923233824.png)

![](asset/Pasted%20image%2020260923234000.png)

rtl+f输入`szxx_session`关键字进行搜索，定位set-cookie的值 进入到请求对象中观察此时的值和接口请求的cookie是一样的，也就是网页首页加载的时候获取到的cookie;

![](asset/Pasted%20image%2020260923234714.png)

![](asset/Pasted%20image%2020260923234919.png)
X-CSRF-TOKEN通过crtl+shift+f全局搜索定位到位置，令牌一般都是在html中进行生成的，在html`_csrf`关键字搜索确定它是HTML页面生成的，清空cookie在观察它的值

![](asset/Pasted%20image%2020260923235223.png)

![](asset/Pasted%20image%2020260923235244.png)

每次请求`x-csrf-token`的值是不断变化的，对`http://www.zjmazhang.gov.cn/hdjlpt/published`这个页面首页加载的接口通过request工具发送请求


![](asset/Pasted%20image%2020260923235440.png)

得到最终的cookie中的`XSRF-TOKEN`,`szxx_session`以及`x_csrf_token`的值，

将获取对应的值在python中向`http://www.zjmazhang.gov.cn/hdjlpt/letter/pubList`接口发送请求，最终获取数据。