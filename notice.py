import configparser
import PySimpleGUI as sg

import sendmail
import mod_popup

config = configparser.ConfigParser()
config.read('config_gui.ini', encoding='utf-8')

sm_def = config['searchMode']['default']
sm_2 = config['searchMode']['second']
sm_3 = config['searchMode']['third']
nm_def = config['noticeMode']['default']
nm_2 = config['noticeMode']['second']
nm_3 = config['noticeMode']['third']
em_1 = config['eventMode']['first']
em_2 = config['eventMode']['second']

fileCount = 0   # 初期化

def noticeMain(eventMode, searchMode, noticeMode, filename, specify, meilvalue, addCc):
    if searchMode == sm_def:    #マルチタイプ
        if noticeMode == nm_def:    # outlookメール
            sendmail.mail(eventMode, filename, meilvalue, addCc)
        elif noticeMode == nm_2:    # 通知
            mod_popup.popup(eventMode, filename)
        else:                       # ポップアップ
            mod_popup.notify(eventMode, filename)
            
            
    if searchMode == sm_2 and filename == specify:    # ファイル名指定 かつ 指定ファイル名と一致するとき
        if noticeMode == nm_def:    # outlookメール
            sendmail.mail(eventMode, filename, meilvalue, addCc)
        elif noticeMode == nm_2:    # 通知
            mod_popup.popup(eventMode, filename)
        else:                       # ポップアップ
            mod_popup.notify(eventMode, filename)        

    if searchMode == sm_3 and eventMode == em_1:      # ファイルカウント
        fileCount = fileCount + 1
        if fileCount == specify:
            mod_popup.countSucsessfully(fileCount)
            fileCount = 0 # 初期化する
        else:   # 未完
            mod_popup.countOnWay(fileCount,specify)
            
    
