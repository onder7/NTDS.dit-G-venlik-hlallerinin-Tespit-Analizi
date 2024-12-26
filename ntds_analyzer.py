import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog, Menu
import subprocess
import datetime
import threading
import re
from datetime import datetime, timedelta
import os
import webbrowser
import sys

class AboutWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Hakkında")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Program bilgileri
        info_frame = ttk.Frame(self, padding="20")
        info_frame.pack(fill=tk.BOTH, expand=True)
        
        # Logo veya başlık
        ttk.Label(info_frame, text="NTDS.dit Analiz Aracı", 
                 font=('Helvetica', 14, 'bold')).pack(pady=10)
        
        # Versiyon
        ttk.Label(info_frame, text="Versiyon 1.0.0", 
                 font=('Helvetica', 10)).pack(pady=5)
        
        # Açıklama
        description = """
        Bu uygulama NTDS.dit dosyasının adli analizi için geliştirilmiş 
        bir araçtır. Windows Event Log analizi ve şüpheli dosya tespiti 
        yaparak güvenlik incelemelerinde kullanılmak üzere tasarlanmıştır.
        """
        desc_label = ttk.Label(info_frame, text=description, wraplength=350, 
                             justify="center")
        desc_label.pack(pady=10)
        
        # Geliştirici bilgileri
        dev_frame = ttk.Frame(info_frame)
        dev_frame.pack(pady=10)
        
        ttk.Label(dev_frame, text="Geliştirici: Önder Aköz",
                 font=('Helvetica', 10, 'bold')).pack()
        
        # İletişim bilgileri için frame
        contact_frame = ttk.Frame(info_frame)
        contact_frame.pack(pady=5)
        
        # Website linki
        website_link = ttk.Label(contact_frame, text="ondernet.net",
                               foreground="blue", cursor="hand2")
        website_link.pack()
        website_link.bind("<Button-1>", 
                         lambda e: webbrowser.open("http://ondernet.net"))
        
        # Email linki
        email_link = ttk.Label(contact_frame, text="onder7@gmail.com",
                              foreground="blue", cursor="hand2")
        email_link.pack()
        email_link.bind("<Button-1>", 
                       lambda e: webbrowser.open("mailto:onder7@gmail.com"))
        
        # Kapat butonu
        ttk.Button(info_frame, text="Kapat", 
                  command=self.destroy).pack(pady=10)

