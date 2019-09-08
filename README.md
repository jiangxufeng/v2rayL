# v2ray
V2Ray 是 Project V 下的一个工具。Project V 包含一系列工具，帮助你打造专属的定制网络体系。而 V2Ray 属于最核心的一个。 简单地说，V2Ray 是一个与 Shadowsocks 类似的代理软件，但比Shadowsocks更具优势

V2Ray 用户手册：https://www.v2ray.com

V2Ray 项目地址：https://github.com/v2ray/v2ray-core

# v2rayL

![v2rayL](http://cloud.thinker.ink/images/857633d396d9f89cc606c0666194f45f.png)

v2ray linux 客户端，使用pyqt5编写GUI界面，核心基于v2ray-core

目前已实现以下功能：

- 全新的UI界面
- 添加订阅地址，自动解析并展示可连接VPN
- 设置自动更新订阅、更换地址
- 支持协议：vmess、shadowsocks
- 通过`vmess://`、`ss://`分享链接添加配置，通过二维码添加配置
- 导出配置、生成配置分享链接、生成分享二维码
- 最小化至托盘、检查更新
- ......

其中vmess支持websocket、mKcp
目前程序可能存在一些bug但是没有测试出，若在使用过程中发现bug，请在issue中提交，以便改进。

# 使用

## 安装
方法一：
```
bash <(curl -s -L http://cloud.thinker.ink/install.sh)
```

方法二：
```
在release中下载最新的install.sh，然后运行 ./install.sh
```

## 更新
方法一：
```
bash <(curl -s -L http://cloud.thinker.ink/update.sh)
```

方法二：
```
在release中下载最新的update.sh，然后运行 ./update.sh
```

# 展示

![首页](http://cloud.thinker.ink/images/690c3ea3c5357273beeef2e6b0c573ee.png)

![setting1](http://cloud.thinker.ink/images/c7c0cafc297d6be5ea6bb7ebcd3a1375.png)

![setting2](http://cloud.thinker.ink/images/37239b8753e2344872477c518a9cd4c8.png)

# 感谢

UI界面设计来源：https://www.codercto.com/a/24461.html

配置方面参考: ![v2rayNG](https://github.com/2dust/v2rayNG)

# 协议

[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


