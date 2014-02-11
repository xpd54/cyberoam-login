#!/bin/python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# This file is in the public domain
### END LICENSE

import urllib, sys,time, getpass,base64
from xml.dom.minidom import parseString

import gettext,os
from multiprocessing import Process
from gettext import gettext as _
gettext.textdomain('xpd54-cyberoam')


from gi.repository import Gtk # pylint: disable=E0611
import logging
logger = logging.getLogger('xpd54_cyberoam')
import ctypes
from xpd54_cyberoam_lib import Window
from xpd54_cyberoam.AboutXpd54CyberoamDialog import AboutXpd54CyberoamDialog
from xpd54_cyberoam.PreferencesXpd54CyberoamDialog import PreferencesXpd54CyberoamDialog
# See xpd54_cyberoam_lib.Window.py for more details about how this class works
class Xpd54CyberoamWindow(Window):
    __gtype_name__ = "Xpd54CyberoamWindow"
    def __init__(self):
        pass
    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(Xpd54CyberoamWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutXpd54CyberoamDialog
        self.PreferencesDialog = PreferencesXpd54CyberoamDialog

        # Code for other initialization actions should be added here.
        self.loginbutton = self.builder.get_object("loginbutton")
        self.logoutbutton = self.builder.get_object("logoutbutton")
        self.deletebutton = self.builder.get_object("deletebutton")
        self.resetbutton = self.builder.get_object("resetbutton")
        self.statusbar = self.builder.get_object("statusbar")
        
        
        self.cyberoamAddressInput = self.builder.get_object("cyberoamAddressInput")
        self.usernameInput = self.builder.get_object("usernameInput")
        self.passwdInput = self.builder.get_object("passwdInput")
        
        self.toolbar = self.builder.get_object("toolbar")
        context = self.toolbar.get_style_context()
        context.add_class(Gtk.STYLE_CLASS_PRIMARY_TOOLBAR)
        
        
    def on_loginbutton_clicked(self , widget):
        address = self.cyberoamAddressInput.get_text()
        name = self.usernameInput.get_text()
        pwd = self.passwdInput.get_text()
        argv = 1
        
        
        # processing error
        #try:
         #   x11 = ctypes.cdll.LoadLibrary('libX11.so')
          #  x11.XInitThreads()
        #except:
        #    print "Warning: failed to XInitThreads()"
        #pro = Process(target=self.afunc, args=(address,name,pwd,argv,))
        #pro.start()
        #self.process = pro
        self.runsystem(address,name,pwd,argv)
        
    def afunc(self,address,name,pwd,argv):
        self.runsystem(address,name,pwd,argv)
 
    def on_logoutbutton_clicked(self , widget):
        addressOut = self.cyberoamAddressInput.get_text()
        nameOut = self.usernameInput.get_text()
        pwdOut = self.passwdInput.get_text()
        argv = 0
        self.runsystem(addressOut,nameOut,pwdOut,argv)
            

    def on_deletebutton_clicked(self , widget):
        if os.path.isfile("cyberoam.config"):
            os.remove("cyberoam.config")
        message = "Your all Login Info is Deleted"
        self.usernameInput.set_editable(True)
        self.passwdInput.set_editable(True)
        self.cyberoamAddressInput.set_editable(True)
        self.usernameInput.set_text("")
        self.passwdInput.set_text("")
        self.cyberoamAddressInput.set_text("")
        self.status_remove()
        self.dialog_Info(message)
        
    def on_resetbutton_clicked(self,wedget):
        if os.path.isfile("cyberoam.config"):
            os.remove("cyberoam.config")
        message = "Every Thing is Reset\n Try to Login Again"
        self.usernameInput.set_editable(True)
        self.passwdInput.set_editable(True)
        self.cyberoamAddressInput.set_editable(True)
        self.usernameInput.set_text("")
        self.passwdInput.set_text("")
        self.cyberoamAddressInput.set_text("")
        self.dialog_Info(message)
    id = 0
    cyberoamAddress = "" #the cyberoam login page address
    username = "" #Your username
    passwd = "" #your password.
    sleepsec=1 #login status check every 3 minutes
    def readfile(self,filename):
            try:
                    infile=open(filename,"rU")
            except IOError:
                    return -1
            a=infile.readline()
            if(a==""):
                    print "eeor"
                    return -1
            self.cyberoamAddress=a.rstrip("\r\n")
            a=infile.readline()
            if(a==""):
                    print "eeor"
                    return -1
            self.username=a.rstrip("\r\n")
            a=infile.readline()
            if(a==""):
                    print "eeor"
                    return -1
            self.passwd=base64.b64decode(a.rstrip("\r\n"))
            infile.close()
            return 0
    
    def login(self,show):
            try:
                    file = urllib.urlopen(self.cyberoamAddress+"/login.xml","mode=191&username="+self.username+"&password="+self.passwd+"&a="+(str)((int)(time.time()*1000)))
            except IOError:
                    print "Error connecting"
                    return
            data = file.read()
            file.close()
            dom = parseString(data)
            xmlTag = dom.getElementsByTagName('message')[0].toxml()
            message=xmlTag.replace('<message>','').replace('</message>','')
            xmlTag = dom.getElementsByTagName('status')[0].toxml()
            status=xmlTag.replace('<status>','').replace('</status>','')
            #print message
            if(show == True):
                self.status_pop()
                self.status_push(message)
                #self.dialog_Info(message)
            if(message =="<![CDATA[You have successfully logged in]]>" ):
                self.cyberoamAddressInput.set_editable(False)
                self.usernameInput.set_editable(False)
                self.passwdInput.set_editable(False)
            if(message == "<![CDATA[The system could not log you on. Make sure your password is correct]]>"):
                if os.path.isfile("cyberoam.config"):
                    os.remove("cyberoam.config")
                self.cyberoamAddressInput.set_editable(False)
                self.usernameInput.set_editable(True)
                self.passwdInput.set_editable(True)
                self.passwdInput.set_text("") 
                self.usernameInput.set_text("")
    def check(self):
            try:
                    file = urllib.urlopen(self.cyberoamAddress+"/live?mode=192&username="+self.username+"&a="+(str)((int)(time.time()*1000)))
            except IOError:
                    #print "Error connecting"
                    message = "Error connection"
                    self.dialog_Error(message)
                    return
            data = file.read()
            file.close()
            dom = parseString(data)
            xmlTag = dom.getElementsByTagName('ack')[0].toxml()
            message=xmlTag.replace('<ack>','').replace('</ack>','')
            return message
            
    def logout(self):
            try:
                    file = urllib.urlopen(self.cyberoamAddress+"/logout.xml","mode=193&username="+self.username+"&a="+(str)((int)(time.time()*1000)))
            except IOError:
                    #print "Error connecting"
                    message = "Error connecting"
                    second  = "Pease Enter Address ID and Password"
                    self.dialog_Error(message,second)
                    return
            data = file.read()
            file.close()
            dom = parseString(data)
            xmlTag = dom.getElementsByTagName('message')[0].toxml()
            message=xmlTag.replace('<message>','').replace('</message>','')
            #print message
            self.dialog_Info(message)
            self.status_pop()
            self.status_push(message)
            if(message == "You have successfully logged off"):
                self.cyberoamAddressInput.set_editable(True)
                self.usernameInput.set_editable(True)
                self.passwdInput.set_editable(True)
    
    def printhelp(self):
            print "Usage:\n\tli\t\t\t\tlogin interactively\n\tli -f ./cyberoam.config\t\tlogin with path to configuration file\n\tlo\t\t\t\tlogout"
    
    def runsystem(self,address,name,pwd,argv):
        if(argv==1):
            if(len(sys.argv)>2 and sys.argv[2]=="-f"):
                if(len(sys.argv)>3 and sys.argv[3]!=""):
                    try:
                        infile=open(sys.argv[3],"rU")
                    except IOError:
                            message = "Error reading file"
                            self.dialog_Error(message)
                            return
                    a=infile.readline()
                    if(a==""):
                        message = "Error reading file"
                        self.dialog_Error(message)
                        return
                    self.cyberoamAddress=a.rstrip("\r\n")
                    a=infile.readline()
                    if(a==""):
                        message = "Error reading file"
                        self.dialog_Error(message)
                        return
                    self.username=a.rstrip("\r\n")
                    a=infile.readline()
                    if(a==""):
                        message = "Error reading file"
                        self.dialog_Error(message)
                        return
                    self.passwd=base64.b64decode(a.rstrip("\r\n"))
                    infile.close()
                else:
                    message = "No configuration file"
                    self.dialog_Error(message)
                    return
            else:
                try:
                    infile=open("cyberoam.config","rU")
                    a=infile.readline()
                    if(a==""):
                        #print "Error reading file"
                        message = "Error reading file"
                        self.dialog_Error(message)
                        return
                    self.cyberoamAddress=a.rstrip("\r\n")
                    a=infile.readline()
                    if(a==""):
                        #print "Error reading file"
                        message = "Error reading file"
                        
                        self.dialog_Error(message)
                        return
                    self.username=a.rstrip("\r\n")
                    a=infile.readline()
                    if(a==""):
                        #print "Error reading file"
                        message = "Error reading file"                        
                        self.dialog_Error(message)
                        return
                    self.passwd=base64.b64decode(a.rstrip("\r\n"))
                    infile.close()
                except IOError:
                    a=address#raw_input("Enter full cyberoam site Address (Default: http://172.22.2.2:8090): ")
                    if(a==""):
                        a="http://172.22.2.2:8090"
                    self.cyberoamAddress=a
                    a=name#raw_input("Enter user name: ")
                    if(a==""):
                        #print "empty input. program terminated"
                        message = "Empty input"
                        second = "Pease Enter Address ID and Password"
                        self.dialog_Error(message,second)
                        return
                    self.username=a
                    a=pwd#getpass.getpass("Enter password: ")
                    if(a==""):
                        #print "empty input. program terminated"
                        message = "Enput input"
                        second = "Pease Enter Address ID and Password"
                        self.dialog_Error(message,second)
                        return
                    self.passwd=a
                    try:
                        ofile=open("cyberoam.config","w")
                        ofile.write(self.cyberoamAddress+"\n"+self.username+"\n"+base64.b64encode(self.passwd))
                        ofile.close()
                    except IOError:
                        #print "Warning: could not saving configuration"
                        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.WARNING,Gtk.ButtonsType.OK, "Warning: could not saving configuration")
                        dialog.format_secondary_text("")
                        dialog.run()
                        dialog.destroy()
            #message = "Logging in...."+self.username
            #self.dialog_Info(message)
            status=self.login(True)
        


        elif(argv==0):
            try:
                        infile=open("cyberoam.config","rU")
                        a=infile.readline()
                        if(a==""):
                                a=address#raw_input("Enter full cyberoam site Address (Default: http://172.22.2.2:8090): ")
                                if(a==""):
                                        a="http://172.22.2.2:8090"
                                self.username=name#raw_input("Enter username: ")
                        self.cyberoamAddress=a.rstrip("\r\n")
                        a=infile.readline()
                        if(a==""):
                                a=address#raw_input("Enter full cyberoam site Address (Default: http://172.22.2.2:8090): ")
                                if(a==""):
                                        a="http://172.22.2.2:8090"
                                self.username=name#raw_input("Enter username: ")
                        self.username=a.rstrip("\r\n")                        
                        infile.close()
            except IOError:
                        a=address#raw_input("Enter full cyberoam site Address (Default: http://172.22.2.2:8090): ")
                        if(a==""):
                                a="http://172.22.2.2:8090"
                        self.username=name#raw_input("Enter username: ")
            #message = "Logging out...."+self.username
            #self.dialog_Info(message)
            self.logout()
        else:
            self.printhelp()
        
    def my_timer(self):
        msg=self.check()
        if(msg!="ack"):
            self.login(False)
          
    def dialog_Error(self,message,second=""):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.ERROR,Gtk.ButtonsType.OK, message)
        dialog.format_secondary_text(second)
        dialog.run()
        dialog.destroy()
        
    def dialog_Info(self,message,second=""):
        dialog = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO,Gtk.ButtonsType.CLOSE, message)
        dialog.format_secondary_text(second)
        dialog.run()
        dialog.destroy()
    def status_push(self,message):
        id = self.statusbar.get_context_id("message")
        self.id = id
        self.statusbar.push(id,message)
    def status_pop(self):
        self.statusbar.pop(self.id)
    def status_remove(self):
        self.statusbar.remove_all(self.id)
     
