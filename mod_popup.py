import PySimpleGUI as sg

def popup(e_Mode,file_name):
    sg.popup_ok(file_name + 'が' + e_Mode + 'されました。')

def notify(e_Mode,file_name):
    sg.popup_notify(file_name + 'が' + e_Mode + 'されました。')

def countSucsessfully(count):
    sg.popup_notify(count + '件のファイルが作成されました。')

def countOnWay(count,specify):
    sg.popup_quick(count + '/' + specify + '件のファイルが作成されています。')
