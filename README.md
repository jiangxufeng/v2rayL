# v2ray
V2Ray 是 Project V 下的一个工具。Project V 包含一系列工具，帮助你打造专属的定制网络体系。而 V2Ray 属于最核心的一个。 简单地说，V2Ray 是一个与 Shadowsocks 类似的代理软件，但比Shadowsocks更具优势

V2Ray 用户手册：https://www.v2ray.com

V2Ray 项目地址：https://github.com/v2ray/v2ray-core

# v2rayL

![v2rayL](http://cloud.thinker.ink/images/857633d396d9f89cc606c0666194f45f.png)

v2ray linux 客户端，使用pyqt5编写GUI界面，核心基于v2ray-core(v2ray-linux-64)

开发环境：`ubuntu18.04+Python3.6`

目前已实现以下功能：

- 全新的UI界面
- 添加订阅地址，自动解析并展示可连接VPN
- 设置自动更新订阅、更换地址
- 支持协议：vmess、shadowsocks
- 通过`vmess://`、`ss://`分享链接添加配置，通过二维码添加配置
- 手动添加配置，修改本地监听端口
- 导出配置、生成配置分享链接、生成分享二维码
- 最小化至托盘、测试延时、检查更新
- 透明代理(Beta)
- ......

其中vmess支持websocket、mKcp、tcp
目前程序可能存在一些bug但是没有测试出，若在使用过程中发现bug，请在issue中提交，以便改进。

**透明代理说明：**

透明代理设置参考v2ray教程：[透明代理(TPROXY)](https://guide.v2fly.org/app/tproxy.html)

测试环境： 三台不同的机器(条件有限)

测试时出现问题： 有些透明代理无法生效，导致代理失败。

解决办法：在测试时发现多尝试启动几次(关闭，开启)或重启程序就可以正常使用

后续会进一步深入优化这个问题，透明代理无法使用时可以关闭，不影响其正常使用
# 使用

## 使用前请注意
使用脚本安装时下载的程序实在`ubuntu 18.04` + `Python3.6`的环境下打包的，因此在Python版本不一致的环境中可能会出现版本不兼容的问题

解决方法：

在自己的电脑上重新打包程序，具体方法如下（参考）
1. 运行`git clone https://github.com/jiangxufeng/v2rayL.git`
2. 进入项目文件夹，然后运行`pip install -r requirements.txt`
3. 运行`cd v2rayL-GUI && pyinstaller -F v2rayLui.py -p config.py -p sub2conf_api.py -p v2rayL_api.py -p v2rayL_threads.py -p utils.py -i images/logo.ico -n v2rayLui`
4. 打包后运行`mv dist/v2rayLui /usr/bin/v2rayL/v2rayLui`

## 安装
```
bash <(curl -s -L http://dl.thinker.ink/install.sh)
```

## 更新
``` bash
bash <(curl -s -L http://dl.thinker.ink/update.sh)
```

## 卸载
``` bash
bash <(curl -s -L http://dl.thinker.ink/uninstall.sh)
```

# 展示

![首页](http://cloud.thinker.ink/download/a043a08860f239f8d0cbeb2dc2a5b6d5.png)

![setting1](http://cloud.thinker.ink/images/617ce660cc4a2a22bd275d73d0d7c616.png)

![setting2](http://cloud.thinker.ink/images/8835526765d479143879c08fe1ecb8a4.png)

# 感谢

UI界面设计来源：https://zmister.com/archives/477.html

配置方面参考: https://github.com/2dust/v2rayNG

# 协议

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


