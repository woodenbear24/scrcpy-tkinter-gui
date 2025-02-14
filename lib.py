import os
import subprocess
import tkinter as tk
import xml.etree.cElementTree as ET
from tkinter import Listbox, Entry, Button, Scrollbar, Frame, Message, PhotoImage, ttk

path = 'gui_config.xml'
process = None


def Refresh_Devices(entry0, event):
    process = subprocess.run("adb devices", shell=True, capture_output=True, text=True, check=True)
    devicelist = process.stdout.strip().splitlines(True)
    devicelist.pop(0)
    print(devicelist)
    for i in range(len(devicelist)):
        devicelist[i] = devicelist[i].split('\t')[0]
    print(devicelist)
    entry0.config(values=devicelist)
    return 0


def Refresh_List(entry0, listbox):
    try:
        device = entry0.get()
        process = subprocess.run(f"adb -s {device} shell pm list packages -3", shell=True, capture_output=True,
                                 text=True, check=True)
        str = process.stdout.strip()
        applist = str.splitlines(True)
        for i in range(len(applist)):
            applist[i] = applist[i][8:]
            applist[i] = applist[i].strip()
        print(applist)
        listbox.delete(0, tk.END)
        for item in applist:
            listbox.insert(tk.END, item)
    except Exception:
        print(f"Scan app Err:{Exception}")
    return 0


def Select_List(listbox, entry1, event):
    selected = listbox.curselection()
    if selected:
        selected_item = listbox.get(selected)
        print(f"Selected:{selected_item}")
        entry1.delete(0, tk.END)
        entry1.insert(0, selected_item)
    return 0


def Setting(entry2, entry3, entry4, mode):
    if not os.path.exists(path):
        print("No config")
        try:
            with open(path, "w") as f:
                f.write("""<?xml version='1.0' encoding='utf-8'?> <settings><bitrate>5</bitrate><codec>h264</codec><arg>-S -w --shortcut-mod=lctrl --power-off-on-close</arg><cmd></cmd></settings>""")
            print("Empty config generated")
        except Exception:
            pass
    if mode == 0:
        Dic = Xml_Read()
        entry2.delete(0, tk.END)
        entry2.insert(0, Dic["bitrate"])
        entry3.delete(0, tk.END)
        entry3.insert(0, Dic['codec'])
        entry4.delete(0, tk.END)
        entry4.insert(0, Dic['arg'])
    elif mode == 1:
        bitrate = entry2.get()
        codec = entry3.get()
        arg = entry4.get()
        Xml_Write(bitrate, codec, arg)
    else:
        pass
    return 0


def Xml_Read():
    Dic = {}
    try:
        tree = ET.parse(path)
        root = tree.getroot()

        # 查找并获取 bitrate 参数
        bitrate_element = root.find('bitrate')
        if bitrate_element is not None:
            Dic['bitrate'] = bitrate_element.text
        else:
            Dic['bitrate'] = None

            # 查找并获取 codec 参数
        codec_element = root.find('codec')
        if codec_element is not None:
            Dic['codec'] = codec_element.text
        else:
            Dic['codec'] = None

        # 查找并获取 arg 参数
        arg_element = root.find('arg')
        if arg_element is not None:
            Dic['arg'] = arg_element.text
        else:
            Dic['arg'] = None

        print(f"Setting:{Dic}")
    except Exception:
        print(f"Err:{Exception}")
        pass
    return Dic


def Xml_Write(bitrate, codec, arg):
    try:
        # 1. 创建根元素
        root = ET.Element("settings")

        # 2. 创建子元素 bitrate 并设置文本
        bitrate_element = ET.SubElement(root, "bitrate")
        bitrate_element.text = str(bitrate)

        # 3. 创建子元素 codec 并设置文本
        codec_element = ET.SubElement(root, "codec")
        codec_element.text = str(codec)

        # 4. 创建子元素 arg 并设置文本
        arg_element = ET.SubElement(root, "arg")
        arg_element.text = str(arg)
        # 5. 创建 XML 树
        tree = ET.ElementTree(root)

        # 6. 写入 XML 文件
        tree.write(path, encoding="utf-8", xml_declaration=True)
        print(f"Saved")

    except Exception:  # 捕获写入过程中可能发生的异常
        print(f"Err:{Exception}")
    return 0


def cmd_generate(entry0, entry1, entry2, entry3, entry4):
    global process
    # try:
    #     process.kill()
    # except:
    #     pass
    cmd = "scrcpy.exe "
    if entry1.get() and entry0.get():
        cmd = cmd + " -s " + entry0.get() + " " + entry4.get() + "  --video-codec " + entry3.get() + " -b " + entry2.get() + "M" + " --start-app=" + entry1.get()
    elif entry0.get():
        cmd = cmd + " -s " + entry0.get() + " " + entry4.get() + "  --video-codec " + entry3.get() + " -b " + entry2.get() + "M"
    print(cmd)
    process = subprocess.Popen(cmd, shell=False)
    return 0
