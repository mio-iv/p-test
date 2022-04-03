import win32com.client
import PySimpleGUI as sg

outlook = win32com.client.Dispatch("Outlook.Application")

mail = outlook.CreateItem(0)

def mail(eventMode, filename, meilvalue, addCc):
    sg.popup_ok(filename + 'が' + eventMode + 'されました。\n' + meilvalue)
    # addCcの使い方どうしましょう。