import tkinter as tk
from tkinter import simpledialog, messagebox
import random
import os

# 食物选择应用主类
class FoodChooserApp:
    # 初始化应用界面
    def __init__(self, root):
        self.root = root
        self.root.title("今天吃什么")
        self.root.geometry("400x250")
        
        # 创建界面元素
        self.label = tk.Label(root, text="点击Go随机选择食物", font=("Consolas", 14))
        self.label.pack(pady=15)
        
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)
        
        self.go_button = tk.Button(button_frame, text="Go", command=self.choose_food, width=12, height=2)
        self.go_button.pack(side=tk.LEFT, padx=10)
        
        self.edit_button = tk.Button(button_frame, text="编辑菜单", command=self.open_edit_window, width=12, height=2)
        self.edit_button.pack(side=tk.LEFT, padx=10)
        
        # Data file path
        self.data_file = "data.txt"
        
        # 创建数据文件（如果不存在）
        if not os.path.exists(self.data_file):
            with open(self.data_file, "w", encoding="utf-8") as f:
                f.write("土豆牛柳盖浇饭 宫保鸡丁盖浇饭 火鸡面 炸鸡 食堂 拼好饭 炒面 炒饭 馄饨 饺子 粥 牛肉面 西红柿鸡蛋面 火鸡面配炸鸡")
    
    # 随机选择食物 (优化内存)
    def choose_food(self):
        try:
            # 流式读取文件，避免加载整个文件到内存
            foods = []
            with open(self.data_file, "r", encoding="utf-8") as f:
                for line in f:
                    foods.extend(line.strip().split())
            # 过滤空项
            foods = [food for food in foods if food]
                
            if not foods:
                self.label.config(text="菜单为空! 请添加食物")
                return
                
            chosen = random.choice(foods)
            self.label.config(text=f"吃: {chosen}", font=("Consolas", 16, "bold"))
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败: {str(e)}")
    
    # 打开编辑菜单窗口 (优化内存)
    def open_edit_window(self):
        edit_win = tk.Toplevel(self.root)
        edit_win.title("编辑菜单")
        edit_win.geometry("500x400")
        
        # 使用Listbox代替ScrolledText，更节省内存
        list_frame = tk.Frame(edit_win)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, 
                                  width=50, height=15, font=("Arial", 12))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # 状态标签用于显示自动保存信息
        self.status_label = tk.Label(edit_win, text="", fg="green")
        self.status_label.pack(side=tk.BOTTOM, pady=5)
        
        # 加载当前食物列表
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                for line in f:
                    foods = line.strip().split()
                    for food in foods:
                        if food:  # 跳过空项
                            self.listbox.insert(tk.END, food)
        except Exception as e:
            messagebox.showerror("错误", f"读取文件失败: {str(e)}")
            return
        
        # 操作按钮
        button_frame = tk.Frame(edit_win)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        add_btn = tk.Button(button_frame, text="添加内容", command=lambda: self.update_file(edit_win, "add"), width=12)
        add_btn.pack(side=tk.LEFT, padx=5)
        
        remove_btn = tk.Button(button_frame, text="删除内容", command=lambda: self.update_file(edit_win, "remove"), width=12)
        remove_btn.pack(side=tk.LEFT, padx=5)
        
        save_btn = tk.Button(button_frame, text="保存", command=lambda: self.save_file(edit_win), width=12)
        save_btn.pack(side=tk.RIGHT, padx=5)
    
    # 更新菜单内容（添加或删除食物）(优化内存)
    def update_file(self, window, action):
        if action == "add":
            new_food = simpledialog.askstring("添加食物", "请输入要添加的食物名称:")
            if new_food and new_food.strip():
                new_food = new_food.strip()
                # 直接添加到Listbox，避免处理整个列表
                self.listbox.insert(tk.END, new_food)
                # 自动保存
                self._auto_save()
        elif action == "remove":
            selected = self.listbox.curselection()
            if selected:
                # 直接删除选中项，避免处理整个列表
                self.listbox.delete(selected[0])
                # 自动保存
                self._auto_save()
            else:
                messagebox.showinfo("提示", "请先选择一个食物")
                
    # 自动保存方法
    def _auto_save(self):
        try:
            # 直接从Listbox获取内容
            foods = [self.listbox.get(i) for i in range(self.listbox.size())]
            content = " ".join(foods)
            
            # 写入文件
            with open(self.data_file, "w", encoding="utf-8") as f:
                f.write(content)
            
            # 更新状态标签
            self.status_label.config(text="自动保存成功!", fg="green")
            # 3秒后清除状态
            self.root.after(3000, lambda: self.status_label.config(text=""))
        except Exception as e:
            self.status_label.config(text=f"自动保存失败: {str(e)}", fg="red")
    
    # 保存菜单到文件 (手动保存)
    def save_file(self, window):
        try:
            # 直接从Listbox获取内容
            foods = [self.listbox.get(i) for i in range(self.listbox.size())]
            content = " ".join(foods)
            
            # 写入文件
            with open(self.data_file, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("成功", "菜单已保存!")
            window.destroy()
        except Exception as e:
            messagebox.showerror("错误", f"保存失败: {str(e)}")

# 程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = FoodChooserApp(root)
    root.mainloop()
