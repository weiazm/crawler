# coding:utf-8
from Tkinter import *

root = Tk()
root.wm_title(u"汽车之家虚假评论识别系统")  # 定义窗口标题
root.geometry('700x500')  # 窗口大小
root.resizable(width=False, height=False)  # 窗口大小不可变

tagPW = PanedWindow(root)
listb = Listbox(root)
listb2 = Listbox(root)
tagPW.pack()
listb.pack()
listb2.pack()
root.mainloop()
