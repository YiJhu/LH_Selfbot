# -*- coding: utf-8 -*-
'''
LH SELF-BOT V1.0 2019/07/27
            V1.1 2019/08/02
            V1.2 2019/08/15
'''
from linepy import *
import time, os, sys, json, codecs, threading
from time import strftime

mail = ''
passwd = ''
token = ''

try:
    try:
        BOT = LINE(idOrAuthToken=mail, passwd=passwd, appName='IOSIPAD\t9.12.0\tLH Super Core\t11.2.5', systemName='LH Super Core')
        print('Email Login Success!')
    except:
        BOT = LINE(idOrAuthToken=token, appName='IOSIPAD\t9.12.0\tLH Super Core\t11.2.5', systemName='LH Super Core')
        print('Token or QR Login Success!')
except:
    print("Login Failed!")

oepoll = OEPoll(BOT)

settingsOpen = codecs.open("./data/setting.json", "r", "utf-8")
settings = json.load(settingsOpen)

def backupData():
    try:
        backup = settings
        add = codecs.open('./data/setting.json', 'w', 'utf-8')
        json.dump(backup, add, sort_keys=True, indent=4, ensure_ascii=False)
        add.close()
    except Exception as e:
        BOT.log("[BACKUP_DATA] ERROR : " + str(e))

