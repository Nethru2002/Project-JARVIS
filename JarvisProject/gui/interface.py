import customtkinter as ctk
import psutil
import math
import time
import random
import datetime

class JarvisUI(ctk.CTk):
    def __init__(self, start_callback):
        super().__init__()

        self.title("A.R.C.H.E.R. NEXUS | HYPER-DRIVE OS")
        self.attributes("-fullscreen", True)
        self.configure(fg_color="#010101")
        ctk.set_appearance_mode("dark")

        self.start_time = time.time()
        self.callback = start_callback
        self.rotation_angle = 0
        self.wave_offset = 0
        self.glow_direction = 1
        self.glow_alpha = 100

        self.setup_layout()
        self.create_widgets()
        self.run_animations()

    def setup_layout(self):
        self.grid_columnconfigure((0, 2), weight=1, minsize=300)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=1)

    def create_widgets(self):
        self.canvas_bg = ctk.CTkCanvas(self, bg="#010101", highlightthickness=0)
        self.canvas_bg.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.draw_hud_accents()

        self.left_sidebar = ctk.CTkFrame(self, fg_color="transparent")
        self.left_sidebar.grid(row=0, column=0, sticky="nsew", padx=40, pady=60)
        
        self.create_telemetry_unit("SYSTEM CORE LOAD", "cpu")
        self.create_telemetry_unit("NEURAL MEMORY", "ram")
        self.create_telemetry_unit("QUANTUM STORAGE", "disk")
        self.create_telemetry_unit("NETWORK LATENCY", "net")

        self.center_stage = ctk.CTkFrame(self, fg_color="transparent")
        self.center_stage.grid(row=0, column=1, sticky="nsew")

        self.core_canvas = ctk.CTkCanvas(self.center_stage, width=600, height=600, bg="#010101", highlightthickness=0)
        self.core_canvas.pack(expand=True)

        self.right_sidebar = ctk.CTkFrame(self, fg_color="transparent")
        self.right_sidebar.grid(row=0, column=2, sticky="nsew", padx=40, pady=60)

        self.status_header = ctk.CTkLabel(self.right_sidebar, text="SYSTEM IDLE", font=("Orbitron", 28, "bold"), text_color="#00fbff")
        self.status_header.pack(pady=(0, 20))

        self.terminal_frame = ctk.CTkFrame(self.right_sidebar, fg_color="#050505", border_width=1, border_color="#004444")
        self.terminal_frame.pack(fill="both", expand=True, pady=20)

        self.console = ctk.CTkTextbox(self.terminal_frame, fg_color="transparent", font=("Consolas", 12), text_color="#00fbff", border_width=0)
        self.console.pack(fill="both", expand=True, padx=5, pady=5)

        self.pass_entry = ctk.CTkEntry(self.right_sidebar, placeholder_text="ENCRYPTION KEY", show="*", height=45, fg_color="#000", border_color="#00fbff", font=("Consolas", 14), justify="center")
        self.pass_entry.pack(fill="x", pady=20)

        self.start_btn = ctk.CTkButton(self.right_sidebar, text="INITIALIZE PROTOCOL", command=self.callback, font=("Orbitron", 16, "bold"), fg_color="#00fbff", text_color="#000", height=60, hover_color="#007a7a")
        self.start_btn.pack(fill="x")

        self.bottom_bar = ctk.CTkFrame(self, height=120, fg_color="transparent")
        self.bottom_bar.grid(row=1, column=0, columnspan=3, sticky="ew", padx=40, pady=(0, 20))

        self.wave_canvas = ctk.CTkCanvas(self.bottom_bar, height=100, bg="#010101", highlightthickness=0)
        self.wave_canvas.pack(fill="x")

    def draw_hud_accents(self):
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        for i in range(0, w, 80):
            for j in range(0, h, 80):
                self.canvas_bg.create_oval(i, j, i+1, j+1, fill="#151515")
        
        self.canvas_bg.create_line(40, 40, 140, 40, fill="#00fbff", width=2)
        self.canvas_bg.create_line(40, 40, 40, 140, fill="#00fbff", width=2)
        self.canvas_bg.create_line(w-40, 40, w-140, 40, fill="#00fbff", width=2)
        self.canvas_bg.create_line(w-40, 40, w-40, 140, fill="#00fbff", width=2)

    def create_telemetry_unit(self, title, name):
        frame = ctk.CTkFrame(self.left_sidebar, fg_color="transparent")
        frame.pack(fill="x", pady=15)
        
        lbl = ctk.CTkLabel(frame, text=title, font=("Orbitron", 10), text_color="#007a7a")
        lbl.pack(anchor="w")
        
        pbar = ctk.CTkProgressBar(frame, progress_color="#00fbff", fg_color="#050505", height=6)
        pbar.set(0)
        pbar.pack(fill="x", pady=5)
        setattr(self, f"bar_{name}", pbar)
        
        val = ctk.CTkLabel(frame, text="0.0%", font=("Consolas", 14), text_color="#00fbff")
        val.pack(anchor="e")
        setattr(self, f"val_{name}", val)

    def draw_reactor(self):
        self.core_canvas.delete("reactor")
        cx, cy = 300, 300
        
        self.rotation_angle += 1
        
        for i in range(12):
            ang = math.radians(i * 30 + self.rotation_angle)
            x1, y1 = cx + math.cos(ang) * 190, cy + math.sin(ang) * 190
            x2, y2 = cx + math.cos(ang) * 230, cy + math.sin(ang) * 230
            self.core_canvas.create_line(x1, y1, x2, y2, fill="#003333", width=2, tags="reactor")

        self.core_canvas.create_oval(cx-160, cy-160, cx+160, cy+160, outline="#00fbff", width=1, dash=(8, 8), tags="reactor")
        
        r_ang = math.radians(-self.rotation_angle * 2.5)
        self.core_canvas.create_arc(cx-140, cy-140, cx+140, cy+140, start=math.degrees(r_ang), extent=45, outline="#00fbff", width=5, style="arc", tags="reactor")
        self.core_canvas.create_arc(cx-140, cy-140, cx+140, cy+140, start=math.degrees(r_ang)+180, extent=45, outline="#00fbff", width=5, style="arc", tags="reactor")

        self.glow_alpha += self.glow_direction * 3
        if self.glow_alpha > 220 or self.glow_alpha < 40: self.glow_direction *= -1
        color = f"#{0:02x}{self.glow_alpha:02x}{self.glow_alpha:02x}"
        
        self.core_canvas.create_oval(cx-90, cy-90, cx+90, cy+90, fill=color, outline="#00fbff", width=1, tags="reactor")
        self.core_canvas.create_oval(cx-25, cy-25, cx+25, cy+25, fill="#00fbff", tags="reactor")

    def animate_wave(self):
        self.wave_canvas.delete("wave")
        w = self.winfo_screenwidth()
        h = 50
        points = []
        self.wave_offset += 0.25
        
        for x in range(0, w + 20, 20):
            y = h + math.sin(x * 0.01 + self.wave_offset) * 25
            points.extend([x, y])
            
        self.wave_canvas.create_line(points, fill="#00fbff", width=2, smooth=True, tags="wave")

    def update_telemetry(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        self.bar_cpu.set(cpu/100)
        self.val_cpu.configure(text=f"{cpu}%")
        self.bar_ram.set(ram/100)
        self.val_ram.configure(text=f"{ram}%")
        self.bar_disk.set(disk/100)
        self.val_disk.configure(text=f"{disk}%")
        self.val_net.configure(text=f"{random.randint(8, 32)} MS")

    def terminal_log(self, text):
        ts = datetime.datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"[{ts}] » {text}\n")
        self.console.see("end")

    def run_animations(self):
        self.draw_reactor()
        self.animate_wave()
        if int(time.time() * 10) % 5 == 0:
            self.update_telemetry()
        self.after(30, self.run_animations)

    def update_status(self, text, color="#00fbff"):
        self.status_header.configure(text=text, text_color=color)

if __name__ == "__main__":
    def dummy(): pass
    app = JarvisUI(dummy)
    app.bind("<Escape>", lambda e: app.destroy())
    app.mainloop()