"""
COUNTER APP - LUÔN HIỆN TRÊN MÀN HÌNH
- Bấm mũi tên PHẢI: +1
- Bấm mũi tên TRÁI: -1
- Hoạt động ngay cả khi click ra ngoài
- Tắt app: Ctrl+Q hoặc click X
"""

import tkinter as tk
from pynput import keyboard

class AlwaysOnTopCounter:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Counter")
        
        # Cài đặt always on top
        self.root.attributes('-topmost', True)
        
        # Làm cửa sổ nhỏ gọn, có thể di chuyển
        self.root.overrideredirect(True)
        
        # Vị trí góc phải trên màn hình
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f'100x50+{screen_width-120}+20')
        
        # Số đếm
        self.counter = 3
        
        # Nền trong suốt
        self.root.configure(bg='black')
        self.root.wm_attributes('-transparentcolor', 'black')
        
        # Label hiển thị số
        self.label = tk.Label(
            self.root,
            text=str(self.counter),
            font=('Arial', 28, 'bold'),
            fg='white',
            bg='black'
        )
        self.label.pack(expand=True, fill='both')
        
        # Cho phép kéo cửa sổ
        self.label.bind('<Button-1>', self.start_move)
        self.label.bind('<B1-Motion>', self.do_move)
        
        # Thêm nút X nhỏ để đóng
        self.close_btn = tk.Label(
            self.root,
            text='×',
            font=('Arial', 16, 'bold'),
            fg='red',
            bg='black',
            cursor='hand2'
        )
        self.close_btn.place(x=80, y=0, width=20, height=20)
        self.close_btn.bind('<Button-1>', lambda e: self.root.quit())
        
        # Hiển thị hướng dẫn
        self.show_help()
        
        # Khởi động listener cho phím toàn cục
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()
        
    def on_key_press(self, key):
        """Bắt phím toàn cục (global hotkey)"""
        try:
            if key == keyboard.Key.right:
                self.increase()
            elif key == keyboard.Key.left:
                self.decrease()
            elif key == keyboard.Key.esc:
                self.root.quit()
        except:
            pass
    
    def increase(self):
        self.counter += 1
        self.update_display()
    
    def decrease(self):
        if self.counter > 0:
            self.counter -= 1
            self.update_display()
    
    def update_display(self):
        # Cập nhật UI trong main thread
        self.root.after(0, self._update_ui)
    
    def _update_ui(self):
        self.label.config(text=str(self.counter))
        
        if self.counter > 0:
            self.label.config(fg='#00ff00')
        else:
            self.label.config(fg='white')
    
    def show_help(self):
        help_text = "← →"
        original_text = self.label.cget('text')
        self.label.config(text=help_text, font=('Arial', 16))
        self.root.after(2000, lambda: self.label.config(
            text=original_text,
            font=('Arial', 28, 'bold')
        ))
    
    def start_move(self, event):
        self.x = event.x
        self.y = event.y
    
    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y
        self.root.geometry(f'+{x}+{y}')
    
    def run(self):
        try:
            self.root.mainloop()
        finally:
            self.listener.stop()


if __name__ == '__main__':
    app = AlwaysOnTopCounter()
    app.run()