def SEND_MESSAGE(op):
    msg = op.message
    text = msg.text
    msg_id = msg.id
    receiver = msg.to
    sender = msg._from
    try:
        if msg.contentType == 0:
            try:
                if msg.toType == 0:
                    if text == "#help":
                        BOT.sendMessage(receiver, "【HELP COMMAND】\n[#me]\n[#mid]\n[#you]\n[#you mid]\n[#time]\n[#tag you]\n[#tag me]")
                    if text == "#me":
                        BOT.sendContact(receiver, sender)
                    if text == "#mid":
                        BOT.sendMessage(receiver, sender)
                    if text == "#you":
                        BOT.sendContact(receiver, receiver)
                    if text == "#you mid":
                        BOT.sendMessage(receiver, receiver)
                    if text == "#tag you":
                        BOT.sendMessageWithMention(receiver, '',[receiver])
                    if text == "#tag me":
                        BOT.sendMessageWithMention(receiver, '',[sender])
                    if text == "#time":
                        now = strftime('%Y-%m-%d %I:%M:%S')
                        BOT.sendMessage(receiver, "Now Time: %s"  % (now))
                if msg.toType == 2:
                    if text == "#help":
                        BOT.sendMessage(receiver,
                                        "【LH SELF BOT HELP COMMAND】\n[#speed]\n[#me]\n[#profile]\n[#mid]\n[#mid:Tag]\n[#gid]\n[#getcontact:Mid]\n[#gowner]\n[#ginfo]\n[#time]\n[#In:Tags]\n[#in:Mid]\n[#tag me]\n[#Tag:Mid]\n[#kick:Mid]\n[#Mk:Tags]\n[#Nk:Name]\n[#Kickall]\n[#time]\n[#Set]")
                    if text =="#speed":
                        TimeS = time.time()
                        BOT.sendMessage(receiver, "...")
                        TimeE = time.time()
                        BOT.sendMessage(receiver, "Speed is: %s s" % (TimeE - TimeS,))
                    if text == "#me":
                        BOT.sendContact(receiver, sender)
                    if text == "#profile":
                        x = BOT.getProfile()
                        BOT.sendMessage(receiver,"【Profile Info】\nName：%s\nMid：%s\nUserid：%s\nPhone Number：%s\nE-Mail：%s\nRegion Code：%s\nThumbnail Url：%s\nAllow Search By Userid：%s\nAllow Search By Email：%s\nPicture Url：\nhttps://profile.line-scdn.net%s\nMusic Profile：%s\nVideo Profile：%s" % (x.displayName, x.mid, x.userid, x.phone, x.email, x.regionCode, x.thumbnailUrl, x.allowSearchByUserid, x.allowSearchByEmail, x.picturePath, x.musicProfile, x.videoProfile))
                    if text == "#mid":
                        BOT.sendMessage(receiver, sender)
                    if "#mid:" in text:
                        key = eval(msg.contentMetadata["MENTION"])
                        key1 = key["MENTIONEES"][0]["M"]
                        key = BOT.getContact(key1)
                        BOT.sendMessage(receiver, "" + key1)
                    if text == "#gid":
                        BOT.sendMessage(receiver, receiver)
                    if "#getcontact:" in text:
                        key = text[-33:]
                        try:
                            contact = BOT.getContact(key)
                            BOT.sendContact(receiver, key)
                        except:
                            pass
                    if text == "#gowner":
                        try:
                            group = BOT.getGroup(receiver)
                            GS = group.creator.mid
                            BOT.sendMessageWithMention(receiver, '',[GS])
                            BOT.sendContact(receiver, GS)
                        except:
                            W = group.members[0].mid
                            BOT.sendMessageWithMention(receiver, 'The original group creator has deleted the account.\nThis is the inherited group creator!\n',[W])
                            BOT.sendContact(receiver, W)
                    if text == "#ginfo":
                        G = BOT.getGroup(receiver)
                        md = "【Group Info】"
                        md += "\n[Group Name]\n" + G.name
                        md += "\n[Group Id]\n" + G.id
                        if G.creator == None: md += "\n[Group Creator]\n" + G.members[0].displayName + " (Inherit)"
                        else: md += "\n[Group Creator]\n" + G.creator.displayName
                        md += "\n[Group Profile]\nhttps://profile.line-scdn.net/%s" % G.pictureStatus
                        md += "\n[Created Time]\n"+ time.strftime('%Y-%m-%d %I:%M:%S %p', time.localtime(G.createdTime/1000))
                        if G.invitee is None: md += "\n----------------------------------------\nMembers： " + str(len(G.members)) + "\nInvitation： 0"
                        else: md += "\n----------------------------------------\nMembers： " + str(len(G.members)) + "\nInvitation： " + str(len(G.invitee))
                        if G.preventedJoinByTicket is False: md += "\nInvitation Url： Allowed."
                        else: md += "\nInvitation Url： Blocked."
                        BOT.sendMessage(receiver, md)
                    if text == "#time":
                        now = strftime('%Y-%m-%d %I:%M:%S')
                        BOT.sendMessage(receiver, "Now Time： %s"  % (now))
                    if text == "#in:":
                        mid = text[4:37]
                        BOT.findAndAddContactsByMid(mid) and BOT.inviteIntoGroup(receiver, [mid])
                    if "#In:" in text:
                        key = eval(msg.contentMetadata["MENTION"])
                        key["MENTIONEES"][0]["M"]
                        targets = []
                        for x in key["MENTIONEES"]:
                            targets.append(x["M"])
                        for target in targets:
                            BOT.findAndAddContactsByMid(target) and BOT.inviteIntoGroup(receiver, [target])
                    if text == "#tag me":
                        BOT.sendMessageWithMention(receiver, '', [sender])
                    if "#Tag:" in text:
                        mid = text[-33:] 
                        BOT.sendMessageWithMention(receiver, '', [mid])
#---------------------KiCK_ONLY---------------------#
                    if "#kick:" in text:
                        if msg.toType == 2:
                            key = text[-33:]
                            try:
                                BOT.kickoutFromGroup(receiver, [key])
                            except:
                                pass
                    if "#Mk:" in text:
                        if msg.toType == 2:
                            key = eval(msg.contentMetadata["MENTION"])
                            key["MENTIONEES"][0]["M"]
                            targets = []
                            for x in key["MENTIONEES"]:
                                targets.append(x["M"])
                            for target in targets:
                                BOT.kickoutFromGroup(receiver, [target])
                    if "#Nk:" in text:
                        if msg.toType == 2:
                            str1 = text[4:].lower()
                            gs = BOT.getGroup(receiver)
                            targets = []
                            for g in gs.members:
                                if str1 in g.displayName:
                                    if str1 == '':
                                        pass
                                    else:
                                        targets.append(g.mid)
                            if targets == []:
                                pass
                            else:
                                for target in targets:
                                    BOT.kickoutFromGroup(receiver, [target])
                    if text == "#Kickall":
                        if msg.toType == 2:
                            if settings['K-lock'] == True:
                                try:
                                    X = BOT.getGroup(receiver)
                                    for x in X.members:
                                        BOT.kickoutFromGroup(receiver, [str(x.mid)])
                                except:
                                    pass
                            else:
                                print("\'K-lock\' is not on <true>")
                                BOT.sendMessage(receiver, "Sorry, this function is lock now.")
