import os
import pandas as pd

# Yüklediğin Cumhurbaşkanlığı klasörünün içerideki ana veri yolu
DATA_DIR = "data"

def mevzuat_ve_vergi_bul(gtip_kodu):
    """
    Kullanıcının girdiği GTİP kodunu, yüklenen Cumhurbaşkanlığı 
    TGTC klasöründeki Excel tablolarında arar.
    """
    # GTİP kodundaki noktaları ve boşlukları temizle (Örn: 8544.49.20.00.00 -> 854449200000)
    temiz_gtip = str(gtip_kodu).replace(".", "").replace(" ", "").strip()
    
    # data klasörünün içindeki tüm excel dosyalarını otomatik tara
    if not os.path.exists(DATA_DIR):
        return {"durum": "Hata", "mesaj": "Klasör yapısı bulunamadı. Lütfen 'data' klasörünü yükleyin."}
        
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(('.xlsx', '.xls')):
                excel_yolu = os.path.join(root, file)
                try:
                    # Excel dosyasını oku
                    df = pd.read_excel(excel_yolu, dtype=str)
                    df.columns = df.columns.str.strip()
                    
                    # Olası gtip/pozisyon sütunlarını tespit et
                    pozisyon_sutunu = None
                    for col in df.columns:
                        if 'POZİSYON' in col.upper() or 'GTİP' in col.upper() or 'GTIP' in col.upper():
                            pozisyon_sutunu = col
                            break
                            
                    if pozisyon_sutunu:
                        # Tablodaki kodları da temizleyerek arama yap
                        df['TEMIZ_KOD'] = df[pozisyon_sutunu].str.replace(".", "", regex=False).str.strip()
                        eslesme = df[df['TEMIZ_KOD'] == temiz_gtip]
                        
                        if not eslesme.empty:
                            satir = eslesme.iloc[0].to_dict()
                            # Vergi haddi sütununu yakala
                            vergi_orani = 0.0
                            for k, v in satir.items():
                                if 'VERGİ' in k.upper() or 'HADDİ' in k.upper():
                                    try: vergi_orani = float(str(v).replace("%", "").strip())
                                    except: pass
                                    break
                            
                            return {
                                "durum": "Başarılı",
                                "dosya": file,
                                "tanim": satir.get('EŞYANIN TANIMI', 'Tanım bulunamadı'),
                                "vergi_orani": vergi_orani,
                                "birim": satir.get('ÖLÇÜ BİRİMİ', '-')
                            }
                except:
                    continue
                    
    return {"durum": "Bulunamadı", "mesaj": "Girilen GTİP kodu klasördeki dökümanlarda eşleşmedi."}