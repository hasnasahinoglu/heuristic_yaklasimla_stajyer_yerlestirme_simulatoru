# gui.py
import tkinter as tk
from tkinter import messagebox, ttk
import time
import os
import webbrowser

from settings import ModernTheme, JSON_DOSYA_ADI
from controller import YerlestirmeYonetici
from utils import generate_html_graph

class StajyerUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Stajyer Yerleştirme Sistemi - Modern Interface")
        self.root.geometry("1600x950")
        self.root.configure(bg=ModernTheme.BG_DARK)
        
        self.yonetici = YerlestirmeYonetici()
        self.yonetici.log_callback = self.log_yaz
        
        self.algoritma_secimi = tk.StringVar(value="Greedy")
        self.setup_styles()
        self.arayuz_olustur()

    def setup_styles(self):
        """Modern dark tema stilleri"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame stilleri
        style.configure('Dark.TFrame', background=ModernTheme.BG_DARK)
        style.configure('Card.TFrame', background=ModernTheme.BG_LIGHTER, relief='flat')
        
        # Label stilleri
        style.configure('Title.TLabel', 
                       background=ModernTheme.BG_DARK, 
                       foreground=ModernTheme.TEXT_PRIMARY,
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure('Subtitle.TLabel', 
                       background=ModernTheme.BG_LIGHTER, 
                       foreground=ModernTheme.TEXT_PRIMARY,
                       font=('Segoe UI', 11, 'bold'))
        
        style.configure('Info.TLabel', 
                       background=ModernTheme.BG_DARK,
                       foreground=ModernTheme.TEXT_SECONDARY,
                       font=('Segoe UI', 10))

    def create_modern_button(self, parent, text, command, bg_color, width=15):
        """Modern stil buton oluşturur"""
        btn = tk.Button(parent, text=text, command=command,
                       bg=bg_color, fg=ModernTheme.BG_DARK,
                       font=('Segoe UI', 10, 'bold'),
                       relief='flat', cursor='hand2',
                       padx=20, pady=10, width=width,
                       activebackground=bg_color,
                       activeforeground=ModernTheme.BG_DARK,
                       borderwidth=0)
        
        # Hover efekti
        def on_enter(e):
            btn['bg'] = self.lighten_color(bg_color, 1.2)
        def on_leave(e):
            btn['bg'] = bg_color
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        
        return btn
    
    def lighten_color(self, hex_color, factor):
        """Rengi açar"""
        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return f'#{r:02x}{g:02x}{b:02x}'

    def arayuz_olustur(self):
        # Ana container
        main_container = tk.Frame(self.root, bg=ModernTheme.BG_DARK)
        main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        # --- HEADER SECTION ---
        header_frame = tk.Frame(main_container, bg=ModernTheme.BG_LIGHTER, 
                               relief='flat', bd=0)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Başlık
        title_frame = tk.Frame(header_frame, bg=ModernTheme.BG_LIGHTER)
        title_frame.pack(fill=tk.X, padx=20, pady=15)
        
        tk.Label(title_frame, text="🎓 Stajyer Yerleştirme Sistemi",
                font=('Segoe UI', 20, 'bold'),
                bg=ModernTheme.BG_LIGHTER,
                fg=ModernTheme.ACCENT_PRIMARY).pack(side=tk.LEFT)
        
        # --- CONTROL PANEL ---
        control_frame = tk.Frame(main_container, bg=ModernTheme.BG_LIGHTER,
                                relief='flat', bd=0)
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        control_inner = tk.Frame(control_frame, bg=ModernTheme.BG_LIGHTER)
        control_inner.pack(fill=tk.X, padx=20, pady=20)
        
        # Sol: Butonlar
        btn_container = tk.Frame(control_inner, bg=ModernTheme.BG_LIGHTER)
        btn_container.pack(side=tk.LEFT, fill=tk.Y)
        
        self.btn_yukle = self.create_modern_button(
            btn_container, "📁 Veri Yükle", self.veri_yukle, 
            ModernTheme.BTN_INFO, width=12)
        self.btn_yukle.pack(side=tk.LEFT, padx=5)
        
        # Algoritma seçimi - Modern radio buttons
        algo_frame = tk.LabelFrame(control_inner, text=" Algoritma Seçimi ",
                                  bg=ModernTheme.BG_LIGHTER,
                                  fg=ModernTheme.TEXT_PRIMARY,
                                  font=('Segoe UI', 10, 'bold'),
                                  relief='flat', bd=2,
                                  highlightbackground=ModernTheme.BORDER,
                                  highlightthickness=1)
        algo_frame.pack(side=tk.LEFT, padx=20, pady=5)
        
        rb1 = tk.Radiobutton(algo_frame, text="⚡ Greedy (Açgözlü)",
                            variable=self.algoritma_secimi, value="Greedy",
                            bg=ModernTheme.BG_LIGHTER, fg=ModernTheme.TEXT_PRIMARY,
                            selectcolor=ModernTheme.BG_DARK,
                            font=('Segoe UI', 10),
                            activebackground=ModernTheme.BG_LIGHTER,
                            activeforeground=ModernTheme.TEXT_PRIMARY,
                            relief='flat')
        rb1.pack(anchor='w', padx=10, pady=5)
        
        rb2 = tk.Radiobutton(algo_frame, text="🧠 Heuristic (Beam Search)",
                            variable=self.algoritma_secimi, value="Heuristic",
                            bg=ModernTheme.BG_LIGHTER, fg=ModernTheme.TEXT_PRIMARY,
                            selectcolor=ModernTheme.BG_DARK,
                            font=('Segoe UI', 10),
                            activebackground=ModernTheme.BG_LIGHTER,
                            activeforeground=ModernTheme.TEXT_PRIMARY,
                            relief='flat')
        rb2.pack(anchor='w', padx=10, pady=5)
        
        # Action butonları
        action_frame = tk.Frame(control_inner, bg=ModernTheme.BG_LIGHTER)
        action_frame.pack(side=tk.LEFT, padx=20)
        
        self.btn_baslat = self.create_modern_button(
            action_frame, "🔄 Sıfırla & Başlat", self.simulasyonu_baslat,
            ModernTheme.BTN_SUCCESS, width=15)
        self.btn_baslat.pack(side=tk.LEFT, padx=5)
        self.btn_baslat.config(state=tk.DISABLED)
        
        self.btn_adim = self.create_modern_button(
            action_frame, "▶ Sonraki İterasyon", self.sonraki_adim,
            ModernTheme.ACCENT_PRIMARY, width=15)
        self.btn_adim.pack(side=tk.LEFT, padx=5)
        self.btn_adim.config(state=tk.DISABLED)

        self.btn_auto = self.create_modern_button(
            action_frame, "⏩ Hızlı Bitir", self.otomatik_bitir,
            ModernTheme.BTN_DANGER, width=12)
        self.btn_auto.pack(side=tk.LEFT, padx=5)
        self.btn_auto.config(state=tk.DISABLED)

        
        self.btn_graph = self.create_modern_button(
            action_frame, "🌐 Graph Göster", self.graph_goster,
            ModernTheme.BTN_WARNING, width=12)
        self.btn_graph.pack(side=tk.LEFT, padx=5)
        self.btn_graph.config(state=tk.DISABLED)
        
        # Sağ: İstatistikler
        stats_container = tk.Frame(control_inner, bg=ModernTheme.BG_DARK,
                                  relief='flat', bd=2,
                                  highlightbackground=ModernTheme.BORDER,
                                  highlightthickness=1)
        stats_container.pack(side=tk.RIGHT, padx=10, fill=tk.Y)
        
        self.lbl_istatistik = tk.Label(stats_container, 
                                      text="⏳ Durum: Bekliyor...",
                                      bg=ModernTheme.BG_DARK,
                                      fg=ModernTheme.TEXT_PRIMARY,
                                      font=('Segoe UI', 11, 'bold'),
                                      padx=15, pady=10)
        self.lbl_istatistik.pack()
        
        self.lbl_sonuc_puan = tk.Label(stats_container, text="",
                                      bg=ModernTheme.BG_DARK,
                                      fg=ModernTheme.ACCENT_SUCCESS,
                                      font=('Segoe UI', 10, 'bold'),
                                      padx=15, pady=5)
        self.lbl_sonuc_puan.pack()
        
        self.lbl_sonuc_sure = tk.Label(stats_container, text="",
                                      bg=ModernTheme.BG_DARK,
                                      fg=ModernTheme.TEXT_SECONDARY,
                                      font=('Segoe UI', 9),
                                      padx=15, pady=5)
        self.lbl_sonuc_sure.pack()
        
        # --- MAIN CONTENT AREA ---
        content_frame = tk.Frame(main_container, bg=ModernTheme.BG_DARK)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sol Panel: Loglar ve Firma Durumu
        left_panel = tk.Frame(content_frame, bg=ModernTheme.BG_DARK)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 8))
        
        # Log Section
        log_card = tk.Frame(left_panel, bg=ModernTheme.BG_LIGHTER, relief='flat')
        log_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        log_header = tk.Frame(log_card, bg=ModernTheme.BG_LIGHTER)
        log_header.pack(fill=tk.X, padx=15, pady=10)
        tk.Label(log_header, text="📋 Sistem Logları",
                font=('Segoe UI', 12, 'bold'),
                bg=ModernTheme.BG_LIGHTER,
                fg=ModernTheme.TEXT_PRIMARY).pack(side=tk.LEFT)
        
        log_text_frame = tk.Frame(log_card, bg=ModernTheme.BG_LIGHTER)
        log_text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.txt_log = tk.Text(log_text_frame, 
                              bg=ModernTheme.BG_DARK,
                              fg=ModernTheme.TEXT_SECONDARY,
                              font=('Consolas', 9),
                              insertbackground=ModernTheme.ACCENT_PRIMARY,
                              relief='flat',
                              padx=10, pady=10)
        self.txt_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        log_scroll = tk.Scrollbar(log_text_frame, command=self.txt_log.yview)
        log_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_log.config(yscrollcommand=log_scroll.set)
        
        # Firma Durumu Section
        firma_card = tk.Frame(left_panel, bg=ModernTheme.BG_LIGHTER, relief='flat')
        firma_card.pack(fill=tk.BOTH, expand=True)
        
        firma_header = tk.Frame(firma_card, bg=ModernTheme.BG_LIGHTER)
        firma_header.pack(fill=tk.X, padx=15, pady=10)
        tk.Label(firma_header, text="🏢 Firma Kontenjan Durumu",
                font=('Segoe UI', 12, 'bold'),
                bg=ModernTheme.BG_LIGHTER,
                fg=ModernTheme.TEXT_PRIMARY).pack(side=tk.LEFT)
        
        firma_text_frame = tk.Frame(firma_card, bg=ModernTheme.BG_LIGHTER)
        firma_text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.txt_kontenjan = tk.Text(firma_text_frame,
                                    bg=ModernTheme.BG_DARK,
                                    fg=ModernTheme.TEXT_SECONDARY,
                                    font=('Consolas', 9),
                                    insertbackground=ModernTheme.ACCENT_PRIMARY,
                                    relief='flat',
                                    padx=10, pady=10)
        self.txt_kontenjan.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        firma_scroll = tk.Scrollbar(firma_text_frame, command=self.txt_kontenjan.yview)
        firma_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_kontenjan.config(yscrollcommand=firma_scroll.set)
        
        # Sağ Panel: Öğrenci Durumları
        right_panel = tk.Frame(content_frame, bg=ModernTheme.BG_DARK)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(8, 0))
        
        # Red Alanlar Section
        red_card = tk.Frame(right_panel, bg=ModernTheme.BG_LIGHTER, relief='flat')
        red_card.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        red_header = tk.Frame(red_card, bg=ModernTheme.BG_LIGHTER)
        red_header.pack(fill=tk.X, padx=15, pady=10)
        tk.Label(red_header, text="❌ Red Alanlar & Bekleyenler",
                font=('Segoe UI', 12, 'bold'),
                bg=ModernTheme.BG_LIGHTER,
                fg=ModernTheme.ACCENT_DANGER).pack(side=tk.LEFT)
        
        red_text_frame = tk.Frame(red_card, bg=ModernTheme.BG_LIGHTER)
        red_text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.txt_red_alanlar = tk.Text(red_text_frame,
                                      bg=ModernTheme.BG_DARK,
                                      fg=ModernTheme.TEXT_SECONDARY,
                                      font=('Consolas', 9),
                                      insertbackground=ModernTheme.ACCENT_PRIMARY,
                                      relief='flat',
                                      padx=10, pady=10)
        self.txt_red_alanlar.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        red_scroll = tk.Scrollbar(red_text_frame, command=self.txt_red_alanlar.yview)
        red_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_red_alanlar.config(yscrollcommand=red_scroll.set)
        
        # Yerleşenler Section
        yerlesen_card = tk.Frame(right_panel, bg=ModernTheme.BG_LIGHTER, relief='flat')
        yerlesen_card.pack(fill=tk.BOTH, expand=True)
        
        yerlesen_header = tk.Frame(yerlesen_card, bg=ModernTheme.BG_LIGHTER)
        yerlesen_header.pack(fill=tk.X, padx=15, pady=10)
        tk.Label(yerlesen_header, text="✅ Yerleşenler",
                font=('Segoe UI', 12, 'bold'),
                bg=ModernTheme.BG_LIGHTER,
                fg=ModernTheme.ACCENT_SUCCESS).pack(side=tk.LEFT)
        
        yerlesen_text_frame = tk.Frame(yerlesen_card, bg=ModernTheme.BG_LIGHTER)
        yerlesen_text_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        self.txt_yerlesen = tk.Text(yerlesen_text_frame,
                                    bg=ModernTheme.BG_DARK,
                                    fg=ModernTheme.TEXT_SECONDARY,
                                    font=('Consolas', 9),
                                    insertbackground=ModernTheme.ACCENT_PRIMARY,
                                    relief='flat',
                                    padx=10, pady=10)
        self.txt_yerlesen.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        yerlesen_scroll = tk.Scrollbar(yerlesen_text_frame, command=self.txt_yerlesen.yview)
        yerlesen_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.txt_yerlesen.config(yscrollcommand=yerlesen_scroll.set)

    def log_yaz(self, mesaj):
        self.txt_log.insert(tk.END, mesaj + "\n")
        self.txt_log.see(tk.END)

    def veri_yukle(self):
        if self.yonetici.veri_yukle():
            self.log_yaz("✓ Veri seti başarıyla yüklendi.")
            self.log_yaz(f"✓ {len(self.yonetici.ogrenciler)} Öğrenci, {len(self.yonetici.firmalar)} Firma yüklendi.")
            self.btn_baslat.config(state=tk.NORMAL)
            self.ekranlari_guncelle()
        else:
            messagebox.showerror("Hata", f"{JSON_DOSYA_ADI} dosyası bulunamadı!")

    def simulasyonu_baslat(self):
        tip = self.algoritma_secimi.get()
        self.txt_log.delete(1.0, tk.END)
        self.log_yaz(f"{'='*60}")
        self.log_yaz(f"  SİMÜLASYON BAŞLATILIYOR: {tip.upper()}")
        self.log_yaz(f"{'='*60}\n")
        
        self.lbl_sonuc_puan.config(text="")
        self.lbl_sonuc_sure.config(text="")
        
        if tip == "Greedy":
            self.yonetici.greedy_baslat()
            self.btn_graph.config(state=tk.DISABLED)
            baslik = f"{'Tur':<4} | {'Normal':^8} | {'Ek':^5} | {'Red':^5} | {'Toplam Yerleşen'}"
            self.log_yaz(baslik)
            self.log_yaz("-" * 60)
        else:
            self.yonetici.heuristic_baslat()
            self.btn_graph.config(state=tk.NORMAL)
        
        self.btn_adim.config(state=tk.NORMAL)
        self.btn_auto.config(state=tk.NORMAL)
        self.ekranlari_guncelle()

    def sonraki_adim(self):
        tip = self.algoritma_secimi.get()
        stats = None
        
        if tip == "Greedy":
            stats = self.yonetici.greedy_iterasyon_calistir()
        else:
            stats = self.yonetici.heuristic_iterasyon_calistir()
        
        if stats:
            yerlesen_toplam = self.yonetici.get_yerlesen_sayisi()
            satir = f"{stats['iterasyon']:<4} | {stats['normal']:^8} | {stats['ek']:^5} | {stats['red']:^5} | {yerlesen_toplam}"
            self.log_yaz(satir)
            self.ekranlari_guncelle()
            self.canli_skor_guncelle()
        
        yerlesemeyenler = self.yonetici.get_yerlesemeyenler()
        if not yerlesemeyenler or stats is None:
            self.bitis_islemleri()

    def otomatik_bitir(self):
        """Simülasyonu sonuna kadar otomatik çalıştırır"""
        # Butonları kilitle
        self.btn_adim.config(state=tk.DISABLED)
        self.btn_auto.config(state=tk.DISABLED)
        
        # ZAMANLAMAYI BURADA BAŞLAT
        self.yonetici.baslama_zamani = time.time()
        
        while True:
            tip = self.algoritma_secimi.get()
            stats = None
            
            # Seçilen algoritmaya göre adım at
            if tip == "Greedy":
                stats = self.yonetici.greedy_iterasyon_calistir()
            else:
                stats = self.yonetici.heuristic_iterasyon_calistir()
            
            # Eğer istatistik dönmediyse (algoritma tıkandıysa veya bittiyse) döngüyü kır
            if stats is None:
                break
            
            # Log ve Arayüz Güncelleme
            yerlesen_toplam = self.yonetici.get_yerlesen_sayisi()
            satir = f"{stats['iterasyon']:<4} | {stats['normal']:^8} | {stats['ek']:^5} | {stats['red']:^5} | {yerlesen_toplam}"
            self.log_yaz(satir)
            self.ekranlari_guncelle()
            self.canli_skor_guncelle()
            
            # Arayüzün donmaması için güncellemeye zorla
            self.root.update()
            
            # Eğer yerleşemeyen kalmadıysa döngüyü kır
            if not self.yonetici.get_yerlesemeyenler():
                break

        # ZAMANLAMAYI BURADA BİTİR
        self.yonetici.bitis_zamani = time.time()
        
        # Döngü bitti, bitiş işlemlerini çağır
        self.bitis_islemleri()

    def canli_skor_guncelle(self):
        res = self.yonetici.sonuclari_al()
        self.lbl_sonuc_puan.config(text=f"💯 Toplam: {res['toplam_memnuniyet']:.1f} puan")

    def bitis_islemleri(self):
        self.btn_adim.config(state=tk.DISABLED)
        self.btn_auto.config(state=tk.DISABLED)
        res = self.yonetici.sonuclari_al()
        
        self.lbl_sonuc_puan.config(text=f"💯 Toplam: {res['toplam_memnuniyet']:.1f} puan")
        
        # Süre gösterimi
        sure_text = f"{res['calisma_suresi']:.3f} sn" if res['calisma_suresi'] > 0 else "N/A (Manuel)"
        self.lbl_sonuc_sure.config(text=f"⏱️ Süre: {sure_text}")
        
        self.log_yaz("\n" + "="*60)
        self.log_yaz(f"  SİMÜLASYON SONUÇLARI ({self.algoritma_secimi.get()})")
        self.log_yaz("="*60)
        self.log_yaz(f" ▸ Toplam İterasyon    : {res['iterasyon_sayisi']}")
        self.log_yaz(f" ▸ Yerleşen / Toplam   : {res['yerlesen_sayisi']} / {len(self.yonetici.ogrenciler)}")
        self.log_yaz(f" ▸ Toplam Memnuniyet   : {res['toplam_memnuniyet']:.1f}")
        self.log_yaz(f" ▸ Ortalama Memnuniyet : {res['ortalama_memnuniyet']:.2f}")
        self.log_yaz(f" ▸ Çalışma Süresi      : {sure_text}")
        self.log_yaz("="*60)
        
        messagebox.showinfo("✅ Tamamlandı", "Simülasyon başarıyla tamamlandı!")
        
        if self.algoritma_secimi.get() == "Heuristic":
            self.graph_goster()

    def graph_goster(self):
        if self.yonetici.algoritma_tipi == "Heuristic" and self.yonetici.beam_states_history:
            generate_html_graph(self.yonetici.beam_states_history, self.yonetici.last_winner_state.id)
            self.log_yaz("✓ Graph HTML dosyası oluşturuldu: beam_simulation_example.html")
            try:
                webbrowser.open("file://" + os.path.realpath("beam_simulation_example.html"))
            except:
                pass

    def ekranlari_guncelle(self):
        yerlesen = self.yonetici.get_yerlesen_sayisi()
        toplam = len(self.yonetici.ogrenciler)
        self.lbl_istatistik.config(text=f"⏳ Tur: {self.yonetici.iterasyon_sayisi} | Yerleşen: {yerlesen}/{toplam}")
        
        # Firma Tablosu
        self.txt_kontenjan.delete(1.0, tk.END)
        # Müsait firmalar için yeşil renk tag'i
        self.txt_kontenjan.tag_config('musait', foreground=ModernTheme.ACCENT_SUCCESS)
        
        # Başlık Hizalama
        header = f"{'ID':<4} | {'D':^2} | {'Firma Adı':<20} | {'Dolu/Kot':^8} | {'Eşik':^5} | {'Yerleşenler'}\n"
        self.txt_kontenjan.insert(tk.END, header)
        self.txt_kontenjan.insert(tk.END, "─" * 100 + "\n")
        
        for f in self.yonetici.firmalar:
            ad = (f.ad[:18] + '..') if len(f.ad) > 20 else f.ad
            ratio = f"{f.doluluk}/{f.kontenjan}"
            ogrler = ", ".join([o.ad.split()[0] for o in f.yerlesen_ogrenciler])
            
            is_musait = f.musait_mi()
            durum_ikon = "🟢" if is_musait else "🔴"
            
            satir = f"[{f.id:^2}] | {durum_ikon} | {ad:<20} | {ratio:^8} | {f.esik_degeri:>4.0f}  | {ogrler}\n"
            
            if is_musait:
                self.txt_kontenjan.insert(tk.END, satir, 'musait')
            else:
                self.txt_kontenjan.insert(tk.END, satir)

        # Red Alanlar / Durum Tablosu
        self.txt_red_alanlar.delete(1.0, tk.END)
        self.txt_red_alanlar.insert(tk.END, f"{'Öğrenci':<18} {'GNO':<4} | {'Red / Durum (Eski)':<25} | {'Red Tercih Listesi'}\n")
        self.txt_red_alanlar.insert(tk.END, "─" * 90 + "\n")
        
        yerlesemeyenler = self.yonetici.get_yerlesemeyenler()
        yerlesemeyenler.sort(key=lambda x: x.gno, reverse=True)
        
        for o in yerlesemeyenler:
            if o.reddedildigi_firmalar:
                durum_txt = "🚫 " + ", ".join([f"F{k}({v:.0f})" for k,v in o.reddedildigi_firmalar.items()])
            else:
                durum_txt = "⏳ Bekliyor"

            yeni_rota = str(o.tercihler) if o.tercihler else "[]"
            
            self.txt_red_alanlar.insert(tk.END, f"{o.ad:<18} {o.gno:<4} | {durum_txt:<20} | {yeni_rota}\n")

        # Yerleşenler Tablosu
        self.txt_yerlesen.delete(1.0, tk.END)
        baslik = f"{'Öğrenci':<18} | {'Firma':<18} | {'Sıra':^4} | {'Tur':^3} | {'Ark':^3} | {'Puan':^5}\n"
        self.txt_yerlesen.insert(tk.END, baslik)
        self.txt_yerlesen.insert(tk.END, "─" * 70 + "\n")
        
        yerlesenler = [o for o in self.yonetici.ogrenciler if o.kalici_yerlesti]
        yerlesenler.sort(key=lambda x: x.yerlesilen_firma_id)
        
        for o in yerlesenler:
            f_ad = (o.yerlesilen_firma[:18]) if o.yerlesilen_firma else "?"
            
            ark_sayisi = 0
            for ark_id in o.arkadaslar:
                arkadas = next((x for x in self.yonetici.ogrenciler if x.id == ark_id), None)
                if arkadas and arkadas.yerlesilen_firma_id == o.yerlesilen_firma_id:
                    ark_sayisi += 1
            
            tercih_sira = o.tercih_siralamasi if o.tercih_siralamasi else "-"
            iterasyon = o.yerlesildigi_iterasyon if o.yerlesildigi_iterasyon else "-"
            
            satir = f"{o.ad:<18} | {f_ad:<18} | {tercih_sira:^4} | {iterasyon:^3} | {ark_sayisi:^3} | {o.memnuniyet_skoru:>5.1f}\n"
            self.txt_yerlesen.insert(tk.END, satir)