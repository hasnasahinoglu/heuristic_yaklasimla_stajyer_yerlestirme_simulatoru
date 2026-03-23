import random
import json

class VeriYoneticisi:

    @staticmethod
    def rastgele_veri_uret(ogrenci_sayisi=50, firma_sayisi=10, max_kontenjan=3, gno_benzerlik_orani=0.5, gno_sapma=0.2, grup_orani=0.7, sabit_tolerans=None):
        
        """
        ogrenci_sayisi (int): Toplam oluşturulacak öğrenci sayısı.
        firma_sayisi (int): Toplam oluşturulacak firma sayısı.
        max_kontenjan (int): Bir firmanın alabileceği maksimum öğrenci sayısı.
        """

        # ----------------------------------------
        # KAPASİTE KONTROLLERİ
        # ----------------------------------------
        # 1. Her firmaya en az 1 öğrenci düşmeli
        if ogrenci_sayisi < firma_sayisi:
            raise ValueError(f"Hata: Öğrenci sayısı ({ogrenci_sayisi}), firma sayısından ({firma_sayisi}) az olamaz.")

        # 2. Toplam kapasite öğrenci sayısını karşılamalı
        toplam_kapasite = firma_sayisi * max_kontenjan
        if ogrenci_sayisi > toplam_kapasite:
            raise ValueError(f"Hata: {ogrenci_sayisi} öğrenci var ama sistemin max kapasitesi {toplam_kapasite} (Firma: {firma_sayisi} x Max: {max_kontenjan}). Lütfen firma sayısını veya max kontenjanı artırın.")

        # -------------------------------
        # İSİM & SOYİSİM HAVUZU
        # -------------------------------
        isimler = [
            "Ahmet","Mehmet","Ayşe","Fatma","Ali","Veli","Zeynep","Elif","Mustafa","Hüseyin","Hatice","Emine","Can","Ece","Burak","Selin",
            "Emre","Deniz","Berk","Merve","Kemal","Seda","Onur","Özge","Cem","Pınar","Murat","Defne","Serkan","İrem","Barış","Gizem",
            "Oğuz","Aslı","Tolga","Cansu","Eren","Ezgi","Kaan","Büşra","Furkan","Damla","Hakan","Ceren","Yusuf","Duygu","Tarık","Begüm",
            "Okan","Simge","Tuğba","Melis","Sultan","Sudenur","Berat","İlker","Harun","Yiğit","Arda","Esra","Hilal","Sinem","Yasemin",
            "Gülsüm","Şevval","Bahar","Derya","Sare","Nehir","Melike","Betül","Nisa","Azra","Enes","Eylül","Nimet","Alper","İclal"
        ]

        soyisimler = [
            "Yılmaz","Kaya","Demir","Çelik","Şahin","Yıldız","Aydın","Öztürk","Arslan","Doğan","Kılıç","Aslan","Çetin","Koç","Kurt",
            "Özdemir","Erdoğan","Polat","Güneş","Aksoy","Karaca","Tekin","Bulut","Yalçın","Güler","Özkan","Özçelik","Yıldırım",
            "Altın","Korkmaz","Başak","Tunç","Sönmez","Ergün","Taş","Acar","Toprak","Ekinci","Özer","Sarı","Aktaş","Keskin","Ceylan",
            "Ateş","Durmaz","Şimşek","Bozkurt","Tan","Sezer","Ülker","Balcı","Duman","Boran","Kavas","Ergen","Güney","Efe","Türkmen"
        ]

        # ----------------------------------------
        # FİRMA ADLARI OLUŞTURMA
        # ----------------------------------------
        firma_tema = [
            "Teknoloji","Yazılım","Danışmanlık","Mühendislik","İnovasyon","Dijital","Sistem","Bilişim",
            "Yapay Zeka","Veri Analiz","Siber Güvenlik","Bulut","Mobil","Web Tasarım","E-Ticaret",
            "Fintek","Blockchain","IoT","Robotik","Otomasyon","Makine Öğrenmesi","Büyük Veri","DevOps",
            "ERP","CRM","Akıllı Sistemler","Analitik","Platform","Mikroservis","Veri Bilimi"
        ]

        random.shuffle(firma_tema)
        son_firma_adlari = []
        for i in range(firma_sayisi):
            tema = firma_tema[i % len(firma_tema)]
            ek = random.choice(['A.Ş.','Teknoloji','Bilişim','Sistemleri'])
            tam_isim = f"{tema} {ek} #{i+1}"
            son_firma_adlari.append(tam_isim)

        # ----------------------------------------
        # KONTENJANLARI DAĞITMA
        # ----------------------------------------
        # 1. Her firmaya en az 1 kontenjan ver
        kontenjanlar = [1] * firma_sayisi
        
        # 2. Geriye kalan öğrenci sayısını hesapla
        kalan_ogrenci = ogrenci_sayisi - firma_sayisi
        
        # 3. Kalan öğrencileri, MAX SINIRA DİKKAT EDEREK dağıt
        while kalan_ogrenci > 0:
            sansli_firma_index = random.randint(0, firma_sayisi - 1)
            
            # Eğer şanslı firmanın yeri varsa ekle
            if kontenjanlar[sansli_firma_index] < max_kontenjan:
                kontenjanlar[sansli_firma_index] += 1
                kalan_ogrenci -= 1
            # Yer yoksa döngü tekrar döner ve başka firma arar

        # ----------------------------------------
        # FİRMALARI OLUŞTUR
        # ----------------------------------------
        firmalar = []
        for i in range(firma_sayisi):
            firmalar.append({
                "id": i + 1,
                "ad": son_firma_adlari[i],
                "kontenjan": kontenjanlar[i]
            })

        # ----------------------------------------
        # ARKADAŞ GRUPLARI (CLIQUES) OLUŞTURMA
        # ----------------------------------------
        grup_olacak_ogr_sayisi = int(ogrenci_sayisi * grup_orani)
        havuz = list(range(1, grup_olacak_ogr_sayisi + 1)) 
        random.shuffle(havuz)
        
        gruplar = [] 
        
        while len(havuz) >= 2:
            grup_boyutu = random.randint(2, 3)
            if len(havuz) < grup_boyutu:
                grup_boyutu = len(havuz)
                
            yeni_grup_uyeleri = []
            for _ in range(grup_boyutu):
                yeni_grup_uyeleri.append(havuz.pop())
            
            ortak_firmalar = random.sample(range(1, firma_sayisi + 1), 3)
            
            # GRUP GNO BELİRLEME
            hedef_gno = None
            if random.random() < gno_benzerlik_orani:
                hedef_gno = random.uniform(2.2, 3.8)

            gruplar.append({
                "uyeler": yeni_grup_uyeleri,
                "ortak_firmalar": ortak_firmalar,
                "hedef_gno": hedef_gno 
            })

        # Hızlı erişim için map oluştur: ogrenci_id -> grup_objesi
        ogrenci_grup_map = {}
        for g in gruplar:
            for uye_id in g["uyeler"]:
                ogrenci_grup_map[uye_id] = g

        # ----------------------------------------
        # ÖĞRENCİLER OLUŞTUR
        # ----------------------------------------
        ogrenciler = []
        kullanilan_isimler = set()

        for i in range(1, ogrenci_sayisi + 1):
            
            # Benzersiz İsim
            while True:
                ad_soyad = f"{random.choice(isimler)} {random.choice(soyisimler)}"
                if ad_soyad not in kullanilan_isimler:
                    kullanilan_isimler.add(ad_soyad)
                    break

            # GNO BELİRLEME
            gno = 0.0
            
            if i in ogrenci_grup_map and ogrenci_grup_map[i]["hedef_gno"] is not None:
                merkez = ogrenci_grup_map[i]["hedef_gno"]
                ham_not = merkez + random.uniform(-gno_sapma, gno_sapma)
                ham_not = max(2.0, min(4.0, ham_not))
                gno = round(ham_not, 2)
            else:
                gno = round(random.uniform(2.0, 4.0), 2)
            
            # TERCİH VE TOLERANS OLUŞTURMA
            mevcut_tercihler = []
            arkadaslar = []
            ark_tol = 0
            
            if i in ogrenci_grup_map:
                grup = ogrenci_grup_map[i]
                secilecek_ortak_sayisi = random.choice([2, 3])
                
                sample_size = min(len(grup["ortak_firmalar"]), secilecek_ortak_sayisi, firma_sayisi)
                if sample_size > 0:
                    mevcut_tercihler.extend(random.sample(grup["ortak_firmalar"], sample_size))
                
                kalan_hak = 3 - len(mevcut_tercihler)
                olasi_digerleri = [x for x in range(1, firma_sayisi + 1) if x not in mevcut_tercihler]
                
                if olasi_digerleri:
                    mevcut_tercihler.extend(random.sample(olasi_digerleri, min(len(olasi_digerleri), kalan_hak)))
                
                random.shuffle(mevcut_tercihler)
                arkadaslar = [uye for uye in grup["uyeler"] if uye != i]
                
                # --- TOLERANS AYARI ---
                if sabit_tolerans is not None:
                    ark_tol = sabit_tolerans
                else:
                    ark_tol = random.randint(1, 3) 
                
            else:
                num_to_select = min(3, firma_sayisi)
                mevcut_tercihler = random.sample(range(1, firma_sayisi + 1), num_to_select)
                arkadaslar = []
                
                ark_tol = 0 if sabit_tolerans is None else sabit_tolerans

            ogrenciler.append({
                "id": i,
                "ad": ad_soyad,
                "gno": gno,
                "tercihler": mevcut_tercihler,
                "arkadaslar": arkadaslar,
                "arkadas_toleransi": ark_tol
            })

        return ogrenciler, firmalar

    @staticmethod
    def json_kaydet(ogrenciler, firmalar, dosya="data_example1.json"):
        with open(dosya, "w", encoding="utf-8") as f:
            json.dump({"ogrenciler": ogrenciler, "firmalar": firmalar}, f, ensure_ascii=False, indent=2)
        print(f" Veri '{dosya}' dosyasına kaydedildi.")

    @staticmethod
    def veri_ozeti(ogrenciler, firmalar):
        toplam = sum(f['kontenjan'] for f in firmalar)
        arkadasli_ogr = sum(1 for o in ogrenciler if len(o['arkadaslar']) > 0)
        
        # Max kontenjanı geçen var mı kontrolü (debug amaçlı)
        max_k = max(f['kontenjan'] for f in firmalar)
        
        print("\n=== SİSTEM ÖZETİ (MAX KONTENJANLI) ===")
        print(f"İstenen Öğrenci  : {len(ogrenciler)}")
        print(f"Firma sayısı     : {len(firmalar)}")
        print(f"Toplam Kontenjan : {toplam}")
        print(f"En Yüksek Kont.  : {max_k} (Limitine uygun mu? kontrol ediniz)")
        print(f"Arkadaş grubu    : {arkadasli_ogr} kişi")
        print("Kontrol          :", "✔ EŞİT" if toplam == len(ogrenciler) else "❌ HATA")
        print("====================\n")

# ---------------------------------------------------------
#  ANA ÇALIŞMA
# ---------------------------------------------------------
if __name__ == "__main__":
    try:
        ogr, fir = VeriYoneticisi.rastgele_veri_uret(
            ogrenci_sayisi=7,   
            firma_sayisi=4,     
            max_kontenjan=3,     
            gno_benzerlik_orani=0.5, 
            gno_sapma=0.2 
        )
        
        VeriYoneticisi.veri_ozeti(ogr, fir)
        VeriYoneticisi.json_kaydet(ogr, fir)
    except ValueError as e:
        print(f" HATA: {e}")