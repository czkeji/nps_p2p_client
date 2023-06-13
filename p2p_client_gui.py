import tkinter as tk
import ttkbootstrap as ttk
from tkinter import messagebox
import threading
import pystray
from PIL import Image
from pystray import MenuItem, Menu
import requests
import json
import random
import os


class MainPage:
    def __init__(self, master: ttk.Window):
        self.root = master
        self.root.title('nps内网穿透P2P客户端')
        self.root.geometry('350x300')
        self.root.iconbitmap('logo.ico')
        self.root.minsize(330, 300)
        self.root.maxsize(350, 500)
        self.root.protocol('WM_DELETE_WINDOW', self.on_exit)
        self.menu = (MenuItem('显示主界面', self.show_window, default=True), Menu.SEPARATOR, MenuItem('退出', self.quit_window))
        self.image = Image.open("logo.png")
        self.icon = pystray.Icon("icon", self.image, "P2P客户端", self.menu)
        threading.Thread(target=self.icon.run, daemon=True).start()
        self.p2p_list_info={}
        self.Create_page()
    def Create_page(self):
        #登陆窗口
        #logo框
        self.login_frame=ttk.Frame(self.root)
        self.login_frame.pack(fill=ttk.BOTH,expand=True)
        self.login_top_frame=ttk.Frame(self.login_frame,bootstyle="info")
        self.login_top_frame.pack()
        self.login_top_label=ttk.Label(self.login_top_frame,text="欢迎登录", justify=ttk.CENTER, anchor=ttk.CENTER, font=("Arial", 20),bootstyle="inverse-info",width=40)
        self.login_top_label.pack(fill=ttk.BOTH,expand=True,pady=20)
        #登录信息框
        self.login_bottom_frame=ttk.Frame(self.login_frame,width=200,height=200)
        label = ttk.Label(self.login_bottom_frame, text="服务器:").grid(column=0, row=0)
        self.login_server_entry=ttk.Entry(self.login_bottom_frame)
        self.login_server_entry.grid(column=1,row=0,pady=10)
        label=ttk.Label(self.login_bottom_frame,text="：").grid(column=2,row=0)
        self.login_serverport_entry=ttk.Entry(self.login_bottom_frame,width=5)
        self.login_serverport_entry.grid(column=3,row=0,pady=10)
        label = ttk.Label(self.login_bottom_frame, text="用户名:").grid(column=0, row=1)
        self.login_user_entry=ttk.Entry(self.login_bottom_frame,width=30)
        self.login_user_entry.grid(column=1,columnspan=3,row=1,pady=10)
        label = ttk.Label(self.login_bottom_frame, text="密  码:").grid(column=0, row=2)
        self.login_pwd_entry=ttk.Entry(self.login_bottom_frame,width=30,show="*")
        self.login_pwd_entry.grid(column=1,columnspan=3,row=2,pady=10)
        self.login_button=ttk.Button(self.login_bottom_frame,text="登录",width=35,command=self.login)
        self.login_button.grid(columnspan=4,row=3)
        self.login_bottom_frame.pack()

        #P2P列表
        self.p2p_list_info_frame=ttk.Frame(self.root)
        #置顶信息框
        self.p2p_list_top_frame=ttk.Frame(self.p2p_list_info_frame,bootstyle="info")
        self.p2p_list_top_frame.pack()
        self.p2p_list_label=ttk.Label(self.p2p_list_top_frame,text="p2p列表", justify=ttk.CENTER, anchor=ttk.CENTER, font=("Arial", 20),bootstyle="inverse-info",width=40)
        self.p2p_list_label.pack(fill=ttk.BOTH,expand=True,pady=20)
        self.exit_client=ttk.Button(self.p2p_list_top_frame,text="退出",command=self.exit_client).pack()
        #p2p列表框
        self.p2p_list_bottom_frame=ttk.Frame(self.p2p_list_info_frame)
        self.p2p_list_bottom_frame.pack(fill=ttk.BOTH,expand=True)
        self.p2p_columns =['p2p连接名称','P2P端口','P2P主机']
        self.p2p_list_table = ttk.Treeview(
            master=self.p2p_list_bottom_frame,
            height=15,
            columns=self.p2p_columns,
            show='headings',
            bootstyle='light',
            yscrollcommand=ttk.X,
        )
        self.p2p_list_table.heading('p2p连接名称', text='p2p连接名称', )  # 定义表头
        self.p2p_list_table.heading('P2P端口', text='P2P端口', )  # 定义表头
        self.p2p_list_table.heading('P2P主机', text='P2P主机', )  # 定义表头
        self.p2p_list_table.column('p2p连接名称', width=130, anchor=ttk.CENTER, )  # 定义列
        self.p2p_list_table.column('P2P端口', width=100, anchor=ttk.CENTER, )  # 定义列
        self.p2p_list_table.column('P2P主机', width=130, anchor=ttk.CENTER, )  # 定义列
        self.p2p_list_table.pack(fill=ttk.BOTH, expand=True)





    def login(self):
        if  self.login_server_entry.get()=="" and self.login_serverport_entry.get()=="" and self.login_user_entry.get()=="" and self.login_pwd_entry.get()=="":
            messagebox.showwarning("提示", "请完整输入服务器及用户密码等信息！")
        else:
            try:
                self.login_url = f'http://{self.login_server_entry.get()}:{self.login_serverport_entry.get()}/login/verify?username={self.login_user_entry.get()}&password={self.login_pwd_entry.get()}'
                self.login_request = requests.post(self.login_url, timeout=20)
                self.login_msg = json.dumps(self.login_request.json())
                self.login_status = json.loads(self.login_msg)
                if self.login_status['status'] == 1:
                    messagebox.showinfo("提示", "登录成功")
                    self.login_frame.pack_forget()
                    self.p2p_list_info_frame.pack(fill=ttk.BOTH, expand=True)
                    self.get_p2p_list()
                else:
                    messagebox.showwarning("登录失败", "请检查服务器及用户密码信息！")
                self.root.geometry("350x500")
            except requests.exceptions.ConnectionError as e:
                messagebox.showwarning("服务器连接失败","请检查服务器地址是否正确！")

    def get_p2p_list(self):
        self.data_list=[]
        self.loging_Cookie=self.login_request.headers['Set-Cookie']
        self.url = f"http://{self.login_server_entry.get()}:{self.login_serverport_entry.get()}/index/gettunnel/"
        self.query = {'type': 'p2p', 'limit': '100'}
        self.headers = {'cookie': self.loging_Cookie,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'}
        self.response=requests.post(self.url,params=self.query,headers=self.headers)
        self.response_data=json.dumps(self.response.json())
        self.data_dict = json.loads(self.response_data)
        for item in self.data_dict['rows']:
            Remark = item['Remark']
            connection_type=item['Mode']
            p2p_port = random.randint(2000, 63550)
            Target = item['Target']
            target_host = Target['TargetStr']
            client_info = item['Client']
            verifykey = client_info['VerifyKey']
            client_status=client_info['Status']
            password = item['Password']
            self.p2p_list_info.update({Remark: {
                "connection_type":connection_type,
                "p2p_port": p2p_port,
                "p2p_target": target_host,
                "p2p_client_verifykey": verifykey,
                "p2p2_password": password,
                "client_status":client_status
            }})
            self.data_list.append([Remark,p2p_port,target_host])
            cmd=f'npc -server={self.login_server_entry.get()}:8024 -vkey={verifykey} -type=tcp -password={password} -target={target_host} -local_port={p2p_port}'
            os.popen(cmd)
        for i in self.data_list:
            self.p2p_list_table.insert('','end',values=i)
    def exit_client(self):
        os.system('%s%s' % ("taskkill /F /IM ", "npc.exe"))
        self.root.quit()

    #任务栏图标
    def on_exit(self):
        self.root.withdraw()
    def show_window(self):
        self.root.deiconify()
    def quit_window(self,icon:pystray.Icon):
        os.system('%s%s' % ("taskkill /F /IM ", "npc.exe"))
        self.icon.stop()
        self.root.destroy()







if __name__ == '__main__':
    root = ttk.Window()
    MainPage(root)
    root.mainloop()