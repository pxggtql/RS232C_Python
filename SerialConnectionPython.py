# #!/usr/bin/env python
# # -*- coding: utf-8 -*-

from tkinter import *
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
import datetime

import serial
import threading
import time

SerialPort = []

#左侧SEND按钮的点击事件
def processSEND1(text):
    print("Send button is clinked")
    fetched_content = text.get('0.0', END)
    write_to_serial(SerialPort[1],fetched_content)
    return fetched_content
#右侧SEND按钮的点击事件
def processSEND2(text):
    print("Send button is clinked")
    fetched_content = text.get('0.0', END)
    write_to_serial(SerialPort[0], fetched_content)
    return fetched_content
#左侧CLEAR按钮的点击事件
def processCLEAR1(Receive):
    print("Clear button is clinked")
    Receive.delete('1.0','end')
#右侧CLEAR按钮的点击事件
def processCLEAR2(Receive):
    print("Clear button is clinked")
    Receive.delete('1.0','end')
#左侧CONNECT按钮的点击事件
def processCONNECT1(port,baud_rate,default_baud_rate = 9600):
    print("Connect button is clicked")
    fetched_port_id = port.get('0.0', END)
    print(fetched_port_id)
    fetched_baud_rate = baud_rate.get('0.0', END)
    port_id = fetched_port_id[:-1]
    if(port_id == ""):
        messagebox.showinfo('ERROR', 'Please input the name of the serial port correctly!')
        return NONE
    print(fetched_baud_rate)
    if(fetched_baud_rate[:-1] == ""):
        baud = default_baud_rate
        showTextPure(shoeBaudRate, "9600")
        messagebox.showinfo('TIPs', 'The default baud rate is 9600')
    else : baud = eval(fetched_baud_rate)

    #print(port,port_id)
    ser1 = open_serial(port_id, baud, None)  # 串口com3、bps为115200，等待时间为永久

    return ser1
#右侧CONNECT按钮的点击事件
def processCONNECT2(port,baud_rate,default_baud_rate = 9600):
    print("Connect button is clicked")
    fetched_port_id = port.get('0.0', END)
    print(fetched_port_id)
    fetched_baud_rate = baud_rate.get('0.0', END)
    port_id = fetched_port_id[:-1]
    print(fetched_baud_rate)
    if(fetched_baud_rate[:-1] == ""):
        baud = default_baud_rate
        showTextPure(shoeBaudRate,"9600")
        messagebox.showinfo('TIPs', 'The default baud rate is 9600')
    else : baud = eval(fetched_baud_rate)

    #print(port,port_id)
    ser2 = open_serial(port_id, baud, None)  # 串口com3、bps为115200，等待时间为永久

    return ser2
#左侧DISCONNECT按钮的点击事件
def processDISCONNECT1():
    print("Disconnect button is clicked")
    close_serial(SerialPort[0])
#左侧DISCONNECT按钮的点击事件
def processDISCONNECT2():
    print("Disconnect button is clicked")
    close_serial(SerialPort[1])
#显示文本
def showText(scl, text):
    curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text = str(curr_time) + "\n" + text + "\n"
    print(text)
    scl.insert(END, text)

def showTextPure(scl, text):
    #curr_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    text =text
    print(text)
    scl.insert(END, text)


# 打开串口
def open_serial(portx, bps, timeout):
    try:
        # 打开串口，并得到串口对象
        ser = serial.Serial(portx, bps, timeout=timeout)
        #设置停止位为 1
        ser.stopbits = 1
        showData.delete('1.0', 'end')
        showCheck.delete('1.0', 'end')
        showStop.delete('1.0', 'end')
        showTextPure(showStop,"1")
        #设置数据位为 8
        ser.bytesize = serial.EIGHTBITS
        showTextPure(showData,"8")
        #设置校验位为偶校验
        ser.parity = serial.PARITY_EVEN
        showTextPure(showCheck,"0")


        # 判断是否成功打开
        if (ser.is_open):
            th = threading.Thread(target=receive_data, args=(ser,))  # 创建一个子线程去等待读数据
            th.start()

    except Exception as e:
        #若创建串口失败，弹窗提示
        messagebox.showinfo('ERROR', 'Please input the name and the baud rate of the serial port correctly!')
        print("error!", e)
    SerialPort.append(ser)

    return ser


DATA = ""  # 读取的数据
NOEND = True  # 是否读取结束