class NTDSAnalyzer(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("NTDS.dit Analysis Tool")
        self.geometry("1000x800")
        
        # Menü çubuğunu oluştur
        self.create_menu()
        
        # Varsayılan dizini ayarla
        self.ntds_path = ""
        
        # Arayüz bileşenleri
        self.create_widgets()
        
        # Olay kimliklerini tanımla
        self.event_ids = {
            "327": "Database Engine detached database",
            "326": "Database Engine attached database",
            "325": "Database Engine created new database",
            "216": "Database location change detected"
        }
        
        self.suspicious_files = []

    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)
        
        # Dosya menüsü
        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Dosya", menu=file_menu)
        file_menu.add_command(label="NTDS.dit Seç", command=self.browse_file)
        file_menu.add_separator()
        file_menu.add_command(label="Çıkış", command=self.quit)
        
        # Analiz menüsü
        analysis_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Analiz", menu=analysis_menu)
        analysis_menu.add_command(label="Analizi Başlat", command=self.start_analysis)
        analysis_menu.add_command(label="Rapor Oluştur", command=self.generate_report)
        analysis_menu.add_command(label="Temizle", command=self.clear_results)
        
        # Yardım menüsü
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Yardım", menu=help_menu)
        help_menu.add_command(label="Hakkında", command=self.show_about)

    def show_about(self):
        AboutWindow(self)

    def create_widgets(self):
        # Ana frame
        main_frame = ttk.Frame(self)
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # NTDS.dit dosya seçici
        file_frame = ttk.LabelFrame(main_frame, text="NTDS.dit Dosya Konumu")
        file_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.path_var = tk.StringVar()
        path_entry = ttk.Entry(file_frame, textvariable=self.path_var, width=70)
        path_entry.pack(side=tk.LEFT, padx=5, pady=5, fill=tk.X, expand=True)
        
        ttk.Button(file_frame, text="Gözat", command=self.browse_file).pack(side=tk.LEFT, padx=5, pady=5)

        # Kontrol paneli
        control_frame = ttk.LabelFrame(main_frame, text="Kontrol Paneli")
        control_frame.pack(fill=tk.X, padx=5, pady=5)

        # Tarih seçici
        date_frame = ttk.Frame(control_frame)
        date_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(date_frame, text="Başlangıç Tarihi:").pack(side=tk.LEFT, padx=5)
        self.start_date = ttk.Entry(date_frame, width=20)
        self.start_date.pack(side=tk.LEFT, padx=5)
        self.start_date.insert(0, (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
        
        ttk.Label(date_frame, text="Bitiş Tarihi:").pack(side=tk.LEFT, padx=5)
        self.end_date = ttk.Entry(date_frame, width=20)
        self.end_date.pack(side=tk.LEFT, padx=5)
        self.end_date.insert(0, datetime.now().strftime('%Y-%m-%d'))

        # Butonlar
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="Analizi Başlat", command=self.start_analysis).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Rapor Oluştur", command=self.generate_report).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Temizle", command=self.clear_results).pack(side=tk.LEFT, padx=5)

        # Sonuçlar için notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Olay günlükleri sekmesi
        self.event_text = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.notebook.add(self.event_text, text="Olay Günlükleri")

        # Şüpheli dosyalar sekmesi
        self.file_text = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.notebook.add(self.file_text, text="Şüpheli Dosyalar")

        # NTDS.dit analiz sonuçları sekmesi
        self.ntds_text = scrolledtext.ScrolledText(self.notebook, wrap=tk.WORD)
        self.notebook.add(self.ntds_text, text="NTDS.dit Analizi")

        # Durum çubuğu
        self.status_var = tk.StringVar()
        self.status_var.set("Hazır")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, padx=5, pady=5)

    def browse_file(self):
        filename = filedialog.askopenfilename(
            title="NTDS.dit Dosyasını Seç",
            filetypes=(("DIT files", "*.dit"), ("All files", "*.*"))
        )
        if filename:
            self.ntds_path = filename
            self.path_var.set(filename)

    def analyze_ntds(self):
        if not self.ntds_path:
            messagebox.showwarning("Uyarı", "Lütfen NTDS.dit dosyasını seçin!")
            return False
            
        try:
            # NTDS.dit dosyasının temel özelliklerini al
            file_stats = os.stat(self.ntds_path)
            
            self.ntds_text.insert(tk.END, "=== NTDS.dit Dosya Analizi ===\n\n")
            self.ntds_text.insert(tk.END, f"Dosya Konumu: {self.ntds_path}\n")
            self.ntds_text.insert(tk.END, f"Dosya Boyutu: {file_stats.st_size / (1024*1024):.2f} MB\n")
            self.ntds_text.insert(tk.END, f"Son Değiştirilme: {datetime.fromtimestamp(file_stats.st_mtime)}\n")
            self.ntds_text.insert(tk.END, f"Son Erişim: {datetime.fromtimestamp(file_stats.st_atime)}\n")
            self.ntds_text.insert(tk.END, f"Oluşturulma: {datetime.fromtimestamp(file_stats.st_ctime)}\n\n")
            
            return True
            
        except Exception as e:
            messagebox.showerror("Hata", f"NTDS.dit analizi sırasında hata oluştu: {str(e)}")
            return False

    def get_event_logs(self):
        try:
            start = datetime.strptime(self.start_date.get(), '%Y-%m-%d')
            end = datetime.strptime(self.end_date.get(), '%Y-%m-%d')
            
            ps_command = f'''
            $startDate = "{start.strftime('%Y-%m-%d')}"
            $endDate = "{end.strftime('%Y-%m-%d')}"
            Get-WinEvent -FilterHashtable @{{
                LogName = 'Application'
                ProviderName = 'ESENT'
                ID = @(216, 325, 326, 327)
                StartTime = $startDate
                EndTime = $endDate
            }} | Select-Object TimeCreated, Id, Message | Sort-Object TimeCreated
            '''
            
            process = subprocess.Popen(
                ['powershell', '-Command', ps_command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output, error = process.communicate()
            
            return output.decode('utf-8')
            
        except Exception as e:
            messagebox.showerror("Hata", f"Olay günlükleri alınırken hata oluştu: {str(e)}")
            return None

    def scan_suspicious_files(self):
        try:
            ps_command = '''
            Get-ChildItem -Path $env:USERPROFILE\Desktop -Filter *.zip -Recurse | 
            Where-Object { $_.Length -gt 10MB } |
            Select-Object FullName, Length, CreationTime |
            Sort-Object CreationTime
            '''
            
            process = subprocess.Popen(
                ['powershell', '-Command', ps_command],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            output, error = process.communicate()
            
            return output.decode('utf-8')
            
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya taraması yapılırken hata oluştu: {str(e)}")
            return None

    def analyze_events(self, events_data):
        suspicious_patterns = []
        
        patterns = {
            'quick_detach_attach': r'(?s).*ID: 327.*?(?=.*ID: 326.*?){1}',
            'new_db_creation': r'ID: 325.*',
            'location_change': r'ID: 216.*'
        }
        
        for pattern_name, pattern in patterns.items():
            matches = re.finditer(pattern, events_data, re.MULTILINE)
            for match in matches:
                suspicious_patterns.append(f"Şüpheli Patern ({pattern_name}): {match.group()}")
                
        return suspicious_patterns

    def start_analysis(self):
        def analyze():
            self.status_var.set("Analiz yapılıyor...")
            self.event_text.delete(1.0, tk.END)
            self.file_text.delete(1.0, tk.END)
            self.ntds_text.delete(1.0, tk.END)
            
            if not self.analyze_ntds():
                self.status_var.set("NTDS.dit analizi başarısız")
                return
            
            events_data = self.get_event_logs()
            if events_data:
                self.event_text.insert(tk.END, "=== OLAY GÜNLÜĞÜ ANALİZİ ===\n\n")
                self.event_text.insert(tk.END, events_data)
                
                suspicious_patterns = self.analyze_events(events_data)
                if suspicious_patterns:
                    self.event_text.insert(tk.END, "\n=== ŞÜPHELİ PATERNLER ===\n\n")
                    for pattern in suspicious_patterns:
                        self.event_text.insert(tk.END, f"{pattern}\n")
            
            files_data = self.scan_suspicious_files()
            if files_data:
                self.file_text.insert(tk.END, "=== ŞÜPHELİ DOSYALAR ===\n\n")
                self.file_text.insert(tk.END, files_data)
            
            self.status_var.set("Analiz tamamlandı")

        # Analizi ayrı bir thread'de başlat
        threading.Thread(target=analyze, daemon=True).start()

    def generate_report(self):
        try:
            report_time = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"NTDS_Analysis_Report_{report_time}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("NTDS.dit Analiz Raporu\n")
                f.write("=" * 50 + "\n\n")
                
                f.write("NTDS.dit Analizi:\n")
                f.write("-" * 30 + "\n")
                f.write(self.ntds_text.get(1.0, tk.END))
                
                f.write("\nOlay Günlüğü Analizi:\n")
                f.write("-" * 30 + "\n")
                f.write(self.event_text.get(1.0, tk.END))
                
                f.write("\nŞüpheli Dosya Analizi:\n")
                f.write("-" * 30 + "\n")
                f.write(self.file_text.get(1.0, tk.END))
            
            messagebox.showinfo("Başarılı", f"Rapor oluşturuldu: {filename}")
            
        except Exception as e:
            messagebox.showerror("Hata", f"Rapor oluşturulurken hata oluştu: {str(e)}")

    def clear_results(self):
        self.event_text.delete(1.0, tk.END)
        self.file_text.delete(1.0, tk.END)
        self.ntds_text.delete(1.0, tk.END)
        self.status_var.set("Hazır")

if __name__ == "__main__":
    app = NTDSAnalyzer()
    app.mainloop()
