from requests import get  
import os, subprocess

versions = ['1.11','1.11.1','1.11.2','1.12','1.12.1','1.12.2','1.13','1.13.1','1.13.2','1.14','1.14.1','1.14.2','1.14.3','1.14.4','1.15','1.15.1','1.15.2','1.16.1','1.16.2','1.16.3','1.16.4','1.16.5','1.17','1.17.1','1.18','1.18.1','1.18.2','1.19','1.19.2','1.19.3','1.19.4','1.20.1','1.20.2']

def download(url, file_name,folder):
    os.mkdir(folder)
    with open(f'{folder}/{file_name}', "wb") as file:
        response = get(url)              
        file.write(response.content)   
 
inp_version = input('버킷 시스템 : 버전을 입력해주세요 1.11 ~ 1.20.2 : ')
if inp_version not in versions:
    while True:
        inp_version = input('버킷 시스템 : 올바른 버전을 입력해주세요 1.11 ~ 1.20.2 : ')
        if inp_version in versions:
            break
folder_name = input('버킷 시스템 : 폴더의 이름을 입력해주세요 : ')
if os.path.isdir(f'{folder_name}/'):
    while True:
        same = input(f'버킷 시스템 : 이미 {folder_name} 이름의 폴더가 존재합니다, 다른 이름을 입력해주세요 :')
        if same != folder_name:
            folder_name = same
            break
ram_set = input('버킷 시스템 : 할당할 램을 적어주세요 <단위 : GB, 숫자만> : ')
if ram_set.isdigit is False:
    while True:
        ram_set = input(f'버킷 시스템 : 정확한 숫자만 적어주세요 <단위 : GB> :')
        if ram_set.isdigit:
            break
print(f'------------ 버킷 시스템 ------------\n다운로드 폴더 이름 : {folder_name} \n다운로드 버전 : Spigot {inp_version}\n램 할당 용량 : {ram_set}GB')
print('버킷 시스템 : 시작됨')
print('버킷 시스템 : 버킷 설치중')
url = f"https://download.getbukkit.org/spigot/spigot-{inp_version}.jar"
download(url,"server.jar",folder_name)
print('버킷 시스템 : 설치 완료')
print('버킷 시스템 : 서버 파일 생성 시작')
with open(f'{folder_name}/prestart.bat','w') as f:
    f.write(f'@echo off \njava -Xms{ram_set}G -Xmx{ram_set}G -Dcom.mojang.eula.agree=true -jar server.jar -nogui  \npause')
with open(f'{folder_name}/start.bat','w') as f:
    f.write(f'@echo off \njava -Xms{ram_set}G -Xmx{ram_set}G -jar server.jar -nogui  \npause')
cmd = 'prestart.bat'
cwd = f'{folder_name}\\'
process = subprocess.run(cmd,cwd=cwd,shell=True,input='stop', text=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE,)
eula_content = ''
with open(f'{folder_name}/eula.txt','r',encoding="UTF-8") as f:
    eula_content = f.read()
eula_content = eula_content.replace('false','true')
with open(f'{folder_name}/eula.txt','w',encoding="UTF-8") as f:
    f.write(eula_content)
os.remove(f'{folder_name}\\prestart.bat')
print('버킷 시스템 : 설치가 완료되었습니다.')
print('주의사항 : \n서버를 실행할때는 start.bat을 실행시켜 실행해주세요.')
print('------------ 버킷 시스템 ------------')