Message_Port1 = ""
# 从串口接收数据
def receive_data(ser):
    global DATA, NOEND

    # 循环接收数据
    while NOEND:
        if ser.in_waiting:

            DATA = ser.read(ser.in_waiting).decode("gbk")
            print("\n>> receive: ", DATA, "\n>>", end="")
            Message_Port1 = DATA

            if(ser == SerialPort[0]):
                showText(serial2Receive,DATA)
            elif(ser == SerialPort[1]):
                showText(serial1Receive, DATA)
            # print(">>", end="")
            if (DATA == "quit"):
                print("oppo seri has closen.\n>>", end="")


# 关闭串口
def close_serial(ser):
    global NOEND
    NOEND = False
    ser.close()


# 写数据
def write_to_serial(ser, text):
    res = ser.write(text.encode("gbk"))  # 写
    return res


# 读数据
def read_from_serial():
    global DATA
    data = DATA
    DATA = ""  # 清空当次读取
    return data


# 实例化object，建立窗口window
window = tk.Tk()

# 第一个串口标题
label1 = Label(window, text='Serial Port1 Name')
label1.grid(row=0, column=0, columnspan=1)

# 第一个串口名字框
serial1Name = Text(window, height=2, width=30)
serial1Name.grid(row=1, column=0, rowspan=2)

# 串口1连接和断开的按钮
btnCN1 = Button(window, text="CONNECT", fg='black', command= lambda : processCONNECT1(serial1Name,shoeBaudRate), height=2, width=12)
btnDCN1 = Button(window, text="DISCONNECT", fg='black', command=processDISCONNECT1, height=2, width=12)
btnCN1.grid(row=0, column=1)
btnDCN1.grid(row=1, column=1)

# 串口1收到信息框
serial1Receive = ScrolledText(window, height=15, width=50)
serial1Receive.grid(row=4, column=0, columnspan=2, sticky="nsew")
# 串口1发出信息框
serial1Send = ScrolledText(window, height=5, width=50)
serial1Send.grid(row=5, column=0, columnspan=2, sticky="nsew")
# 串口1发送和删除按钮
btnSEND1 = Button(window, text="SEND", fg="black", command=lambda: processSEND1(serial1Send), width=10)
btnCLEAR1 = Button(window, text="CLEAR", fg="black", command=processCLEAR1(serial1Receive), width=10)
btnSEND1.grid(row=6, column=0, columnspan=1, sticky=tk.E, padx=6)
btnCLEAR1.grid(row=6, column=1, columnspan=1)

# 第二个串口标题
label2 = Label(window, text='Serial Port2 Name')
label2.grid(row=0, column=5, columnspan=1)
# 第二个串口名字框
serial2Name = Text(window, height=2, width=30)
serial2Name.grid(row=1, column=5, rowspan=2)
# 串口2连接和断开的按钮
btnCN2 = Button(window, text="CONNECT", fg='black', command= lambda : processCONNECT2(serial2Name,shoeBaudRate), height=2, width=12)
btnDCN2 = Button(window, text="DISCONNECT", fg='black', command=processDISCONNECT2, height=2, width=12)
btnCN2.grid(row=0, column=6)
btnDCN2.grid(row=1, column=6)
# 串口2收到信息框
serial2Receive = ScrolledText(window, height=15, width=50)
serial2Receive.grid(row=4, column=5, columnspan=2, sticky="nsew")
# 串口2发出信息框
serial2Send = ScrolledText(window, height=5, width=50)
serial2Send.grid(row=5, column=5, columnspan=2, sticky="nsew")
# 串口2发送和删除按钮
btnSEND2 = Button(window, text="SEND", fg="black", command=lambda: processSEND2(serial2Send), width=10)
btnCLEAR2 = Button(window, text="CLEAR", fg="black", command=processCLEAR2(serial2Receive), width=10)
btnSEND2.grid(row=6, column=5, columnspan=1, sticky=tk.E, padx=6)
btnCLEAR2.grid(row=6, column=6, columnspan=1)

# 波特率标题
label3 = Label(window, text='Baud Rate')
label3.grid(row=0, column=2, columnspan=2)
# 波特率显示框
shoeBaudRate = Text(window, height=2, width=30)
shoeBaudRate.grid(row=1, column=2, columnspan=3)
# 数据位标题
label4 = Label(window, text='Byte size')
label4.grid(row=2, column=2)
# 数据位显示框
showData = Text(window, height=2, width=10)
showData.grid(row=3, column=2)
# 校验位标题
label6 = Label(window, text='Parity')
label6.grid(row=2, column=3)
# 校验位显示框
showCheck = Text(window, height=2, width=10)
showCheck.grid(row=3, column=3)
# 停止位标题
label5 = Label(window, text='Stop bits')
label5.grid(row=2, column=4)
# 停止位显示框
showStop = Text(window, height=2, width=10)
showStop.grid(row=3, column=4)
# 给窗口的可视化起名字

window.title('Serial Port Connection')

window.mainloop()











