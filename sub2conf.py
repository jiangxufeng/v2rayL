# -*- coding:utf-8 -*-
# author: Suummmmer

import base64
import json
import pickle
import requests
from config import conf_template as conf


class Sub2Conf(object):
    def __init__(self, url=None):
        # 原始数据
        self.origin = []
        # 解析后配置
        try:
            with open("/etc/v2rayL/data", "rb") as f:
                self.conf = pickle.load(f)
        except:
            self.conf = dict()

        if url:  
            try:
                ret = requests.get(url)
                if ret.status_code != 200:
                    return 
                all_subs = base64.b64decode(ret.text + "==").decode().strip().split("\n")
            except Exception as e:
                pass

            for sub in all_subs:
                self.origin.append(sub.split("://"))

            for ori in self.origin:
                if ori[0] == "vmess":
                    self.vmess2conf(ori[1])



        with open("/etc/v2rayL/data", "wb") as jf:
            pickle.dump(self.conf, jf)


    def vmess2conf(self, b64str):
        ret = eval(base64.b64decode(b64str).decode())
        self.conf[ret['ps']] = ret


    def setconf(self, region):
        conf['outbounds'][0]["settings"]["vnext"][0] = {
            "address": self.conf[region]["add"],
            "port": int(self.conf[region]["port"]),
            "users": [
              {
                "id": self.conf[region]["id"],
                "alterId": self.conf[region]["aid"]
              }
            ] 
        }

        conf['outbounds'][0]["streamSettings"] = {
            "network": self.conf[region]["net"],
            "wsSettings":{
              "path": self.conf[region]["path"],
              "headers": {
                "Host": self.conf[region]['host']
              }
            }
        }
        
        with open("/etc/v2rayL/config.json", "w") as f:
            f.write(json.dumps(conf, indent=4))



if __name__ == '__main__':
    s = Sub2Conf("https://sub.qianglie.xyz/subscribe.php?sid=4594&token=TCDWnwMD0rGg")
    print(s.conf)

    s.setconf("1.0x TW-BGP-A 台湾")

