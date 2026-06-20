import customtkinter as ctk
import psutil
import math
import time
import datetime

class JarvisUI(ctk.CTk):
    def __init__(self, start_callback):
        super().__init__()

        self.title("J.A.R.V.I.S. - Advanced Reactive Virtual Interface System")
        self.attributes("-fullscreen", True)
        self.configure(fg_color="#020202") 
        ctk.set_appearance_mode("dark")

        self.start_time = time.time()

        self.top_bar = ctk.CTkFrame(self, fg_color="transparent", height=50)
        self.top_bar.pack(fill="x", side="top", padx=40, pady=20)
        
        self.clock_label = ctk.CTkLabel(self.top_bar, text="", font=("Orbitron", 18), text_color="#00fbff")
        self.clock_label.pack(side="right")
        
        self.coord_label = ctk.CTkLabel(self.top_bar, text="LOCATION: ENCRYPTED | SECTOR: 7-G", 
                                        font=("Consolas", 14), text_color="#007a7a")
        self.coord_label.pack(side="left")

        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True)

        self.main_container.grid_columnconfigure((0, 2), weight=1)
        self.main_container.grid_columnconfigure(1, weight=2)
        self.main_container.grid_rowconfigure(0, weight=1)

        self.left_panel = ctk.CTkFrame(self.main_container, fg_color="#080808", border_width=1, border_color="#00fbff")
        self.left_panel.grid(row=0, column=0, padx=30, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.left_panel, text="SYSTEM VITALS", font=("Orbitron", 16, "bold"), text_color="#00fbff").pack(pady=20)
        
        self.create_vital_meter("CPU LOAD", "cpu")
        self.create_vital_meter("MEMORY ALLOC", "ram")
        self.create_vital_meter("DISK CAPACITY", "disk")
        self.create_vital_meter("NETWORK LOAD", "net")

        self.center_panel = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.center_panel.grid(row=0, column=1, sticky="nsew")

        self.canvas = ctk.CTkCanvas(self.center_panel, width=600, height=600, bg="#020202", highlightthickness=0)
        self.canvas.pack(pady=40)
        
        self.draw_hex_grid()
        
        self.ring_outer = self.canvas.create_oval(50, 50, 550, 550, outline="#003333", width=1, dash=(10, 10))
        self.ring_middle = self.canvas.create_oval(100, 100, 500, 500, outline="#00fbff", width=2)
        self.ring_inner = self.canvas.create_oval(180, 180, 420, 420, outline="#007a7a", width=12)
        
        self.core_dot = self.canvas.create_oval(290, 290, 310, 310, fill="#00fbff")
        
        self.angle = 0
        self.animate_hud()

        self.right_panel = ctk.CTkFrame(self.main_container, fg_color="#080808", border_width=1, border_color="#00fbff")
        self.right_panel.grid(row=0, column=2, padx=30, pady=20, sticky="nsew")

        self.status_label = ctk.CTkLabel(self.right_panel, text="[ STANDBY ]", font=("Orbitron", 24, "bold"), text_color="#00fbff")
        self.status_label.pack(pady=40)

        ctk.CTkLabel(self.right_panel, text="MANUAL OVERRIDE", font=("Consolas", 12), text_color="#007a7a").pack()
        self.pass_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Passcode Required...", show="*", 
                                       fg_color="#000", border_color="#00fbff", height=40, font=("Consolas", 14))
        self.pass_entry.pack(pady=20, padx=30, fill="x")

        self.start_btn = ctk.CTkButton(self.right_panel, text="INITIALIZE PROTOCOL", command=start_callback, 
                                       font=("Orbitron", 14, "bold"), fg_color="#00fbff", text_color="black", height=60)
        self.start_btn.pack(side="bottom", pady=60, padx=30, fill="x")

        self.bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.bottom_frame.pack(fill="x", side="bottom", padx=30, pady=20)

        self.console = ctk.CTkTextbox(self.bottom_frame, height=140, font=("Consolas", 13), 
                                      fg_color="#050505", text_color="#00fbff", border_color="#007a7a", border_width=1)
        self.console.pack(fill="x")
        
        self.terminal_log("A.R.C.H.E.R. OS v4.0.0 HYPER-DRIVE SECURE BOOT SUCCESSFUL...")

    def draw_hex_grid(self):
        """Draws a subtle hexagon background pattern behind the reactor"""
        for i in range(0, 600, 50):
            for j in range(0, 600, 50):
                self.canvas.create_polygon(
                    i, j, 
                    i+25, j-15, 
                    i+50, j, 
                    i+50, j+30, 
                    i+25, j+45, 
                    i, j+30, 
                    outline="#080808", 
                    fill="" 
                )

    def create_vital_meter(self, label_text, attr_name):
        """Helper to create progress-bar style vital meters"""
        lbl = ctk.CTkLabel(self.left_panel, text=label_text, font=("Consolas", 12), text_color="#007a7a")
        lbl.pack(pady=(25, 0), padx=30, anchor="w")
        
        pbar = ctk.CTkProgressBar(self.left_panel, progress_color="#00fbff", fg_color="#121212", height=10)
        pbar.set(0)
        pbar.pack(fill="x", padx=30, pady=5)
        setattr(self, f"{attr_name}_bar", pbar)
        
        val_lbl = ctk.CTkLabel(self.left_panel, text="0%", font=("Orbitron", 14), text_color="#00fbff")
        val_lbl.pack(padx=30, anchor="e")
        setattr(self, f"{attr_name}_val", val_lbl)

    def animate_hud(self):
        """Infinite loop for the pulsing core and real-time system monitoring"""
        self.angle += 2
        
        pulse_val = (math.sin(self.angle/12) + 1) * 127
        pulse_color = f"#{int(pulse_val):02x}fbff"
        self.canvas.itemconfig(self.ring_middle, outline=pulse_color)
        
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        disk = psutil.disk_usage('/').percent
        
        self.cpu_bar.set(cpu / 100)
        self.cpu_val.configure(text=f"{cpu}%")
        self.ram_bar.set(ram / 100)
        self.ram_val.configure(text=f"{ram}%")
        self.disk_bar.set(disk / 100)
        self.disk_val.configure(text=f"{disk}%")
        
        now = datetime.datetime.now().strftime("%H:%M:%S")
        uptime = int(time.time() - self.start_time)
        self.clock_label.configure(text=f"SYS TIME: {now} | UPTIME: {uptime}s")

        self.after(50, self.animate_hud)

    def terminal_log(self, text):
        """Adds a line to the console with a timestamp"""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"\n[{timestamp}] >>> {text}")
        self.console.see("end")
        self.update_idletasks()