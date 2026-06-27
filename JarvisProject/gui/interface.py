import customtkinter as ctk
import psutil
import math
import time
import random
import datetime

class JarvisUI(ctk.CTk):
    def __init__(self, start_callback):
        super().__init__()

        self.title("A.R.C.H.E.R.")
        self.attributes("-fullscreen", True)
        self.configure(fg_color="#000")
        ctk.set_appearance_mode("dark")

        self.callback = start_callback
        self.angle = 0
        self.pulse = 0
        self.start_time = time.time()
        
        self.theme_color = "#00fbff"
        self.sec_color = "#5e17eb"

        self.setup_canvas()
        self.setup_fixed_widgets()
        self.run_engine()

    def setup_canvas(self):
        self.canvas = ctk.CTkCanvas(self, bg="#000", highlightthickness=0)
        self.canvas.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.w = self.winfo_screenwidth()
        self.h = self.winfo_screenheight()
        self.draw_hex_grid()

    def draw_hex_grid(self):
        s = 60
        v_gap = s * math.sqrt(3)
        for x in range(0, self.w + s, int(s * 1.5)):
            for y in range(0, self.h + s, int(v_gap)):
                offset = (v_gap / 2) if (x // (s * 1.5)) % 2 else 0
                pts = []
                for i in range(6):
                    a = math.radians(i * 60)
                    pts.append((x + s * math.cos(a), y + offset + s * math.sin(a)))
                self.canvas.create_polygon(pts, outline="#030303", fill="", width=1)

    def draw_radar(self, x, y, r):
        self.canvas.delete("radar")
        self.canvas.create_oval(x-r, y-r, x+r, y+r, outline="#004444", width=1, tags="radar")
        self.canvas.create_oval(x-r/2, y-r/2, x+r/2, y+r/2, outline="#002222", width=1, tags="radar")
        sweep_angle = (time.time() * 80) % 360
        sx = x + r * math.cos(math.radians(sweep_angle))
        sy = y + r * math.sin(math.radians(sweep_angle))
        self.canvas.create_line(x, y, sx, sy, fill=self.theme_color, width=2, tags="radar")

    def draw_data_columns(self):
        if random.random() > 0.8:
            self.canvas.delete("data_bits")
            for i in range(8):
                rx = random.choice([20, self.w-40])
                ry = random.randint(100, self.h-100)
                val = hex(random.randint(1000, 9999)).upper()
                self.canvas.create_text(rx, ry, text=val, fill="#003333", font=("Consolas", 8), tags="data_bits")

    def setup_fixed_widgets(self):
        self.side_panel = ctk.CTkFrame(self, fg_color="transparent", width=400)
        self.side_panel.place(relx=0.98, rely=0.5, anchor="e")

        self.status_lbl = ctk.CTkLabel(self.side_panel, text="SYSTEM IDLE", font=("Orbitron", 34, "bold"), text_color=self.theme_color)
        self.status_lbl.pack(pady=10)

        self.terminal_box = ctk.CTkTextbox(self.side_panel, width=380, height=250, fg_color="#030303", border_width=1, border_color=self.theme_color, font=("Consolas", 12), text_color=self.theme_color)
        self.terminal_box.pack(pady=5)

        self.pass_entry = ctk.CTkEntry(self.side_panel, placeholder_text="NEURAL KEY", show="*", width=350, height=45, fg_color="#000", border_color=self.theme_color, font=("Consolas", 14), justify="center")
        self.pass_entry.pack(pady=10)

        self.start_btn = ctk.CTkButton(self.side_panel, text="INITIALIZE", command=self.callback, font=("Orbitron", 14, "bold"), fg_color=self.theme_color, text_color="#000", height=50, width=350)
        self.start_btn.pack(pady=5)

    def draw_gauge(self, x, y, r, val, title, color):
        self.canvas.create_arc(x-r, y-r, x+r, y+r, start=90, extent=-(val*3.6), outline=color, width=8, style="arc", tags="gauges")
        self.canvas.create_text(x, y, text=f"{int(val)}%", fill=color, font=("Orbitron", 12, "bold"), tags="gauges")
        self.canvas.create_text(x, y+r+15, text=title, fill="#004444", font=("Orbitron", 8), tags="gauges")

    def draw_waveform(self):
        self.canvas.delete("wave")
        points = []
        for x in range(0, self.w, 40):
            y = (self.h - 50) + math.sin(x*0.02 + time.time()*8) * 15
            points.extend([x, y])
        self.canvas.create_line(points, fill=self.theme_color, width=2, smooth=True, tags="wave")

    def draw_core(self):
        self.canvas.delete("core")
        cx, cy = self.w / 2, self.h / 2
        self.angle += 2.0
        for i in range(4):
            r = 240 - (i * 45)
            spd = self.angle * (1 if i%2==0 else -1.2)
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=spd, extent=40, outline=self.theme_color, width=2, style="arc", tags="core")
            self.canvas.create_arc(cx-r, cy-r, cx+r, cy+r, start=spd+180, extent=40, outline=self.theme_color, width=2, style="arc", tags="core")
        
        glow = int((math.sin(time.time()*4)+1)*80 + 40)
        c_glow = f"#00{max(0,min(255,glow)):02x}{max(0,min(255,glow)):02x}"
        self.canvas.create_oval(cx-60, cy-60, cx+60, cy+60, fill=c_glow, outline="", tags="core")

    def run_engine(self):
        self.draw_core()
        self.draw_waveform()
        self.draw_radar(150, 150, 80)
        self.draw_data_columns()
        
        if int(time.time() * 2) % 2 == 0:
            self.canvas.delete("gauges")
            cpu = psutil.cpu_percent()
            ram = psutil.virtual_memory().percent
            disk = psutil.disk_usage('/').percent
            net = random.randint(12, 38)
            
            self.draw_gauge(150, 350, 50, cpu, "CPU", self.theme_color)
            self.draw_gauge(150, 500, 50, ram, "RAM", self.sec_color)
            self.draw_gauge(150, 650, 50, disk, "DISK", "#ff0055")
            self.draw_gauge(150, 800, 50, net, "LAT", "#ffff00")

        self.canvas.delete("info")
        now = datetime.datetime.now()
        self.canvas.create_text(self.w/2, 40, text=now.strftime("%H:%M:%S"), fill=self.theme_color, font=("Orbitron", 30, "bold"), tags="info")
        self.canvas.create_text(self.w/2, 80, text=f"UPTIME: {int(time.time()-self.start_time)}S", fill="#004444", font=("Consolas", 12), tags="info")
        
        self.after(60, self.run_engine)

    def terminal_log(self, msg):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.terminal_box.insert("end", f"\n[{ts}] » {msg}\n")
        self.terminal_box.see("end")
        self.update_idletasks()

    def update_status(self, text, color="#00fbff"):
        self.status_lbl.configure(text=text, text_color=color)
        self.theme_color = color
        self.terminal_box.configure(border_color=color)
        self.pass_entry.configure(border_color=color)
        self.start_btn.configure(fg_color=color)

if __name__ == "__main__":
    app = JarvisUI(lambda: print("Nexus Init"))
    app.bind("<Escape>", lambda e: app.destroy())
    app.mainloop()