# -*- coding:utf-8 -*-
# Author: Suummmmer
# Date: 2019-08-13

import subprocess
import pickle
import requests
from sub2conf_api import Sub2Conf, MyException


class CurrentStatus(object):
    """
    保存当前状态
    """
    def __init__(self, current="未连接至VPN", url=None, auto=False, check=False,
                 http=1081, socks=1080, log=True):
        """
        :param current: 当前连接状态
        :param url: 当前订阅地址
        :param auto: 是否开启自动更新订阅
        :param check: 是否开启自动检查更新
        :param http: http监听端口
        :param socks: socks监听端口
        :param log: 是否启用v2rayL日志
        """
        self.current = current
        self.url = url
        self.auto = auto
        self.check = check
        self.http = http
        self.socks = socks
        self.log = log


class V2rayL(object):
    def __init__(self):

        try:
            with open("/etc/v2rayL/ncurrent", "rb") as f:
                # self.current, self.url, self.auto, self.check, self.http, self.socks, self.log = pickle.load(f)
                self.current_status = pickle.load(f)
        except:
            # self.current = "未连接至VPN"
            # self.url = None
            # self.auto = False
            # self.check = False
            # self.http = 1081
            # self.socks = 1080
            # self.log = True
            self.current_status = CurrentStatus()

        self.subs = Sub2Conf(subs_url=self.current_status.url)

        # if self.current_status.auto and self.current_status.url:
        #     try:
        #         self.subs.update()
        #     except:
        #         with open("/etc/v2rayL/ncurrent", "wb") as jf:
        #             self.current_status = CurrentStatus(http=self.current_status.http,
        #                                                 socks=self.current_status.socks,
        #                                                 log=self.current_status.log)
        #             pickle.dump(self.current_status, jf)
        #         raise MyException("更新失败, 已关闭自动更新，请更新订阅地址")

    def auto_check(self, flag):
        """
        启用/禁用自动检查更新
        """
        if flag:
            with open("/etc/v2rayL/ncurrent", "wb") as jf:
                self.current_status.check = True
                pickle.dump(self.current_status, jf)
        else:
            with open("/etc/v2rayL/ncurrent", "wb") as jf:
                self.current_status.check = False
                pickle.dump(self.current_status, jf)

    def subscribe(self, flag):
        """
        启用/禁用自动更新订阅
        """
        if flag:
            with open("/etc/v2rayL/ncurrent", "wb") as jf:
                self.current_status.auto = True
                pickle.dump(self.current_status, jf)
        else:
            with open("/etc/v2rayL/ncurrent", "wb") as jf:
                self.current_status.auto = False
                pickle.dump(self.current_status, jf)

    def logging(self, flag):
        """
        启用/禁用日志
        """
        if flag:
            with open("/etc/v2rayL/ncurrent", "wb") as jf:
                self.current_status.log = True
                pickle.dump(self.current_status, jf)
        else:
            with open("/etc/v2rayL/ncurrent", "wb") as jf:
                self.current_status.log = False
                pickle.dump(self.current_status, jf)

    # def auto_on(self, flag):
    #     """
    #     启用/禁用开机自动连接
    #     """
    #     if flag:
    #         with open("/etc/v2rayL/ncurrent", "wb") as jf:
    #             self.current_status.on = True
    #             pickle.dump(self.current_status, jf)
    #     else:
    #         with open("/etc/v2rayL/ncurrent", "wb") as jf:
    #             self.current_status.on = False
    #             pickle.dump(self.current_status, jf)

    def connect(self, region, flag):
        """
        连接VPN
        :param region: VPN别名
        :param flag: 是否是正常连接/更新端口重连
        :return:
        """
        if not flag:
            self.subs.setconf(region, self.current_status.http, self.current_status.socks)
        try:
            output = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
            if "Active: active" in output:
                subprocess.call(["sudo systemctl restart v2rayL.service"], shell=True)
            else:
                subprocess.call(["sudo systemctl start v2rayL.service"], shell=True)
                output = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
                if "Active: active" not in output:
                    raise MyException("v2rayL.service 启动失败")
        except:
            raise MyException("连接失败，请尝试更新订阅后再次连接或检查v2rayL.service是否正常运行")
        else:
            self.current_status.current = region
            with open("/etc/v2rayL/ncurrent", "wb") as jf:
                pickle.dump(self.current_status, jf)

    def disconnect(self):
        """
        断开连接
        """
        try:
            output = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
            if "Active: active" in output:
                subprocess.call(["sudo systemctl stop v2rayL.service"], shell=True)
                self.current_status.current = "未连接至VPN"
                with open("/etc/v2rayL/ncurrent", "wb") as jf:
                    pickle.dump(self.current_status, jf)
            else:
                if self.current_status.current != "未连接至VPN":
                    self.current_status.current = "未连接至VPN"
                    with open("/etc/v2rayL/ncurrent", "wb") as jf:
                        pickle.dump(self.current_status, jf)
                else:
                    raise MyException("服务未开启，无需断开连接.")
        except Exception as e:
            raise MyException(e.args[0])

    def update(self, url):
        """
        更新订阅
        """
        if url:  # 如果存在订阅地址
            self.subs = Sub2Conf(subs_url=url)
            self.subs.update()
            with open("/etc/v2rayL/ncurrent", "wb") as jf:
                self.current_status.url = url
                pickle.dump(pickle.dump(self.current_status, jf), jf)

        else:
            if self.current_status.current in self.subs.saved_conf["subs"]:
                try:
                    self.disconnect()
                except:
                    pass

                with open("/etc/v2rayL/ncurrent", "wb") as jf:
                    self.current_status = CurrentStatus(http=self.current_status.http,
                                                        socks=self.current_status.socks,
                                                        log=self.current_status.log)
                    pickle.dump(self.current_status, jf)

            else:
                with open("/etc/v2rayL/ncurrent", "wb") as jf:
                    self.current_status = CurrentStatus(http=self.current_status.http,
                                                        socks=self.current_status.socks,
                                                        log=self.current_status.log)
                    pickle.dump(self.current_status, jf)

            with open("/etc/v2rayL/data", "wb") as f:
                pickle.dump({"local": self.subs.saved_conf["local"], "subs": {}}, f)

    def addconf(self, uri):
        """
        删除配置
        """
        self.subs = Sub2Conf(conf_url=uri)
        self.subs.add_conf_by_uri()

    def delconf(self, region):
        """
        删除配置
        """
        self.subs.delconf(region)

    def ping(self):
        """
        测试延时
        """
        try:
            proxy = {
                "http": "127.0.0.1:{}".format(self.current_status.http),
                "https": "127.0.0.1:{}".format(self.current_status.http)
            }
            req = requests.get("http://www.google.com", proxies=proxy, timeout=10)
            if req.status_code == 200:
                return int(req.elapsed.total_seconds()*1000)
            return req.reason
        except:
            raise MyException("测试超时")


if __name__ == '__main__':
    def ping():
        try:
            proxy = {
                "http": "127.0.0.1:1081",
                "https": "127.0.0.1:1081"
            }
            req = requests.get("http://www.google.com", proxies=proxy, timeout=10)
            if req.status_code == 200:
                return req.elapsed.total_seconds()*1000
        except:
            print(11)