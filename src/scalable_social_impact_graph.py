import matplotlib.pyplot as plt
import copy
import numpy as np 
import random
from collections import defaultdict
from data_create import VeriYoneticisi
from controller_test import YerlestirmeYonetici
from models import Ogrenci, Firma

# =========================================================
# YARDIMCI FONKSİYONLAR
# =========================================================
def veriyi_hazirla(ham_ogrenciler, ham_firmalar):
    """Verilerin deep copy'sini oluşturur."""
    ogrenciler = [Ogrenci(copy.deepcopy(o)) for o in ham_ogrenciler]
    firmalar = [Firma(copy.deepcopy(f)) for f in ham_firmalar]
    return ogrenciler, firmalar

def ortalama_al(liste):
    return sum(liste) / len(liste) if liste else 0

def test_senaryolarini_calistir():
    yonetici = YerlestirmeYonetici()
    FIXED_BEAM_WIDTH = 8
    DENEME_SAYISI = 50  
    
    # SENARYO AYARLARI
    MAX_KONTENJAN = 3     # Her firma max 3 kişi alabilir
    ORTALAMA_DOLULUK = 2.2 # Firma başına ortalama öğrenci

    print(f" KAPSAMLI TEST BAŞLIYOR (BW={FIXED_BEAM_WIDTH}, Tekrar={DENEME_SAYISI})...")

    # =================================================================
    # SENARYO A: ÖLÇEKLENEBİLİRLİK (Süre vs Öğrenci Sayısı)
    # =================================================================
    print("\n--- [1/2] SENARYO A: ÖLÇEKLENEBİLİRLİK (Greedy vs Heuristic) ---")
    
    # Firmaları 20'den başlatıp 400'e kadar artırıyoruz
    firma_sayilari = range(20, 400, 20)
    
    x_ogr_counts = []
    y_time_greedy = []
    y_time_heuristic = []
    
    for f_count in firma_sayilari:
        # Maksimum kapasite ortalama 2.2 ile çarpıyoruz.
        # Böylece bazı firmalar 3, bazıları 2, bazıları 1 kişilik olacak.
        hedef_ogr_sayisi = int(f_count * ORTALAMA_DOLULUK)
        
        print(f" Firma: {f_count} (Ogr: {hedef_ogr_sayisi})...", end=" ")
        
        t_greedy, t_heu, t_ogr = [], [], []
        
        for _ in range(DENEME_SAYISI):
            raw_ogr, raw_fir = VeriYoneticisi.rastgele_veri_uret(
                ogrenci_sayisi=hedef_ogr_sayisi,
                firma_sayisi=f_count,
                max_kontenjan=MAX_KONTENJAN,  
                gno_benzerlik_orani=0.6, 
                grup_orani=0.7
            )
            t_ogr.append(len(raw_ogr))
            
            # Greedy Testi
            og, fg = veriyi_hazirla(raw_ogr, raw_fir)
            yonetici.veri_yukle_objelerle(og, fg)
            res_g = yonetici.headless_calistir("Greedy")
            t_greedy.append(res_g['calisma_suresi'])
            
            # Heuristic Testi
            oh, fh = veriyi_hazirla(raw_ogr, raw_fir)
            yonetici.veri_yukle_objelerle(oh, fh)
            res_h = yonetici.headless_calistir("Heuristic", beam_width=FIXED_BEAM_WIDTH)
            t_heu.append(res_h['calisma_suresi'])
            
        x_ogr_counts.append(ortalama_al(t_ogr))
        y_time_greedy.append(ortalama_al(t_greedy))
        y_time_heuristic.append(ortalama_al(t_heu))
        print("Tamam.")

    # GRAFİK A ÇİZİMİ
    plt.figure(figsize=(10, 6))
    plt.plot(x_ogr_counts, y_time_greedy, 'r--o', label="Greedy Süre")
    plt.plot(x_ogr_counts, y_time_heuristic, 'b-o', label="Heuristic Süre")
    plt.xlabel('Toplam Öğrenci Sayısı')
    plt.ylabel('Çalışma Süresi (Saniye)')
    plt.title('Ölçeklenebilirlik Analizi')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.savefig("analiz_A_olceklenebilirlik.png")
    print(" Grafik A kaydedildi.")

    # =================================================================
    # SENARYO B: SOSYAL ETKİ (Grup Oranı vs Memnuniyet)
    # =================================================================
    print("\n--- [2/2] SENARYO B: SOSYAL ETKİ (Greedy vs Heuristic) ---")
    
    grup_oranlari = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
    
    y_score_greedy = []
    y_score_heuristic = []
    
    # Sabit büyüklükte bir veri seti
    SABIT_FIRMA = 50
    SABIT_OGRENCI = 120 
    
    for oran in grup_oranlari:
        print(f"⚡ Grup Oranı: {oran}...", end=" ")
        
        s_greedy, s_heu = [], []
        for _ in range(DENEME_SAYISI):
            raw_ogr, raw_fir = VeriYoneticisi.rastgele_veri_uret(
                ogrenci_sayisi=SABIT_OGRENCI,
                firma_sayisi=SABIT_FIRMA,
                max_kontenjan=MAX_KONTENJAN, 
                gno_benzerlik_orani=0.6, 
                grup_orani=oran
            )
            
            # Greedy
            og, fg = veriyi_hazirla(raw_ogr, raw_fir)
            yonetici.veri_yukle_objelerle(og, fg)
            res_g = yonetici.headless_calistir("Greedy")
            s_greedy.append(res_g['ortalama_memnuniyet'])
            
            # Heuristic
            oh, fh = veriyi_hazirla(raw_ogr, raw_fir)
            yonetici.veri_yukle_objelerle(oh, fh)
            res_h = yonetici.headless_calistir("Heuristic", beam_width=FIXED_BEAM_WIDTH)
            s_heu.append(res_h['ortalama_memnuniyet'])
            
        y_score_greedy.append(ortalama_al(s_greedy))
        y_score_heuristic.append(ortalama_al(s_heu))
        print("Tamam.")

    # GRAFİK B ÇİZİMİ
    plt.figure(figsize=(10, 6))
    plt.plot(grup_oranlari, y_score_greedy, 'r--s', label="Greedy Puan")
    plt.plot(grup_oranlari, y_score_heuristic, 'b-s', label="Heuristic Puan")
    plt.xlabel('Grup Oranı')
    plt.ylabel('Ortalama Memnuniyet Puanı')
    plt.title('Sosyal Bağların Algoritmalara Etkisi')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend()
    plt.savefig("analiz_B_sosyal_etki.png")
    print(" Grafik B kaydedildi.")

    print("\n TÜM TESTLER TAMAMLANDI!")

if __name__ == "__main__":
    test_senaryolarini_calistir()