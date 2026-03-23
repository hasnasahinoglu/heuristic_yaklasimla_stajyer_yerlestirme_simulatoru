class StandartMemnuniyetHesaplama:
    """Greedy ve Heuristic algoritmalarının adil karşılaştırması için"""
    
    WEIGHT_TERCIH = 10
    WEIGHT_ARKADAS = 50
    MAX_TERCIH = 5
    DECAY_RATE = 0.20
    
    @staticmethod
    def tercih_puani(tercih_sirasi, iterasyon=1):
        if tercih_sirasi <= StandartMemnuniyetHesaplama.MAX_TERCIH:
            base_point = StandartMemnuniyetHesaplama.WEIGHT_TERCIH * (
                StandartMemnuniyetHesaplama.MAX_TERCIH + 1 - tercih_sirasi
            )
        else:
            base_point = 5
            
        multiplier = (1 - StandartMemnuniyetHesaplama.DECAY_RATE) ** (iterasyon - 1)
        return base_point * multiplier
    
    @staticmethod
    def arkadas_puani(arkadas_sayisi):
        return StandartMemnuniyetHesaplama.WEIGHT_ARKADAS * min(arkadas_sayisi, 2)
    
    
    @staticmethod
    def hesapla_ogrenci_memnuniyeti(ogrenci, tum_ogrenciler):
        if not ogrenci.kalici_yerlesti:
            return 0
        
        iterasyon = ogrenci.yerlesildigi_iterasyon if ogrenci.yerlesildigi_iterasyon else 1
      
        if ogrenci.yerlesilen_firma_id in ogrenci.tercihler:
            sira = ogrenci.tercihler.index(ogrenci.yerlesilen_firma_id) + 1
        else:
            sira = 6
        
        tercih_puan = StandartMemnuniyetHesaplama.tercih_puani(sira, iterasyon)
        
        arkadas_count = 0
        for ark_id in ogrenci.arkadaslar:
            arkadas = next((o for o in tum_ogrenciler if o.id == ark_id), None)
            if arkadas and arkadas.yerlesilen_firma_id == ogrenci.yerlesilen_firma_id:
                arkadas_count += 1
        
        multiplier = 10*(1 - StandartMemnuniyetHesaplama.DECAY_RATE) ** (iterasyon - 1)
        
        if ogrenci.tercih_siralamasi == 1:
            arkadas_puan = (ogrenci.tercih_siralamasi-1)*multiplier * min(arkadas_count,1) + arkadas_count*10
        else:
            arkadas_puan = (ogrenci.tercih_siralamasi-1)*multiplier * min(arkadas_count,1) + (arkadas_count-1)*10* min(arkadas_count,1)
        
        return tercih_puan + arkadas_puan

    @staticmethod
    def hesapla_sistem_memnuniyeti(ogrenciler):
        toplam = 0
        yerlesen_sayisi = 0
        
        for ogrenci in ogrenciler:
            if ogrenci.kalici_yerlesti:
                puan = StandartMemnuniyetHesaplama.hesapla_ogrenci_memnuniyeti(ogrenci, ogrenciler)
                ogrenci.memnuniyet_skoru = puan
                toplam += puan
                yerlesen_sayisi += 1
            else:
                ogrenci.memnuniyet_skoru = 0
        
        ortalama = (toplam / yerlesen_sayisi) if yerlesen_sayisi > 0 else 0
        return {
            'toplam_memnuniyet': toplam,
            'ortalama_memnuniyet': ortalama,
            'yerlesen_sayisi': yerlesen_sayisi
        }