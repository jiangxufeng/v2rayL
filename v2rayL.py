# -*- coding:utf-8 -*-

import sys
import subprocess
import pickle
from sub2conf import Sub2Conf
from time import sleep


class V2rayL(object):
    def __init__(self):
        
        try:
            with open("/etc/v2rayL/current", "rb") as f:
                self.current, self.url = pickle.load(f)
        except:
            self.current = "未连接VPN"
            self.url = None

        self.subs = Sub2Conf(self.url)
        print("\r------------------------------------------")
        print("当前状态: {}".format(self.current))
        print("订阅地址：{}".format(self.url if self.url else "无"))
        print("\r------------------------------------------\n")

        
    def run(self):
        print("1. 连接VPN\n2. 断开VPN\n3. 更新订阅\n4. 更换订阅地址\n5. 退出\n")
        choice = input("请输入 >> ")
        #choice = sys.stdin.readline().strip()

        if choice == "1":
            self.connect()
        elif choice == "2":
            self.disconnect()
        elif choice == "3":
            self.update(flag=False)
        elif choice == "4":
            self.update(flag=True)

        elif choice == "5":
            exit()
        else:
            print("请输入正确的选项...........\n")
            self.run()
            

    def connect(self):
        print("\r------------------------------------------\n")
        t = self.subs.conf.items()
        if not t:
            print("无可连接的VPN，请输入订阅地址更新\n")
            print("\r------------------------------------------\n")
            self.run()
        else:
            print("{:^5}              {:<20}\n".format("序号", "地区"))
            tmp = dict()
            num = 1
            for k, v in self.subs.conf.items():
                print("{:^5}              {:<20}\n".format(num, k))
                tmp[num] = k
                num +=1

            print("{:^5}              {:<20}\n".format(0, "返回上一层"))
            choice = input("请输入 >> ")

            if choice == "0":
                self.run()
            elif choice in [str(i) for i in range(num)]:
                self.subs.setconf(tmp[int(choice)])
                try:
                    output = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
                    if "Active: active" in output:
                        subprocess.call(["sudo systemctl restart v2rayL.service"], shell=True)
                    else:
                        subprocess.call(["sudo systemctl start v2rayL.service"], shell=True)
                except:
                    print("连接失败，请尝试更新订阅后再次连接......")
                    self.run()
                else:   
                    print("\r\n正在连接................\n")
                    sleep(3)
                    print("成功连接到VPN：{}\n".format(tmp[int(choice)]))
                    print("\r------------------------------------------\n")
                    self.current = tmp[int(choice)]
                    with open("/etc/v2rayL/current", "wb") as jf:
                        pickle.dump((self.current, self.url), jf)

            else:
                print("\r------------------------------------------\n")
                print("请输入正确的选项...........\n")
                self.connect()

    def disconnect(self):
        try:
            output = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
            if "Active: active" in output:
                subprocess.call(["sudo systemctl stop v2rayL.service"], shell=True)
                sleep(3)
                print("\r正在断开连接...............................\n")
                print("VPN连接已断开..............\n")
                print("\r------------------------------------------\n")
                self.current = "未连接至VPN"
                with open("/etc/v2rayL/current", "wb") as jf:
                        pickle.dump((self.current, self.url), jf)
                self.run()
            else:
                print("\r------------------------------------------\n")
                print("服务未开启，无需断开连接................\n")
                print("\r------------------------------------------\n")
                self.run()
        except Exception as e:
            print("\r------------------------------------------\n")
            print(e)
            print("服务出错，请稍后再试.................\n")
            print("\r------------------------------------------\n")

        # https://sub.qianglie.xyz/subscribe.php?sid=4594&token=TCDWnwMD0rGg
    def update(self, flag):
        if flag:
            print("\r------------------------------------------\n")
            url = input("请输入地址>> ")
            print("\r\n正在更新订阅地址............................\n")
            self.subs = Sub2Conf(url) 
            print("订阅地址更新完成，VPN已更新.....\n")
            print("\r------------------------------------------\n")
            with open("/etc/v2rayL/current", "wb") as jf:
                pickle.dump((self.current, url), jf)
            self.run()
        else:
            try:
                with open("/etc/v2rayL/current", "rb") as f:
                    _, self.url = pickle.load(f)
            except:
                print("\r------------------------------------------\n")
                print("\r当前不存在订阅地址，请输入订阅地址\n")
                self.update(flag=True)
            else:    
                print("\r------------------------------------------\n")
                print("\r\n正在更新................\n")
                self.subs = Sub2Conf(self.url)
                print("订阅地址更新完成，VPN已更新\n")
                print("\r------------------------------------------\n")


if __name__ == '__main__':
    v = V2rayL()
    v.run()
    # t = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
    # print("===================")
    # print(t)
    # print("=====================")
    # print("Active: active" in t)