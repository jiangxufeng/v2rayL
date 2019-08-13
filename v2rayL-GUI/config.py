# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-08-13

conf_template = {
  "log":{},
  "dns":{},
  "stats":{},
  "inbounds":[
    {
      "port":"1080",
      "protocol":"socks",
      "settings":{
        "auth":"noauth",
        "udp": True
      },
      "tag":"in-0"
    }
  ],
  "outbounds":[
    {
      "protocol":"",
      "settings":{},
      "tag":"out-0",
      "streamSettings":{}
    },
    {
      "tag":"direct",
      "protocol":"freedom",
      "settings":{}
    },
    {
      "tag":"blocked",
      "protocol":"blackhole",
      "settings":{}
    }
  ],
  "routing":{
    "domainStrategy":"IPOnDemand",
    "rules":[
      {
        "type":"field",
        "ip":[
          "geoip:private"
        ],
        "outboundTag":"direct"
      }
    ]
  },
  "policy":{},
  "reverse":{},
  "transport":{}
}