#!/bin/env python
#coding:utf-8
#weixin&email合并
import time,datetime
import requests
import json
import commands
import pickle
import argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import sys
from  smtplib  import SMTP_SSL
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.header import Header
reload(sys)
sys.setdefaultencoding('utf8')
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
#weixin
def get_token():
    data='token.pkl'
    try:
        f=file(data,'rb')
        data_dict=pickle.load(f)
        f.close()
    except:
        data_dict={}
    try:
        expires_time=data_dict['expires_time']
    except:
        expires_time=0 
            
    now_time=int(time.mktime(datetime.datetime.now().timetuple()))
    if now_time >= expires_time:
        ###########
        url='https:/'
        ##########
        r=requests.get(url,verify=False)
        result=r.json()

        if len(result) != 0:
            now_time=int(time.mktime(datetime.datetime.now().timetuple()))
            expires_time=now_time+10-10
            result['expires_time']=expires_time
            f=file(data,'wb')
            pickle.dump(result,f)
            f.close()
            access_token=result['access_token']
        else:
            print "Get token error,exit!"
            access_token=''
    else:
        access_token=data_dict['access_token']
    return access_token


def sendmsg(token,content):
    notify_contact= '@all'
    t=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
    content=content+"       "+str(t)
   
    values={
		"touser":notify_contact,
		"msgtype": "text",
		"agentid": 1,
		"text":{
			"content": content.encode('UTF-8')
			
		},
	}
    url='https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='+token
    return requests.post(url,data=json.dumps(values),verify=False)

#email
def send_with_attachment(sub,content,i,contacts):
    smtpHost = 'smtp.exmail.qq.com'
    sslPort  = '465'
    #################
    fromMail = ''
    username = ''
    password = ''
    #############
    toMail   = contacts
    subject = sub
    body     =  content
    encoding = 'utf-8'
    mail = MIMEMultipart('related')
    mail['Subject'] = Header(subject,encoding)
    mail['From'] = fromMail
    mail['To'] = ';'.join(toMail)
    msgText = MIMEText(body._encode(encoding),'html','utf-8')
    mail.attach(msgText)
    with open('/root/py-web/images/'+i+'.png','rb') as fp:
        msgImage = MIMEImage(fp.read())
    msgImage.add_header('Content-ID','<image1>')
    mail.attach(msgImage)
    try:
        smtp = SMTP_SSL(smtpHost,sslPort)
        smtp.ehlo()
        smtp.login(username,password) 
        smtp.sendmail(fromMail,toMail,mail.as_string())
        smtp.close() 
    except  Exception as e:
        print e
def send(sub,content,contacts):
    smtpHost = 'smtp.exmail.qq.com'
    sslPort  = '465'
    toMail   = contacts
    ##############
    fromMail = ''
    username = ''
    password = ''
    #############
    subject = sub
    body     =  content
    encoding = 'utf-8'
    mail = MIMEText(body._encode(encoding),'plain',encoding)
    mail['Subject'] = Header(subject,encoding)
    mail['From'] = fromMail
    mail['To'] = ';'.join(toMail)
    try:
        smtp = SMTP_SSL(smtpHost,sslPort)
        smtp.ehlo()
        smtp.login(username,password) 
        smtp.sendmail(fromMail,toMail,mail.as_string())
        smtp.close() 
    except  Exception as e:
        print e
if __name__ == "__main__":
    token=get_token()
    parser=argparse.ArgumentParser()
    parser.add_argument("content",default=None)
    args = parser.parse_args()
    content=args.content
    sendmsg(token, content)


