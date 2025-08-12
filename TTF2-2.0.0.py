import os
import shutil
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import platform
import webbrowser
from datetime import datetime
import urllib.request
import zipfile
import tempfile
import sys
import winreg
import urllib.parse
import re
import threading

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(sys.argv[0]))

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("TTF2工具集")
        self.root.geometry("1356x894")
        self.root.resizable(True, True)

        self.center_window(self.root)

        if platform.system() == "Windows":
            default_font = ("Microsoft YaHei", 10)
        else:
            default_font = ("WenQuanYi Micro Hei", 10)
        self.root.option_add("*Font", default_font)
        
        self.installed_frameworks = self.get_installed_frameworks()
        
        self.uninstall_buttons = {}        
        self.download_buttons = {}
        
        self.local_storage = os.path.join(get_app_dir(), "框架储存位置")
        os.makedirs(self.local_storage, exist_ok=True)
        
        self.create_main_widgets()
        
        self.install_window = None
        self.uninstall_window = None

        self.local_storage = os.path.join(get_app_dir(), "框架储存位置")
        self.ensure_local_storage_exists() 

    def center_window(self, window):
        window.update_idletasks()
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        window.geometry(f'{window_width}x{window_height}+{x}+{y}')              

    def create_main_widgets(self):
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        right_content = ttk.Frame(right_frame)
        right_content.pack(expand=True, anchor="n", fill=tk.BOTH)

        modsite_frame = ttk.LabelFrame(
            right_content,
            text="MOD网站链接",
            padding="20"
        )
        modsite_frame.pack(anchor="nw", pady=(100, 10), padx=(1, 50))

        disclaimer_frame = ttk.Frame(right_content)
        disclaimer_frame.pack(anchor="n", fill=tk.X, pady=(10, 0), padx=(1, 50))

        disclaimer_sep = ttk.Separator(disclaimer_frame, orient='horizontal')
        disclaimer_sep.pack(fill=tk.X, pady=(2, 8))        

        label_disclaimer = ttk.Label(
            disclaimer_frame,
            text="——免责声明——",
            font=("Microsoft YaHei", 15, "bold"),
            foreground="red"
        )
        label_disclaimer.pack(anchor="center")

        label_disclaimer_content = ttk.Label(
            disclaimer_frame,
            text="本软件仅用于学习、交流目的,所有资源均来自互联网公开渠道,版权归原作者所有.请勿将本软件用于任何商业用途或违法用途.因使用本软件造成的任何后果,开发者不承担任何责任.若您不同意本声明,请立即删除本软件及相关文件.使用此软件任何功能代表你已同意此声明.如有侵权请联系删除。",
            font=("Microsoft YaHei", 10),
            wraplength=280,
            justify="center",
            foreground="#444"
        )
        label_disclaimer_content.pack(anchor="center", pady=(5, 10))
        links_text = tk.Text(disclaimer_frame, height=10, width=33, font=("Microsoft YaHei", 10), wrap=tk.NONE, bg="#f8f8f8", relief=tk.FLAT)
        links_text.insert(tk.END, "北极星CN官网链接：", "blue")
        links_text.insert(tk.END, "https://northstar.cool/\n")
        links_text.insert(tk.END, "\n")
        links_text.insert(tk.END, "北极星EN Github链接：", "blue")
        links_text.insert(tk.END, "https://github.com/R2Northstar\n")
        links_text.insert(tk.END, "\n")
        links_text.insert(tk.END, "Vanilla+ Github链接：", "blue")
        links_text.insert(tk.END, "https://github.com/NachosChipeados/NP.VanillaPlus\n")            
        links_text.insert(tk.END, "Vanilla+ 作者Github主页链接：", "blue") 
        links_text.insert(tk.END, "https://github.com/NachosChipeados\n")
        links_text.insert(tk.END, "\n")               
        links_text.insert(tk.END, "离子框架Github链接：", "blue")      
        links_text.insert(tk.END, "https://github.com/sonny-tel/Ion\n")
        links_text.insert(tk.END, "离子框架 作者Github主页链接：", "blue")
        links_text.insert(tk.END, "https://github.com/sonny-tel")
        links_text.tag_configure("blue", foreground="#1a73e8", font=("Microsoft YaHei", 10, "bold"))
        links_text.config(state=tk.DISABLED, cursor="arrow")
        links_text.pack(anchor="center", pady=(0, 10), fill=tk.X, expand=True)

        label_mod_error1 = ttk.Label(disclaimer_frame, text="定位“MOD报错”位置功能 正在设想开发中", font=("Microsoft YaHei", 10), foreground="#888888")
        label_mod_error1.pack(anchor="center", pady=(100, 0))
        label_mod_error2 = ttk.Label(disclaimer_frame, text="其实没做出来是因为懒~", font=("Microsoft YaHei", 10), foreground="#888888")
        label_mod_error2.pack(anchor="center", pady=(0, 10))  

        btn_frame = ttk.Frame(modsite_frame)
        btn_frame.pack(fill=tk.X)

        ttk.Button(
            btn_frame,
            text="TTF2-Thunderstore",
            command=lambda: webbrowser.open("https://thunderstore.io/c/northstar/")
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="TTF2-Nexus",
            command=lambda: webbrowser.open("https://www.nexusmods.com/games/titanfall2")
        ).pack(side=tk.LEFT, padx=5)

        github_btn_frame = ttk.Frame(right_content)
        github_btn_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 20))

        ttk.Button(
            github_btn_frame,
            text="Github项目开源链接",
            width=16,
            command=lambda: webbrowser.open("https://github.com/TwoSevenFour-274/TTF2-Toolset")
        ).pack(side=tk.LEFT, padx=(5, 20), anchor="e")

        ttk.Button(
            github_btn_frame,
            text="关闭",
            width=8,
            command=self.root.destroy
        ).pack(side=tk.RIGHT, padx=5, anchor="e")
        
        ttk.Label(
            left_frame, 
            text="TTF2工具集", 
            font=("Microsoft YaHei", 20, "bold")
        ).pack(pady=15)
        
        canvas_frame = ttk.Frame(left_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(canvas_frame)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        content_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        ttk.Label(
            content_frame, 
            text="框架安装", 
            font=("Microsoft YaHei", 14, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))
        
        functions_frame = ttk.LabelFrame(content_frame, text="框架列表", padding="15")
        functions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(
            functions_frame, 
            text="社区服", 
            font=("Microsoft YaHei", 12, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))
        
        cn_north_frame = ttk.Frame(functions_frame)
        cn_north_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(cn_north_frame, text="CN北-框架", width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(cn_north_frame, text="安装", command=self.install_cn_north_frame).pack(side=tk.LEFT, padx=5)
        
        uninstall_btn_state = tk.NORMAL if "社区服-CN北-框架" in self.installed_frameworks else tk.DISABLED
        cn_north_uninstall_btn = ttk.Button(
            cn_north_frame, 
            text="卸载", 
            command=self.uninstall_cn_north_frame,
            state=uninstall_btn_state
        )
        cn_north_uninstall_btn.pack(side=tk.LEFT, padx=5)
        self.uninstall_buttons["社区服-CN北-框架"] = cn_north_uninstall_btn
        
        ttk.Button(
            cn_north_frame, 
            text="下载框架到本地", 
            command=lambda: self.download_framework(
                "社区服-CN北-框架", 
                "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-1/Community.Service-CN.North-Frame.zip"
            )
        ).pack(side=tk.LEFT, padx=5)
        
        cn_north_lts_frame = ttk.Frame(functions_frame)
        cn_north_lts_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(cn_north_lts_frame, text="CN北-LTS-框架", width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(cn_north_lts_frame, text="安装", command=self.install_cn_north_lts_frame).pack(side=tk.LEFT, padx=5)
        
        uninstall_btn_state = tk.NORMAL if "社区服-CN北-LTS-框架" in self.installed_frameworks else tk.DISABLED
        cn_north_lts_uninstall_btn = ttk.Button(
            cn_north_lts_frame, 
            text="卸载", 
            command=self.uninstall_cn_north_lts_frame,
            state=uninstall_btn_state
        )
        cn_north_lts_uninstall_btn.pack(side=tk.LEFT, padx=5)
        self.uninstall_buttons["社区服-CN北-LTS-框架"] = cn_north_lts_uninstall_btn
        
        ttk.Button(
            cn_north_lts_frame, 
            text="下载框架到本地", 
            command=lambda: self.download_framework(
                "社区服-CN北-LTS-框架", 
                "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-6/Community.service-CN.North-LTS-framework.zip"
            )
        ).pack(side=tk.LEFT, padx=5)
        
        en_north_frame = ttk.Frame(functions_frame)
        en_north_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(en_north_frame, text="EN北-框架", width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(en_north_frame, text="安装", command=self.install_en_north_frame).pack(side=tk.LEFT, padx=5)
        
        uninstall_btn_state = tk.NORMAL if "社区服-EN北-框架" in self.installed_frameworks else tk.DISABLED
        en_north_uninstall_btn = ttk.Button(
            en_north_frame, 
            text="卸载", 
            command=self.uninstall_en_north_frame,
            state=uninstall_btn_state
        )
        en_north_uninstall_btn.pack(side=tk.LEFT, padx=5)
        self.uninstall_buttons["社区服-EN北-框架"] = en_north_uninstall_btn
        
        ttk.Button(
            en_north_frame, 
            text="下载框架到本地", 
            command=lambda: self.download_framework(
                "社区服-EN北-框架", 
                "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-7/Community.Service-EN.North-Framework.zip"
            )
        ).pack(side=tk.LEFT, padx=5)

        ttk.Label(
            functions_frame, 
            text="官服", 
            font=("Microsoft YaHei", 12, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))        
        
        official_frame1 = ttk.Frame(functions_frame)
        official_frame1.pack(fill=tk.X, pady=5)
        
        ttk.Label(official_frame1, text="CN北-框架", width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(official_frame1, text="安装", command=self.install_official_cn_north_frame).pack(side=tk.LEFT, padx=5)
        
        uninstall_btn_state = tk.NORMAL if "官服-CN北-框架" in self.installed_frameworks else tk.DISABLED
        official1_uninstall_btn = ttk.Button(
            official_frame1, 
            text="卸载", 
            command=self.uninstall_official_cn_north_frame,
            state=uninstall_btn_state
        )
        official1_uninstall_btn.pack(side=tk.LEFT, padx=5)
        self.uninstall_buttons["官服-CN北-框架"] = official1_uninstall_btn
        
        ttk.Button(
            official_frame1, 
            text="下载框架到本地", 
            command=lambda: self.download_framework(
                "官服-CN北-框架", 
                "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-3/Official.Service-CN.North-Frame.zip"
            )
        ).pack(side=tk.LEFT, padx=5)
        
        official_frame2 = ttk.Frame(functions_frame)
        official_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Label(official_frame2, text="EN北-VanillaPlus框架-普通版", width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(official_frame2, text="安装", command=self.install_official_en_north_vanillaplus_regular).pack(side=tk.LEFT, padx=5)
        
        uninstall_btn_state = tk.NORMAL if "官服-EN北-VanillaPlus框架-普通版" in self.installed_frameworks else tk.DISABLED
        official2_uninstall_btn = ttk.Button(
            official_frame2, 
            text="卸载", 
            command=self.uninstall_official_en_north_vanillaplus_regular,
            state=uninstall_btn_state
        )
        official2_uninstall_btn.pack(side=tk.LEFT, padx=5)
        self.uninstall_buttons["官服-EN北-VanillaPlus框架-普通版"] = official2_uninstall_btn
        
        ttk.Button(
            official_frame2, 
            text="下载框架到本地", 
            command=lambda: self.download_framework(
                "官服-EN北-VanillaPlus框架-普通版", 
                "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-5/Official.Uniform-EN.North-Vanilla.Plus.Frame-Regular.Edition.zip"
            )
        ).pack(side=tk.LEFT, padx=5)
        
        official_frame3 = ttk.Frame(functions_frame)
        official_frame3.pack(fill=tk.X, pady=5)
        
        ttk.Label(official_frame3, text="EN北-VanillaPlus框架-改动版", width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(official_frame3, text="安装", command=self.install_official_en_north_vanillaplus_modified).pack(side=tk.LEFT, padx=5)
        
        uninstall_btn_state = tk.NORMAL if "官服-EN北-VanillaPlus框架-改动版" in self.installed_frameworks else tk.DISABLED
        official3_uninstall_btn = ttk.Button(
            official_frame3, 
            text="卸载", 
            command=self.uninstall_official_en_north_vanillaplus_modified,
            state=uninstall_btn_state
        )
        official3_uninstall_btn.pack(side=tk.LEFT, padx=5)
        self.uninstall_buttons["官服-EN北-VanillaPlus框架-改动版"] = official3_uninstall_btn
        
        ttk.Button(
            official_frame3, 
            text="下载框架到本地", 
            command=lambda: self.download_framework(
                "官服-EN北-VanillaPlus框架-改动版", 
                "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-4/Official.Service-EN.North-Vanilla.Plus.Framework-Modified.Version.zip"
            )
        ).pack(side=tk.LEFT, padx=5)

       
        ttk.Label(
            functions_frame, 
            text="官服×社区服", 
            font=("Microsoft YaHei", 12, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))        
        
        hybrid_frame1 = ttk.Frame(functions_frame)
        hybrid_frame1.pack(fill=tk.X, pady=5)
        
        ttk.Label(hybrid_frame1, text="EN北-ION-离子框架-HUD可以使用", width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(hybrid_frame1, text="安装", command=self.install_hybrid_en_ion_hud_available).pack(side=tk.LEFT, padx=5)
        
        uninstall_btn_state = tk.NORMAL if "官服×社区服-EN北-ION-离子框架-HUD可以使用" in self.installed_frameworks else tk.DISABLED
        hybrid1_uninstall_btn = ttk.Button(
            hybrid_frame1, 
            text="卸载", 
            command=self.uninstall_hybrid_en_ion_hud_available,
            state=uninstall_btn_state
        )
        hybrid1_uninstall_btn.pack(side=tk.LEFT, padx=5)
        self.uninstall_buttons["官服×社区服-EN北-ION-离子框架-HUD可以使用"] = hybrid1_uninstall_btn
        
        ttk.Button(
            hybrid_frame1, 
            text="下载框架到本地", 
            command=lambda: self.download_framework(
                "官服×社区服-EN北-ION-离子框架-HUD可以使用", 
                "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2/Official+EN.North-ION-Ion.Frame-HUD.can.be.used.zip"
            )
        ).pack(side=tk.LEFT, padx=5)
        
        hybrid_frame2 = ttk.Frame(functions_frame)
        hybrid_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Label(hybrid_frame2, text="EN北-ION-离子框架-HUD无法使用", width=40).pack(side=tk.LEFT, padx=5)
        ttk.Button(hybrid_frame2, text="安装", command=self.install_hybrid_en_ion_hud_unavailable).pack(side=tk.LEFT, padx=5)
        
        uninstall_btn_state = tk.NORMAL if "官服×社区服-EN北-ION-离子框架-HUD无法使用" in self.installed_frameworks else tk.DISABLED
        hybrid2_uninstall_btn = ttk.Button(
            hybrid_frame2, 
            text="卸载", 
            command=self.uninstall_hybrid_en_ion_hud_unavailable,
            state=uninstall_btn_state
        )
        hybrid2_uninstall_btn.pack(side=tk.LEFT, padx=5)
        self.uninstall_buttons["官服×社区服-EN北-ION-离子框架-HUD无法使用"] = hybrid2_uninstall_btn
        
        ttk.Button(
            hybrid_frame2, 
            text="下载框架到本地", 
            command=lambda: self.download_framework(
                "官服×社区服-EN北-ION-离子框架-HUD无法使用", 
                "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-2/Official+EN.North-ION-Ion.Frame-HUD.is.not.available.zip"
            )
        ).pack(side=tk.LEFT, padx=5)
      
        top_sep = ttk.Separator(functions_frame, orient='horizontal')
        top_sep.pack(fill=tk.X, pady=(2, 2))  

        note_frame = ttk.Frame(functions_frame)
        note_frame.pack(fill=tk.X, pady=(0, 10))

        note_title_frame = ttk.Frame(note_frame)
        note_title_frame.pack(fill=tk.X, pady=(0, 5))

        note_label = ttk.Label(
            note_title_frame, 
            text="                                      ——必看——", 
            font=("Microsoft YaHei", 15, "bold"),
            justify="center"
        )
        note_label.pack(side=tk.LEFT, padx=(0, 10))
        
        note_text_frame = ttk.Frame(note_frame)
        note_text_frame.pack(fill=tk.X)

        note_text_scrollbar = ttk.Scrollbar(note_text_frame, orient="vertical")
        note_text_scrollbar.grid(row=0, column=2, sticky="ns")

        note_text = tk.Text(
            note_text_frame, 
            height=6,
            wrap=tk.WORD,
            font=("Microsoft YaHei", 13),
            padx=5,
            pady=5,
            bg="#f0f0f0",
            relief=tk.FLAT,
            yscrollcommand=note_text_scrollbar.set
        )
        note_text.grid(row=0, column=0, sticky="nsew")

        steampp_btn = ttk.Button(
            note_text_frame,
            text="Steam++官网",
            command=lambda: webbrowser.open("https://steampp.net/")
        )
        steampp_btn.grid(row=0, column=1, sticky="ne", padx=(10, 5), pady=10)

        note_text_frame.columnconfigure(0, weight=1)
        note_text_frame.rowconfigure(0, weight=1)
        note_text_scrollbar.config(command=note_text.yview)
      
        note_text.insert(tk.END, "在线安装需要自备")
        note_text.insert(tk.END, "「VPN」\n", "red")
        note_text.insert(tk.END, "\n或者使用Steam++")
        note_text.insert(tk.END, "「加速Github」\n", "red")
        note_text.insert(tk.END, "加速前在脚本配置添加")  
        note_text.insert(tk.END, "「Github 增强-高速下载」", "red")
        note_text.insert(tk.END, "脚本\n\n另外也不排除你能")  
        note_text.insert(tk.END, "「裸连」", "red") 
        note_text.insert(tk.END, "上Github。\n")                 
        note_text.insert(tk.END, "\n\n")  
        note_text.insert(tk.END, "\n不会的可以去用离线版了\n")
        note_text.insert(tk.END, "\n离线版还不会用你可以")
        note_text.insert(tk.END, "「不用打MOD了」", "red")   
        note_text.insert(tk.END, "\n\n先去学点")             
        note_text.insert(tk.END, "「计算机知识」", "red")
        note_text.insert(tk.END, "好吗？  OK???????")
        
       
        note_text.tag_configure("red", foreground="red", font=("Microsoft YaHei", 13, "bold"))  
        
   
        note_text.config(state=tk.DISABLED)
        

        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        content_frame.bind("<Configure>", on_frame_configure)
        
        def on_canvas_configure(event):
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        self.canvas.bind("<Configure>", on_canvas_configure)
        
        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(
            left_frame, 
            textvariable=self.status_var, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, pady=10)
        
        creator_label = ttk.Label(
            left_frame, 
            text="制作人-274", 
            font=("Microsoft YaHei", 10)
        )
        creator_label.pack(side=tk.BOTTOM, pady=5)
    
    def _on_mousewheel(self, event):
        if platform.system() == "Windows":
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Linux":
            if event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            else:
                self.canvas.yview_scroll(1, "units")
    
    def show_coming_soon(self):
        messagebox.showinfo("提示", "该功能正在开发中，敬请期待！")
    
    def get_installed_frameworks(self):
        installed = []
        log_dir = self.get_log_directory()
        
        for filename in os.listdir(log_dir):
            if filename.startswith("install_log_") and filename.endswith(".json"):
                try:
                    with open(os.path.join(log_dir, filename), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data:
                            category = data[0]["category"]
                            framework = data[0]["framework"]
                            installed.append(f"{category}-{framework}")
                except Exception as e: 
                    continue
        return installed
    
    def get_log_directory(self):
        if platform.system() == "Windows":
            log_dir = os.path.join(os.environ['USERPROFILE'], 'Documents', 'TTF2_Toolset_Logs')
        else:
            log_dir = os.path.join(os.path.expanduser('~'), 'TTF2_Toolset_Logs')
        
        os.makedirs(log_dir, exist_ok=True)
        return log_dir
    
    def refresh_installed_status(self):
        self.installed_frameworks = self.get_installed_frameworks()
        
        for framework_id, button in self.uninstall_buttons.items():
            if framework_id in self.installed_frameworks:
                button.config(state=tk.NORMAL)
            else:
                button.config(state=tk.DISABLED)
        
        self.status_var.set("状态已更新")
        self.root.update_idletasks()  

    def ensure_local_storage_exists(self):
        if not os.path.exists(self.local_storage):
            os.makedirs(self.local_storage, exist_ok=True)
            print(f"已创建本地存储目录: {self.local_storage}")        
    
    def download_framework(self, framework_id, url):
        confirm = messagebox.askyesno(
            "确认下载",
            f"您确定要下载 {framework_id} 框架吗？\n文件大小约为50-200MB，下载可能需要一些时间,\n如果下载出现报错为\n （下载失败:[WinError10060]由于连接方在一段时间后没有正确答复或连接的 主机没有反应，连接尝试失败)\n请看主界面-必看-标题的内容。",
            parent=self.root
        )
        
        if not confirm:
            return
        
        try:
            self.ensure_local_storage_exists()
            
            download_window = tk.Toplevel(self.root)
            download_window.title("下载框架")
            download_window.geometry("500x180")
            download_window.transient(self.root)
            download_window.grab_set()
            self.center_window(download_window)
            
            ttk.Label(download_window, text=f"框架: {framework_id}", font=("Microsoft YaHei", 10)).pack(pady=(10, 5))
            
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(download_window, variable=progress_var, maximum=100)
            progress_bar.pack(fill=tk.X, padx=20, pady=5)
            
            status_var = tk.StringVar(value="准备开始下载...")
            status_label = ttk.Label(download_window, textvariable=status_var)
            status_label.pack(pady=5)
            
            cancel_var = tk.BooleanVar(value=False)
            downloaded_file_path = None
            
            def cancel_download():
                cancel_var.set(True)
                status_var.set("正在取消下载并清理...")
                download_window.update()
            
            cancel_btn = ttk.Button(
                download_window, 
                text="取消下载", 
                command=cancel_download
            )
            cancel_btn.pack(pady=10)
            
            parsed_url = urllib.parse.urlparse(url)
            filename = os.path.basename(parsed_url.path)
            local_path = os.path.join(self.local_storage, filename)
            downloaded_file_path = local_path
            
            status_var.set(f"正在下载: {framework_id}")
            download_window.update()
            
            def update_progress(count, block_size, total_size):
                if cancel_var.get():
                    raise Exception("用户取消了下载")
                
                if total_size > 0:
                    downloaded = count * block_size
                    progress = (downloaded / total_size) * 100
                    progress_var.set(progress)
                    status_var.set(f"下载中: {downloaded/1024/1024:.2f}MB / {total_size/1024/1024:.2f}MB")
                    download_window.update()
            
            def download_task():
                try:
                    urllib.request.urlretrieve(url, local_path, reporthook=update_progress)
                    
                    status_var.set(f"下载完成! 保存到: {local_path}")
                    messagebox.showinfo("下载完成", f"{framework_id} 已下载到本地存储目录", parent=download_window)
                except Exception as e:
                    if cancel_var.get():
                        try:
                            if os.path.exists(local_path):
                                os.remove(local_path)
                                status_var.set("已取消下载并删除残留文件")
                        except Exception as delete_error:
                            status_var.set(f"删除残留文件失败: {str(delete_error)}")
                        
                        messagebox.showinfo("下载取消", "下载已被取消，残留文件已清理", parent=download_window)
                    else:
                        error_msg = f"下载失败: {str(e)}"
                        if "No such file or directory" in str(e):
                            error_msg += "\n可能原因: 本地存储目录被删除或无法访问"
                        messagebox.showerror("下载错误", error_msg, parent=download_window)
                finally:
                    try:
                        download_window.after(2000, download_window.destroy)
                    except:
                        pass
            
            import threading
            threading.Thread(target=download_task, daemon=True).start()
            
        except Exception as e:
            error_msg = f"下载失败: {str(e)}"
            if "No such file or directory" in str(e):
                error_msg += "\n可能原因: 本地存储目录被删除或无法访问"
            messagebox.showerror("下载错误", error_msg)    
    
    def install_framework(self, framework_name, category, download_url):
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title(f"安装 {category} - {framework_name}")
            self.install_window.geometry("802x740")
            self.install_window.transient(self.root)
            self.install_window.grab_set()

            self.center_window(self.install_window)

            parsed_url = urllib.parse.urlparse(download_url)
            filename = os.path.basename(parsed_url.path)
            local_path = os.path.join(self.local_storage, filename)   

            if os.path.exists(local_path):
                download_url = local_path                     

            installer = FrameworkInstaller(
                self.install_window,
                framework_name=framework_name,
                category=category,
                download_url=download_url
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
    def install_hybrid_en_ion_hud_available(self):
        self.install_framework(
            "EN北-ION-离子框架-HUD可以使用", 
            "官服×社区服", 
            "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2/Official+EN.North-ION-Ion.Frame-HUD.can.be.used.zip"
        )
    
    def install_hybrid_en_ion_hud_unavailable(self):
        self.install_framework(
            "EN北-ION-离子框架-HUD无法使用", 
            "官服×社区服", 
            "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-2/Official+EN.North-ION-Ion.Frame-HUD.is.not.available.zip"
        )
    
    def install_cn_north_frame(self):
        self.install_framework(
            "CN北-框架", 
            "社区服", 
            "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-1/Community.Service-CN.North-Frame.zip"
        )
    
    def install_official_cn_north_frame(self):
        self.install_framework(
            "CN北-框架", 
            "官服", 
            "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-3/Official.Service-CN.North-Frame.zip"
        )
    
    def install_official_en_north_vanillaplus_modified(self):
        self.install_framework(
            "EN北-VanillaPlus框架-改动版", 
            "官服", 
            "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-4/Official.Service-EN.North-Vanilla.Plus.Framework-Modified.Version.zip"
        )
    
    def install_official_en_north_vanillaplus_regular(self):
        self.install_framework(
            "EN北-VanillaPlus框架-普通版", 
            "官服", 
            "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-5/Official.Uniform-EN.North-Vanilla.Plus.Frame-Regular.Edition.zip"
        )
    
    def install_cn_north_lts_frame(self):
        self.install_framework(
            "CN北-LTS-框架", 
            "社区服", 
            "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-6/Community.service-CN.North-LTS-framework.zip"
        )
    
    def install_en_north_frame(self):
        self.install_framework(
            "EN北-框架", 
            "社区服", 
            "https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-7/Community.Service-EN.North-Framework.zip"
        )
    
    def uninstall_hybrid_en_ion_hud_available(self):
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服×社区服 EN北-ION-离子框架-HUD可以使用")
            self.uninstall_window.geometry("802x546")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()

            self.center_window(self.uninstall_window)            
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="EN北-ION-离子框架-HUD可以使用",
                category="官服×社区服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
    def uninstall_hybrid_en_ion_hud_unavailable(self):
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服×社区服 EN北-ION-离子框架-HUD无法使用")
            self.uninstall_window.geometry("802x546")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()

            self.center_window(self.uninstall_window)             
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="EN北-ION-离子框架-HUD无法使用",
                category="官服×社区服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
    def uninstall_cn_north_frame(self):
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载社区服 CN北-框架")
            self.uninstall_window.geometry("802x546")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()

            self.center_window(self.uninstall_window)             
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="CN北-框架",
                category="社区服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
    def uninstall_official_cn_north_frame(self):
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服 CN北-框架")
            self.uninstall_window.geometry("802x546")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()

            self.center_window(self.uninstall_window)             
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="CN北-框架",
                category="官服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
    def uninstall_official_en_north_vanillaplus_modified(self):
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服 EN北-VanillaPlus框架-改动版")
            self.uninstall_window.geometry("802x546")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()

            self.center_window(self.uninstall_window)             
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="EN北-VanillaPlus框架-改动版",
                category="官服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
    def uninstall_official_en_north_vanillaplus_regular(self):
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服 EN北-VanillaPlus框架-普通版")
            self.uninstall_window.geometry("802x546")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()

            self.center_window(self.uninstall_window)         

            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="EN北-VanillaPlus框架-普通版",
                category="官服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
    def uninstall_cn_north_lts_frame(self):
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载社区服 CN北-LTS-框架")
            self.uninstall_window.geometry("802x546") 
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()

            self.center_window(self.uninstall_window)             
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="CN北-LTS-框架",
                category="社区服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
    def uninstall_en_north_frame(self):
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载社区服 EN北-框架")
            self.uninstall_window.geometry("802x546")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()

            self.center_window(self.uninstall_window)             
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="EN北-框架",
                category="社区服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()   
                 
class FrameworkInstaller:
    def __init__(self, root, framework_name, category, download_url=None):
        self.root = root
        self.framework_name = framework_name
        self.category = category
        self.download_url = download_url
        self.on_complete = None  
        
        self.status_var = tk.StringVar(value=f"准备安装 {category} - {framework_name}")
        
        self.game_dir = ""
        self.search_method = tk.StringVar(value="auto")  
        
        self.log_dir = MainInterface.get_log_directory(self)
        self.install_log = os.path.join(self.log_dir, f"install_log_{category}_{framework_name}.json".replace("-", "_").replace("×", "x"))
        
        self.create_install_widgets()
        
        self.search_method.set("auto")
        self.update_directory_display()

        self.scan_in_progress = False
        self.scan_canceled = False        
    
    def create_install_widgets(self):
        main_canvas_frame = ttk.Frame(self.root)
        main_canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = ttk.Scrollbar(main_canvas_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas = tk.Canvas(main_canvas_frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        scrollbar.config(command=self.canvas.yview)
        
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
        content_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=content_frame, anchor="nw", width=750)  
        
        ttk.Label(
            content_frame, 
            text=f"安装 {self.category} - {self.framework_name}", 
            font=("Microsoft YaHei", 16, "bold")
        ).pack(pady=15)
        
        info_frame = ttk.LabelFrame(content_frame, text="框架信息\n\n如果出现未响应 或弹窗\n(安装过程中发生错误：[WinError10060]由于连接方在一段时间后没有正确答复或连接的主机没有反应，连接尝试失败)\n请查看主界面-必看-标题的内容", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text=f"名称: {self.framework_name}").pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"分类: {self.category}").pack(anchor=tk.W, pady=2)
        
        url_frame = ttk.Frame(info_frame)
        url_frame.pack(fill=tk.X, pady=2)
        ttk.Label(url_frame, text="下载地址:").pack(side=tk.LEFT, anchor=tk.W)
        url_text = tk.Text(url_frame, height=3, width=70, wrap="word", font=("Microsoft YaHei", 9))
        url_text.insert(tk.END, self.download_url)
        url_text.config(state="disabled")
        url_text.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        search_frame = ttk.LabelFrame(content_frame, text="搜索方式", padding="10")
        search_frame.pack(fill=tk.X, pady=10)
        
        auto_search_btn = ttk.Radiobutton(
            search_frame,
            text="自动搜索游戏目录",
            variable=self.search_method,
            value="auto",
            command=self.update_directory_display
        )
        auto_search_btn.pack(anchor=tk.W, padx=5, pady=5)
        
        manual_search_btn = ttk.Radiobutton(
            search_frame,
            text="手动选择游戏目录",
            variable=self.search_method,
            value="manual",
            command=self.update_directory_display
        )
        manual_search_btn.pack(anchor=tk.W, padx=5, pady=5)
        
        scan_disk_btn = ttk.Radiobutton(
            search_frame,
            text="扫盘！！！（风险自负）",
            variable=self.search_method,
            value="scan",
            command=self.show_scan_warning
        )
        scan_disk_btn.pack(anchor=tk.W, padx=5, pady=5)
        
        dir_frame = ttk.LabelFrame(content_frame, text="游戏目录", padding="10")
        dir_frame.pack(fill=tk.X, pady=10)
        
        self.game_dir_var = tk.StringVar(value="正在搜索游戏目录...")
        dir_entry = ttk.Label(dir_frame, textvariable=self.game_dir_var, wraplength=600)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.browse_btn = ttk.Button(dir_frame, text="浏览...", command=self.browse_game_directory)
        self.browse_btn.pack(side=tk.RIGHT, padx=5)
        self.browse_btn.config(state=tk.DISABLED)  
        
        progress_frame = ttk.LabelFrame(content_frame, text="安装进度", padding="10")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5)
        
        status_label = ttk.Label(content_frame, textvariable=self.status_var, wraplength=700)
        status_label.pack(anchor=tk.W, pady=5, fill=tk.X, padx=5)
        
        btn_frame = ttk.Frame(content_frame)
        btn_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(
            btn_frame, 
            text="开始安装", 
            command=self.start_installation
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_frame, 
            text="取消", 
            command=self.root.destroy
        ).pack(side=tk.RIGHT, padx=10)
        
        def on_frame_configure(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
        content_frame.bind("<Configure>", on_frame_configure)
        
        def on_canvas_configure(event):
            canvas_width = event.width
            self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
        self.canvas.bind("<Configure>", on_canvas_configure)           

    def show_scan_warning(self):
        warn_win = tk.Toplevel(self.root)
        warn_win.title("警告")
        warn_win.geometry("500x200")
        warn_win.transient(self.root)
        warn_win.grab_set()

        self.center_window(warn_win)
        
        warn_win.transient(self.root)
        warn_win.grab_set()        
        
        ttk.Label(warn_win, text="——警告——", font=("Microsoft YaHei", 14, "bold"), foreground="red").pack(pady=(20, 10))
        
        warning_text = "扫盘有风险，如若硬盘损坏"
        red_text = "概不负责"
        ttk.Label(warn_win, text=warning_text).pack()
        ttk.Label(warn_win, text=red_text, foreground="red", font=("Microsoft YaHei", 10, "bold")).pack()
        ttk.Label(warn_win, text="请谨慎操作！").pack(pady=(0, 20))
        
        btn_frame = ttk.Frame(warn_win)
        btn_frame.pack()
        
        ttk.Button(btn_frame, text="继续", command=lambda: [warn_win.destroy(), self.start_disk_scan()]).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="取消", command=lambda: [warn_win.destroy(), self.search_method.set("auto"), self.update_directory_display()]).pack(side=tk.RIGHT, padx=10)

    def center_window(self, window):
        window.update_idletasks()
        
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        width = window.winfo_width()
        height = window.winfo_height()
        
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        
        window.geometry(f"+{x}+{y}")        

    def start_disk_scan(self):
        self.scan_window = tk.Toplevel(self.root)
        self.scan_window.title("扫盘中...")
        self.scan_window.geometry("602x533")
        self.scan_window.transient(self.root)
        self.scan_window.grab_set()
        self.scan_window.protocol("WM_DELETE_WINDOW", self.cancel_scan_process)

        self.center_window(self.scan_window)        
        
        ttk.Label(self.scan_window, text="正在扫描整个计算机，查找Titanfall2.exe...").pack(pady=10)
        self.scan_progress_var = tk.DoubleVar()
        scan_progress_bar = ttk.Progressbar(self.scan_window, variable=self.scan_progress_var, maximum=100)
        scan_progress_bar.pack(fill=tk.X, padx=20, pady=5)
        
        self.scan_status_var = tk.StringVar(value="准备开始...")
        ttk.Label(self.scan_window, textvariable=self.scan_status_var).pack(pady=5)
        
        self.current_path_var = tk.StringVar(value="")
        ttk.Label(self.scan_window, textvariable=self.current_path_var, wraplength=550).pack(pady=5)
        
        stats_frame = ttk.Frame(self.scan_window)
        stats_frame.pack(fill=tk.X, padx=20, pady=5)
        
        ttk.Label(stats_frame, text="已扫描文件:").pack(side=tk.LEFT)
        self.scanned_files_var = tk.StringVar(value="0")
        ttk.Label(stats_frame, textvariable=self.scanned_files_var).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Label(stats_frame, text="找到位置:").pack(side=tk.LEFT)
        self.found_paths_var = tk.StringVar(value="0")
        ttk.Label(stats_frame, textvariable=self.found_paths_var).pack(side=tk.LEFT)
        
        result_frame = ttk.LabelFrame(self.scan_window, text="找到的游戏目录")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        result_scrollbar = ttk.Scrollbar(result_frame)
        result_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_listbox = tk.Listbox(
            result_frame, 
            yscrollcommand=result_scrollbar.set
        )
        self.result_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        result_scrollbar.config(command=self.result_listbox.yview)
        
        btn_frame = ttk.Frame(self.scan_window)
        btn_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.cancel_scan = False
        ttk.Button(btn_frame, text="取消扫描", command=self.cancel_scan_process).pack(side=tk.RIGHT)
        
        self.select_btn = ttk.Button(btn_frame, text="选择", command=self.select_scan_result, state=tk.DISABLED)
        self.select_btn.pack(side=tk.LEFT)
        
        self.result_listbox.bind("<<ListboxSelect>>", self.on_result_select)
        
        import threading
        threading.Thread(target=self.scan_for_titanfall2, daemon=True).start()
    
    def cancel_scan_process(self):
        self.cancel_scan = True
        self.scan_status_var.set("正在取消扫描...")
        self.scan_window.update()
        if self.scan_window:
            self.scan_window.destroy()
        self.search_method.set("auto")
        self.update_directory_display()
    
    def on_result_select(self, event):
        selection = self.result_listbox.curselection()
        if selection:
            self.select_btn.config(state=tk.NORMAL)
    
    def select_scan_result(self):
        selection = self.result_listbox.curselection()
        if not selection:
            return
        path = self.result_listbox.get(selection[0])
        self.game_dir = path
        self.game_dir_var.set(path)
        if self.scan_window:
            self.scan_window.destroy()
        self.status_var.set(f"已选择扫盘找到的目录: {path}")
    
    def scan_for_titanfall2(self):
        self.scan_in_progress = True
        self.scan_canceled = False
        self.cancel_scan = False
        
        drives = self.get_available_drives()
        total_drives = len(drives)
        found_paths = []
        scanned_files = 0
        
        skip_dirs = {"Windows", "Program Files", "Program Files (x86)", "ProgramData", "AppData", "System Volume Information", "$RECYCLE.BIN", "Recovery", "Temp", "tmp", "MSOCache", "PerfLogs", "Intel", "AMD", "NVIDIA"}
        
        for drive_index, drive in enumerate(drives):
            if self.cancel_scan:
                self.scan_status_var.set("扫描已取消")
                break
                
            self.scan_status_var.set(f"扫描驱动器 {drive} ({drive_index+1}/{total_drives})")
            self.scan_progress_var.set((drive_index / total_drives) * 100)
            self.scan_window.update()
            
            for root, dirs, files in os.walk(drive, topdown=True):
                if self.cancel_scan:
                    break
                    
                dirs[:] = [d for d in dirs if d not in skip_dirs]
                
                self.current_path_var.set(root)
                
                for file in files:
                    if file.lower().endswith('.exe'):
                        scanned_files += 1
                        self.scanned_files_var.set(str(scanned_files))
                        
                        if scanned_files % 1000 == 0:
                            self.scan_window.update()
                            
                        if file.lower() in ["titanfall2.exe", "titanfall 2.exe"]:
                            game_dir = root
                            if game_dir not in found_paths:
                                found_paths.append(game_dir)
                                self.found_paths_var.set(str(len(found_paths)))
                                self.result_listbox.insert(tk.END, game_dir)
                                self.result_listbox.see(tk.END)
                                self.scan_window.update()
                
                time.sleep(0.001)
                if time.time() % 0.5 < 0.01:
                    self.scan_window.update()
            
            if self.cancel_scan:
                break
        
        if not self.cancel_scan:
            self.scan_status_var.set(f"扫描完成，共找到 {len(found_paths)} 个可能的位置")
            self.scan_progress_var.set(100)
            
            if found_paths:
                self.select_btn.config(state=tk.NORMAL)
        
        self.scan_in_progress = False

    def _on_mousewheel(self, event):
        if platform.system() == "Windows":
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Linux":
            if event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            else:
                self.canvas.yview_scroll(1, "units")
        self.scan_in_progress = False                
    
    def update_directory_display(self):
        method = self.search_method.get()
        if method == "auto":
            self.game_dir = self.find_titanfall2_directory()
            if self.game_dir:
                self.game_dir_var.set(f"自动找到: {self.game_dir}")
            else:
                self.game_dir_var.set("自动搜索未找到游戏目录，请尝试手动选择或扫盘")
            self.browse_btn.config(state=tk.DISABLED)
        elif method == "manual":
            self.game_dir = ""
            self.game_dir_var.set("请点击浏览按钮选择目录")
            self.browse_btn.config(state=tk.NORMAL)
        elif method == "scan":
            self.game_dir = ""
            self.game_dir_var.set("请先完成扫盘操作")
            self.browse_btn.config(state=tk.DISABLED)
    
    def find_titanfall2_directory(self):
        self.status_var.set("正在搜索Titanfall2游戏目录...")
        self.root.update()
        
        game_exe_names = ["Titanfall2.exe", "Titanfall 2.exe"]
        
        try:
            for reg_path in [
                r"SOFTWARE\Respawn\Titanfall2",
                r"SOFTWARE\WOW6432Node\Respawn\Titanfall2"
            ]:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                    for value_name in ["Install Dir", "path", "InstallDir"]:
                        try:
                            install_dir = winreg.QueryValueEx(key, value_name)[0]
                            for exe_name in game_exe_names:
                                if os.path.exists(os.path.join(install_dir, exe_name)):
                                    print(f"从Respawn注册表找到游戏目录: {install_dir}")
                                    return install_dir
                        except Exception:
                            continue
                except Exception:
                    continue
        except Exception as e:
            print(f"Respawn注册表搜索错误: {str(e)}")
        
        try:
            steam_paths = self.find_steam_library_folders()
            for steam_path in steam_paths:
                steam_apps = os.path.join(steam_path, "steamapps", "common", "Titanfall2")
                for exe_name in game_exe_names:
                    if os.path.exists(os.path.join(steam_apps, exe_name)):
                        print(f"从Steam库找到游戏目录: {steam_apps}")
                        return steam_apps
        except Exception as e:
            print(f"Steam库搜索错误: {str(e)}")
        
        try:
            ea_app_paths = self.find_ea_app_paths()
            for path in ea_app_paths:
                for exe_name in game_exe_names:
                    if os.path.exists(os.path.join(path, exe_name)):
                        print(f"从EA App找到游戏目录: {path}")
                        return path
            
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Origin")
                origin_path = winreg.QueryValueEx(key, "ClientPath")[0]
                origin_games = os.path.join(os.path.dirname(origin_path), "Games", "Titanfall2")
                for exe_name in game_exe_names:
                    if os.path.exists(os.path.join(origin_games, exe_name)):
                        print(f"从Origin找到游戏目录: {origin_games}")
                        return origin_games
            except Exception as e:
                print(f"Origin路径搜索错误: {str(e)}")
        except Exception as e:
            print(f"EA/Origin搜索错误: {str(e)}")            
            

        common_paths = []
        
        drives = self.get_available_drives()
        
        for drive in drives:
            common_paths.extend([
                os.path.join(drive, "Program Files", "EA Games", "Titanfall 2"),
                os.path.join(drive, "Program Files (x86)", "EA Games", "Titanfall 2"),
                os.path.join(drive, "Program Files", "Origin Games", "Titanfall 2"),
                os.path.join(drive, "Program Files (x86)", "Origin Games", "Titanfall 2"),
                os.path.join(drive, "EA Games", "Titanfall 2"),
                os.path.join(drive, "Origin Games", "Titanfall 2"),
                os.path.join(drive, "Games", "Titanfall 2"),
                os.path.join(drive, "Games", "EA Games", "Titanfall 2"),
                os.path.join(drive, "Games", "Origin Games", "Titanfall 2"),
                os.path.join(drive, "Program Files", "Steam", "steamapps", "common", "Titanfall2"),
                os.path.join(drive, "Program Files (x86)", "Steam", "steamapps", "common", "Titanfall2"),
                os.path.join(drive, "SteamLibrary", "steamapps", "common", "Titanfall2"),
                os.path.join(drive, "Steam", "steamapps", "common", "Titanfall2"),
                os.path.join(drive, "Games", "Steam", "steamapps", "common", "Titanfall2"),
            ])
        
        user_profile = os.environ.get("USERPROFILE", "")
        if user_profile:
            common_paths.extend([
                os.path.join(user_profile, "Documents", "Electronic Arts", "Titanfall 2"),
                os.path.join(user_profile, "OneDrive", "Documents", "Electronic Arts", "Titanfall 2"),
                os.path.join(user_profile, "SteamLibrary", "steamapps", "common", "Titanfall2"),
                os.path.join(user_profile, "Games", "Titanfall 2"),
            ])
        
        for path in common_paths:
            for exe_name in game_exe_names:
                if os.path.exists(os.path.join(path, exe_name)):
                    print(f"从常见路径找到游戏目录: {path}")
                    return path
        
        try:
            recent_game_path = self.find_recent_game_path()
            if recent_game_path:
                for exe_name in game_exe_names:
                    if os.path.exists(os.path.join(recent_game_path, exe_name)):
                        print(f"从最近游戏路径找到游戏目录: {recent_game_path}")
                        return recent_game_path
        except Exception as e:
            print(f"最近游戏路径搜索错误: {str(e)}")
        
        return None
    
    def find_steam_library_folders(self):
        steam_libraries = []
        
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
            steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
            steam_libraries.append(steam_path)
            
            vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
            if os.path.exists(vdf_path):
                with open(vdf_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    paths = re.findall(r'"path"\s+"([^"]+)"', content)
                    for path in paths:
                        path = path.replace("\\\\", "\\")
                        if path not in steam_libraries:
                            steam_libraries.append(path)
        except Exception as e:
            print(f"Steam库文件夹搜索错误: {str(e)}")
        
        return steam_libraries
    
    def find_ea_app_paths(self):
        ea_paths = []
        
        try:
            for reg_path in [r"SOFTWARE\WOW6432Node\Electronic Arts\EA Desktop", r"SOFTWARE\Electronic Arts\EA Desktop"]:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                    ea_path = winreg.QueryValueEx(key, "InstallPath")[0]
                    possible_game_dirs = [
                        os.path.join(os.path.dirname(ea_path), "Games", "Titanfall2"),
                        os.path.join(os.path.dirname(ea_path), "Games", "Titanfall 2")
                    ]
                    ea_paths.extend(possible_game_dirs)
                except Exception:
                    pass
        except Exception as e:
            print(f"EA App路径搜索错误: {str(e)}")
        
        return ea_paths
    
    def get_available_drives(self):
        drives = []
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        return drives
    
    def find_recent_game_path(self):
        try:
            for reg_path in [
                r"SOFTWARE\Electronic Arts\EA Desktop\Games",
                r"SOFTWARE\WOW6432Node\Electronic Arts\EA Desktop\Games",
                r"SOFTWARE\Electronic Arts\Origin\Games",
                r"SOFTWARE\WOW6432Node\Electronic Arts\Origin\Games"
            ]:
                try:
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_path)
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        subkey_name = winreg.EnumKey(key, i)
                        if "titanfall" in subkey_name.lower():
                            subkey = winreg.OpenKey(key, subkey_name)
                            install_dir = winreg.QueryValueEx(subkey, "InstallDir")[0]
                            return install_dir
                except Exception:
                    pass
        except Exception as e:
            print(f"最近游戏路径搜索错误: {str(e)}")
        
        return None
    
    def browse_game_directory(self):
        directory = filedialog.askdirectory(title="选择游戏目录")
        if directory:
            self.game_dir = directory
            self.game_dir_var.set(directory)
            if not os.path.exists(os.path.join(directory, "Titanfall2.exe")):
                self.status_var.set("警告: 所选目录中未找到Titanfall2.exe，请确保选择正确")
            else:
                self.status_var.set("目录设置完成")
    
    def get_all_files(self, directory):
        file_list = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                file_list.append(relative_path)
        return file_list
    
    def start_installation(self):
        if not self.game_dir:
            messagebox.showerror("错误", "请先设置游戏目录")
            return
        
        if not self.download_url:
            messagebox.showerror("错误", "未提供下载URL")
            return
        
        progress_window = tk.Toplevel(self.root)
        progress_window.title("安装中")
        progress_window.geometry("500x120")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        ttk.Label(progress_window, text=f"正在安装 {self.framework_name}，请稍候...").pack(pady=10)
        install_progress = ttk.Progressbar(progress_window, variable=self.progress_var, maximum=100)
        install_progress.pack(fill=tk.X, padx=20, pady=10)
        
        self.root.update()
        time.sleep(0.5)
        
        try:
            is_local_file = os.path.exists(self.download_url) and os.path.isfile(self.download_url)
            
            if is_local_file:
                zip_path = self.download_url
                self.status_var.set("使用本地框架文件进行安装...")
                self.progress_var.set(50)
                self.root.update()
            else:
                temp_dir = tempfile.mkdtemp()
                zip_path = os.path.join(temp_dir, "download.zip")
                
                self.status_var.set("正在下载框架文件...")
                self.root.update()
                
                def update_download_progress(count, block_size, total_size):
                    if total_size > 0:
                        downloaded = count * block_size
                        progress = (downloaded / total_size) * 50
                        self.progress_var.set(progress)
                        self.status_var.set(f"下载中: {downloaded/1024/1024:.2f}MB / {total_size/1024/1024:.2f}MB")
                        self.root.update()
                
                urllib.request.urlretrieve(self.download_url, zip_path, reporthook=update_download_progress)
            
            self.status_var.set("正在解压框架文件...")
            self.progress_var.set(50)
            self.root.update()
            
            extract_dir = os.path.join(tempfile.mkdtemp(), "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                file_list = zip_ref.namelist()
                
                total_files = len(file_list)
                
                for i, file in enumerate(file_list):
                    if file.endswith('/'):
                        continue
                        
                    zip_ref.extract(file, extract_dir)
                    
                    progress = 50 + (i + 1) / total_files * 50
                    self.progress_var.set(progress)
                    self.status_var.set(f"解压中: {file} ({i+1}/{total_files})")
                    self.root.update()
            
            installed_files = []
            total_files = 0
            
            self.status_var.set("正在复制文件到游戏目录...")
            self.root.update()
            
            all_files = []
            for root, dirs, files in os.walk(extract_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    all_files.append(file_path)
            
            for i, source_path in enumerate(all_files):
                relative_path = os.path.relpath(source_path, extract_dir)
                dest_path = os.path.join(self.game_dir, relative_path)
                
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                shutil.copy2(source_path, dest_path)
                installed_files.append({
                    "path": relative_path,
                    "is_dir": False,
                    "timestamp": datetime.now().isoformat(),
                    "framework": self.framework_name,
                    "category": self.category
                })
                total_files += 1
                
                progress = 50 + (i + 1) / len(all_files) * 50
                self.progress_var.set(progress)
                self.status_var.set(f"正在安装: {relative_path} ({i+1}/{len(all_files)})")
                self.root.update()
            
            for root, dirs, _ in os.walk(extract_dir):
                relative_root = os.path.relpath(root, extract_dir)
                if relative_root != ".":
                    installed_files.append({
                        "path": relative_root,
                        "is_dir": True,
                        "timestamp": datetime.now().isoformat(),
                        "framework": self.framework_name,
                        "category": self.category
                    })
            
            os.makedirs(os.path.dirname(self.install_log), exist_ok=True)
            
            with open(self.install_log, "w", encoding="utf-8") as f:
                json.dump(installed_files, f, ensure_ascii=False, indent=2)
            
            if not is_local_file:
                shutil.rmtree(os.path.dirname(zip_path))
            shutil.rmtree(os.path.dirname(extract_dir))
            
            self.status_var.set(f"{self.framework_name} 安装完成，共安装了{len(all_files)}个文件")
            messagebox.showinfo("成功", f"{self.framework_name} 安装成功！\n已安装 {len(all_files)} 个文件到游戏目录")
            
            if self.on_complete:
                self.on_complete()
                
            self.root.destroy()
        
        except Exception as e:
            self.status_var.set(f"安装失败: {str(e)}")
            messagebox.showerror("错误", f"安装过程中发生错误:\n{str(e)}")
        
        finally:
            progress_window.destroy()


class FrameworkUninstaller:
    def __init__(self, root, framework_name, category):
        self.root = root
        self.framework_name = framework_name
        self.category = category
        self.on_complete = None  
        
        self.status_var = tk.StringVar(value=f"准备卸载 {category} - {framework_name}")
        
        self.game_dir = self.find_titanfall2_directory()
        
        self.log_dir = MainInterface.get_log_directory(self)
        self.install_log = os.path.join(self.log_dir, f"install_log_{category}_{framework_name}.json".replace("-", "_").replace("×", "x"))
        
        self.create_uninstall_widgets()
    
    def create_uninstall_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            main_frame, 
            text=f"卸载 {self.category} - {self.framework_name}", 
            font=("Microsoft YaHei", 16, "bold")
        ).pack(pady=15)
        
        info_frame = ttk.LabelFrame(main_frame, text="框架信息", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text=f"名称: {self.framework_name}").pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"分类: {self.category}").pack(anchor=tk.W, pady=2)
        
        log_exists = os.path.exists(self.install_log)
        log_status = "已找到安装日志" if log_exists else "未找到安装日志"
        ttk.Label(info_frame, text=f"安装日志状态: {log_status}").pack(anchor=tk.W, pady=2)
        
        dir_frame = ttk.LabelFrame(main_frame, text="游戏目录", padding="10")
        dir_frame.pack(fill=tk.X, pady=10)
        
        self.game_dir_var = tk.StringVar(value=self.game_dir if self.game_dir else "未找到游戏目录，请手动选择")
        dir_entry = ttk.Label(dir_frame, textvariable=self.game_dir_var, wraplength=600)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        browse_btn = ttk.Button(dir_frame, text="浏览...", command=self.browse_game_directory)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
        progress_frame = ttk.LabelFrame(main_frame, text="卸载进度", padding="10")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5)
        
        status_label = ttk.Label(main_frame, textvariable=self.status_var, wraplength=700)
        status_label.pack(anchor=tk.W, pady=5, fill=tk.X, padx=5)
        
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=15)
        
        ttk.Button(
            btn_frame, 
            text="开始卸载", 
            command=self.start_uninstallation
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            btn_frame, 
            text="取消", 
            command=self.root.destroy
        ).pack(side=tk.RIGHT, padx=10)
    
    def find_titanfall2_directory(self):
        game_exe_names = ["Titanfall2.exe", "Titanfall 2.exe"]
        
        for reg_path in [
            r"SOFTWARE\Respawn\Titanfall2",
            r"SOFTWARE\WOW6432Node\Respawn\Titanfall2"
        ]:
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                for value_name in ["Install Dir", "path", "InstallDir"]:
                    try:
                        install_dir = winreg.QueryValueEx(key, value_name)[0]
                        for exe_name in game_exe_names:
                            if os.path.exists(os.path.join(install_dir, exe_name)):
                                return install_dir
                    except Exception:
                        continue
            except Exception:
                continue
        
        try:
            steam_paths = self.find_steam_library_folders()
            for steam_path in steam_paths:
                steam_apps = os.path.join(steam_path, "steamapps", "common", "Titanfall2")
                for exe_name in game_exe_names:
                    if os.path.exists(os.path.join(steam_apps, exe_name)):
                        return steam_apps
        except Exception:
            pass
        
        try:
            ea_app_paths = self.find_ea_app_paths()
            for path in ea_app_paths:
                for exe_name in game_exe_names:
                    if os.path.exists(os.path.join(path, exe_name)):
                        return path
        except Exception:
            pass
        
        drives = self.get_available_drives()
        common_paths = []
        for drive in drives:
            common_paths.extend([
                os.path.join(drive, "Program Files", "EA Games", "Titanfall 2"),
                os.path.join(drive, "Program Files (x86)", "EA Games", "Titanfall 2"),
                os.path.join(drive, "Program Files", "Origin Games", "Titanfall 2"),
                os.path.join(drive, "Program Files (x86)", "Origin Games", "Titanfall 2"),
                os.path.join(drive, "EA Games", "Titanfall 2"),
                os.path.join(drive, "Origin Games", "Titanfall 2"),
                os.path.join(drive, "Games", "Titanfall 2"),
                os.path.join(drive, "Program Files", "Steam", "steamapps", "common", "Titanfall2"),
                os.path.join(drive, "Program Files (x86)", "Steam", "steamapps", "common", "Titanfall2"),
                os.path.join(drive, "SteamLibrary", "steamapps", "common", "Titanfall2"),
            ])
        
        user_profile = os.environ.get("USERPROFILE", "")
        if user_profile:
            common_paths.extend([
                os.path.join(user_profile, "Documents", "Electronic Arts", "Titanfall 2"),
                os.path.join(user_profile, "OneDrive", "Documents", "Electronic Arts", "Titanfall 2"),
            ])
        
        for path in common_paths:
            for exe_name in game_exe_names:
                if os.path.exists(os.path.join(path, exe_name)):
                    return path
        
        return None
    
    def find_steam_library_folders(self):
        steam_libraries = []
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
            steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
            steam_libraries.append(steam_path)
            
            vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
            if os.path.exists(vdf_path):
                with open(vdf_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    paths = re.findall(r'"path"\s+"([^"]+)"', content)
                    for path in paths:
                        path = path.replace("\\\\", "\\")
                        if path not in steam_libraries:
                            steam_libraries.append(path)
        except Exception:
            pass
        return steam_libraries
    
    def find_ea_app_paths(self):
        ea_paths = []
        try:
            for reg_path in [r"SOFTWARE\WOW6432Node\Electronic Arts\EA Desktop", r"SOFTWARE\Electronic Arts\EA Desktop"]:
                try:
                    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path)
                    ea_path = winreg.QueryValueEx(key, "InstallPath")[0]
                    possible_game_dirs = [
                        os.path.join(os.path.dirname(ea_path), "Games", "Titanfall2"),
                        os.path.join(os.path.dirname(ea_path), "Games", "Titanfall 2")
                    ]
                    ea_paths.extend(possible_game_dirs)
                except Exception:
                    pass
        except Exception:
            pass
        return ea_paths
    
    def get_available_drives(self):
        drives = []
        for letter in "CDEFGHIJKLMNOPQRSTUVWXYZ":
            drive = f"{letter}:\\"
            if os.path.exists(drive):
                drives.append(drive)
        return drives
    
    def browse_game_directory(self):
        directory = filedialog.askdirectory(title="选择游戏目录")
        if directory:
            self.game_dir = directory
            self.game_dir_var.set(directory)
            if not any(os.path.exists(os.path.join(directory, exe)) for exe in ["Titanfall2.exe", "Titanfall 2.exe"]):
                self.status_var.set("警告: 所选目录中未找到游戏可执行文件")
            else:
                self.status_var.set("目录设置完成")
    
    def start_uninstallation(self):
        if not self.game_dir:
            messagebox.showerror("错误", "请先设置有效的游戏目录")
            return
        
        if not os.path.exists(self.install_log):
            messagebox.showerror("错误", f"未找到 {self.framework_name} 的安装日志，无法卸载")
            return
        
        try:
            with open(self.install_log, "r", encoding="utf-8") as f:
                installed_files = json.load(f)
        except Exception as e:
            messagebox.showerror("错误", f"读取安装日志失败: {str(e)}")
            return
        
        if not installed_files:
            messagebox.showerror("错误", "安装日志为空，无法卸载")
            return
        
        progress_window = tk.Toplevel(self.root)
        progress_window.title("卸载中")
        progress_window.geometry("500x120")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        ttk.Label(progress_window, text=f"正在卸载 {self.framework_name}，请稍候...").pack(pady=10)
        uninstall_progress = ttk.Progressbar(progress_window, variable=self.progress_var, maximum=100)
        uninstall_progress.pack(fill=tk.X, padx=20, pady=10)
        
        self.root.update()
        time.sleep(0.5)
        
        try:
            files = [item for item in installed_files if not item.get("is_dir", False)]
            dirs = [item for item in installed_files if item.get("is_dir", False)]
            
            total_items = len(files) + len(dirs)
            processed = 0
            
            for item in files:
                file_path = os.path.join(self.game_dir, item["path"])
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        self.status_var.set(f"已删除文件: {item['path']}")
                    except Exception as e:
                        self.status_var.set(f"删除文件失败: {item['path']} - {str(e)}")
                else:
                    self.status_var.set(f"文件不存在: {item['path']}")
                
                processed += 1
                progress = (processed / total_items) * 100
                self.progress_var.set(progress)
                self.root.update()
            
            for item in reversed(dirs):
                dir_path = os.path.join(self.game_dir, item["path"])
                if os.path.exists(dir_path) and os.path.isdir(dir_path):
                    try:
                        if not os.listdir(dir_path):
                            os.rmdir(dir_path)
                            self.status_var.set(f"已删除目录: {item['path']}")
                        else:
                            self.status_var.set(f"目录不为空，未删除: {item['path']}")
                    except Exception as e:
                        self.status_var.set(f"删除目录失败: {item['path']} - {str(e)}")
                else:
                    self.status_var.set(f"目录不存在: {item['path']}")
                
                processed += 1
                progress = (processed / total_items) * 100
                self.progress_var.set(progress)
                self.root.update()
            
            folders_to_remove = ["R2Northstar", "R2Vanilla", "R2Titanfall"]
            for folder in folders_to_remove:
                folder_path = os.path.join(self.game_dir, folder)
                if os.path.exists(folder_path):
                    try:
                        shutil.rmtree(folder_path)
                        self.status_var.set(f"已删除文件夹: {folder}")
                    except Exception as e:
                        self.status_var.set(f"删除文件夹失败: {folder} - {str(e)}")
                else:
                    self.status_var.set(f"文件夹不存在: {folder}")
                self.root.update()
            
            if os.path.exists(self.install_log):
                os.remove(self.install_log)
            
            self.status_var.set(f"{self.framework_name} 卸载完成")
            messagebox.showinfo("成功", f"{self.framework_name} 卸载成功！")
            
            if self.on_complete:
                self.on_complete()
                
            self.root.destroy()
        
        except Exception as e:
            self.status_var.set(f"卸载失败: {str(e)}")
            messagebox.showerror("错误", f"卸载过程中发生错误:\n{str(e)}")
        
        finally:
            progress_window.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainInterface(root)
    root.mainloop()            
