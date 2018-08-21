# -*- coding: utf-8 -*-

from linepy import *
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
from humanfriendly import format_timespan, format_size, format_number, format_length
import time, random, sys, json, codecs, threading, glob, re, string, os, requests, subprocess, six, ast, pytz, urllib, urllib.parse
from gtts import gTTS
from googletrans import Translator

load_dotenv(find_dotenv())

LINE_EMAIL = os.getenv('LINE_EMAIL')
LINE_PASS = os.getenv('LINE_PASS')

line= LINE(LINE_EMAIL, LINE_PASS)

oepoll = OEPoll(line)

prohibitedWords = ['Asu', 'Jancuk', 'Tai']
userTemp = {}
userKicked = []

def TERIMA_PESAN(op):
    try:
        msg = op.message

        text = msg.text
        receiver = msg.to
        sender = msg._from
        msg_id = msg.id

        # Jika kita menerima pesan dari grup
        if msg.toType == 2:
            var_dump(userTemp)
            displayName = line.getContact(sender).displayName
            if text in prohibitedWords:

                if sender in userTemp:
                    userTemp[sender] = userTemp.get(sender) + 1

                    # Jika sudah melebihi dari 3, maka akan terkick
                    if userTemp.get(sender) > 3:
                        userKicked.append(sender)
                        line.kickoutFromGroup(receiver, userKicked)
                        line.log("{} telah terkick dari grup".format(displayName))
                        userTemp.pop(sender)
                else:
                    userTemp[sender] = 1
    except Exception as e:
        line.log(str(e))


oepoll.addOpInterruptWithDict({
    OpType.RECEIVE_MESSAGE : TERIMA_PESAN
})

while True:
    oepoll.trace()
