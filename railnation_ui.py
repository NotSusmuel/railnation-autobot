import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
from datetime import datetime

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False
    print("Warning: pyautogui not found. Install it with: pip install pyautogui")
    print("The UI will work but bot functionality will be limited.")

class RailnationBotUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Railnation Autobot - Modern UI")
        self.root.geometry("800x600")
        self.root.configure(bg="#1e1e2e")
        
        # Bot state
        self.running = False
        self.bot_thread = None
        
        # Configuration variables
        self.video_wait_time = tk.IntVar(value=60)
        self.check_interval = tk.IntVar(value=1)
        self.click_delay = tk.IntVar(value=2)
        
        self.setup_ui()
        self.setup_keyboard_shortcuts()
        
    def setup_ui(self):
        # Title bar
        title_frame = tk.Frame(self.root, bg="#89b4fa", height=60)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="🚂 Railnation Autobot",
            font=("Segoe UI", 20, "bold"),
            bg="#89b4fa",
            fg="#1e1e2e"
        )
        title_label.pack(pady=15)
        
        # Main container
        main_container = tk.Frame(self.root, bg="#1e1e2e")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left panel - Controls
        left_panel = tk.Frame(main_container, bg="#313244", width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Control buttons section
        control_label = tk.Label(
            left_panel,
            text="Controls",
            font=("Segoe UI", 14, "bold"),
            bg="#313244",
            fg="#cdd6f4"
        )
        control_label.pack(pady=(20, 10))
        
        # Start button
        self.start_button = tk.Button(
            left_panel,
            text="▶ START (F5)",
            font=("Segoe UI", 12, "bold"),
            bg="#a6e3a1",
            fg="#1e1e2e",
            activebackground="#94d2a1",
            activeforeground="#1e1e2e",
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            command=self.start_bot
        )
        self.start_button.pack(fill=tk.X, padx=20, pady=5)
        
        # Stop button
        self.stop_button = tk.Button(
            left_panel,
            text="⏹ STOP (F6)",
            font=("Segoe UI", 12, "bold"),
            bg="#f38ba8",
            fg="#1e1e2e",
            activebackground="#e38ba8",
            activeforeground="#1e1e2e",
            relief=tk.FLAT,
            cursor="hand2",
            height=2,
            state=tk.DISABLED,
            command=self.stop_bot
        )
        self.stop_button.pack(fill=tk.X, padx=20, pady=5)
        
        # Settings section
        settings_label = tk.Label(
            left_panel,
            text="Settings",
            font=("Segoe UI", 14, "bold"),
            bg="#313244",
            fg="#cdd6f4"
        )
        settings_label.pack(pady=(30, 10))
        
        # Video wait time setting
        self.create_setting(
            left_panel,
            "Video Wait Time (seconds):",
            self.video_wait_time,
            1,
            120
        )
        
        # Check interval setting
        self.create_setting(
            left_panel,
            "Check Interval (seconds):",
            self.check_interval,
            1,
            10
        )
        
        # Click delay setting
        self.create_setting(
            left_panel,
            "Click Delay (seconds):",
            self.click_delay,
            1,
            10
        )
        
        # Status indicator
        self.status_frame = tk.Frame(left_panel, bg="#313244")
        self.status_frame.pack(pady=(30, 10))
        
        tk.Label(
            self.status_frame,
            text="Status:",
            font=("Segoe UI", 11, "bold"),
            bg="#313244",
            fg="#cdd6f4"
        ).pack()
        
        self.status_label = tk.Label(
            self.status_frame,
            text="● Stopped",
            font=("Segoe UI", 11),
            bg="#313244",
            fg="#f38ba8"
        )
        self.status_label.pack()
        
        # Right panel - Log
        right_panel = tk.Frame(main_container, bg="#313244")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        log_label = tk.Label(
            right_panel,
            text="Activity Log",
            font=("Segoe UI", 14, "bold"),
            bg="#313244",
            fg="#cdd6f4"
        )
        log_label.pack(pady=(20, 10))
        
        # Log text area
        self.log_text = scrolledtext.ScrolledText(
            right_panel,
            font=("Consolas", 9),
            bg="#1e1e2e",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief=tk.FLAT,
            wrap=tk.WORD
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
        # Clear log button
        clear_button = tk.Button(
            right_panel,
            text="Clear Log",
            font=("Segoe UI", 9),
            bg="#45475a",
            fg="#cdd6f4",
            activebackground="#585b70",
            activeforeground="#cdd6f4",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.clear_log
        )
        clear_button.pack(pady=(0, 20))
        
    def create_setting(self, parent, label_text, variable, min_val, max_val):
        frame = tk.Frame(parent, bg="#313244")
        frame.pack(fill=tk.X, padx=20, pady=5)
        
        label = tk.Label(
            frame,
            text=label_text,
            font=("Segoe UI", 9),
            bg="#313244",
            fg="#cdd6f4"
        )
        label.pack(anchor=tk.W)
        
        control_frame = tk.Frame(frame, bg="#313244")
        control_frame.pack(fill=tk.X, pady=(5, 0))
        
        scale = tk.Scale(
            control_frame,
            from_=min_val,
            to=max_val,
            orient=tk.HORIZONTAL,
            variable=variable,
            bg="#45475a",
            fg="#cdd6f4",
            highlightthickness=0,
            troughcolor="#1e1e2e",
            activebackground="#89b4fa",
            relief=tk.FLAT
        )
        scale.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        value_label = tk.Label(
            control_frame,
            textvariable=variable,
            font=("Segoe UI", 9, "bold"),
            bg="#313244",
            fg="#89b4fa",
            width=4
        )
        value_label.pack(side=tk.RIGHT, padx=(10, 0))
        
    def setup_keyboard_shortcuts(self):
        self.root.bind('<F5>', lambda e: self.start_bot())
        self.root.bind('<F6>', lambda e: self.stop_bot())
        
    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        self.log("Log cleared.")
        
    def start_bot(self):
        if not PYAUTOGUI_AVAILABLE:
            self.log("ERROR: pyautogui is not installed!")
            self.log("Install it with: pip install pyautogui")
            return
            
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.status_label.config(text="● Running", fg="#a6e3a1")
            self.log("Bot started!")
            
            # Start bot in separate thread
            self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
            self.bot_thread.start()
            
    def stop_bot(self):
        if self.running:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_label.config(text="● Stopped", fg="#f38ba8")
            self.log("Bot stopped!")
            
    def run_bot(self):
        """Main bot loop - adapted from original script"""
        if not PYAUTOGUI_AVAILABLE:
            self.log("ERROR: Cannot run bot without pyautogui!")
            self.stop_bot()
            return
            
        video_wait = self.video_wait_time.get()
        check_interval = self.check_interval.get()
        click_delay = self.click_delay.get()
        
        while self.running:
            try:
                # Look for ad symbol
                adsymbol = None
                try:
                    adsymbol = pyautogui.locateOnScreen("images/adsymbol.png", confidence=0.8)
                    if not adsymbol:
                        adsymbol = pyautogui.locateOnScreen("images/adsymbol2.png", confidence=0.8)
                except pyautogui.ImageNotFoundException:
                    self.log("Ad-Symbol nicht gefunden, suche nach Collectmoney-Symbol.")
                    adsymbol = None
                    
                    # Look for collect money symbol
                    collectmoney = None
                    try:
                        collectmoney = pyautogui.locateOnScreen("images/collectmoney.png")
                        if not collectmoney:
                            collectmoney = pyautogui.locateOnScreen("images/collectmoney2.png", confidence=0.7)
                    except pyautogui.ImageNotFoundException:
                        self.log("Collectmoney-Symbol nicht gefunden, suche nach der nächsten Seite.")
                        collectmoney = None
                        if self.nextpage():
                            self.log("Nächste Seite gefunden und geklickt.")
                            time.sleep(click_delay)
                            continue
                            
                if adsymbol:
                    self.log("Ad-Symbol gefunden.")
                    pyautogui.click(adsymbol)
                    time.sleep(click_delay)
                    
                    if self.playvideo():
                        self.log("Video gestartet")
                        for _ in range(video_wait):
                            if not self.running:
                                break
                            if self.sonderbonus():
                                self.log("Sonderbonus gefunden und geklickt.")
                                break
                            else:
                                self.log(f"Versuch {_+1}/{video_wait}")
                            time.sleep(check_interval)
                            if _ == video_wait - 1:
                                self.log("Sonderbonus nicht gefunden, fehlerbehebung wird ausgeführt.")
                                self.fehlerbehebung()
                                
                        time.sleep(click_delay)
                        if self.playvideo():
                            self.log("Sonderbonusvideo gestartet")
                            for _ in range(video_wait):
                                if not self.running:
                                    break
                                if self.closesondermenu() or self.redeem():
                                    self.log("Sonderbonusvideo erfolgreich geschlossen oder eingelöst.")
                                    break
                                else:
                                    self.log(f"Versuch {_+1}/{video_wait}")
                                time.sleep(check_interval)
                                if _ == video_wait - 1:
                                    self.log("Sonderbonusvideo nicht geschlossen, fehlerbehebung wird ausgeführt.")
                                    self.fehlerbehebung()
                                    
                elif collectmoney:
                    self.log("Collectmoney-Symbol gefunden.")
                    pyautogui.click(collectmoney)
                    time.sleep(click_delay)
                    continue
                    
                time.sleep(check_interval)
                
            except Exception as e:
                self.log(f"Fehler: {str(e)}")
                time.sleep(check_interval)
                
    # Bot functions from original script
    def nextpage(self):
        try:
            nextpage = pyautogui.locateOnScreen("images/nextpage.png", confidence=0.9)
        except pyautogui.ImageNotFoundException:
            nextpage = None
            
        if nextpage:
            pyautogui.click(nextpage)
            return True
        else:
            self.log("Nächste Seite nicht gefunden.")
            return False
            
    def playvideo(self):
        try:
            playbutton = pyautogui.locateOnScreen("images/playsymbol.png", confidence=0.8)
        except pyautogui.ImageNotFoundException:
            playbutton = None
            
        if playbutton:
            pyautogui.click(playbutton)
            return True
        else:
            self.log("Play-Button nicht gefunden.")
            return False
            
    def sonderbonus(self):
        try:
            sonderbonus = pyautogui.locateOnScreen("images/sonderbonus.png", confidence=0.8)
        except pyautogui.ImageNotFoundException:
            sonderbonus = None
            
        if sonderbonus:
            pyautogui.click(sonderbonus)
            return True
        else:
            return False
            
    def closesondermenu(self):
        try:
            closesondermenu = pyautogui.locateOnScreen("images/closesondermenu.png", confidence=0.8)
        except pyautogui.ImageNotFoundException:
            closesondermenu = None
            
        if closesondermenu:
            pyautogui.click(closesondermenu)
            return True
        else:
            return False
            
    def redeem(self):
        try:
            redeem = pyautogui.locateOnScreen("images/redeem.png", confidence=0.8)
        except pyautogui.ImageNotFoundException:
            redeem = None
            
        if redeem:
            pyautogui.click(redeem)
            return True
        else:
            return False
            
    def closeadmenu(self):
        try:
            closeadmenu = pyautogui.locateOnScreen("images/closeadmenu.png", confidence=0.8)
        except pyautogui.ImageNotFoundException:
            closeadmenu = None
            
        if closeadmenu:
            pyautogui.click(closeadmenu)
        else:
            self.log("Schließen-Symbol nicht gefunden.")
            
        try:
            closeadmenu2 = pyautogui.locateOnScreen("images/abbrechen.png")
        except pyautogui.ImageNotFoundException:
            closeadmenu2 = None
            
        if closeadmenu2:
            pyautogui.click(closeadmenu2)
        else:
            self.log("Abbrechen-Symbol nicht gefunden.")
            
    def fehlerbehebung(self):
        self.log("Führe Fehlerbehebung aus...")
        self.closeadmenu()
        self.closesondermenu()
        self.redeem()
        self.nextpage()
        self.playvideo()
        self.sonderbonus()

def main():
    root = tk.Tk()
    app = RailnationBotUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
