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
                self.current, self.url, self.auto = pickle.load(f)
        except:
            self.current = "未连接VPN"
            self.url = None
            self.auto = False

        self.subs = Sub2Conf(subs_url=self.url)

        if self.auto:
            try:
                self.subs.update()
            except:
                print("\n自动更新失败： 地址错误或不存在，请更换订阅地址。")
                self.update()

        print("\r------------------------------------------")
        print("当前状态: {}".format(self.current))
        print("自动更新: {}".format("开启" if self.auto else "关闭"))
        print("订阅地址：{}".format(self.url if self.url else "无"))
        print("\r------------------------------------------")

        
    def run(self):
        print("\n1. 连接VPN\n2. 断开VPN\n3. 配置\n4. 订阅\n5. 查看当前状态\n0. 退出\n")
        choice = input("请输入 >> ")
        #choice = sys.stdin.readline().strip()

        if choice == "1":
            self.connect()
        elif choice == "2":
            self.disconnect()
        elif choice == "3":
            self.cgeconf()
        elif choice == "4":
            # self.update(flag=True)
            self.subscribe()
        elif choice == "5":
            self.status()

        elif choice == "0":
            exit()
        else:
            print("请输入正确的选项...........\n")
            self.run()

    def cgeconf(self):
        print("\r\n------------------------------------------\n")
        print("1. 添加配置\n2. 删除配置\n0. 返回上一层\n")
        choice = input("请输入 >> ")
        if choice == "1":
            self.addconf()

        elif choice == "2":
            self.delconf()

        elif choice == "0":
            self.run()

        else:
            print("\n请输入正确的选项...........\n")
            self.run()
    

    def subscribe(self):
        print("\r\n------------------------------------------\n")
        print("1. 开启自动更新订阅\n2. 关闭自动更新订阅\n3. 修改订阅地址\n0. 返回上一层\n")
        choice = input("请输入 >> ")
        if choice == "1":
            with open("/etc/v2rayL/current", "wb") as jf:
                self.auto = True
                pickle.dump((self.current, self.url, self.auto), jf)
            print("\n已开启自动更新订阅，下次进入生效\n")
            print("\r------------------------------------------")
            self.run()

        elif choice == "2":
            with open("/etc/v2rayL/current", "wb") as jf:
                self.auto = False
                pickle.dump((self.current, self.url, self.auto), jf)
            print("\n已关闭自动更新订阅，下次进入生效\n")
            print("\r------------------------------------------")
            self.run()

        elif choice == "3":
            self.update()

        elif choice == "0":
            self.run()
        else:
            print("\n请输入正确的选项...........\n")
            self.run()

    def status(self):
        print("\r------------------------------------------")
        print("当前状态: {}".format(self.current))
        print("自动更新: {}".format("开启" if self.auto else "关闭"))
        print("订阅地址：{}".format(self.url if self.url else "无"))
        print("\r------------------------------------------")
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
                    print("\r\n正在连接................\n")
                    output = subprocess.getoutput(["sudo systemctl status v2rayL.service"])
                    if "Active: active" in output:
                        subprocess.call(["sudo systemctl restart v2rayL.service"], shell=True)
                    else:
                        subprocess.call(["sudo systemctl start v2rayL.service"], shell=True)
                except:
                    print("连接失败，请尝试更新订阅后再次连接......")
                    self.run()
                else:   
                    sleep(2)
                    print("成功连接到VPN：{}\n".format(tmp[int(choice)]))
                    print("\r------------------------------------------\n")
                    self.current = tmp[int(choice)]
                    with open("/etc/v2rayL/current", "wb") as jf:
                        pickle.dump((self.current, self.url, self.auto), jf)

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
                        pickle.dump((self.current, self.url, self.auto), jf)
                
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
        print("\r\n------------------------------------------\n")
        url = input("请输入地址，输入 0 返回上一层>> ")
        if url == "0":
            self.subscribe()
        else:
            print("\r\n正在更新订阅地址............................\n")
            self.subs = Sub2Conf(subs_url=url)
            self.subs.update()
            print("订阅地址更新完成，VPN已更新.....\n")
            print("\r------------------------------------------\n")
            with open("/etc/v2rayL/current", "wb") as jf:
                pickle.dump((self.current, url, self.auto), jf)
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
        url = input("请输入配置信息链接, 0返回上一层\n(目前支持 vmess://和ss://)>>> ")
        if url == "0":
            self.run()
        else:
            print("\r\n正在添加配置...................\n")
            self.subs = Sub2Conf(conf_url=url)
            self.subs.add_conf_by_uri()
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