#---------------------KiCK_ONLY---------------------#

#---------------------File_ONLY---------------------#
#DEL THIS FN. 
#---------------------File_ONLY---------------------#

#---------------------Switch_ONLY---------------------#
                    if text == "#Set":
                        BOT.sendMessage(receiver, "【LH SELF BOT SET COMMAND】\n[#ALR:ON/OFF]\n[#AFM:ON/OFF]\n[#AJG:ON/OFF]\n[#ARG:ON/OFF]\n[#AGM:ON/OFF]\n[#Rename:]")
                    if "#ALR:" in text:
                        str1 = text[5:]
                        try:
                            if str1.lower() == "on":
                                try:
                                    settings['A-LeaveR'] = True
                                    backupData()
                                    BOT.sendMessage(receiver, "Auto Leave Room On.")
                                except:
                                    pass
                            elif str1.lower() == "off":
                                try:
                                    settings['A-LeaveR'] = False
                                    backupData()
                                    BOT.sendMessage(receiver, "Auto Leave Room Off.")
                                except:
                                    pass
                        except:
                            pass
                    if "#AFM:" in text:
                        str1 = text[5:]
                        try:
                            if str1.lower() == "on":
                                try:
                                    settings['A-ADDMSG'] = True
                                    backupData()
                                    BOT.sendMessage(receiver, "Auto Add Friend Message On.")
                                except:
                                    pass
                            elif str1.lower() == "off":
                                try:
                                    settings['A-ADDMSG'] = False
                                    backupData()
                                    BOT.sendMessage(receiver, "Auto Add Friend Message Off.")
                                except:
                                    pass
                        except:
                            pass
                    if "#AJG:" in text:
                        str1 = text[5:]
                        try:
                            if str1.lower() == "on":
                                try:
                                    settings['A-JOIN'] = True
                                    backupData()
                                    BOT.sendMessage(receiver, "Auto Join Group On.")
                                except:
                                    pass
                            elif str1.lower() == "off":
                                try:
                                    settings['A-JOIN'] = False
                                    backupData()
                                    BOT.sendMessage(receiver, "Auto Join Group Off.")
                                except:
                                    pass
                        except:
                            pass
                    if "#ARG:" in text:
                        str1 = text[5:]
                        try:
                            if str1.lower() == "on":
                                try:
                                    settings['A-REJECTG'] = True
                                    backupData()
                                    BOT.sendMessage(receiver, "Auto Reject Group Invitation On.")
                                except:
                                    pass
                            elif str1.lower() == "off":
                                try:
                                    settings['A-REJECTG'] = False
                                    backupData()
                                    BOT.sendMessage(receiver, "Auto Reject Group Invitation Off.")
                                except:
                                    pass
                        except:
                            pass
                    if "#AGM:" in text:
                        str1 = text[5:]
                        try:
                            if str1.lower() == "on":
                                try:
                                    settings['A-JOIN_MSG'] = True
                                    backupData()
                                    BOT.sendMessage(receiver, "Auto Group Join Welcome MSG On.")
                                except:
                                    pass
                            elif str1.lower() == "off":
                                try:
                                    settings['A-JOIN_MSG'] = False
                                    backupData()
                                    BOT.sendMessage(receiver, "Auto Group Join Welcome MSG Off.")
                                except:
                                    pass
                        except:
                            pass
                    if "#Rename:" in text:
                        str1 = text[8:]
                        profile = BOT.getProfile()
                        profile.displayName = str1
                        BOT.updateProfile(profile)
                        BOT.sendMessage(receiver, "[Successfully Changed Name]\n->" + str1 + "\n" + strftime('%H:%M:%S'))
                            
#---------------------Switch_ONLY---------------------#

