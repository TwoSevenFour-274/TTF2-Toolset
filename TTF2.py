import os
import shutil
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import platform
import webbrowser 
from datetime import datetime

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
        right_content.pack(expand=True)  # 让内容在右侧框架中居中
        
     
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
        
        ttk.Label(
            cn_north_frame, 
            text="CN北-框架", 
            width=40
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            cn_north_frame, 
            text="安装", 
            command=self.install_cn_north_framework
        ).pack(side=tk.LEFT, padx=5)
   
        uninstall_btn_state = tk.NORMAL if "社区服-CN北-框架" in self.installed_frameworks else tk.DISABLED
        ttk.Button(
            cn_north_frame, 
            text="卸载", 
            command=self.uninstall_cn_north_framework,
            state=uninstall_btn_state
        ).pack(side=tk.LEFT, padx=5)
        
     
        other_community_frame = ttk.Frame(functions_frame)
        other_community_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            other_community_frame, 
            text="CN北-LTS-框架", 
            width=40
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            other_community_frame, 
            text="安装", 
            command=self.install_cn_north_lts_framework,
            state=tk.NORMAL
        ).pack(side=tk.LEFT, padx=5)
        
     
        uninstall_btn_state = tk.NORMAL if "社区服-CN北-LTS-框架" in self.installed_frameworks else tk.DISABLED
        ttk.Button(
            other_community_frame, 
            text="卸载", 
            command=self.uninstall_cn_north_lts_framework,
            state=uninstall_btn_state
        ).pack(side=tk.LEFT, padx=5)
        
        en_north_frame = ttk.Frame(functions_frame)
        en_north_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            en_north_frame, 
            text="EN北-框架", 
            width=40
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            en_north_frame, 
            text="安装", 
            command=self.install_en_north_framework,
            state=tk.NORMAL
        ).pack(side=tk.LEFT, padx=5)
        

        uninstall_btn_state = tk.NORMAL if "社区服-EN北-框架" in self.installed_frameworks else tk.DISABLED
        ttk.Button(
            en_north_frame, 
            text="卸载", 
            command=self.uninstall_en_north_framework,
            state=uninstall_btn_state
        ).pack(side=tk.LEFT, padx=5)
        
  
        ttk.Label(
            functions_frame, 
            text="官服", 
            font=("SimHei", 12, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))
        
     
        official_frame1 = ttk.Frame(functions_frame)
        official_frame1.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            official_frame1, 
            text="CN北-框架", 
            width=40
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            official_frame1, 
            text="安装", 
            command=self.install_official_cn_north_framework,
            state=tk.NORMAL
        ).pack(side=tk.LEFT, padx=5)
        
    
        uninstall_btn_state = tk.NORMAL if "官服-CN北-框架" in self.installed_frameworks else tk.DISABLED
        ttk.Button(
            official_frame1, 
            text="卸载", 
            command=self.uninstall_official_cn_north_framework,
            state=uninstall_btn_state
        ).pack(side=tk.LEFT, padx=5)
        
    
        official_frame2 = ttk.Frame(functions_frame)
        official_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            official_frame2, 
            text="EN北-VanillaPlus框架-普通版", 
            width=40
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            official_frame2, 
            text="安装", 
            command=self.install_official_en_vanilla_plus_normal,
            state=tk.NORMAL
        ).pack(side=tk.LEFT, padx=5)
        
     
        uninstall_btn_state = tk.NORMAL if "官服-EN北-VanillaPlus框架-普通版" in self.installed_frameworks else tk.DISABLED
        ttk.Button(
            official_frame2, 
            text="卸载", 
            command=self.uninstall_official_en_vanilla_plus_normal,
            state=uninstall_btn_state
        ).pack(side=tk.LEFT, padx=5)
        
   
        official_frame3 = ttk.Frame(functions_frame)
        official_frame3.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            official_frame3, 
            text="EN北-VanillaPlus框架-改动版", 
            width=40
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            official_frame3, 
            text="安装", 
            command=self.install_official_en_vanilla_plus_modified,
            state=tk.NORMAL
        ).pack(side=tk.LEFT, padx=5)
        
       
        uninstall_btn_state = tk.NORMAL if "官服-EN北-VanillaPlus框架-改动版" in self.installed_frameworks else tk.DISABLED
        ttk.Button(
            official_frame3, 
            text="卸载", 
            command=self.uninstall_official_en_vanilla_plus_modified,
            state=uninstall_btn_state
        ).pack(side=tk.LEFT, padx=5)
        
      
        ttk.Label(
            functions_frame, 
            text="官服×社区服", 
            font=("SimHei", 12, "bold")
        ).pack(anchor=tk.W, pady=(10, 5))
        
    
        hybrid_frame1 = ttk.Frame(functions_frame)
        hybrid_frame1.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            hybrid_frame1, 
            text="EN北-ION-离子框架-HUD可以使用", 
            width=40
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            hybrid_frame1, 
            text="安装", 
            command=self.install_hybrid_en_ion_hud_available,
            state=tk.NORMAL 
        ).pack(side=tk.LEFT, padx=5)
        
       
        uninstall_btn_state = tk.NORMAL if "官服×社区服-EN北-ION-离子框架-HUD可以使用" in self.installed_frameworks else tk.DISABLED
        ttk.Button(
            hybrid_frame1, 
            text="卸载", 
            command=self.uninstall_hybrid_en_ion_hud_available,
            state=uninstall_btn_state
        ).pack(side=tk.LEFT, padx=5)
        
   
        hybrid_frame2 = ttk.Frame(functions_frame)
        hybrid_frame2.pack(fill=tk.X, pady=5)
        
        ttk.Label(
            hybrid_frame2, 
            text="EN北-ION-离子框架-HUD无法使用", 
            width=40
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            hybrid_frame2, 
            text="安装", 
            command=self.install_hybrid_en_ion_hud_unavailable,
            state=tk.NORMAL  # 改为可用状态
        ).pack(side=tk.LEFT, padx=5)
        
      
        uninstall_btn_state = tk.NORMAL if "官服×社区服-EN北-ION-离子框架-HUD无法使用" in self.installed_frameworks else tk.DISABLED
        ttk.Button(
            hybrid_frame2, 
            text="卸载", 
            command=self.uninstall_hybrid_en_ion_hud_unavailable,
            state=uninstall_btn_state
        ).pack(side=tk.LEFT, padx=5)
        
      
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
     
        for filename in os.listdir("."):
            if filename.startswith("install_log_") and filename.endswith(".json"):
                try:
                   
                    with open(filename, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if data:
                            category = data[0]["category"]
                            framework = data[0]["framework"]
                            installed.append(f"{category}-{framework}")
                except:
                    continue
        return installed
    
    def refresh_installed_status(self):
       
        self.installed_frameworks = self.get_installed_frameworks()
   
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_main_widgets()
    
    def install_hybrid_en_ion_hud_available(self):
      
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装官服×社区服 EN北-ION-离子框架-HUD可以使用")
            self.install_window.geometry("671x492")
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="EN北-ION-离子框架-HUD可以使用",
                category="官服×社区服",
                source_dir=os.path.join("文件存储", "官+EN北-ION-离子框架-HUD可以使用")  # 使用指定的源文件名
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
 
    def uninstall_hybrid_en_ion_hud_available(self):

        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服×社区服 EN北-ION-离子框架-HUD可以使用")
            self.uninstall_window.geometry("671x492")
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
            self.install_window.geometry("671x492")
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="EN北-ION-离子框架-HUD无法使用",
                category="官服×社区服",
                source_dir=os.path.join("文件存储", "官+EN北-ION-离子框架-HUD无法使用")  
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
    def uninstall_hybrid_en_ion_hud_unavailable(self):
      
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服×社区服 EN北-ION-离子框架-HUD无法使用")
            self.uninstall_window.geometry("671x492")
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
    
    # 以下为原有框架的安装卸载方法，保持不变
    def install_cn_north_framework(self):
   
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装社区服 CN北-框架")
            self.install_window.geometry("671x492")
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="CN北-框架",
                category="社区服",
                source_dir=os.path.join("文件存储", "社区服-CN北-框架")
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
    def uninstall_cn_north_framework(self):
      
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载社区服 CN北-框架")
            self.uninstall_window.geometry("671x492")
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
    
    def install_cn_north_lts_framework(self):

        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装社区服 CN北-LTS-框架")
            self.install_window.geometry("671x492")
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="CN北-LTS-框架",
                category="社区服",
                source_dir=os.path.join("文件存储", "社区服-CN北-LTS-框架")
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
    def uninstall_cn_north_lts_framework(self):
   
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载社区服 CN北-LTS-框架")
            self.uninstall_window.geometry("671x492")
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
    
    def install_en_north_framework(self):
 
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装社区服 EN北-框架")
            self.install_window.geometry("671x492")
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="EN北-框架",
                category="社区服",
                source_dir=os.path.join("文件存储", "社区服-EN北-框架")
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
    def uninstall_en_north_framework(self):
        
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载社区服 EN北-框架")
            self.uninstall_window.geometry("671x492")
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
    
    def install_official_cn_north_framework(self):
    
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装官服 CN北-框架")
            self.install_window.geometry("671x492")
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="CN北-框架",
                category="官服",
                source_dir=os.path.join("文件存储", "官服-CN北-框架")
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
    def uninstall_official_cn_north_framework(self):
   
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服 CN北-框架")
            self.uninstall_window.geometry("671x492")
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
    
    def install_official_en_vanilla_plus_normal(self):
   
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装官服 EN北-VanillaPlus框架-普通版")
            self.install_window.geometry("671x492")
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="EN北-VanillaPlus框架-普通版",
                category="官服",
                source_dir=os.path.join("文件存储", "官服-EN北-VanillaPlus框架-普通版")
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
    def uninstall_official_en_vanilla_plus_normal(self):
   
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服 EN北-VanillaPlus框架-普通版")
            self.uninstall_window.geometry("671x492")
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
    
    def install_official_en_vanilla_plus_modified(self):
     
        if not hasattr(self, 'install_window') or not self.install_window or not self.install_window.winfo_exists():
            self.install_window = tk.Toplevel(self.root)
            self.install_window.title("安装官服 EN北-VanillaPlus框架-改动版")
            self.install_window.geometry("671x492")
            self.install_window.transient(self.root)
            self.install_window.grab_set()
            
            installer = FrameworkInstaller(
                self.install_window,
                framework_name="EN北-VanillaPlus框架-改动版",
                category="官服",
                source_dir=os.path.join("文件存储", "官服-EN北-VanillaPlus框架-改动版")
            )
            installer.on_complete = self.refresh_installed_status
        else:
            self.install_window.lift()
    
    def uninstall_official_en_vanilla_plus_modified(self):
    
        if not hasattr(self, 'uninstall_window') or not self.uninstall_window or not self.uninstall_window.winfo_exists():
            self.uninstall_window = tk.Toplevel(self.root)
            self.uninstall_window.title("卸载官服 EN北-VanillaPlus框架-改动版")
            self.uninstall_window.geometry("671x492")
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


class FrameworkInstaller:
    def __init__(self, root, framework_name, category, source_dir):
        self.root = root
        self.framework_name = framework_name
        self.category = category
        self.source_dir = source_dir
        self.on_complete = None  
        
       
        self.status_var = tk.StringVar(value=f"准备安装 {category} - {framework_name}")
        
       
        self.game_dir = self.find_titanfall2_directory()
        
    
        self.install_log = f"install_log_{category}_{framework_name}.json".replace("-", "_").replace("×", "x")
        
       
        self.create_install_widgets()
    
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
        self.canvas_window = self.canvas.create_window((0, 0), window=content_frame, anchor="nw", width=620)
        
     
        ttk.Label(
            content_frame, 
            text=f"安装 {self.category} - {self.framework_name}", 
            font=("SimHei", 16, "bold")
        ).pack(pady=15)
        
      
        info_frame = ttk.LabelFrame(content_frame, text="框架信息", padding="10")
        info_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(info_frame, text=f"名称: {self.framework_name}").pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"分类: {self.category}").pack(anchor=tk.W, pady=2)
        ttk.Label(info_frame, text=f"源目录: {self.source_dir}").pack(anchor=tk.W, pady=2)
       
        dir_frame = ttk.LabelFrame(content_frame, text="游戏目录", padding="10")
        dir_frame.pack(fill=tk.X, pady=10)
        
        self.game_dir_var = tk.StringVar(value=self.game_dir if self.game_dir else "未找到Titanfall2.exe，请手动选择")
        dir_entry = ttk.Label(dir_frame, textvariable=self.game_dir_var)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        browse_btn = ttk.Button(dir_frame, text="浏览...", command=self.browse_game_directory)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        
       
        progress_frame = ttk.LabelFrame(content_frame, text="安装进度", padding="10")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5)
        
       
        ttk.Label(content_frame, textvariable=self.status_var).pack(anchor=tk.W, pady=5)
        
  
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
    
    def find_titanfall2_directory(self):
        
        self.status_var.set("正在搜索Titanfall2游戏目录...")
        self.root.update()
        
 
        common_paths = [
            os.path.join(os.environ.get("ProgramFiles", ""), "Origin Games", "Titanfall 2"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Origin Games", "Titanfall 2"),
            os.path.join(os.environ.get("USERPROFILE", ""), "Documents", "Electronic Arts", "Titanfall 2")
        ]
        
   
        for path in common_paths:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
     
        if platform.system() == "Windows":
            drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
            for drive in drives:
                for root, _, files in os.walk(drive):
                    if "Titanfall2.exe" in files:
                        return root
                    if root.count(os.sep) > 5:  
                        continue
        
        return None
    
    def browse_game_directory(self):
     
        directory = filedialog.askdirectory(title="选择Titanfall2.exe所在目录")
        if directory and os.path.exists(os.path.join(directory, "Titanfall2.exe")):
            self.game_dir = directory
            self.game_dir_var.set(directory)
        elif directory:
            messagebox.showerror("错误", "所选目录中未找到Titanfall2.exe")
    
    def get_all_files(self, directory):
       
        file_list = []
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, directory)
                file_list.append(relative_path)
        return file_list
    
    def start_installation(self):
    
        if not os.path.exists(self.source_dir):
            messagebox.showerror("错误", f"源目录不存在: {self.source_dir}")
            return
        
      
        if not self.game_dir or not os.path.exists(os.path.join(self.game_dir, "Titanfall2.exe")):
            messagebox.showerror("错误", "请先设置有效的游戏目录")
            return
        
        
        progress_window = tk.Toplevel(self.root)
        progress_window.title("安装中")
        progress_window.geometry("400x100")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        ttk.Label(progress_window, text=f"正在安装 {self.framework_name}，请稍候...").pack(pady=10)
        install_progress = ttk.Progressbar(progress_window, variable=self.progress_var, maximum=100)
        install_progress.pack(fill=tk.X, padx=20, pady=10)
        
        self.root.update()
        time.sleep(0.5)
        
        try:
      
            source_files = self.get_all_files(self.source_dir)
            total_files = len(source_files)
            installed_files = []
            
           
            for i, relative_path in enumerate(source_files):
                source_path = os.path.join(self.source_dir, relative_path)
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
                
                
                progress = (i + 1) / total_files * 100
                self.progress_var.set(progress)
                self.status_var.set(f"正在安装: {relative_path} ({i+1}/{total_files})")
                self.root.update()
        
            for root, dirs, _ in os.walk(self.source_dir):
                relative_root = os.path.relpath(root, self.source_dir)
                if relative_root != ".":
                    installed_files.append({
                        "path": relative_root,
                        "is_dir": True,
                        "timestamp": datetime.now().isoformat(),
                        "framework": self.framework_name,
                        "category": self.category
                    })
            
            
            with open(self.install_log, "w", encoding="utf-8") as f:
                json.dump(installed_files, f, ensure_ascii=False, indent=2)
            
            self.status_var.set(f"{self.framework_name} 安装完成，共安装了{total_files}个文件")
            messagebox.showinfo("成功", f"{self.framework_name} 安装成功！\n已安装 {total_files} 个文件到游戏目录")
            
            
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
        
     
        self.install_log = f"install_log_{category}_{framework_name}.json".replace("-", "_").replace("×", "x")
        
   
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
        self.canvas_window = self.canvas.create_window((0, 0), window=content_frame, anchor="nw", width=620)
        
     
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
        
        self.game_dir_var = tk.StringVar(value=self.game_dir if self.game_dir else "未找到Titanfall2.exe，请手动选择")
        dir_entry = ttk.Label(dir_frame, textvariable=self.game_dir_var)
        dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        browse_btn = ttk.Button(dir_frame, text="浏览...", command=self.browse_game_directory)
        browse_btn.pack(side=tk.RIGHT, padx=5)
        

        progress_frame = ttk.LabelFrame(content_frame, text="卸载进度", padding="10")
        progress_frame.pack(fill=tk.X, pady=10)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=5)
        
        
        ttk.Label(content_frame, textvariable=self.status_var).pack(anchor=tk.W, pady=5)
        
   
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
      
        self.status_var.set("正在搜索Titanfall2游戏目录...")
        self.root.update()
        
   
        common_paths = [
            os.path.join(os.environ.get("ProgramFiles", ""), "Origin Games", "Titanfall 2"),
            os.path.join(os.environ.get("ProgramFiles(x86)", ""), "Origin Games", "Titanfall 2"),
            os.path.join(os.environ.get("USERPROFILE", ""), "Documents", "Electronic Arts", "Titanfall 2")
        ]
        
        
        for path in common_paths:
            if os.path.exists(os.path.join(path, "Titanfall2.exe")):
                return path
        
      
        if platform.system() == "Windows":
            drives = [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]
            for drive in drives:
                for root, _, files in os.walk(drive):
                    if "Titanfall2.exe" in files:
                        return root
                    if root.count(os.sep) > 5:  
                        continue
        
        return None
    
    def browse_game_directory(self):
       
        directory = filedialog.askdirectory(title="选择Titanfall2.exe所在目录")
        if directory and os.path.exists(os.path.join(directory, "Titanfall2.exe")):
            self.game_dir = directory
            self.game_dir_var.set(directory)
        elif directory:
            messagebox.showerror("错误", "所选目录中未找到Titanfall2.exe")
    
    def start_uninstallation(self):

      
        if not self.game_dir or not os.path.exists(os.path.join(self.game_dir, "Titanfall2.exe")):
            messagebox.showerror("错误", "请先设置有效的游戏目录")
            return
        
        
        if not os.path.exists(self.install_log):
            messagebox.showerror("错误", f"未找到 {self.framework_name} 的安装记录")
            return
    
       
        progress_window = tk.Toplevel(self.root)
        progress_window.title("卸载中")
        progress_window.geometry("400x100")
        progress_window.transient(self.root)
        progress_window.grab_set()
        
        ttk.Label(progress_window, text=f"正在卸载 {self.framework_name}，请稍候...").pack(pady=10)
        uninstall_progress = ttk.Progressbar(progress_window, variable=self.progress_var, maximum=100)
        uninstall_progress.pack(fill=tk.X, padx=20, pady=10)
        
        self.root.update()
        time.sleep(0.5)
        
        try:
           
            with open(self.install_log, "r", encoding="utf-8") as f:
                installed_files = json.load(f)
            
            total_items = len(installed_files)
            removed_items = 0
            
         
            files = [item for item in installed_files if not item.get("is_dir", False)]
            dirs = [item for item in installed_files if item.get("is_dir", False)]
            
       
            dirs.sort(key=lambda x: x["path"].count(os.sep), reverse=True)
            
          
            for item in files:
                file_path = os.path.join(self.game_dir, item["path"])
                if os.path.exists(file_path):
                    try:
                        os.remove(file_path)
                        removed_items += 1
                    except Exception as e:
                        self.status_var.set(f"警告: 无法删除文件 {file_path}: {str(e)}")
                
          
                progress = (removed_items / total_items) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"正在卸载: {item['path']} ({removed_items}/{total_items})")
                self.root.update()
            
      
            for item in dirs:
                dir_path = os.path.join(self.game_dir, item["path"])
                if os.path.exists(dir_path) and os.path.isdir(dir_path):
                    try:
                        os.rmdir(dir_path)  
                        removed_items += 1
                    except Exception as e:
                        self.status_var.set(f"警告: 无法删除目录 {dir_path}: {str(e)}")
                
                
                progress = (removed_items / total_items) * 100
                self.progress_var.set(progress)
                self.status_var.set(f"正在卸载: {item['path']} ({removed_items}/{total_items})")
                self.root.update()
            
          
            self.status_var.set("正在执行强制清理...")
            self.root.update()
            
       
            folders_to_remove = ["R2Northstar", "R2Titanfall", "R2Vanilla"]
            for folder in folders_to_remove:
                folder_path = os.path.join(self.game_dir, folder)
                if os.path.exists(folder_path) and os.path.isdir(folder_path):
                    try:
                       
                        shutil.rmtree(folder_path, ignore_errors=True)
                        self.status_var.set(f"已强制删除文件夹: {folder}")
                    except Exception as e:
                        self.status_var.set(f"警告: 无法删除文件夹 {folder}: {str(e)}")
                self.root.update()
            
          
            if os.path.exists(self.install_log):
                os.remove(self.install_log)
            
            self.status_var.set(f"{self.framework_name} 卸载完成，共处理了{total_items}个项目")
            messagebox.showinfo("成功", f"{self.framework_name} 卸载成功！\n已清理相关文件并强制删除指定文件夹")
            
            
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

    

