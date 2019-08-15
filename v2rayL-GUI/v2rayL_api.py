# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-08-13

import subprocess
import pickle
import re
from sub2conf_api import Sub2Conf, MyException


class V2rayL(object):
    def __init__(self):

        try:
            with open("/etc/v2rayL/current", "rb") as f:
                self.current, self.url, self.auto = pickle.load(f)
        except:
            self.current = "未连接至VPN"
            self.url = None
            self.auto = False

        self.subs = Sub2Conf(subs_url=self.url)

        if self.auto and self.url:
            try:
                self.subs.update()
            except:
                with open("/etc/v2rayL/current", "wb") as jf:
                    pickle.dump((self.current, None, False), jf)
                raise MyException("更新失败, 已关闭自动更新，请更新订阅地址")

    def subscribe(self, flag):
        if flag:
            with open("/etc/v2rayL/current", "wb") as jf:
                self.auto = True
                pickle.dump((self.current, self.url, self.auto), jf)
        else:
            with open("/etc/v2rayL/current", "wb") as jf:
                self.auto = False
                pickle.dump((self.current, self.url, self.auto), jf)

    def connect(self, region):
        self.subs.setconf(region)
        try:
            output = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
            if "Active: active" in output:
                subprocess.call(["sudo systemctl restart v2rayL.service"], shell=True)
            else:
                subprocess.call(["sudo systemctl start v2rayL.service"], shell=True)
        except:
            raise MyException("连接失败，请尝试更新订阅后再次连接......")
        else:
            self.current = region
            with open("/etc/v2rayL/current", "wb") as jf:
                pickle.dump((self.current, self.url, self.auto), jf)

    def disconnect(self):
        try:
            output = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
            if "Active: active" in output:
                subprocess.call(["sudo systemctl stop v2rayL.service"], shell=True)
                self.current = "未连接至VPN"
                with open("/etc/v2rayL/current", "wb") as jf:
                    pickle.dump((self.current, self.url, self.auto), jf)
            else:
                raise MyException("服务未开启，无需断开连接.")
        except Exception as e:
            raise MyException(e)

    def update(self, url):
        if url:  # 如果存在订阅地址
            self.subs = Sub2Conf(subs_url=url)
            self.subs.update()
            with open("/etc/v2rayL/current", "wb") as jf:
                pickle.dump((self.current, url, self.auto), jf)

        else:
            with open("/etc/v2rayL/current", "wb") as jf:
                pickle.dump((self.current, None, False), jf)

    def addconf(self, uri):
        self.subs = Sub2Conf(conf_url=uri)
        self.subs.add_conf_by_uri()

    def delconf(self, region):
        self.subs.delconf(region)

    def ping(self, addr):
        try:
            p = subprocess.getoutput(["ping -c 1 "+addr])
            res = re.search("time=(.*?)ms", p)
            return res.group(1)
        except:
            raise MyException("测试超时")



if __name__ == '__main__':
    v = V2rayL()
    # t = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
    # print("===================")
    # print(t)
    # print("=====================")
    # print("Active: active" in t)