#---------------------THIS_IS_INVITE_BOT_ONLY---------------------#
#DEL THIS FN.
#---------------------THIS_IS_INVITE_BOT_ONLY---------------------#

            except:
                pass
    except Exception as e:
        BOT.log("[SEND_MESSAGE] ERROR : " + str(e))

def NOTIFIED_INVITE_INTO_ROOM(op):
    try:
        if settings['A-LeaveR'] == True:
            try:
                BOT.leaveRoom(op.param1)
                BOT.log("Invite Room")
            except:
                pass
    except Exception as e:
        BOT.log("[NOTIFIED_INVITE_INTO_ROOM] ERROR : " + str(e))

def NOTIFIED_LEAVE_ROOM(op):
    try:
        if settings['A-LeaveR'] == True:
            try:
                BOT.leaveRoom(op.param1)
                BOT.log("Leave Room")
            except:
                pass
    except Exception as e:
        BOT.log("[NOTIFIED_LEAVE_ROOM] ERROR : " + str(e))

def NOTIFIED_INVITE_INTO_GROUP(op):
    try:
        if settings['A-JOIN'] == True:
            try:
                BOT.acceptGroupInvitation(op.param1)
            except:
                pass
        if settings['A-REJECTG'] == True:
            try:
                BOT.rejectGroupInvitation(op.param1)
            except:
                pass
    except Exception as e:
        BOT.log("[NOTIFIED_INVITE_INTO_GROUP] ERROR : " + str(e))

def NOTIFIED_ACCEPT_GROUP_INVITATION(op):
    try:
        if settings['A-JOIN_MSG'] == True:
            try:
                BOT.sendMessage(op.param1, "Welcome\t" + BOT.getContact(op.param2).displayName + "\tto join us.")
            except:
                pass
    except Exception as e:
        BOT.log("[NOTIFIED_ACCEPT_GROUP_INVITATION] ERROR : " + str(e))

def NOTIFIED_LEAVE_GROUP(op):
    try:
        pass
    except Exception as e:
        BOT.log("[NOTIFIED_LEAVE_GROUP] ERROR : " + str(e))

def NOTIFIED_ADD_CONTACT(op):
    try:
        if settings['A-ADDMSG'] == True:
            add = open("./data/add.txt", "r")
            AddListedMid = add.readline()
            add.close()
            if op.param1 in AddListedMid:
                pass
            else:
                add = open("./data/add.txt", "a")
                add.write(str(op.param1))
                add.close()
                BOT.log("Add " + op.param1 + " to AddListed Mid Name: " + BOT.getContact(op.param1).displayName)
                BOT.sendMessage(op.param1, "Hi,\t" + BOT.getContact(op.param1).displayName + "\tThank you for adding my friend.")
        else:
            add = open("./data/add.txt", "r")
            AddListedMid = add.readline()
            add.close()
            if op.param1 in AddListedMid:
                pass
            else:
                add = open("./data/add.txt", "a")
                add.write(str(op.param1))
                add.close()
                BOT.log("Add " + op.param1 + " to AddListed Mid Name: " + BOT.getContact(op.param1).displayName)
    except Exception as e:
        BOT.log("[NOTIFIED_ADD_CONTACT] ERROR : " + str(e))

oepoll.addOpInterruptWithDict({
    OpType.SEND_MESSAGE: SEND_MESSAGE,
    OpType.NOTIFIED_INVITE_INTO_GROUP: NOTIFIED_INVITE_INTO_GROUP,
    OpType.NOTIFIED_INVITE_INTO_ROOM: NOTIFIED_INVITE_INTO_ROOM,
    OpType.NOTIFIED_ACCEPT_GROUP_INVITATION: NOTIFIED_ACCEPT_GROUP_INVITATION,
    OpType.NOTIFIED_LEAVE_ROOM: NOTIFIED_LEAVE_ROOM,
    OpType.NOTIFIED_LEAVE_GROUP: NOTIFIED_LEAVE_GROUP,
    OpType.NOTIFIED_ADD_CONTACT: NOTIFIED_ADD_CONTACT
    })

while True:
    oepoll.trace()
