# _*_ coding: utf-8 _*_
_author__ = 'marshen'
__date__ = '2019/2/18 17:52'


if __name__ == '__main__':
    # coding: utf-8
    import smtplib
    from email.mime.text import MIMEText
    from email.header import Header

    sender = '13676071720@163.com'
    receiver = '13676071720@163.com'
    subject = 'python email test'
    smtpserver = 'smtp.163.com'
    username = '13676071720@163.com'
    password = 'smj123'

    msg = MIMEText('Hello Python', 'text', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')

    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()
