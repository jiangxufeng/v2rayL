#!/bin/bash

echo "创建   /etc/v2rayL"
sudo mkdir /etc/v2rayL
echo "创建   /usr/bin/v2rayL"
sudo mkdir /usr/bin/v2rayL
echo "复制文件至 /usr/bin/v2rayL"
sudo cp ./v2ray-core/{geoip.dat,geosite.dat,v2ctl,v2ray,v2ray.sig,v2ctl.sig} /usr/bin/v2rayL
echo "复制文件至 /etc/systemd/system/"
sudo cp ./v2ray-core/v2rayL.service /etc/systemd/system/
sudo chmod 777 -R /etc/v2rayL
sudo chmod 777 -R /usr/bin/v2rayL
echo "完成."
