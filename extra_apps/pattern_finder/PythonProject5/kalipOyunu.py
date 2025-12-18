import sys


def piyon_dizilimlerini_bul(n):
    """
    Verilen n sayısı için kurallara uygun tüm dizilimleri bulur.
    Kural 1: İlk piyon 'b' (beyaz) olmalı.
    Kural 2: 'ss' (iki siyah) yan yana gelemez.
    """
    sonuclar = []

    def olustur(mevcut_dizilim):
        # Eğer istenilen uzunluğa ulaştıysak listeye ekle
        if len(mevcut_dizilim) == n:
            sonuclar.append(mevcut_dizilim)
            return

        # Her zaman Beyaz (b) ekleyebiliriz
        olustur(mevcut_dizilim + "b")

        # Eğer son eklenen Siyah (s) değilse, Siyah ekleyebiliriz
        if mevcut_dizilim[-1] != "s":
            olustur(mevcut_dizilim + "s")

    # Başlangıç durumu: İlk piyon kesinlikle beyaz
    if n > 0:
        olustur("b")

    return sonuclar


def main():
    print("==========================================")
    print("   SATRANÇ PİYON DİZİLİM HESAPLAYICI")
    print("==========================================")

    while True:
        try:
            giris = input("\nLütfen piyon/kare sayısını girin (Çıkış için 'q'): ")

            if giris.lower() == 'q':
                print("Programdan çıkılıyor...")
                break

            n = int(giris)

            if n <= 0:
                print("Lütfen 0'dan büyük bir sayı girin!")
                continue

            print(f"\nHesaplanıyor... ({n} kare için)\n")

            tum_olasiliklar = piyon_dizilimlerini_bul(n)

            print(f"{'No':<5} | {'Kod':<15} | {'Görsel'}")
            print("-" * 40)

            for index, dizilim in enumerate(tum_olasiliklar, 1):
                gorsel = dizilim.replace('b', '⬜').replace('s', '⬛')
                print(f"{index:<5} | {dizilim:<15} | {gorsel}")

            print("-" * 40)
            print(f"SONUÇ: Toplam {len(tum_olasiliklar)} farklı dizilim bulundu.")
            print("==========================================")

        except ValueError:
            print("Hata: Lütfen geçerli bir tam sayı girin!")


if __name__ == "__main__":
    main()