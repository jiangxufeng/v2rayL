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

        self.subs = Sub2Conf(subs_url=self.url)
        print("\r------------------------------------------")
        print("当前状态: {}".format(self.current))
        print("订阅地址：{}".format(self.url if self.url else "无"))
        print("\r------------------------------------------\n")

        
    def run(self):
        print("1. 连接VPN\n2. 断开VPN\n3. 添加配置\n4. 删除配置\n5. 更换订阅地址\n6. 退出\n")
        choice = input("请输入 >> ")
        #choice = sys.stdin.readline().strip()

        if choice == "1":
            self.connect()
        elif choice == "2":
            self.disconnect()
        elif choice == "3":
            # self.update(flag=False)
            self.addconf()
        elif choice == "4":
            # self.update(flag=False)
            self.delconf()
        elif choice == "5":
            # self.update(flag=True)
            self.update()

        elif choice == "6":
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
            print("{:^5}\t\t{:<10}\t{:<20}\n".format("序号", "协议","地区"))
            tmp = dict()
            num = 1
            for k, v in self.subs.conf.items():
                print("{:^5}\t\t{:<10}\t{:<20}\n".format(num, v["prot"], k))
                tmp[num] = k
                num +=1

            print("{:^5}\t\t{:<10}\n".format(0, "返回上一层"))
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
                    sleep(2)
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
                print("\r\n正在断开连接...............................\n")
                subprocess.call(["sudo systemctl stop v2rayL.service"], shell=True)
                sleep(2)
                print("VPN连接已断开..............\n")
                print("\r------------------------------------------\n")
                self.current = "未连接至VPN"
                with open("/etc/v2rayL/current", "wb") as jf:
                        pickle.dump((self.current, self.url), jf)
                
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
    # def update(self, flag):
    def update(self):
        # if flag:
        print("\r------------------------------------------\n")
        url = input("请输入地址>> ")
        print("\r\n正在更新订阅地址............................\n")
        self.subs = Sub2Conf(subs_url=url) 
        print("订阅地址更新完成，VPN已更新.....\n")
        print("\r------------------------------------------\n")
        with open("/etc/v2rayL/current", "wb") as jf:
            pickle.dump((self.current, url), jf)
        self.run()
        # else:
        #     try:
        #         with open("/etc/v2rayL/current", "rb") as f:
        #             _, self.url = pickle.load(f)
        #     except:
        #         print("\r------------------------------------------\n")
        #         print("\r当前不存在订阅地址，请输入订阅地址\n")
        #         self.update(flag=True)
        #     else:    
        #         print("\r------------------------------------------\n")
        #         print("\r\n正在更新................\n")
        #         self.subs = Sub2Conf(self.url)
        #         print("订阅地址更新完成，VPN已更新\n")
        #         print("\r------------------------------------------\n")

    def addconf(self):
        print("\r------------------------------------------\n")
        url = input("请输入配置信息链接(目前支持 vmess://)\n\t\t>> ")
        print("\r\n正在添加配置...................\n")
        self.subs = Sub2Conf(conf_url=url)
        print("配置添加成功，VPN已更新.....\n")
        self.run()
    
    def delconf(self):
        print("\r------------------------------------------\n")
        t = self.subs.conf.items()
        if not t:
            print("当前无可连接VPN.\n")
            print("\r------------------------------------------\n")
            self.run()
        else:
            print("{:^5}\t\t{:<10}\t{:<20}\n".format("序号", "协议","地区"))
            tmp = dict()
            num = 1
            for k, v in self.subs.conf.items():
                print("{:^5}\t\t{:<10}\t{:<20}\n".format(num, v["prot"], k))
                tmp[num] = k
                num +=1

            print("{:^5}\t\t{:<10}\n".format(0, "返回上一层"))
            choice = input("请输入需要删除的序号 >> ")

            if choice == "0":
                self.run()

            elif choice in [str(i) for i in range(num)]:
                self.subs.delconf(tmp[int(choice)])
                print("成功删除配置：{}\n".format(tmp[int(choice)]))
                print("\r------------------------------------------\n")
                self.run()

            else:
                print("\r------------------------------------------\n")
                print("请输入正确的选项...........\n")
                self.delconf()


if __name__ == '__main__':
    v = V2rayL()
    v.run()
    # t = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
    # print("===================")
    # print(t)
    # print("=====================")
    # print("Active: active" in t)