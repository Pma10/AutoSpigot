import tkinter as tk
from tkinter import simpledialog, messagebox, Text
from requests import get  
import os, subprocess
import threading

versions = ['1.11','1.11.1','1.11.2','1.12','1.12.1','1.12.2','1.13','1.13.1','1.13.2','1.14','1.14.1','1.14.2','1.14.3','1.14.4','1.15','1.15.1','1.15.2','1.16.1','1.16.2','1.16.3','1.16.4','1.16.5','1.17','1.17.1','1.18','1.18.1','1.18.2','1.19','1.19.2','1.19.3','1.19.4','1.20.1','1.20.2']

def download(url, file_name,folder):
    os.mkdir(folder)
    with open(f'{folder}/{file_name}', "wb") as file:
        response = get(url)              
        file.write(response.content)   

def start_server():
    inp_version = version_entry.get()
    folder_name = folder_entry.get()
    ram_set = ram_entry.get()

    if inp_version not in versions:
        messagebox.showerror("Error", "잘못된 버전입니다")
        return
    if ram_set.isdigit() is False:
        messagebox.showerror("Error","램 할당은 숫자만 입력해주세요")
        return
    log_text.configure(state="normal") 
    log_text.insert(tk.END, f"다운로드 폴더: {folder_name}\n버전: Spigot {inp_version}\nRAM 할당: {ram_set}GB\n")
    log_text.configure(state="disabled")

    def run_task():
        url = f"https://download.getbukkit.org/spigot/spigot-{inp_version}.jar"
        download(url, "server.jar", folder_name)

        with open(f'{folder_name}/prestart.bat','w') as f:
            f.write(f'@echo off \njava -Xms{ram_set}G -Xmx{ram_set}G -Dcom.mojang.eula.agree=true -jar server.jar -nogui  \npause')
        with open(f'{folder_name}/start.bat','w') as f:
            f.write(f'@echo off \njava -Xms{ram_set}G -Xmx{ram_set}G -jar server.jar -nogui  \npause')
        log_text.configure(state="normal")
        log_text.insert(tk.END, f"서버 구성중\n")
        log_text.configure(state="disabled")
        cmd = 'prestart.bat'
        cwd = f'{folder_name}\\'
        process = subprocess.run(cmd, cwd=cwd, shell=True, input='stop', text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        eula_content = ''
        with open(f'{folder_name}/eula.txt','r',encoding="UTF-8") as f:
            eula_content = f.read()
        eula_content = eula_content.replace('false','true')
        with open(f'{folder_name}/eula.txt','w',encoding="UTF-8") as f:
            f.write(eula_content)
        os.remove(f'{folder_name}\\prestart.bat')
        
        log_text.configure(state="normal")
        log_text.insert(tk.END, "설치가 완료되었습니다\n")
        log_text.configure(state="disabled")
        messagebox.showinfo('AutoSpigot','설치가 완료되었습니다.')

    task_thread = threading.Thread(target=run_task)
    task_thread.start()

root = tk.Tk()
root.title("AutoSpigot")

version_label = tk.Label(root, text="Minecraft 버전 (1.11 - 1.20.2):")
version_entry = tk.Entry(root)

folder_label = tk.Label(root, text="다운로드 폴더 이름:")
folder_entry = tk.Entry(root)

ram_label = tk.Label(root, text="RAM 할당 (GB):")
ram_entry = tk.Entry(root)

install_button = tk.Button(root, text="서버 설치", command=start_server)

log_text = Text(root, height=10, width=50)

log_text.configure(state="disabled")  # 로그 텍스트 창을 읽기 전용으로 설정

version_label.pack()
version_entry.pack()

folder_label.pack()
folder_entry.pack()

ram_label.pack()
ram_entry.pack()

install_button.pack()
log_text.pack()
root.mainloop()
