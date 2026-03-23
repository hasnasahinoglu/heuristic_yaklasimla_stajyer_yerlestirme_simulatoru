import matplotlib.pyplot as plt
import copy
import numpy as np
from data_create import VeriYoneticisi
from controller_test import YerlestirmeYonetici
from models import Ogrenci, Firma

# =========================================================
# YARDIMCI FONKSİYONLAR
# =========================================================
def veriyi_hazirla(ham_ogrenciler, ham_firmalar):
    """Verilerin kopyasını oluşturur, böylece algoritmalar orijinal veriyi bozmaz."""
    ogrenciler = [Ogrenci(copy.deepcopy(o)) for o in ham_ogrenciler]
    firmalar = [Firma(copy.deepcopy(f)) for f in ham_firmalar]
    return ogrenciler, firmalar

def test_senaryosu_calistir():
    print("🚀 TEST BAŞLIYOR: Standart Sapma ve Güven Aralığı Analizi...")
    
    yonetici = YerlestirmeYonetici()
    DENEME_SAYISI = 50  

    # =========================================================
    # PARAMETRELER 
    # =========================================================
    FIRMA_SAYISI = 50
    MAX_KONTENJAN = 3
    OGRENCI_SAYISI = 130 

    print(f"--- SENARYO 1: BEAM WIDTH ANALİZİ ({DENEME_SAYISI} Tekrar) ---")
    print(f"⚙️ Ayarlar: {FIRMA_SAYISI} Firma, {OGRENCI_SAYISI} Öğrenci, Max Kontenjan: {MAX_KONTENJAN}")

    test_beam_widths = [3, 5, 8, 12, 16, 20, 25, 30, 40, 50, 70, 100]
    
    # 1. Sabit Veri Setlerini Üret
    print("ℹ️  Veri setleri hazırlanıyor...")
    sabit_veri_setleri = []
    for _ in range(DENEME_SAYISI):
        
        raw_ogr, raw_fir = VeriYoneticisi.rastgele_veri_uret(
            ogrenci_sayisi=OGRENCI_SAYISI, 
            firma_sayisi=FIRMA_SAYISI,     
            max_kontenjan=MAX_KONTENJAN,   
            gno_benzerlik_orani=0.5, 
            gno_sapma=0.2
        )
        sabit_veri_setleri.append((raw_ogr, raw_fir))

    # 2. Greedy Referansını ve Varyasyonunu Hesapla
    print("ℹ️  Greedy referans puanı ve sapması hesaplanıyor...")
    greedy_results = []
    for raw_ogr, raw_fir in sabit_veri_setleri:
        ogr_g, fir_g = veriyi_hazirla(raw_ogr, raw_fir)
        yonetici.veri_yukle_objelerle(ogr_g, fir_g)
        res = yonetici.headless_calistir("Greedy")
        greedy_results.append(res['toplam_memnuniyet'])
    
    # Greedy İstatistikleri
    greedy_mean = np.mean(greedy_results)
    greedy_std = np.std(greedy_results)
    print(f"📊 Greedy Ort: {greedy_mean:.2f}, Std Sapma: {greedy_std:.2f}")

    # 3. Beam Width Testi
    avg_heu_scores = []
    std_heu_scores = [] 
    avg_heu_times = []

    print("ℹ️  Heuristic testleri başlıyor:")
    for width in test_beam_widths:
        tur_heu_puanlari = []
        tur_heu_sureleri = []
        
        print(f"BW:{width}", end="|", flush=True)
        
        for i in range(DENEME_SAYISI):
            raw_ogr, raw_fir = sabit_veri_setleri[i]
            ogr_h, fir_h = veriyi_hazirla(raw_ogr, raw_fir)
            yonetici.veri_yukle_objelerle(ogr_h, fir_h)
            res_h = yonetici.headless_calistir("Heuristic", beam_width=width)
            
            tur_heu_puanlari.append(res_h['toplam_memnuniyet'])
            tur_heu_sureleri.append(res_h['calisma_suresi'])
            
        avg_heu_scores.append(np.mean(tur_heu_puanlari))
        std_heu_scores.append(np.std(tur_heu_puanlari))
        avg_heu_times.append(np.mean(tur_heu_sureleri))

    print("\n✅ Testler tamamlandı. Hesaplamalar yapılıyor...")

    # =========================================================
    # TREND VE R^2 HESAPLAMA
    # =========================================================
    x = np.array(test_beam_widths)
    y = np.array(avg_heu_scores)
    
    # Polinom Fit
    z = np.polyfit(x, y, 2) 
    p = np.poly1d(z)
    trend_y = p(x)

    # R^2
    y_mean_val = np.mean(y)
    ss_tot = np.sum((y - y_mean_val)**2)
    ss_res = np.sum((y - trend_y)**2)
    r_squared = 1 - (ss_res / ss_tot)

    # =========================================================
    # GRAFİK ÇİZİMİ 
    # =========================================================
    fig, ax1 = plt.subplots(figsize=(12, 7))
    
    ax1.set_xlabel('Beam Width (Arama Genişliği)')
    ax1.set_ylabel('Toplam Memnuniyet Puanı', color='#3b679e')
    
    # --- HEURISTIC ÇİZİMİ ---
    # Ortalamayı çiz
    ax1.plot(test_beam_widths, avg_heu_scores, marker='o', markersize=5, 
             color='#4a86e8', label='Heuristic (Ortalama)')
    
    # Trendi çiz
    ax1.plot(x, trend_y, "k--", linewidth=1.5, alpha=0.8,
             label=f'Trend ($R^2 = {r_squared:.3f}$)')
             
    # Puanların +/- 1 standart sapma aralığını boya
    y_upper = np.array(avg_heu_scores) + np.array(std_heu_scores)
    y_lower = np.array(avg_heu_scores) - np.array(std_heu_scores)
    ax1.fill_between(test_beam_widths, y_lower, y_upper, color='#4a86e8', alpha=0.15, label='Heuristic Dağılım Aralığı')

    # --- GREEDY ÇİZİMİ ---
    # Ortalamayı düz çizgi olarak çiz
    greedy_line = [greedy_mean] * len(test_beam_widths)
    ax1.plot(test_beam_widths, greedy_line, linestyle='--', color='#cc0000', label='Greedy (Referans)')
    
    # Greedy düz gitse de aslında veriler bu aralıkta oynuyor
    g_upper = [greedy_mean + greedy_std] * len(test_beam_widths)
    g_lower = [greedy_mean - greedy_std] * len(test_beam_widths)
    ax1.fill_between(test_beam_widths, g_lower, g_upper, color='#cc0000', alpha=0.1, label='Greedy Dağılım Aralığı')

    
    ax1.tick_params(axis='y', labelcolor='#3b679e')
    ax1.legend(loc='upper left', fontsize=9, framealpha=0.9)
    
    # İkinci Eksen (Süre)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Ortalama Süre (saniye)', color='#6aa84f')
    ax2.plot(test_beam_widths, avg_heu_times, marker='x', linestyle=':', 
             color='#6aa84f', alpha=0.7, label='Çalışma Süresi')
    ax2.tick_params(axis='y', labelcolor='#6aa84f')
    
    plt.title(f"Beam Width Performans Analizi\n(Gölgeli alanlar +/- 1 Standart Sapma aralığıdır)", fontsize=13)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    
    plt.savefig("analiz_beam_width_golgeli.png")
    print(f"📊 Grafik kaydedildi: analiz_beam_width_golgeli.png")
    plt.show()

if __name__ == "__main__":
    test_senaryosu_calistir()