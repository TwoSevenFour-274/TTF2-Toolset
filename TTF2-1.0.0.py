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

class MainInterface:
    def __init__(self, root):
        self.root = root
        self.root.title("TTF2工具集")
        self.root.geometry("1280x800")
        self.root.resizable(True, True)
        
       
        if platform.system() == "Windows":
            default_font = ("SimHei", 10)
        else:
            default_font = ("WenQuanYi Micro Hei", 10)
        self.root.option_add("*Font", default_font)
        
       
        self.installed_frameworks = self.get_installed_frameworks()

       
        self.uninstall_buttons = {}        
        
      
        self.create_main_widgets()
        
        
        self.install_window = None
        self.uninstall_window = None

    def create_main_widgets(self):

        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
       
        left_frame = ttk.Frame(main_container)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
      
        right_frame = ttk.Frame(main_container)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
      
        right_content = ttk.Frame(right_frame)
        right_content.pack(expand=True)
        
       
        ttk.Label(
            right_content, 
            text="其他功能因为懒 正在拖延中", 
            font=("SimHei", 14, "italic")
        ).pack(pady=(0, 10))
        
      
        ttk.Button(
            right_content,
            text="Github链接",
            command=lambda: webbrowser.open("https://github.com/TwoSevenFour-274/TTF2-Toolset")
        ).pack()
        
     
        ttk.Label(
            left_frame, 
            text="TTF2工具集", 
            font=("SimHei", 20, "bold")
        ).pack(pady=15)
        
        
        canvas_frame = ttk.Frame(left_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
       
        scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical")
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        
        self.canvas = tk.Canvas(canvas_frame, yscrollcommand=scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
       
        scrollbar.config(command=self.canvas.yview)
        
      
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
       
        content_frame = ttk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=content_frame, anchor="nw")
        
        
        ttk.Label(
            content_frame, 
            text="框架安装", 
            font=("SimHei", 14, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))
        
       
        functions_frame = ttk.LabelFrame(content_frame, text="框架列表", padding="15")
        functions_frame.pack(fill=tk.X, pady=10)
        
        
        ttk.Label(
            functions_frame, 
            text="社区服", 
            font=("SimHei", 12, "bold")
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

       
        ttk.Label(
            functions_frame, 
            text="官服", 
            font=("SimHei", 12, "bold")
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


        ttk.Label(
            functions_frame, 
            text="官服×社区服", 
            font=("SimHei", 12, "bold")
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
            font=("SimHei", 10)
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
    
  
    def install_hybrid_en_ion_hud_available(self):
 
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装官服×社区服 EN北-ION-离子框架-HUD可以使用")
            self.install_window.geometry("800x700") 
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
         
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="EN北-ION-离子框架-HUD可以使用",
                category="官服×社区服",
                download_url="https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2/Official+EN.North-ION-Ion.Frame-HUD.can.be.used.zip"
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
   
    def uninstall_hybrid_en_ion_hud_available(self):
      
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服×社区服 EN北-ION-离子框架-HUD可以使用")
            self.uninstall_window.geometry("800x700")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="EN北-ION-离子框架-HUD可以使用",
                category="官服×社区服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
   
    def install_hybrid_en_ion_hud_unavailable(self):
 
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装官服×社区服 EN北-ION-离子框架-HUD无法使用")
            self.install_window.geometry("800x700") 
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
           
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="EN北-ION-离子框架-HUD无法使用",
                category="官服×社区服",
                download_url="https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-2/Official+EN.North-ION-Ion.Frame-HUD.is.not.available.zip"
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
   
    def uninstall_hybrid_en_ion_hud_unavailable(self):
        
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服×社区服 EN北-ION-离子框架-HUD无法使用")
            self.uninstall_window.geometry("800x700")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="EN北-ION-离子框架-HUD无法使用",
                category="官服×社区服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
  
    def install_cn_north_frame(self):
       
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装社区服 CN北-框架")
            self.install_window.geometry("800x700")  
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
           
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="CN北-框架",
                category="社区服",
                download_url="https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-1/Community.Service-CN.North-Frame.zip"
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
  
    def uninstall_cn_north_frame(self):
        
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载社区服 CN北-框架")
            self.uninstall_window.geometry("800x700")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="CN北-框架",
                category="社区服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
 
    def install_official_cn_north_frame(self):
      
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装官服 CN北-框架")
            self.install_window.geometry("800x700")  
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
          
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="CN北-框架",
                category="官服",
                download_url="https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-3/Official.Service-CN.North-Frame.zip" 
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
   
    def uninstall_official_cn_north_frame(self):
        
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服 CN北-框架")
            self.uninstall_window.geometry("800x700")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="CN北-框架",
                category="官服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
   
    def install_official_en_north_vanillaplus_modified(self):
    
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装官服 EN北-VanillaPlus框架-改动版")
            self.install_window.geometry("800x700")  
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
         
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="EN北-VanillaPlus框架-改动版",
                category="官服",
                download_url="https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-4/Official.Service-EN.North-Vanilla.Plus.Framework-Modified.Version.zip"
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
   
    def uninstall_official_en_north_vanillaplus_modified(self):
        
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服 EN北-VanillaPlus框架-改动版")
            self.uninstall_window.geometry("800x700")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="EN北-VanillaPlus框架-改动版",
                category="官服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
  
    def install_official_en_north_vanillaplus_regular(self):
      
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装官服 EN北-VanillaPlus框架-普通版")
            self.install_window.geometry("800x700")  
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
          
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="EN北-VanillaPlus框架-普通版",
                category="官服",
                download_url="https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-5/Official.Uniform-EN.North-Vanilla.Plus.Frame-Regular.Edition.zip"
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
   
    def uninstall_official_en_north_vanillaplus_regular(self):
       
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服 EN北-VanillaPlus框架-普通版")
            self.uninstall_window.geometry("800x700")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="EN北-VanillaPlus框架-普通版",
                category="官服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
   
    def install_cn_north_lts_frame(self):
       
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装社区服 CN北-LTS-框架")
            self.install_window.geometry("800x700")  
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
         
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="CN北-LTS-框架",
                category="社区服",
                download_url="https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-6/Community.service-CN.North-LTS-framework.zip"
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
  
    def uninstall_cn_north_lts_frame(self):
       
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载社区服 CN北-LTS-框架")
            self.uninstall_window.geometry("800x700") 
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()
            
            uninstaller = FrameworkUninstaller(
                self.uninstall_window,
                framework_name="CN北-LTS-框架",
                category="社区服"
            )
            uninstaller.on_complete = self.refresh_installed_status
        else:
            self.uninstall_window.lift()
    
    
    def install_en_north_frame(self):
   
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装社区服 EN北-框架")
            self.install_window.geometry("800x700")  
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
          
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="EN北-框架",
                category="社区服",
                download_url="https://github.com/TwoSevenFour-274/TTF2-MOD-Frame/releases/download/TTF2-7/Community.Service-EN.North-Framework.zip"
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
    
    def uninstall_en_north_frame(self):
        """卸载社区服 EN北-框架"""
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载社区服 EN北-框架")
            self.uninstall_window.geometry("800x700")  
            self.uninstall_window.transient(self.root)
            self.uninstall_window.grab_set()
            
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
            font=("SimHei", 16, "bold")
        ).pack(pady=15)
        
        
        info_frame = ttk.LabelFrame(content_frame, text="框架信息", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
       
        ttk.Label(info_frame, text=f"名称: {self.framework_name}").pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"分类: {self.category}").pack(anchor=tk.W, pady=2)
        
        url_frame = ttk.Frame(info_frame)
        url_frame.pack(fill=tk.X, pady=2)
        ttk.Label(url_frame, text="下载地址:").pack(side=tk.LEFT, anchor=tk.W)
        url_text = tk.Text(url_frame, height=3, width=70, wrap="word", font=("SimHei", 9))
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
    
    def _on_mousewheel(self, event):
      
        if platform.system() == "Windows":
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Linux":
            if event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            else:
                self.canvas.yview_scroll(1, "units")
    
    def update_directory_display(self):
        
        method = self.search_method.get()
        if method == "auto":
          
            self.game_dir = self.find_titanfall2_directory()
            if self.game_dir:
                self.game_dir_var.set(f"自动找到: {self.game_dir}")
            else:
                self.game_dir_var.set("自动搜索未找到游戏目录，请尝试手动选择")
            self.browse_btn.config(state=tk.DISABLED)
        else:
         
            self.game_dir = ""
            self.game_dir_var.set("请点击浏览按钮选择目录")
            self.browse_btn.config(state=tk.NORMAL)
    
    def find_titanfall2_directory(self):
    
        self.status_var.set("正在搜索Titanfall2游戏目录...")
        self.root.update()
        
       
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
            steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
            steam_apps = os.path.join(steam_path, "steamapps", "common", "Titanfall2")
            if os.path.exists(os.path.join(steam_apps, "Titanfall2.exe")):
                return steam_apps
        except Exception:
            pass
        
      
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Origin")
            origin_path = winreg.QueryValueEx(key, "ClientPath")[0]
            origin_games = os.path.join(os.path.dirname(origin_path), "Games", "Titanfall2")
            if os.path.exists(os.path.join(origin_games, "Titanfall2.exe")):
                return origin_games
        except Exception:
            pass
        
       
        ea_paths = [
            os.path.join(os.environ.get("ProgramFiles", ""), "EA Games", "Titanfall 2"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "EA Games", "Titanfall 2")
        ]
        for path in ea_paths:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
       
        origin_default_paths = [
            os.path.join(os.environ.get("ProgramFiles", ""), "Origin Games", "Titanfall 2"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Origin Games", "Titanfall 2")
        ]
        for path in origin_default_paths:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
       
        steam_libraries = [
            os.path.join(os.environ.get("ProgramFiles", ""), "Steam", "steamapps", "common", "Titanfall2"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Steam", "steamapps", "common", "Titanfall2"),
            os.path.join("D:", "SteamLibrary", "steamapps", "common", "Titanfall2"),
            os.path.join("E:", "SteamLibrary", "steamapps", "common", "Titanfall2"),
            os.path.join("F:", "SteamLibrary", "steamapps", "common", "Titanfall2"),
            os.path.join(os.environ.get("USERPROFILE", ""), "SteamLibrary", "steamapps", "common", "Titanfall2")
        ]
        for path in steam_libraries:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
       
        user_docs = [
            os.path.join(os.environ.get("USERPROFILE", ""), "Documents", "Electronic Arts", "Titanfall 2"),
            os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Documents", "Electronic Arts", "Titanfall 2")
        ]
        for path in user_docs:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
       
        other_paths = [
            os.path.join("C:", "Games", "Titanfall 2"),
            os.path.join("D:", "Games", "Titanfall 2"),
            os.path.join("E:", "Games", "Titanfall 2"),
            os.path.join("F:", "Games", "Titanfall 2")
        ]
        for path in other_paths:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
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
            
           
            extract_dir = os.path.join(temp_dir, "extracted")
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
            
    
            shutil.rmtree(temp_dir)
            
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
            text=f"卸载 {self.category} - {self.framework_name}", 
            font=("SimHei", 16, "bold")
        ).pack(pady=15)
        
       
        info_frame = ttk.LabelFrame(content_frame, text="框架信息", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text=f"名称: {self.framework_name}").pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"分类: {self.category}").pack(anchor=tk.W, pady=2)
        
      
        dir_frame = ttk.LabelFrame(content_frame, text="游戏目录", padding="10")
        dir_frame.pack(fill=tk.X, pady=10)
        
        self.game_dir_var = tk.StringVar(value=self.game_dir if self.game_dir else "未找到游戏目录，请手动选择")
        dir_entry = ttk.Label(dir_frame, textvariable=self.game_dir_var, wraplength=600)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        browse_btn = ttk.Button(dir_frame, text="浏览...", command=self.browse_game_directory)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
       
        progress_frame = ttk.LabelFrame(content_frame, text="卸载进度", padding="10")
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
            text="开始卸载", 
            command=self.start_uninstallation
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
    
    def _on_mousewheel(self, event):
      
        if platform.system() == "Windows":
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        elif platform.system() == "Linux":
            if event.delta > 0:
                self.canvas.yview_scroll(-1, "units")
            else:
                self.canvas.yview_scroll(1, "units")
    
    def find_titanfall2_directory(self):
     
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam")
            steam_path = winreg.QueryValueEx(key, "InstallPath")[0]
            steam_apps = os.path.join(steam_path, "steamapps", "common", "Titanfall2")
            if os.path.exists(os.path.join(steam_apps, "Titanfall2.exe")):
                return steam_apps
        except Exception:
            pass
        
     
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Origin")
            origin_path = winreg.QueryValueEx(key, "ClientPath")[0]
            origin_games = os.path.join(os.path.dirname(origin_path), "Games", "Titanfall2")
            if os.path.exists(os.path.join(origin_games, "Titanfall2.exe")):
                return origin_games
        except Exception:
            pass
        
       
        ea_paths = [
            os.path.join(os.environ.get("ProgramFiles", ""), "EA Games", "Titanfall 2"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "EA Games", "Titanfall 2")
        ]
        for path in ea_paths:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
     
        origin_default_paths = [
            os.path.join(os.environ.get("ProgramFiles", ""), "Origin Games", "Titanfall 2"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Origin Games", "Titanfall 2")
        ]
        for path in origin_default_paths:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
       
        steam_libraries = [
            os.path.join(os.environ.get("ProgramFiles", ""), "Steam", "steamapps", "common", "Titanfall2"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Steam", "steamapps", "common", "Titanfall2"),
            os.path.join("D:", "SteamLibrary", "steamapps", "common", "Titanfall2"),
            os.path.join("E:", "SteamLibrary", "steamapps", "common", "Titanfall2"),
            os.path.join("F:", "SteamLibrary", "steamapps", "common", "Titanfall2"),
            os.path.join(os.environ.get("USERPROFILE", ""), "SteamLibrary", "steamapps", "common", "Titanfall2")
        ]
        for path in steam_libraries:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
     
        user_docs = [
            os.path.join(os.environ.get("USERPROFILE", ""), "Documents", "Electronic Arts", "Titanfall 2"),
            os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Documents", "Electronic Arts", "Titanfall 2")
        ]
        for path in user_docs:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
      
        other_paths = [
            os.path.join("C:", "Games", "Titanfall 2"),
            os.path.join("D:", "Games", "Titanfall 2"),
            os.path.join("E:", "Games", "Titanfall 2"),
            os.path.join("F:", "Games", "Titanfall 2")
        ]
        for path in other_paths:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
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