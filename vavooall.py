import requests
import re

URL = "https://vavoo.to/channels"
PROXY_BASE = "https://latte-proxy2.hf.space/proxy/m3u?
url=https://vavoo.to/play/{}/index.m3u8"
LOGO_URL = "https://raw.githubusercontent.com/reelman543/ES26-edt/refs/heads/main/vavoo.png"
OUTPUT_FILE = "vavooall.m3u"

TURKISH_CHAR_MAP = str.maketrans({
    'ç': 'c', 'Ç': 'C',
    'ğ': 'g', 'Ğ': 'G',
    'ı': 'i', 'İ': 'I',
    'ö': 'o', 'Ö': 'O',
    'ş': 's', 'Ş': 'S',
    'ü': 'u', 'Ü': 'U'
})

NAME_CORRECTIONS = {
    "S NEMA": "SİNEMA",
    "T RK": "TÜRK",
    "M Z K": "MÜZİK",
    "A LE": "AİLE",
    "AKS YON": "AKSİYON",
    "KOMED": "KOMEDİ",
    "YERL": "YERLİ",
    "KURD": "KURDİ",
    "OCUK": "ÇOCUK",
    "CAY": "ÇAY",
    "D Ğ N": "DOĞAN",
    "VINC": "VINCI",
    "KOMEDİI": "KOMEDİ",
    "ÇÇOÇUK": "ÇOCUK",
    "M N KA": "MİNİKA",
    "CÇOÇUK": "ÇOCUK",
    "ÇÇOCUK": "ÇOCUK",
    "CÇOCUK": "ÇOCUK",
}
COUNTRY_LANG_MAP = {
    "Albania": "Arnavutça",
    "Arabia": "Arapça",
    "Balkans": "Balkan Dilleri",
    "Bulgaria": "Bulgarca",
    "France": "Fransızca",
    "Germany": "Almanca",
    "Italy": "İtalyanca",
    "Netherlands": "Felemenkçe",
    "Poland": "Lehçe",
    "Portugal": "Portekizce",
    "Romania": "Romence",
    "Russia": "Rusça",
    "Spain": "İspanyolca",
    "Turkey": "Türkçe",
    "United Kingdom": "İngilizce"
}
COUNTRY_NAME_MAP = {
    "Albania": "Arnavutluk",
    "Arabia": "Arabistan",
    "Balkans": "Balkanlar",
    "Bulgaria": "Bulgaristan",
    "France": "Fransa",
    "Germany": "Almanya",
    "Italy": "İtalya",
    "Netherlands": "Hollanda",
    "Poland": "Polonya",
    "Portugal": "Portekiz",
    "Romania": "Romanya",
    "Russia": "Rusya",
    "Spain": "İspanya",
    "Turkey": "Türkiye",
    "United Kingdom": "İngiltere"
}




def normalize_tvg_id(name):
    name_ascii = name.translate(TURKISH_CHAR_MAP)
    return re.sub(r'\W+', '_', name_ascii.strip()).upper()

def fix_channel_name(name):
    for wrong, correct in NAME_CORRECTIONS.items():
        name = re.sub(wrong, correct, name, flags=re.IGNORECASE)
    return name.strip()

def fetch_all_channels():
    response = requests.get(URL)
    if response.status_code != 200:
        print("Hata: Kanal listesi alınamadı.")
        return []

    channels = response.json()

    for ch in channels:
        ch["name"] = fix_channel_name(ch.get("name", ""))
        ch["country"] = ch.get("country", "Unknown")

    def sort_key(ch):
        country = ch.get("country", "").lower()
        name = ch.get("name", "").lower()
        return (country, name)

    return sorted(channels, key=sort_key)

def generate_m3u(channels):
    country_counts = {}
    for ch in channels:
        country = ch.get("country", "Unknown")
        country_counts[country] = country_counts.get(country, 0) + 1

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        for ch in channels:
            name = ch.get("name", "Unknown").strip()
            tvg_id = normalize_tvg_id(name)
            proxy_url = PROXY_BASE.format(ch.get("id"))
            country_en = ch.get("country", "Unknown")

            lang = COUNTRY_LANG_MAP.get(country_en, "Bilinmiyor")
            country_tr = COUNTRY_NAME_MAP.get(country_en, country_en)
            group_title = f"{country_tr} ({country_counts.get(country_en, 0)})"

            f.write(
                f'#EXTINF:-1 tvg-name="{name}" tvg-language="{lang}" '
                f'tvg-country="{country_tr}" tvg-id="{tvg_id}" tvg-logo="{LOGO_URL}" '
                f'group-title="{group_title}",{name}\n{proxy_url}\n'
            )

    print(f"{len(channels)} Tane kanal bulundu → '{OUTPUT_FILE}' dosyasına yazıldı.")


if __name__ == "__main__":
    all_channels = fetch_all_channels()
    generate_m3u(all_channels)
