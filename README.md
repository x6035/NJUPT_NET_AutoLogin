# 南邮校园网自动登录
## 项目中含有两个程序
---
## 1、校园网一键登录（Net_Connect.exe）
使用方法：下载config.ini，放到exe同级目录下，文件里填写自己的

 Ⅰ校园网账号（username=）

 Ⅱ校园网密码（password=）

 Ⅲ运营商类型（type=0），0为校园网  1为电信  2为移动

---
## 2、网络连接一键切换（Switch_Net.exe）
### 此工具主要用于方便快捷应对学校断网（本科限定福利）
功能：运行`Switch_Net.exe`时，自动检测当前某有线连接是否启用，是的话禁用，同时连接配置里填写的wifi;如果当前有线连接已经禁用，则将其启用。

使用方法：下载config.ini，放到exe同级目录下，文件里填写自己的

Ⅰ、有线网络的名称（ethernet_interface=）

Ⅱ、WIFI名称（wifi_ssid=）

Ⅲ、WIFI密码（wifi_password=）

---
## 3、关于舒服的全自动登录联网方法
### 配置方法：打开windows的任务计划程序，右侧操作里选择导入任务，选择项目里的`校园网检测.xml`。
---
## 4、构建
python3.11.1

pyinstaller --onefile .pyfile

## 5、注意事项
1、确保程序以管理员身份运行

2、确保校园网已经连接