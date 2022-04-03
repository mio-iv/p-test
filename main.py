# -*- coding: utf-8 -*-
#!/usr/bin/env python

# ファイル監視用モジュール
import os
import time
from numpy import s_
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
# GUI用モジュール
from posixpath import basename
import PySimpleGUI as sg
# import os # かぶりあり
import pandas as pd
import tabula
import configparser
# 他ファイル
import notice

# 設定
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

# 暫定的な関数
def eventdera(detectionfilename,eventMode):
    if values['searchMode'] == sm_2: # ファイル名指定モード
        specify = values['specifyFile']
    elif values['searchMode'] == nm_3: # ファイルカウントモード
        specify = values['specifyCount']
    else: # マルチタイプモード ※指定なし
        specify = ''
    notice.noticeMain(
        eventMode,              # イベントモード（新規作成・更新)
        values['searchMode'],   # 監視モード
        values['noticeMode'],   # 通知モード
        detectionfilename,   # 検知ファイル名
        specify,    # 指定設定
        values['meilvalue'],    # 追加文面
        values['addCc']         # ㏄を追加するかいなか
    )

# イベントハンドラ
class ChangeHandler(FileSystemEventHandler):
 
    # ファイルやフォルダが作成された場合
    def on_created(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        eventdera(filename, em_1)
        
        # print('%sを作成しました。' % filename)
 
    # ファイルやフォルダが更新された場合
    def on_modified(self, event):
        filepath = event.src_path
        filename = os.path.basename(filepath)
        eventdera(filename, em_2)

# メイン処理
if __name__ == '__main__':

    # sg.theme_previewer() # デザインテーマの一覧を表示 どうするかは未定
    sg.theme('sample_desktop')

    layout = [  [sg.Text('フォルダを監視します。')],
            [sg.Text('********************************************************************')],
            [sg.Text('フォルダ', size=(15, 1)), sg.Input(), sg.FolderBrowse('フォルダを選択', key='InputFolderPath')],
            [sg.Text('監視モード', size=(15, 1)), sg.Combo((sm_def, sm_2, sm_3), default_value=sm_def, size=(10, 1), key='searchMode')],
            [sg.Text('通知タイプ', size=(15, 1)), sg.Combo((nm_def, nm_2, nm_3), default_value=nm_def, size=(10, 1), key='noticeMode')],
            [sg.Text('********************************************************************')],
            [sg.Text('指定ファイル設定')],
            [sg.Text('追跡ファイル名を指定', size=(15, 1)), sg.InputText('', size=(20, 1), key='specifyFile')],
            [sg.Text('********************************************************************')],
            [sg.Text('カウント設定')],
            [sg.Text('ファイル数を指定', size=(15, 1)), sg.InputText('', size=(10, 1), key='specifyCount')],
            [sg.Text('********************************************************************')],
            [sg.Text('メールモード設定')],
            [sg.Text('追加メツセージ', size=(15, 1)), sg.InputText('', size=(30, 2), key='meilvalue')],
            [sg.Text('ccの追加', size=(15, 1)), sg.Combo(('あり', 'なし'), default_value='あり', size=(10, 1), key='addCc')],
            [sg.Button('監視開始', key='start'), sg.Button('停止', key='stop')]
        ]
    # ウインドウ起動
    window = sg.Window('フォルダ監視ツール', layout)
    # ウインドウのイベントを受け付けます
    while True:
        windowEvent, values = window.read()

        if windowEvent == sg.WIN_CLOSED:
            break
        
        if windowEvent == 'start':
            if values['InputFolderPath'] == '': # モードと設定値チェック（まだ甘いが暫定案）
                sg.popup_ok('フォルダが指定されていません。')
                break
            elif values['searchMode'] == sm_2 and values['specifyFile'] == '':
                sg.popup_ok('追跡ファイルが指定されていません。')
                break
            elif values['searchMode'] == sm_3 and values['specifyCount'] == '':
                sg.popup_ok('ファイル数が指定されていません')
                break
            else:
                sg.popup_ok('フォルダ監視を開始します。')
                # フォルダパスを取得
                current_directory = os.path.dirname(values['InputFolderPath'])
                # インスタンス作成
                event_handler = ChangeHandler()
                observer = Observer()
                # フォルダの監視
                observer.schedule(event_handler, current_directory, recursive=True)
                # 監視開始
                observer.start()                                     
        
        if windowEvent == 'stop': # [読み取り]ボタンが押されたときの処理
            # 監視の終了
            observer.stop()
            # スレッド停止を待つ
            observer.join()            
            sg.popup_ok('フォルダ監視を終了します。')

    window.close()




