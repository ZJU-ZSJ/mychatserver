# -*- coding=utf-8 -*-
from flask import render_template, redirect, url_for, flash,request,session
from flask_login import login_required, login_user, logout_user,current_user
from app.admin import admin
from app import db
from app.models import User,Message
import json,collections

@admin.route('/login', methods=['POST'])
def login():
    username_temp = request.args.get('username')
    passwd_temp = request.args.get('passwd')
    if passwd_temp=='' or username_temp=='':
        return "empty username or password"
    user = User.query.filter_by(username=username_temp).first()
    if user is None:
        "not exist username"
    if user is not None and user.verify_password(passwd_temp):
        login_user(user)
        return "success"
    return "wrong password"

@admin.route('/register', methods=['POST'])
def register():
    username_temp = request.args.get('username')
    passwd_temp = request.args.get('passwd')
    email_temp = request.args.get('email')
    phone_temp = request.args.get('phone')
    user = User.query.filter_by(username=username_temp).first()
    if user is not None:
        return "username existed"
    try:
        user = User(username=username_temp, password=passwd_temp,email = email_temp,phone = phone_temp)
        print(user.password_hash)
        print(user.username)
        db.session.add(user)
        print('done')
        print('done')
        return "success"
    except:
        return "username existed"

@admin.route('/sendmsg', methods=['POST'])
def sendmsg():
    username_temp = request.args.get('username')
    content_temp = request.args.get('content')
    try:
        message = Message(username=username_temp, content=content_temp)
        db.session.add(message)
        print(Message.query.order_by(Message.id.desc()).first().id)
        return str(Message.query.order_by(Message.id.desc()).first().id)
    except:
        return "failed"

@admin.route('/getmsg', methods=['POST'])
def getmsg():
    i=0
    msg_json=collections.OrderedDict()
    last_temp = request.args.get('last')
    if last_temp == -1:
        for msg in Message.query.order_by(Message.id.desc()).all():
            print msg.id
            msg_json[i] = {"content":msg.content,"username":msg.username,"id":msg.id} 
            i = i+1
        msg_temp = json.dumps(msg_json)
    else:
        for msg in Message.query.filter(Message.id>last_temp).order_by(Message.id.desc()):
            print msg.id
            msg_json[i] = {"content":msg.content,"username":msg.username,"id":msg.id} 
            i = i+1
        msg_temp = json.dumps(msg_json)
    return msg_temp