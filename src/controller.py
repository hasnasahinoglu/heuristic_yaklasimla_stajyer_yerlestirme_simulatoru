import json
import random
import time
from models import Ogrenci, Firma, State
from scoring import StandartMemnuniyetHesaplama
from settings import JSON_DOSYA_ADI

class YerlestirmeYonetici:
    
    def __init__(self):
        self.ogrenciler = []
        self.firmalar = []
        self.iterasyon_sayisi = 0
        self.algoritma_tipi = "Greedy"
        self.baslama_zamani = None
        self.bitis_zamani = None
        self.log_callback = None
        
        self.beam_states_history = []
        self.last_winner_state = None
        self.heu_fixed_assignments = {}
    
        self.beam_width = 8

    def veri_yukle_objelerle(self, ogrenciler_listesi, firmalar_listesi):
        self.ogrenciler = ogrenciler_listesi
        self.firmalar = firmalar_listesi
        self.beam_states_history = []
        self.last_winner_state = None
        self.iterasyon_sayisi = 0

    def headless_calistir(self, algoritma="Greedy", beam_width=8):
        self.algoritma_tipi = algoritma
        self.beam_width = beam_width
        
        if algoritma == "Greedy":
            self.greedy_baslat()
        else:
            self.heuristic_baslat()
            
        start = time.time()
        
        while True:
            stats = None
            if algoritma == "Greedy":
                stats = self.greedy_iterasyon_calistir()
            else:
                stats = self.heuristic_iterasyon_calistir()
                
            if stats is None:
                break
            
            if not self.get_yerlesemeyenler():
                break
        
        end = time.time()
        sonuclar = self.sonuclari_al()
        sonuclar['calisma_suresi'] = end - start
        return sonuclar
        
    def veri_yukle(self, dosya_yolu=JSON_DOSYA_ADI):
        try:
            with open(dosya_yolu, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.ogrenciler = [Ogrenci(o) for o in data['ogrenciler']]
            self.firmalar = [Firma(f) for f in data['firmalar']]
            return True
        except FileNotFoundError:
            return False

    def log(self, mesaj):
        if self.log_callback:
            self.log_callback(mesaj)
        else:
            print(mesaj)

    def get_yerlesen_sayisi(self):
        return sum(1 for o in self.ogrenciler if o.kalici_yerlesti)
    
    def get_yerlesemeyenler(self):
        return [o for o in self.ogrenciler if not o.kalici_yerlesti]

    def greedy_baslat(self):
        self.algoritma_tipi = "Greedy"
        self.iterasyon_sayisi = 0
        self.baslama_zamani = None 
        self.bitis_zamani = None
        
        for o in self.ogrenciler:
            o.kalici_yerlesti = False
            o.yerlesti_mi = False
            o.memnuniyet_skoru = 0
            o.tercih_siralamasi = None 
            o.reddedildigi_firmalar = {}
        for f in self.firmalar:
            f.yerlesen_ogrenciler = []
            f.doluluk = 0

    def greedy_iterasyon_calistir(self):
        self.iterasyon_sayisi += 1
        yerlesemeyenler = self.get_yerlesemeyenler()
        if not yerlesemeyenler: return None

        yerlesemeyenler.sort(key=lambda x: x.gno, reverse=True)
        yerlesen_bu_tur = 0
        ek_yerlesen = 0
        
        print(f"\n{'-'*60}")
        print(f"TUR {self.iterasyon_sayisi} BAŞLIYOR - GREEDY")
        print(f"{'-'*60}")

        for ogr in yerlesemeyenler:
            if ogr.yerlesti_mi: continue
            
            print(f"\n Öğrenci: {ogr.ad} (GNO: {ogr.gno}) işleniyor...")
            print(f" Tercihleri: {ogr.tercihler}")

            placed_flag = False
            for i, fid in enumerate(ogr.tercihler):
                if fid in ogr.reddedildigi_firmalar: 
                    print(f"   {i+1}. Tercih (ID:{fid}): Daha önce reddedildiği için atlandı. ")
                    continue
                
                firma = next((f for f in self.firmalar if f.id == fid), None)
                firma_adi = firma.ad if firma else "Bilinmiyor"

                if firma and firma.musait_mi():
                    print(f"   {i+1}. Tercih ({firma_adi} - ID:{fid}): KONTENJAN VAR")
                    
                    firma.ogrenci_ekle(ogr)
                    ogr.tercih_siralamasi = i + 1
                    ogr.yerlesildigi_iterasyon = self.iterasyon_sayisi
                    yerlesen_bu_tur += 1
                    placed_flag = True
                    
                    icerideki_arkadaslar = [a.ad for a in firma.yerlesen_ogrenciler if a.id in ogr.arkadaslar]
                    arkadas_msg = f"{len(icerideki_arkadaslar)} kişi ({', '.join(icerideki_arkadaslar)})" if icerideki_arkadaslar else "Yok"
                    print(f"YERLEŞTİRİLDİ! Firmadaki Arkadaşları: {arkadas_msg}")
                    break
                else:
                    doluluk = f"{firma.doluluk}/{firma.kontenjan}" if firma else "?/?"
                    print(f"{i+1}. Tercih ({firma_adi} - ID:{fid}): DOLU ({doluluk}) ")
            
            if not placed_flag:
                print(f"Bu tur hiçbir tercihine yerleşemedi.")

        reddedilenler_listesi = []
        print(f"\n DEĞERLENDİRME VE RED KONTROLLERİ...")
        for firma in self.firmalar:
            for ogr in firma.yerlesen_ogrenciler[:]:
                if ogr.yerlesildigi_iterasyon != self.iterasyon_sayisi: continue
                
                gno_puan = ogr.gno * 25
                mulakat = random.uniform(0, 100)
                skor = 0.5 * gno_puan + 0.5 * mulakat
                
                ogr.son_mulakat_puani = mulakat
                ogr.son_degerlendirme_puani = skor
                
                print(f"   {firma.ad} Değerlendiriyor -> {ogr.ad}: Puan {skor:.1f} (Eşik: {firma.esik_degeri:.1f})")

                if skor < firma.esik_degeri:
                    print(f"       RED EDİLDİ! (Puan yetersiz)")
                    firma.ogrenci_cikar(ogr)
                    ogr.reddedildigi_firmalar[firma.id] = skor
                    reddedilenler_listesi.append(ogr)
                else:
                    print(f"       ONAYLANDI (Kalıcı Yerleşti)")
                    ogr.kalici_yerlesti = True

        hala_bosta = self.get_yerlesemeyenler()
        musait_firmalar = [f for f in self.firmalar if f.musait_mi()]
        musait_ids = [f.id for f in musait_firmalar]
        
        yerlesmemis_sayi = len(hala_bosta)
        for ogr in hala_bosta:
            ogr.tercihleri_guncelle(musait_ids, yerlesmemis_sayi)
            
        if yerlesen_bu_tur == 0 and hala_bosta and musait_firmalar:
            random.shuffle(musait_firmalar)
            f_idx = 0
            print(f"\nTIKANIKLIK GİDERME (EK KONTENJAN)...")
            for ogr in hala_bosta:
                if not musait_firmalar: break
                if f_idx >= len(musait_firmalar): break
                
                hedef = musait_firmalar[f_idx]
                if hedef.musait_mi():
                    print(f"    {ogr.ad} -> {hedef.ad} (Rastgele Zorunlu Atama)")
                    hedef.ogrenci_ekle(ogr, zorla=True)
                    ogr.yerlesildigi_iterasyon = self.iterasyon_sayisi
                    ogr.tercih_siralamasi = 7
                    ek_yerlesen += 1
                else:
                    f_idx += 1
        
        for f in self.firmalar: f.esik_dusur()
        
        StandartMemnuniyetHesaplama.hesapla_sistem_memnuniyeti(self.ogrenciler)

        return {
            'iterasyon': self.iterasyon_sayisi,
            'normal': yerlesen_bu_tur,
            'ek': ek_yerlesen,
            'red': len(reddedilenler_listesi)
        }

    def heuristic_baslat(self):
        self.greedy_baslat()
        self.algoritma_tipi = "Heuristic"
        self.heu_fixed_assignments = {}
        self.beam_states_history = []
        
        caps = {f.id: f.kontenjan for f in self.firmalar}
        root = State({}, caps, 0, "BAŞLANGIÇ", None, 0)
        self.beam_states_history.append(root)
        self.last_winner_state = root
        
        self.log("Heuristic (Beam Search) Başlatıldı.")

    def heuristic_iterasyon_calistir(self):
        self.iterasyon_sayisi += 1
        
        active_students = [s for s in self.ogrenciler if not s.kalici_yerlesti]
        if not active_students: return None
        
        current_caps = {f.id: (f.kontenjan - f.doluluk) for f in self.firmalar}
        musait_ids = [fid for fid, cap in current_caps.items() if cap > 0]
        
        if not musait_ids: return None
        
        print(f"\n{'-'*60}")
        print(f"TUR {self.iterasyon_sayisi} BAŞLIYOR - HEURISTIC BEAM SEARCH")
        print(f"{'-'*60}")

        if self.iterasyon_sayisi > 1:
            yerlesmemis_sayi = len(active_students)
            self.log("\n\nYeni iterayson için tercihler güncelleniyor\n")
            for s in active_students:                
                s.tercihleri_guncelle(musait_ids, yerlesmemis_sayi)
                self.log(f"{s.ad:<15} | {', '.join(map(str, s.tercihler)):<25}")
            self.log(f"\n   {len(active_students)} öğrenci için tercihler güncellendi.")

        beam = []
        start_node = State({}, current_caps, self.last_winner_state.score, 
                           f"--- TUR {self.iterasyon_sayisi} ---", self.last_winner_state.id, self.iterasyon_sayisi)
        self.beam_states_history.append(start_node)
        beam.append(start_node)
        
        active_students.sort(key=lambda x: x.gno, reverse=True)
        
        self.log(f"   Beam Search çalışıyor (Width: {self.beam_width})...")
        print(f"    Beam Search {len(active_students)} öğrenci için en iyi kombinasyonu arıyor...")
        
        for student in active_students:
            new_beam = []
            for state in beam:
                branches = self._heu_expand(state, student)
                for b in branches:
                    if student.id in b.assignments:
                        f_id = b.assignments[student.id]
                        step_score = self._heu_calc_score(student, f_id, b.assignments)
                    else:
                        step_score = 0
                    
                    b.score = state.score + step_score
                    new_beam.append(b)
                    self.beam_states_history.append(b)
            
            new_beam.sort(key=lambda x: x.score, reverse=True)
            beam = new_beam[:self.beam_width]
        
        best_state = beam[0]
        self.log(f"   Beam Search bitti. Aday çözüm skoru: {best_state.score:.1f}")

        yerlesen_bu_tur = 0
        reddedilen_sayisi = 0
        
        candidates = best_state.assignments
        
        print(f"\n SEARCH KARARI (EN İYİ SENARYO):")
        
        for s_id, f_id in candidates.items():
            ogr = next(s for s in self.ogrenciler if s.id == s_id)
            firma = next(f for f in self.firmalar if f.id == f_id)
            firma_adi = firma.ad
            
            try:
                tercih_sirasi = ogr.tercihler.index(f_id) + 1
                tercih_bilgisi = f"{tercih_sirasi}. Tercihi"
            except ValueError:
                tercih_bilgisi = "Tercih Dışı / Zorunlu"
                
            print(f"    {ogr.ad} -> {firma_adi} ({tercih_bilgisi})")
            
            gno_puan = ogr.gno * 25
            mulakat = random.uniform(0, 100)
            skor = 0.5 * gno_puan + 0.5 * mulakat
            
            ogr.son_mulakat_puani = mulakat
            ogr.son_degerlendirme_puani = skor
            
            is_forced = (f_id not in ogr.tercihler)
            
            if is_forced:
                firma.ogrenci_ekle(ogr, zorla=True)
                ogr.yerlesildigi_iterasyon = self.iterasyon_sayisi
                self.heu_fixed_assignments[s_id] = f_id
                ogr.tercih_siralamasi = 7
                yerlesen_bu_tur += 1
                print("     Zorunlu atama yapıldı.")
            elif skor >= firma.esik_degeri:
                firma.ogrenci_ekle(ogr)
                ogr.yerlesildigi_iterasyon = self.iterasyon_sayisi
                self.heu_fixed_assignments[s_id] = f_id
                
                if f_id in ogr.tercihler:
                    ogr.tercih_siralamasi = ogr.tercihler.index(f_id) + 1
                else:
                    ogr.tercih_siralamasi = 6
                
                arkadas_sayisi = sum(1 for a in firma.yerlesen_ogrenciler if a.id in ogr.arkadaslar)
                print(f"      Yerleşti. (Mülakat: {skor:.1f} >= {firma.esik_degeri:.1f}). Arkadaş: {arkadas_sayisi}")
                yerlesen_bu_tur += 1
            else:
                ogr.reddedildigi_firmalar[f_id] = skor
                reddedilen_sayisi += 1
                print(f"      RED! (Mülakat: {skor:.1f} < {firma.esik_degeri:.1f})")
        
        stats = StandartMemnuniyetHesaplama.hesapla_sistem_memnuniyeti(self.ogrenciler)
        real_score = stats['toplam_memnuniyet']
        
        final_node = State({}, {}, real_score, f"RED SONRASI: {reddedilen_sayisi} Red", best_state.id, self.iterasyon_sayisi)
        self.beam_states_history.append(final_node)
        self.last_winner_state = final_node
        
        for f in self.firmalar: f.esik_dusur()
        
        if yerlesen_bu_tur == 0 and reddedilen_sayisi == 0 and active_students:
             self.log("   Tıkanıklık! Zorunlu bitirme veya ek mantık gerekebilir.")
        
        self.log(f"{'Tur':<4} | {'Normal':^8} | {'Ek':^5} | {'Red':^5} | {'Toplam Yerleşen'}")
        self.log("-" * 60)
        return {
            'iterasyon': self.iterasyon_sayisi,
            'normal': yerlesen_bu_tur,
            'ek': 0,
            'red': reddedilen_sayisi
        }

    def _heu_expand(self, current_state, student):
        branches = []
        firm_dict = {f.id: f for f in self.firmalar}
        candidates = []
        
        limit = student.arkadas_toleransi
        part_tolerance = student.tercihler[:limit+1]
        part_rest = student.tercihler[limit+1:]
        
        valid_in_tolerance = []
        for f_id in part_tolerance:
            if current_state.firm_capacities.get(f_id, 0) > 0:
                valid_in_tolerance.append(f_id)
        
        if valid_in_tolerance:
            candidates = valid_in_tolerance
        else:
            for f_id in part_rest:
                if current_state.firm_capacities.get(f_id, 0) > 0:
                    candidates.append(f_id)
                    break 

        if not candidates:
            tum_bos_firmalar = [fid for fid, cap in current_state.firm_capacities.items() if cap > 0]
            sorted_reds = sorted(student.reddedildigi_firmalar.items(), key=lambda item: item[1], reverse=True)
            for red_fid, red_score in sorted_reds:
                if red_fid in tum_bos_firmalar:
                    candidates.append(red_fid)
                    break 

        assigned = False
        for f_id in candidates:
            new_assign = current_state.assignments.copy()
            new_assign[student.id] = f_id
            
            new_caps = current_state.firm_capacities.copy()
            new_caps[f_id] -= 1
            
            f_name = firm_dict[f_id].ad
            is_forced = (f_id not in student.tercihler)
            
            if is_forced:
                log = f"{student.ad} -> {f_name} (ZORLA/RED)"
            else:
                log = f"{student.ad} -> {f_name}"
            
            new_state = State(new_assign, new_caps, current_state.score, log, current_state.id, self.iterasyon_sayisi)
            branches.append(new_state)
            assigned = True
            
        if not assigned:
            pas_state = State(current_state.assignments.copy(), current_state.firm_capacities.copy(), 
                              current_state.score, f"{student.ad} -> PAS", current_state.id, self.iterasyon_sayisi)
            branches.append(pas_state)
            
        return branches

    def _heu_calc_score(self, student, firm_id, current_branch_assignments):
        if firm_id in student.tercihler:
            sira = student.tercihler.index(firm_id) + 1
        else:
            sira = 6
        
        puan_tercih = StandartMemnuniyetHesaplama.tercih_puani(sira, self.iterasyon_sayisi)
        
        arkadas_count = 0
        for ark_id in student.arkadaslar:
            if ark_id in self.heu_fixed_assignments and self.heu_fixed_assignments[ark_id] == firm_id:
                arkadas_count += 1
            elif ark_id in current_branch_assignments and current_branch_assignments[ark_id] == firm_id:
                arkadas_count += 1
                
        puan_ark = StandartMemnuniyetHesaplama.arkadas_puani(arkadas_count)
        return puan_tercih + puan_ark

    def sonuclari_al(self):
        if self.baslama_zamani is not None and self.bitis_zamani is not None:
            sure = self.bitis_zamani - self.baslama_zamani
        else:
            sure = 0
            
        stats = StandartMemnuniyetHesaplama.hesapla_sistem_memnuniyeti(self.ogrenciler)
        stats['calisma_suresi'] = sure
        stats['iterasyon_sayisi'] = self.iterasyon_sayisi
        return stats