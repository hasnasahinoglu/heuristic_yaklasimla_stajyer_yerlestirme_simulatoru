import random

class Ogrenci:
    def __init__(self, data):
        self.id = data.get('id')
        self.ad = data.get('ad')
        self.gno = data.get('gno')
        self.tercihler = data.get('tercihler', [])
        self.arkadaslar = data.get('arkadaslar', [])
        self.arkadas_toleransi = data.get('arkadas_toleransi', 0)
        
        self.yerlesti_mi = False
        self.kalici_yerlesti = False
        self.yerlesilen_firma = None
        self.yerlesilen_firma_id = None
        self.yerlesildigi_iterasyon = None
        self.tercih_siralamasi = None
        
        self.reddedildigi_firmalar = {}
        self.memnuniyet_skoru = 0
        
        self.son_mulakat_puani = None
        self.son_degerlendirme_puani = None

    def tercihleri_guncelle(self, musait_firmalar_idleri, yerlesmemis_ogrenci_sayisi):
        uygun_adaylar = [fid for fid in musait_firmalar_idleri 
                         if fid not in self.reddedildigi_firmalar]
        if not uygun_adaylar:
            self.tercihler = []
        else:
            random.shuffle(uygun_adaylar)
            uygun_firma_sayisi = len(uygun_adaylar)
            if yerlesmemis_ogrenci_sayisi <= uygun_firma_sayisi:
                max_tercih = yerlesmemis_ogrenci_sayisi
            else:
                max_tercih = min(5, uygun_firma_sayisi)
            self.tercihler = uygun_adaylar[:max_tercih]

class Firma:
    def __init__(self, data):
        self.id = data.get('id')
        self.ad = data.get('ad')
        self.kontenjan = data.get('kontenjan')
        self.doluluk = 0
        self.yerlesen_ogrenciler = []
        self.esik_degeri = random.uniform(25, 50)

    def musait_mi(self):
        return self.doluluk < self.kontenjan

    def ogrenci_ekle(self, ogrenci, zorla=False):
        if self.musait_mi():
            self.yerlesen_ogrenciler.append(ogrenci)
            self.doluluk += 1
            ogrenci.yerlesti_mi = True
            ogrenci.kalici_yerlesti = True
            ogrenci.yerlesilen_firma = self.ad + (" (Ek)" if zorla else "")
            ogrenci.yerlesilen_firma_id = self.id
            return True
        return False

    def ogrenci_cikar(self, ogrenci):
        if ogrenci in self.yerlesen_ogrenciler:
            self.yerlesen_ogrenciler.remove(ogrenci)
            self.doluluk -= 1
            ogrenci.yerlesti_mi = False
            ogrenci.kalici_yerlesti = False
            ogrenci.yerlesilen_firma = None
            ogrenci.yerlesilen_firma_id = None

    def esik_dusur(self, miktar=5.0):
        self.esik_degeri -= miktar
        if self.esik_degeri < 20.0:
            self.esik_degeri = 20.0

class State:
    def __init__(self, assignments, firm_capacities, score, log_history, parent_id=None, round_num=1):
        self.assignments = assignments
        self.firm_capacities = firm_capacities
        self.score = score
        self.log_history = log_history
        self.id = id(self)
        self.parent_id = parent_id
        self.round_num = round_num