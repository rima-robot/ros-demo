#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
from std_msgs.msg import String
from simple_voice.srv import *
import urllib
import json

state = 0
LAN = 0
file_strs =[]



def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html


def listener():
    rospy.Subscriber("Rog_result", String, callback)

    rospy.spin()

def str_fix(str):
    global file_strs
    result = ""
    for file_str in file_strs:
        file_strs_left= file_str.split('|')[0]
        strs = file_strs_left.split(',')
        b = True
        for ele in strs:
            if ele not in str:
                b=False
                break
        if b:
	    pub_msg(file_str.split('|')[2])
            return file_str.split('|')[1]
    return str
def callback(data):

    words=data.data
    if words !='识别错误':
        s=get_ans(words) 
        pub.publish(s)
        rospy.loginfo(s)

       



def get_ans(info):
    key = '###################此处为key#################'
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='
    request = api + info
    response = getHtml(request)
    dic_json = json.loads(response)
    result = dic_json['text']
    return result


if __name__ == '__main__':
    rospy.init_node("Main")
    rospy.loginfo('开始')
    pub = rospy.Publisher('speak_string', String, queue_size=10)

    # str=raw_input("press to publish")
    listener()   
