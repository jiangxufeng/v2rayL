#!/bin/bash

echo "创建   /etc/v2rayL"
sudo mkdir /etc/v2rayL
echo "创建   /usr/bin/v2rayL"
sudo mkdir /usr/bin/v2rayL
echo "复制文件至 /usr/bin/v2rayL"
sudo cp ./v2ray-core/{geoip.dat,geosite.dat,v2ctl,v2ray,v2ray.sig,v2ctl.sig} /usr/bin/v2rayL
echo "复制文件至 /etc/systemd/system/"
sudo cp ./v2ray-core/v2rayL.service /etc/systemd/system/
echo "设置权限和快捷方式"
sudo chmod 777 -R /etc/v2rayL
sudo chmod 777 -R /usr/bin/v2rayL
echo "复制静态文件"
cp -r ./v2rayL-GUI/images /etc/v2rayL
echo "解压可执行程序"
tar xvJf ./v2rayL-exec/v2rayLui-v1.1.tar.xz -C /usr/bin/v2rayL/

project_path=$(cd `dirname $0`; pwd)
current_user=$USER

echo $current_user

echo "[Desktop Entry]\nType=Application\nExec=/usr/bin/v2rayL/v2rayLui\nHidden=false\nNoDisplay=false\nX-GNOME-Autostart-enabled=true\nName[zh_CN]=v2rayL
Name=v2rayL\nComment[zh_CN]=V2rayL\nComment=v2ray-v2rayL" > /home/${current_user}/.config/autostart/v2rayL.desktop

echo "alias v2rayL='python ${project_path}/v2rayL.py'" | sudo tee -a ~/.zshrc
echo "alias v2rayL='python ${project_path}/v2rayL.py'" | sudo tee -a ~/.bashrc  

source ~/.zshrc
source ~/.bashrc 
echo "$current_user ALL=NOPASSWD:/bin/systemctl restart v2rayL.service,/bin/systemctl start v2rayL.service,/bin/systemctl stop v2rayL.service,/bin/systemctl status v2rayL.service,/bin/systemctl enable v2rayL.service" | sudo tee -a /etc/sudoers
echo "设置开机自启动"
sudo systemctl enable v2rayL.service
/usr/bin/v2rayL/v2rayLui &
echo "完成."
