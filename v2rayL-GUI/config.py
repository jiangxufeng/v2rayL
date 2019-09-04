# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-08-13

conf_template = {
  "dns": {
      "servers": [
          "1.1.1.1"
      ]
  },
  "inbounds": [{
        "port": 1080,
        "protocol": "socks",
        "settings": {
            "auth": "noauth",
            "udp": True,
            "userLevel": 8
        },
        "sniffing": {
            "destOverride": [
                "http",
                "tls"
            ],
            "enabled": True
        },
        "tag": "socks"
    },
    {
        "port": 1081,
        "protocol": "http",
        "settings": {
            "userLevel": 8
        },
        "tag": "http"
    }
  ],
  "log": {
      "loglevel": "warning"
  },
  "outbounds": [{
          "mux": {
              "enabled": False
          },
          "protocol": "",
          "settings": {},
          "streamSettings": {},
          "tag": "proxy"
      },
      {
          "protocol": "freedom",
          "settings": {},
          "tag": "direct"
      },
      {
          "protocol": "blackhole",
          "settings": {
              "response": {
                  "type": "http"
              }
          },
          "tag": "block"
      }
  ],
  "policy": {
      "levels": {
          "8": {
              "connIdle": 300,
              "downlinkOnly": 1,
              "handshake": 4,
              "uplinkOnly": 1
          }
      },
      "system": {
          "statsInboundUplink": True,
          "statsInboundDownlink": True
      }
  },
  "routing": {
      "domainStrategy": "IPIfNonMatch",
      "rules": []
  },
  "stats": {}
}