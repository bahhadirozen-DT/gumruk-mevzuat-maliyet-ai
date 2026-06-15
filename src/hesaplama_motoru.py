import sys
from mevzuat_isleyici import mevzuat_ve_vergi_bul

def ithalat_simulasyonu(gtip_kodu, mal_bedeli, navlun, sigorta, depo_gun, tonaj):
    # 1. Cumhurbaşkanlığı veritabanından gümrük vergisini bul
    mevzuat = mevzuat_ve_vergi_bul(gtip_kodu)
    vergi_orani = mevzuat.get("vergi_orani", 0.0) if mevzuat["durum"] == "Başarılı" else 0.0
    esya_tanimi = mevzuat.get("tanim", "Bilinmeyen Eşya")
    
    # 2. CIF Hesaplama
    cif_matrah = mal_bedeli + navlun + sigorta
    gumruk_vergisi = cif_matrah * (vergi_orani / 100)
    
    # 3. Depo ve Ardiye Giderleri (Sabitler)
    beyanname_damga = 1150.00
    ordino_ucreti = 150.00
    gunluk_ardiye_ton_basi = 15.00
    toplam_depo_masrafi = ordino_ucreti + (tonaj * depo_gun * gunluk_ardiye_ton_basi)
    lokal_nakliye_musavirlik = 450.00
    
    # 4. KDV Matrahı ve KDV Hesabı (%20 varsayılan)
    kdv_matrahi = cif_matrah + gumruk_vergisi + beyanname_damga + toplam_depo_masrafi + lokal_nakliye_musavirlik
    kdv_tutari = kdv_matrahi * 0.20
    
    # 5. Toplam Sonuçlar
    toplam_maliyet = cif_matrah + gumruk_vergisi + beyanname_damga + toplam_depo_masrafi + lokal_nakliye_musavirlik + kdv_tutari
    
    print(f"\n==================================================")
    print(f"📊 GÜMRÜK & DEPO TESLİM MALİYET RAPORU")
    print(f"==================================================")
    print(f"📦 Ürün Tanımı    : {esya_tanimi}")
    print(f"🔢 GTİP Kodu      : {gtip_kodu}")
    print(f"💰 CIF Matrahı     : {cif_matrah:,.2f} USD")
    print(f"🏛️ Gümrük Vergisi : {gumruk_vergisi:,.2f} USD (%{vergi_orani})")
    print(f"🏢 Depo/Ardiye    : {toplam_depo_masrafi:,.2f} USD ({depo_gun} Gün)")
    print(f"🧾 KDV Tutarı     : {kdv_tutari:,.2f} USD")
    print(f"🏁 TOPLAM MALİYET : {toplam_maliyet:,.2f} USD")
    print(f"==================================================")

if __name__ == "__main__":
    # Test çalıştırması (Örn: 854449200000 kodu için 10.000$ mal bedeli)
    ithalat_simulasyonu("854449200000", 10000, 1500, 150, 4, 12)