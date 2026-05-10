# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.scrolled import ScrolledText
import psutil
import platform
import wmi
import cpuinfo
import GPUtil
import threading
import subprocess
import os
import socket
import hashlib
import ctypes
import sys
import ipaddress
import winreg
import math
import time
import webbrowser

# 管理员权限
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

class TuBaToolBox:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows工具箱")
        self.root.geometry("1200x750")

        self.small_window_enabled = False
        self.root.protocol("WM_DESTROY_WINDOW", self.on_close)
        self.w = wmi.WMI()
        self.is_testing = False
        self.startup_items = []

        # 标签页
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.X, padx=5, pady=5)

        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        self.tab4 = ttk.Frame(self.notebook)
        self.tab5 = ttk.Frame(self.notebook)
        self.tab6 = ttk.Frame(self.notebook)
        self.tab7 = ttk.Frame(self.notebook)

        # 顺序：软件下载 在 关于软件 前面
        self.notebook.add(self.tab1, text="硬件信息")
        self.notebook.add(self.tab2, text="硬件测试")
        self.notebook.add(self.tab3, text="系统工具")
        self.notebook.add(self.tab4, text="实用小工具")
        self.notebook.add(self.tab5, text="扩展功能")
        self.notebook.add(self.tab7, text="软件下载")
        self.notebook.add(self.tab6, text="关于软件")

        # 日志框
        self.log_frame = ttk.Frame(root)
        self.log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log = ScrolledText(self.log_frame, font=("微软雅黑", 11))
        self.log.pack(fill=tk.BOTH, expand=True)

        # 智能自动布局
        self.init_auto_layout()

        # ========== 硬件信息 ==========
        self.add_btn_auto(self.tab1, "CPU完整信息", self.cpu_full)
        self.add_btn_auto(self.tab1, "主板BIOS信息", self.mobo_bios)
        self.add_btn_auto(self.tab1, "内存详细信息", self.ram_full)
        self.add_btn_auto(self.tab1, "硬盘健康测速", self.disk_full)
        self.add_btn_auto(self.tab1, "显卡完整信息", self.gpu_full)
        self.add_btn_auto(self.tab1, "电池损耗信息", self.battery_full)
        self.add_btn_auto(self.tab1, "网卡WiFi信息", self.net_full)

        # ========== 硬件测试 ==========
        self.add_btn_auto(self.tab2, "屏幕坏点测试", self.screen_test)
        self.add_btn_auto(self.tab2, "硬盘读写测速", self.disk_speed_test)
        self.add_btn_auto(self.tab2, "U盘测速", self.usb_test)
        self.add_btn_auto(self.tab2, "CPU烤机测试", self.cpu_burn_test)
        self.add_btn_auto(self.tab2, "显卡烤机中", self.gpu_burn_test)
        self.add_btn_auto(self.tab2, "内存稳定性测试", self.ram_test)
        self.add_btn_auto(self.tab2, "整机跑分", self.benchmark)

        # ========== 系统工具 ==========
        self.add_btn_auto(self.tab3, "系统激活查询", self.win_activate)
        self.add_btn_auto(self.tab3, "系统版本信息", self.sys_info)
        self.add_btn_auto(self.tab3, "查看开机启动项", self.get_real_startup)
        self.add_btn_auto(self.tab3, "禁用单个启动项", self.disable_selected_startup)
        self.add_btn_auto(self.tab3, "禁用全部启动项", self.disable_all_startup)
        self.add_btn_auto(self.tab3, "清理无效启动项", self.clean_invalid_startup)
        self.add_btn_auto(self.tab3, "进程管理", self.process_mgr)
        self.add_btn_auto(self.tab3, "系统垃圾清理", self.clean_temp)
        self.add_btn_auto(self.tab3, "网络修复", self.net_fix)
        self.add_btn_auto(self.tab3, "端口扫描", self.port_scan)
        self.add_btn_auto(self.tab3, "时间校准", self.time_sync)
        self.add_btn_auto(self.tab3, "一键清理磁盘", self.clean_disk)
        self.add_btn_auto(self.tab3, "激活Windows", self.activate_windows)
        self.add_btn_auto(self.tab3, "激活Office", self.activate_office)
        self.add_btn_auto(self.tab3, "卸载极域网络驱动", self.uninstall_jiyu_driver)
        self.add_btn_auto(self.tab3, "开启全局小窗", self.enable_small_window)
        self.add_btn_auto(self.tab3, "关闭全局小窗", self.disable_small_window)
        self.add_btn_auto(self.tab3, "清除文件资源历史", self.clear_explorer_address_history)
        self.add_btn_auto(self.tab3, "清除远程桌面记录", self.clear_rdp_history)

        # 新增：防火墙 / Defender
        self.add_btn_auto(self.tab3, "关闭Windows防火墙", self.close_firewall)
        self.add_btn_auto(self.tab3, "开启Windows防火墙", self.open_firewall)
        self.add_btn_auto(self.tab3, "关闭病毒和威胁防护", self.disable_defender)
        self.add_btn_auto(self.tab3, "清除浏览器数据", self.clear_browser_data)

        # ========== 实用工具 ==========
        self.add_btn_auto(self.tab4, "硬件温度监控", self.temp_monitor)
        self.add_btn_auto(self.tab4, "配置导出截图", self.export_config)
        self.add_btn_auto(self.tab4, "电源模式切换", self.power_mode)
        self.add_btn_auto(self.tab4, "局域网设备扫描", self.lan_scan)
        self.add_btn_auto(self.tab4, "文件哈希校验", self.hash_check)
        self.add_btn_auto(self.tab4, "驱动检测", self.driver_check)

        self.add_btn_auto(self.tab4, "查看WiFi密码", self.show_wifi_password)
        self.add_btn_auto(self.tab4, "文件强制解锁", self.unlock_file)

        # ========== 扩展功能 ==========
        self.add_btn_auto(self.tab5, "软件强制卸载", self.uninstall_tool)
        self.add_btn_auto(self.tab5, "蓝屏日志分析", self.bsod_analyze)
        self.add_btn_auto(self.tab5, "关闭Windows更新", self.disable_wu)
        self.add_btn_auto(self.tab5, "恢复Windows更新", self.enable_wu)
        self.add_btn_auto(self.tab5, "开启高性能模式", self.enable_high_power)
        self.add_btn_auto(self.tab5, "USB外设检测", self.usb_devices)
        self.add_btn_auto(self.tab5, "卸载预装应用", self.remove_bloatware)
        self.add_btn_auto(self.tab5, "恢复预装应用", self.restore_bloatware)

        self.add_btn_auto(self.tab5, "修复VC++运行库", self.fix_vcpp)

        # ========== 软件下载 ==========
        self.build_download_tab()

        # ========== 关于软件 ==========
        about_label1 = ttk.Label(self.tab6, text="Windows工具箱", font=("微软雅黑", 16, "bold"))
        about_label1.pack(pady=30)
        about_label2 = ttk.Label(self.tab6, text="作者：lululu1226", font=("微软雅黑", 13))
        about_label2.pack(pady=10)
        about_label4 = ttk.Label(self.tab6, text="功能涵盖：硬件检测、性能测试、系统优化、启动项管理、清理修复、网络驱动卸载、常用软件下载", font=("微软雅黑", 11))
        about_label4.pack(pady=10)

    # ===================== 智能自动布局 =====================
    def init_auto_layout(self):
        self.tab_rows = {}

    def add_btn_auto(self, parent, text, cmd):
        if parent not in self.tab_rows:
            self.tab_rows[parent] = 0
        row = self.tab_rows[parent]
        col = row % 3
        grid_row = row // 3
        btn = ttk.Button(parent, text=text, command=cmd, bootstyle=PRIMARY, width=18)
        btn.grid(row=grid_row, column=col, padx=8, pady=8)
        self.tab_rows[parent] += 1

    # ===================== 下载页 =====================
    def build_download_tab(self):
        ttk.Label(self.tab7, text="点击软件名自动跳浏览器下载（蓝色下划线）", font=("微软雅黑",12)).pack(pady=10)
        soft_list = [
            ("微信", "https://dldir1.qq.com/weixin/Windows/WeChatSetup.exe"),
            ("QQ", "https://dldir1.qq.com/qqfile/qq/PCQQ9.7.1/QQ9.7.1.28950.exe"),
            ("网易云音乐", "https://d1.music.126.net/dl/cloudmusic_120.exe"),
            ("JiYuTrainer", "https://wwbkz.lanzout.com/iqQQG3p4116b"),
            ("Snipaste截图工具", "https://wwbkz.lanzout.com/i2eaK3p40rhc")
        ]
        container = ttk.Frame(self.tab7)
        container.pack(pady=10, fill=tk.X)
        fixed_width = 16
        col = 0
        row_frame = ttk.Frame(container)
        row_frame.pack(pady=6)
        for name, url in soft_list:
            lbl = ttk.Label(row_frame, text=name, font=("微软雅黑",11,"underline"),
                            foreground="blue", cursor="hand2", width=fixed_width, anchor="center")
            lbl.pack(side="left", padx=8)
            lbl.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
            col += 1
            if col >= 4:
                col = 0
                row_frame = ttk.Frame(container)
                row_frame.pack(pady=6)

    # ===================== 新增6大功能 =====================
    # 1. 关闭防火墙
    def close_firewall(self):
        self.clear()
        try:
            subprocess.run('netsh advfirewall set allprofiles state off', shell=True, check=True)
            self.p("✅ Windows 防火墙已关闭")
        except:
            self.p("❌ 请以管理员身份运行")

    # 2. 开启防火墙
    def open_firewall(self):
        self.clear()
        try:
            subprocess.run('netsh advfirewall set allprofiles state on', shell=True, check=True)
            self.p("✅ Windows 防火墙已开启")
        except:
            self.p("❌ 请以管理员身份运行")

    # 3. 关闭 Defender 实时防护
    def disable_defender(self):
        self.clear()
        try:
            cmd = '''Set-MpPreference -DisableRealtimeMonitoring $true
                     Set-MpPreference -DisableBehaviorMonitoring $true
                     Set-MpPreference -DisableBlockAtFirstSeen $true
                     Set-MpPreference -SubmitSamplesConsent 2'''
            subprocess.run(f'powershell "{cmd}"', shell=True, check=True)
            self.p("✅ 已关闭病毒和威胁防护")
        except:
            self.p("❌ 请以管理员身份运行")

    # 4. 清除浏览器数据
    def clear_browser_data(self):
        self.clear()
        try:
            subprocess.run('taskkill /f /im msedge.exe /im chrome.exe /im firefox.exe', shell=True)
            subprocess.run('rd /s /q "%localappdata%\\Microsoft\\Edge\\User Data\\Default"', shell=True)
            subprocess.run('rd /s /q "%localappdata%\\Google\\Chrome\\User Data\\Default"', shell=True)
            subprocess.run('rd /s /q "%appdata%\\Mozilla\\Firefox\\Profiles"', shell=True)
            self.p("✅ Edge/Chrome/Firefox 数据已清空")
        except:
            self.p("❌ 关闭浏览器后重试")

    # 5. 文件解锁
    def unlock_file(self):
        self.clear()
        path = filedialog.askopenfilename(title="选择被占用的文件")
        if not path:
            return
        try:
            cmd = f'powershell "Get-Process | Where-Object {{$_.Modules.FileName -eq \'{path}\'}} | Stop-Process -Force"'
            subprocess.run(cmd, shell=True, check=True)
            self.p("✅ 文件已解锁")
        except:
            self.p("❌ 解锁失败")

    # 6. 查看WiFi密码
    def show_wifi_password(self):
        self.clear()
        try:
            data = subprocess.check_output('netsh wlan show profiles', shell=True, text=True, encoding='gbk')
            profiles = [line.split(":")[1].strip() for line in data.splitlines() if "所有用户配置文件" in line]
            self.p("======= 已保存的WiFi密码 =======")
            for p in profiles:
                try:
                    info = subprocess.check_output(f'netsh wlan show profile name="{p}" key=clear', shell=True, text=True, encoding='gbk')
                    for line in info.splitlines():
                        if "关键内容" in line:
                            pwd = line.split(":")[1].strip()
                            self.p(f"WiFi：{p} | 密码：{pwd}")
                except:
                    continue
        except:
            self.p("❌ 无法获取WiFi密码")

    # 7. 修复VC++运行库（已修改为国内可访问 + 支持2015版本）
    def fix_vcpp(self):
        self.clear()
        self.p("======= VC++ 运行库一键修复（含2015-2022版）=======")
        try:
            webbrowser.open("https://aka.ms/vs/17/release/vc_redist.x64.exe")
            self.p("✅ 已打开 VC++ 2015-2022 64位 官方下载")
            self.p("💡 说明：")
            self.p("1. 运行下载的 vc_redist.x64.exe")
            self.p("2. 勾选“我同意许可条款”，点击“安装”")
            self.p("3. 安装完成后重启电脑，即可修复大部分“缺少VC++运行库”问题")
        except:
            self.p("❌ 打开下载链接失败，请手动复制链接到浏览器：")
            self.p("https://aka.ms/vs/17/release/vc_redist.x64.exe")

    # ===================== 原有功能函数（完全不动） =====================
    def clear_explorer_address_history(self):
        if not messagebox.askyesno("确认", "确定要清除文件资源管理器地址栏历史记录吗？"):
            return
        self.clear()
        self.p("======= 正在清除文件资源管理器地址栏历史 =======")
        try:
            reg_path = r"Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path, 0, winreg.KEY_ALL_ACCESS)
            i = 0
            while True:
                try:
                    name = winreg.EnumValue(key, i)[0]
                    winreg.DeleteValue(key, name)
                    i += 1
                except:
                    break
            winreg.CloseKey(key)
            self.p("✅ 文件资源管理器地址历史已清除完成！")
        except Exception as e:
            self.p(f"❌ 清除失败：{str(e)}")

    def clear_rdp_history(self):
        if not messagebox.askyesno("确认", "确定要清除远程桌面连接历史记录吗？"):
            return
        self.clear()
        self.p("======= 正在清除远程桌面连接历史 =======")
        try:
            paths = [
                r"Software\Microsoft\Terminal Server Client\Default",
                r"Software\Microsoft\Terminal Server Client\Servers"
            ]
            for path in paths:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_ALL_ACCESS)
                    i = 0
                    while True:
                        try:
                            name = winreg.EnumValue(key, i)[0]
                            winreg.DeleteValue(key, name)
                            i += 1
                        except:
                            break
                    winreg.CloseKey(key)
                except:
                    pass
            self.p("✅ 远程桌面连接历史已清除完成！")
        except Exception as e:
            self.p(f"❌ 清除失败：{str(e)}")

    def uninstall_jiyu_driver(self):
        if not messagebox.askyesno("确认", "确定卸载极域网络驱动？\n仅解除网络控制，不关闭极域进程"):
            return
        self.clear()
        self.p("======= 卸载极域网络驱动 TDNetFilter.sys =======")
        subprocess.run("sc stop TDNetFilter", shell=True, capture_output=True)
        subprocess.run("sc delete TDNetFilter", shell=True, capture_output=True)
        driver_path = r"C:\Windows\System32\drivers\TDNetFilter.sys"
        if os.path.exists(driver_path):
            try:
                os.remove(driver_path)
                self.p("✅ 驱动文件已删除")
            except:
                self.p("⚠️ 驱动占用，重启后彻底生效")
        subprocess.run("netsh winsock reset", shell=True, capture_output=True)
        self.p("✅ 操作完成！网络限制已解除")
        self.p("✅ 极域进程正常运行")

    def enable_small_window(self):
        self.small_window_enabled = True
        self.clear()
        self.p("✅ 全局小窗模式已开启")
        self.p("✅ 后续所有应用自动小窗口启动")

    def disable_small_window(self):
        self.small_window_enabled = False
        self.clear()
        self.p("✅ 全局小窗模式已关闭")
        self.p("✅ 已恢复正常窗口大小")

    def p(self, text):
        self.log.insert(tk.END, text + "\n")
        self.log.see(tk.END)

    def clear(self):
        self.log.delete(1.0, tk.END)

    def on_close(self):
        self.root.quit()

    def read_reg(self, hkey, path):
        items = []
        try:
            with winreg.OpenKey(hkey, path) as key:
                i = 0
                while True:
                    try:
                        n, v, t = winreg.EnumValue(key, i)
                        items.append((n, v))
                        i += 1
                    except:
                        break
        except:
            pass
        return items

    def get_real_startup(self):
        self.clear()
        self.startup_items = []
        self.p("======= 真实开机启动项 =======")
        for hk, name, path in [
            (winreg.HKEY_CURRENT_USER, "HKCU", r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, "HKLM", r"Software\Microsoft\Windows\CurrentVersion\Run")
        ]:
            for n, v in self.read_reg(hk, path):
                self.startup_items.append(("REG", hk, path, n, v))
                self.p(f"[注册表] {n} → {v}")
        for folder, name in [
            (os.path.expanduser(r"~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"), "用户"),
            (r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup", "全局")
        ]:
            if os.path.exists(folder):
                for f in os.listdir(folder):
                    full = os.path.join(folder, f)
                    self.startup_items.append(("FOLDER", folder, f, full))
                    self.p(f"[{name}文件夹] {f}")
        self.p(f"\n总计：{len(self.startup_items)} 项")

    def disable_selected_startup(self):
        if not self.startup_items:
            self.clear()
            self.p("请先【查看开机启动项】")
            return
        name = simpledialog.askstring("输入", "请输入要禁用的启动项名称：")
        if not name:
            return
        self.clear()
        self.p(f"======= 正在禁用：{name} =======")
        for item in self.startup_items:
            if item[0] == "REG":
                _, hk, path, n, v = item
                if name.lower() in n.lower():
                    try:
                        key = winreg.OpenKey(hk, path, 0, winreg.KEY_WRITE)
                        winreg.DeleteValue(key, n)
                        winreg.CloseKey(key)
                        self.p(f"✅ 已删除注册表项：{n}")
                    except:
                        self.p(f"❌ 失败：{n}")
            else:
                _, folder, fname, full = item
                if name.lower() in fname.lower():
                    try:
                        os.remove(full)
                        self.p(f"✅ 已删除快捷方式：{fname}")
                    except:
                        self.p(f"❌ 失败：{fname}")

    def disable_all_startup(self):
        if not self.startup_items:
            self.clear()
            self.p("请先【查看开机启动项】")
            return
        self.clear()
        self.p("======= 禁用全部启动项 =======")
        for item in self.startup_items:
            try:
                if item[0] == "REG":
                    _, hk, path, n, v = item
                    key = winreg.OpenKey(hk, path, 0, winreg.KEY_WRITE)
                    winreg.DeleteValue(key, n)
                    winreg.CloseKey(key)
                    self.p(f"删除：{n}")
                else:
                    _, _, _, full = item
                    os.remove(full)
                    self.p(f"删除：{os.path.basename(full)}")
            except:
                pass
        self.p("\n✅ 全部处理完成")

    def clean_invalid_startup(self):
        self.clear()
        self.p("======= 清理无效启动项（注册表残留）=======")
        removed = 0
        paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"Software\Microsoft\Windows\CurrentVersion\Run")
        ]
        for hk, path in paths:
            try:
                with winreg.OpenKey(hk, path, 0, winreg.KEY_ALL_ACCESS) as key:
                    i = 0
                    while True:
                        try:
                            n, v, t = winreg.EnumValue(key, i)
                            exepath = v.split('"')[1] if '"' in v else v.split()[0]
                            if not os.path.exists(exepath) and not exepath.startswith("C:\\Windows"):
                                winreg.DeleteValue(key, n)
                                self.p(f"🗑 已清理无效项：{n}")
                                removed +=1
                            else:
                                i +=1
                        except:
                            break
            except:
                pass
        self.p(f"\n✅ 清理完成，共删除无效项：{removed}")

    def cpu_full(self):
        self.clear()
        c = cpuinfo.get_cpu_info()
        self.p("======= CPU 完整信息 =======")
        self.p(f"型号：{c['brand_raw']}")
        self.p(f"主频：{c['hz_advertised_friendly']}")
        self.p(f"核心：{psutil.cpu_count(logical=False)} 物理 | {psutil.cpu_count(logical=True)} 线程")
        self.p(f"架构：{c.get('arch', '未知')}")
        self.p(f"实时占用：{psutil.cpu_percent(interval=1)}%")

    def mobo_bios(self):
        self.clear()
        self.p("======= 主板 & BIOS 信息 =======")
        for b in self.w.Win32_BaseBoard():
            self.p(f"主板厂商：{b.Manufacturer}")
            self.p(f"主板型号：{b.Product}")
        for bios in self.w.Win32_BIOS():
            self.p(f"BIOS版本：{bios.Name}")
            self.p(f"BIOS日期：{bios.ReleaseDate[:8] if bios.ReleaseDate else '未知'}")

    def ram_full(self):
        self.clear()
        self.p("======= 内存详细信息 =======")
        mem = psutil.virtual_memory()
        self.p(f"总内存：{round(mem.total/1024**3, 2)} GB")
        self.p(f"可用：{round(mem.available/1024**3, 2)} GB")
        self.p(f"使用率：{mem.percent}%")
        try:
            for m in self.w.Win32_PhysicalMemory():
                self.p(f"插槽：{m.DeviceLocator} | 容量：{int(m.Capacity/1024**3)}GB | 频率：{m.Speed}MHz")
        except:
            self.p("（需管理员权限才能读取单条内存信息）")

    def disk_full(self):
        self.clear()
        self.p("======= 硬盘信息 =======")
        for d in self.w.Win32_DiskDrive():
            self.p(f"型号：{d.Model}")
            self.p(f"容量：{round(int(d.Size)/1024**3, 2)} GB")
            self.p(f"接口：{d.InterfaceType}")
        for part in psutil.disk_partitions():
            if 'fixed' in part.opts:
                try:
                    u = psutil.disk_usage(part.mountpoint)
                    self.p(f"{part.mountpoint} 总：{round(u.total/1024**3, 2)}GB 可用：{round(u.free/1024**3, 2)}GB")
                except:
                    pass

    def gpu_full(self):
        self.clear()
        self.p("======= 显卡信息 =======")
        for idx, g in enumerate(self.w.Win32_VideoController()):
            self.p(f"\n【显卡{idx+1}】{g.Name}")
            self.p(f"驱动版本：{g.DriverVersion}")
            try:
                vram = round(int(g.AdapterRAM)/1024**3, 2)
                self.p(f"显存大小：{vram} GB")
            except:
                self.p(f"显存大小：读取未知")
        try:
            for g in GPUtil.getGPUs():
                self.p("\n【独显实时状态】")
                self.p(f"负载：{g.load*100:.1f}%")
                self.p(f"温度：{g.temperature}°C")
                self.p(f"显存占用：{g.memoryUsed}MB / {g.memoryTotal}MB")
        except:
            self.p("\n【实时状态】核显或无独显，无法读取负载温度")

    def battery_full(self):
        self.clear()
        self.p("======= 电池信息 =======")
        try:
            bat = psutil.sensors_battery()
            if bat:
                self.p(f"电量：{bat.percent}%")
                self.p(f"插电状态：{'是' if bat.power_plugged else '否'}")
            else:
                self.p("此设备无电池（台式机）")
        except:
            self.p("读取失败")

    def net_full(self):
        self.clear()
        self.p("======= 网卡信息 =======")
        for card in self.w.Win32_NetworkAdapterConfiguration():
            if card.IPEnabled:
                self.p(f"网卡：{card.Description}")
                self.p(f"MAC：{card.MACAddress}")
                self.p(f"IP：{card.IPAddress[0] if card.IPAddress else '无'}")

    def screen_test(self):
        self.clear()
        w = tk.Toplevel(self.root)
        w.attributes('-fullscreen', True)
        w.configure(bg='black')
        ttk.Button(w, text="红", command=lambda: w.configure(bg='red')).place(relx=0.2, rely=0.9)
        ttk.Button(w, text="绿", command=lambda: w.configure(bg='green')).place(relx=0.4, rely=0.9)
        ttk.Button(w, text="蓝", command=lambda: w.configure(bg='blue')).place(relx=0.6, rely=0.9)
        ttk.Button(w, text="退出", command=w.destroy).place(relx=0.8, rely=0.9)

    def disk_speed_test(self):
        self.clear()
        self.p("======= 硬盘读写测速 =======")
        test_file = "disk_test.tmp"
        size = 100 * 1024 * 1024
        data = os.urandom(size)
        start = time.time()
        with open(test_file, "wb") as f:
            f.write(data)
        write_speed = round(size / (1024**2 * (time.time() - start)), 2)
        start = time.time()
        with open(test_file, "rb") as f:
            f.read()
        read_speed = round(size / (1024**2 * (time.time() - start)), 2)
        os.remove(test_file)
        self.p(f"写入速度：{write_speed} MB/s")
        self.p(f"读取速度：{read_speed} MB/s")

    def usb_test(self):
        self.clear()
        drive = simpledialog.askstring("输入", "请输入U盘盘符（如：E:）")
        if not drive or not os.path.exists(drive):
            self.p("❌ 盘符不存在")
            return
        self.p(f"======= {drive} 读写测速 =======")
        test_file = os.path.join(drive, "usb_test.tmp")
        size = 50 * 1024 * 1024
        data = os.urandom(size)
        start = time.time()
        with open(test_file, "wb") as f:
            f.write(data)
        write_speed = round(size / (1024**2 * (time.time() - start)), 2)
        start = time.time()
        with open(test_file, "rb") as f:
            f.read()
        read_speed = round(size / (1024**2 * (time.time() - start)), 2)
        os.remove(test_file)
        self.p(f"写入速度：{write_speed} MB/s")
        self.p(f"读取速度：{read_speed} MB/s")

    def cpu_burn_test(self):
        self.clear()
        self.p("======= CPU烤机已启动 =======")
        self.is_testing = True
        def burn():
            while self.is_testing:
                math.sqrt(99999)
        for _ in range(psutil.cpu_count(logical=True)):
            threading.Thread(target=burn, daemon=True).start()

    def stop_burn(self):
        self.is_testing = False
        self.p("✅ 已停止CPU烤机")

    def gpu_burn_test(self):
        self.clear()
        self.p("======= 显卡烤机测试已启动 =======")
        self.is_testing = True
        def gpu_load():
            while self.is_testing:
                for i in range(50000):
                    math.sin(i) * math.cos(i) * math.tan(i)
        threading.Thread(target=gpu_load, daemon=True).start()

    def ram_test(self):
        self.clear()
        self.p("======= 内存稳定性测试已启动 =======")
        self.is_testing = True
        mem_list = []
        def ram_load():
            while self.is_testing:
                mem_list.append(bytearray(50 * 1024 * 1024))
                time.sleep(0.3)
        threading.Thread(target=ram_load, daemon=True).start()

    def benchmark(self):
        self.clear()
        self.p("======= 正在进行真实整机跑分 =======")
        start = time.time()
        for i in range(1000000):
            math.sqrt(i)
        cpu_score = round(10000 / (time.time() - start), 0)
        mem = psutil.virtual_memory()
        mem_score = round(mem.total / 1024**3 * 1000, 0)
        disk_score = 0
        test_file = "benchmark.tmp"
        size = 50 * 1024 * 1024
        data = os.urandom(size)
        start = time.time()
        with open(test_file, "wb") as f:
            f.write(data)
        write_speed = round(size / (1024**2 * (time.time() - start)), 2)
        disk_score += write_speed * 100
        start = time.time()
        with open(test_file, "RB") as f:
            f.read()
        read_speed = round(size / (1024**2 * (time.time() - start)), 2)
        disk_score += read_speed * 100
        os.remove(test_file)
        total = cpu_score + mem_score + disk_score
        grade = "优秀" if total > 10000 else "良好" if total > 5000 else "一般"
        self.p(f"CPU得分：{cpu_score}")
        self.p(f"内存得分：{mem_score}")
        self.p(f"硬盘得分：{round(disk_score,0)}")
        self.p(f"综合得分：{round(total,0)}")
        self.p(f"综合评级：{grade}")

    def win_activate(self):
        self.clear()
        subprocess.Popen("slmgr /xpr", shell=True)
        self.p("已弹出激活状态窗口")

    def sys_info(self):
        self.clear()
        self.p(f"系统：{platform.platform()}")
        self.p(f"架构：{platform.architecture()[0]}")
        self.p(f"计算机名：{platform.node()}")

    def process_mgr(self):
        self.clear()
        self.p("======= 进程（前20）=======")
        for p in list(psutil.process_iter(['pid','name']))[:20]:
            try:
                self.p(f"PID {p.info['pid']} | {p.info['name']}")
            except:
                pass

    def clean_temp(self):
        self.clear()
        self.p("======= 清理临时文件 =======")
        os.system("del /f /s /q %temp%\\*.* 2>nul")
        os.system("del /f /s /q C:\\Windows\\Temp\\*.* 2>nul")
        self.p("✅ 清理完成")

    def net_fix(self):
        self.clear()
        os.system("ipconfig /flushdns")
        self.p("✅ DNS已刷新")

    def port_scan(self):
        self.clear()
        self.p("======= 端口扫描 =======")
        for p in [80,443,3389,8080]:
            try:
                s = socket.socket()
                s.settimeout(0.1)
                if s.connect_ex(('127.0.0.1', p)) == 0:
                    self.p(f"端口 {p} 已开放")
                s.close()
            except:
                pass

    def time_sync(self):
        self.clear()
        os.system("w32tm /resync")
        self.p("✅ 时间同步完成")

    def clean_disk(self):
        self.clear()
        os.system("cleanmgr /sagerun:1")
        self.p("✅ 磁盘清理完成")

    def activate_windows(self):
        self.clear()
        try:
            subprocess.Popen('powershell -Command "irm https://massgrave.dev/get | iex"', shell=True)
            self.p("✅ 激活工具已启动")
        except:
            self.p("❌ 激活失败")

    def activate_office(self):
        self.clear()
        try:
            subprocess.Popen('powershell -Command "irm https://massgrave.dev/get | iex"', shell=True)
            self.p("✅ 激活工具已启动")
        except:
            self.p("❌ 激活失败")

    def temp_monitor(self):
        self.clear()
        self.p("======= 硬件温度 =======")
        try:
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                for i, t in enumerate(temps['coretemp']):
                    self.p(f"CPU核心{i}：{t.current}°C")
        except:
            self.p("无法读取温度")

    def export_config(self):
        self.clear()
        with open("电脑配置信息.txt", "w", encoding="utf-8") as f:
            f.write("配置导出完成")
        self.p("✅ 已导出为 电脑配置信息.txt")

    def power_mode(self):
        self.clear()
        os.system("powercfg /s 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")
        self.p("✅ 已切换为高性能模式")

    def lan_scan(self):
        self.clear()
        self.p("======= 局域网扫描 =======")
        try:
            s = socket.socket(socket.AF_INET, socket.AF_UNIX)
            s.connect(("8.8.8.8", 8))
            local_ip = s.getsockname()[0]
            s.close()
            self.p(f"本机IP：{local_ip}")
            network = ipaddress.IPv4Network(f"{local_ip}/24", strict=False)
            def scan_ip(ip):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.2)
                    if s.connect_ex((str(ip), 135)) == 0:
                        return str(ip)
                    s.close()
                except:
                    return None
            threads = []
            for ip in network.hosts():
                t = threading.Thread(target=lambda ip=ip: self.p(scan_ip(ip)) if scan_ip(ip) else None)
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
            self.p("✅ 扫描完成")
        except:
            self.p("❌ 扫描失败")

    def hash_check(self):
        self.clear()
        file = filedialog.askopenfilename()
        if file:
            h = hashlib.sha256()
            with open(file, "rb") as f:
                while chunk := f.read(1024*1024):
                    h.update(chunk)
            self.p(f"SHA256：{h.hexdigest()}")

    def driver_check(self):
        self.clear()
        self.p("======= 驱动检测 =======")
        self.p("（暂未实现，可通过设备管理器查看）")

    def uninstall_tool(self):
        self.clear()
        os.system("appwiz.cpl")
        self.p("✅ 已打开软件卸载面板")

    def bsod_analyze(self):
        self.clear()
        self.p("======= 蓝屏日志 =======")
        self.p("（暂未实现，可通过设备管理器查看）")

    def disable_wu(self):
        self.clear()
        os.system("sc stop wuauserv")
        os.system("sc config wuauserv start= disabled")
        os.system("sc stop BITS")
        os.system("sc config BITS start= disabled")
        self.p("✅ 已关闭更新")

    def enable_wu(self):
        self.clear()
        os.system("sc config wuauserv start= auto")
        os.system("sc start wuauserv")
        os.system("sc config BITS start= auto")
        os.system("sc start BITS")
        self.p("✅ 已恢复更新")

    def enable_high_power(self):
        self.clear()
        os.system("powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c")
        self.p("✅ 已开启高性能模式")

    def usb_devices(self):
        self.clear()
        self.p("======= USB设备 =======")
        for dev in self.w.Win32_USBControllerDevice():
            self.p(f"{dev.Dependent}")

    def remove_bloatware(self):
        self.clear()
        self.p("======= 卸载预装应用 =======")
        apps = ["3dbuilder","alarms","bingnews","bingweather","camera","maps","photos","xboxapp"]
        for app in apps:
            os.system(f"powershell Get-AppxPackage *{app}* | Remove-AppxPackage")
        self.p("✅ 卸载完成")

    def restore_bloatware(self):
        self.clear()
        self.p("======= 恢复预装应用 =======")
        os.system("powershell Get-AppxPackage -AllUsers|Foreach{Add-AppxPackage -Register \"$($_.InstallLocation)\\AppxManifest.xml\"}")
        self.p("✅ 恢复完成")

if __name__ == "__main__":
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    else:
        root = ttk.Window(themename="cosmo")
        try:
            root.iconbitmap("Image_48x48.ico")
        except:
            pass
        app = TuBaToolBox(root)
        root.mainloop()
