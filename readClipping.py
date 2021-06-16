#!/usr/bin/env python
# -*- coding: utf-8 -*-
import collections
import json
import os
import re
import random
import smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from secrets import password

BOUNDARY = u"==========\r\n"
DATA_FILE = u"clips.json"
OUTPUT_DIR = u"output"
sendMailArray = []

def get_sections(filename):
    with open(filename, 'rb') as f:
        content = f.read().decode('utf-8')
    content = content.replace(u'\ufeff', u'')
    return content.split(BOUNDARY)


def get_clip(section):
    clip = {}

    lines = [l for l in section.split(u'\r\n') if l]
    if len(lines) != 3:
        return

    clip['book'] = lines[0]
    match = re.search(r'(\d+)-\d+', lines[1])
    if not match:
        return
    position = match.group(1)

    clip['position'] = int(position)
    clip['content'] = lines[2]

    return clip


def export_txt(clips):
    """
    Export each book's clips to single text.
    """

    for book in clips:
        # for every book sort quotes
        loc= sorted(clips[book])
        #pick a random quote to append
        x = random.randint(0,len(loc)-1)
        sendMailArray.append(book+" : "+clips[book][loc[x]])
    print(sendMailArray,"\n")
    sendMail(sendMailArray)


def load_clips():
    """
    Load previous clips from DATA_FILE
    """
    try:
        with open(DATA_FILE, 'rb') as f:
            return json.load(f)
    except (IOError, ValueError):
        return {}


def save_clips(clips):
    """
    Save new clips to DATA_FILE
    """
    with open(DATA_FILE, 'w') as f:
        json.dump(clips, f)

def sendMail(sendMailArray):
    # add sender and receiver
    senderEmail = "senderemail@gmail.com"
    recvEmail="receiveremail@gmail.com"
    smtpServer = "smtp.gmail.com"
    port = 587  # For starttls
    # Create a secure SSL context
    context = ssl.create_default_context()
    subject = "Your Daily Quotes"
    #create the email by extracting quotes
    body=""
    for entry in sendMailArray:
        body += "\n\n"+entry
    print(body)

    message = MIMEMultipart()
    message["From"] = senderEmail
    message["To"] = recvEmail
    message["Subject"] = subject
    message["Bcc"] = recvEmail  # Recommended for mass emails
    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()
    # Try to log in to server and send email
    try:
        server = smtplib.SMTP(smtpServer,port)
        server.ehlo() # Can be omitted
        server.starttls(context=context) # Secure the connection
        server.ehlo() # Can be omitted
        server.login(senderEmail, password)
        server.sendmail(senderEmail,recvEmail,text)
        print(body, " sent to ", recvEmail)
    except Exception as e:
        # Print any error messages to stdout
        print(e)
    finally:
        server.quit()

def main():
    # load old clips
    clips = collections.defaultdict(dict)
    clips.update(load_clips())

    # extract clips
    sections = get_sections(u'My Clippings.txt')
    for section in sections:
        clip = get_clip(section)
        if clip:
            clips[clip['book']][str(clip['position'])] = clip['content']

    # remove key with empty value
    clips = {k: v for k, v in clips.items() if v}

    # save/export clips
    save_clips(clips)
    export_txt(clips)


if __name__ == '__main__':
    main()