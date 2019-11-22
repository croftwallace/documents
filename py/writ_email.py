import smtplib, getpass
from email.mime.text import MIMEText
import time
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email import encoders
from email.mime.base import MIMEBase
from email.utils import parseaddr, formataddr
from email.mime.image import MIMEImage

 
# host_name = 'smtp.gmail.com'
host_name = 'smtp.qq.com'
# host_name = 'smtp.163.com'
port = 465
 
sender = '1174195985@qq.com'
#receiver = '917247085@qq.com'
receiver = 'libai3101@163.com'
receivers = ['libai3101@163.com','1174195985@qq.com']


#password = getpass.getpass()
password = 'cpzbrzyrbghmjeje'
 
#msg = "Subject: Test Mail Hello from wallace !!!"
#message = MIMEText(content, 'plain', 'utf-8')#正文内容   plain代表纯文本

content='''doc of work'''

file = '邱荣华周报2019-03-08.docx'
 
# 构造一个MIMEMultipart对象代表邮件本身
message= MIMEMultipart()
message.attach(MIMEText(content, 'html', 'utf-8'))# 正文内容   plain代表纯文本,html代表支持html文本
 
message['From'] =sender
message['To'] = ','.join(receivers) #与真正的收件人的邮箱不是一回事
#message['Cc']=','.join(cc_mail) #抄送人
 
subject = 'email'
message['Subject'] = subject  #邮件标题
 
#添加文件到附件
with open(file,'rb') as f:
    # MIMEBase表示附件的对象
    mime = MIMEBase('text', 'txt', filename=file)
    # filename是显示附件名字
    mime.add_header('Content-Disposition', 'attachment', filename=file)
    # 获取附件内容
    mime.set_payload(f.read())
    encoders.encode_base64(mime)
    # 作为附件添加到邮件
    message.attach(mime)    



 
s = smtplib.SMTP_SSL(host_name, port)
s.login(sender, password)
s.sendmail(sender, receivers, str(message))
s.quit()
 
print("Mail sent Successfully")