# 1. 内容分析

开发一个简单的邮件客户端，将邮件（文字和图片）发送给任意收件人。你的客户端将需要连接到邮件服务器，使用SMTP 协议与邮件服务器进行对话，并向邮件服务器发送电子邮件。同时，本次实验不能使用Python的`smtplib `的模块，而只使用`socket`库完成设计。本次实验将实现一个SMTP客户端，使用QQ邮箱作为发件人，向指定的另一个QQ邮箱发送一封邮件。

SMTP定义了邮件客户端与SMTP 服务器之间，以及两台SMTP 服务器之间发送邮件的通信规则。SMTP 协议属于TCP/IP 协议族，通信双方采用一问一答的命令/响应形式进行对话，且定了对话的规则和所有命令/响应的语法格式。



# 2. 设计方法

使用Python和socket库进行编程，构建一个`Email`类，初始化根据用户信息与服务器建立连接。之后获取文字内容和图片进行邮件发送。本次实验的基本流程如下：

1. 与QQ邮件服务器建立TCP连接，域名`smtp.qq.com`，SMTP默认端口号25。建立连接后服务器将返回状态码`220`，代表服务就绪（类似HTTP，SMTP也使用状态码通知客户端状态信息）。
2. 发送`HELO`命令，开始与服务器的交互，服务器将返回状态码`250`（请求动作正确完成）。
3. 发送`AUTH LOGIN`命令，开始验证身份，服务器将返回状态码`334`（服务器等待用户输入验证信息）。
4. 发送**经过base64编码**的用户名，服务器将返回状态码`334`（服务器等待用户输入验证信息）。
5. 发送**经过base64编码**的密码，本次使用QQ邮箱分配的认证码进行登录，服务器将返回状态码`235`（用户验证成功）。
6. 发送`MAIL FROM`命令，并包含发件人邮箱地址，服务器将返回状态码`250`（请求动作正确完成）。
7. 发送`RCPT TO`命令，并包含收件人邮箱地址，服务器将返回状态码`250`（请求动作正确完成）。
8. 发送`DATA`命令，表示即将发送邮件内容，服务器将返回状态码`354`（开始邮件输入，以”.”结束）。
9. 发送邮件内容，包括文字和图片附件，服务器将返回状态码`250`（请求动作正确完成）。
10. 发送`QUIT`命令，断开与邮件服务器的连接。

上传的代码文件中删去了邮箱号和对应的密码。



# 3. 结果分析

SMTP协议为一问一答的形式，所以对整个过程的中客户端收到的应答进行打印，结果如下，可以看到整个过程的所有连接接收到正确的应答。

![image-20201230020442584](https://github.com/Thooooor/SMTPEmail/blob/master/README.assets/image-20201230020442584.png?raw=true)

最终在邮箱收到发送的邮件，包含标题、文字内容和图片附件。

![image-20201230020630267](https://github.com/Thooooor/SMTPEmail/blob/master/README.assets/image-20201230020630267.png?raw=true)

