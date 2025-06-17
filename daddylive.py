import re
import requests
import os
import unicodedata

ulke_cevirisi = {
    "AFRICA": "Afrika",
    "ARGENTINA": "Arjantin",
    "AUSTRALIA": "Avustralya",
    "BOSNIA AND HERZEGOVINA": "Bosna Hersek",
    "BRAZIL": "Brezilya",
    "BULGARIA": "Bulgaristan",
    "CANADA": "Kanada",
    "CHILE": "Şili",
    "COLUMBIA": "Kolombiya",
    "CROATIA": "Hırvatistan",
    "CYPRUS": "Kıbrıs",
    "DENMARK": "Danimarka",
    "EGYPT": "Mısır",
    "FRANCE": "Fransa",
    "GERMANY": "Almanya",
    "GREECE": "Yunanistan",
    "ICELAND": "İzlanda",
    "INDIA": "Hindistan",
    "IRELAND": "İrlanda",
    "ISRAEL": "İsrail",
    "ITALY": "İtalya",
    "MALAYSIA": "Malezya",
    "MEXICO": "Meksika",
    "NETHERLANDS": "Hollanda",
    "NEW ZEALAND": "Yeni Zelanda",
    "OTHERS": "Diğer",
    "PAKISTAN": "Pakistan",
    "POLAND": "Polonya",
    "PORTUGAL": "Portekiz",
    "QATAR": "Katar",
    "ROMANIA": "Romanya",
    "RUSSIA": "Rusya",
    "SAUDI ARABIA": "Suudi Arabistan",
    "SERBIA": "Sırbistan",
    "SOUTH AFRICA": "Güney Afrika",
    "SPAIN": "İspanya",
    "SWEDEN": "İsveç",
    "TURKEY": "Türkiye",
    "UNITED ARAB EMIRATES": "Birleşik Arap Emirlikleri",
    "UNITED KINGDOM": "Birleşik Krallık",
    "UNITED STATES": "Amerika Birleşik Devletleri",
    "URUGUAY": "Uruguay"
}

ulke_kisaltmalari = {
    "AFRICA": "AF",
    "ARGENTINA": "AR",
    "AUSTRALIA": "AU",
    "BOSNIA AND HERZEGOVINA": "BA",
    "BRAZIL": "BR",
    "BULGARIA": "BG",
    "CANADA": "CA",
    "CHILE": "CL",
    "COLUMBIA": "CO",
    "CROATIA": "HR",
    "CYPRUS": "CY",
    "DENMARK": "DK",
    "EGYPT": "EG",
    "FRANCE": "FR",
    "GERMANY": "DE",
    "GREECE": "GR",
    "ICELAND": "IS",
    "INDIA": "IN",
    "IRELAND": "IE",
    "ISRAEL": "IL",
    "ITALY": "IT",
    "MALAYSIA": "MY",
    "MEXICO": "MX",
    "NETHERLANDS": "NL",
    "NEW ZEALAND": "NZ",
    "OTHERS": "OT",
    "PAKISTAN": "PK",
    "POLAND": "PL",
    "PORTUGAL": "PT",
    "QATAR": "QA",
    "ROMANIA": "RO",
    "RUSSIA": "RU",
    "SAUDI ARABIA": "SA",
    "SERBIA": "RS",
    "SOUTH AFRICA": "ZA",
    "SPAIN": "ES",
    "SWEDEN": "SE",
    "TURKEY": "TR",
    "UNITED ARAB EMIRATES": "AE",
    "UNITED KINGDOM": "UK",
    "UNITED STATES": "US",
    "URUGUAY": "UY"
}

dil_cevirisi = {
    "AFRICA": "Afrikaanca",
    "ARGENTINA": "İspanyolca",
    "AUSTRALIA": "İngilizce",
    "BOSNIA AND HERZEGOVINA": "Boşnakça",
    "BRAZIL": "Portekizce",
    "BULGARIA": "Bulgarca",
    "CANADA": "İngilizce",
    "CHILE": "İspanyolca",
    "COLUMBIA": "İspanyolca",
    "CROATIA": "Hırvatça",
    "CYPRUS": "Yunanca",
    "DENMARK": "Danca",
    "EGYPT": "Arapça",
    "FRANCE": "Fransızca",
    "GERMANY": "Almanca",
    "GREECE": "Yunanca",
    "ICELAND": "İzlandaca",
    "INDIA": "Hintçe",
    "IRELAND": "İngilizce",
    "ISRAEL": "İbranice",
    "ITALY": "İtalyanca",
    "MALAYSIA": "Malayca",
    "MEXICO": "İspanyolca",
    "NETHERLANDS": "Felemenkçe",
    "NEW ZEALAND": "İngilizce",
    "OTHERS": "Çeşitli",
    "PAKISTAN": "Urduca",
    "POLAND": "Lehçe",
    "PORTUGAL": "Portekizce",
    "QATAR": "Arapça",
    "ROMANIA": "Romence",
    "RUSSIA": "Rusça",
    "SAUDI ARABIA": "Arapça",
    "SERBIA": "Sırpça",
    "SOUTH AFRICA": "İngilizce",
    "SPAIN": "İspanyolca",
    "SWEDEN": "İsveççe",
    "TURKEY": "Türkçe",
    "UNITED ARAB EMIRATES": "Arapça",
    "UNITED KINGDOM": "İngilizce",
    "UNITED STATES": "İngilizce",
    "URUGUAY": "İspanyolca"
}

def get_playlist_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Hata: URL'den veri alınamadı. Durum kodu: {response.status_code}")
            return None
    except Exception as e:
        print(f"Hata: {e}")
        return None

def create_tvg_id(channel_name, country):
   
    cleaned_name = re.sub(r'[^a-zA-Z0-9 ]', '', channel_name)
    cleaned_name = cleaned_name.replace(' ', '.').upper()
    
   
    country_code = ""
    for eng_country, tr_country in ulke_cevirisi.items():
        if tr_country == country:
            country_code = ulke_kisaltmalari.get(eng_country, "")
            break
    
    
    if not country_code:
        country_code = country[:2].upper() if country else "XX"
    
    
    tvg_id = f"{cleaned_name}.{country_code}"[:50]
    return tvg_id

def parse_m3u(content):
    lines = content.strip().split('\n')
    channels = []
    i = 0
    while i < len(lines):
        if lines[i].startswith('#EXTINF'):
            info_line = lines[i]
            url_line = lines[i+1] if i+1 < len(lines) else ""
            
            channel_info = {}
            
            
            group_match = re.search(r'group-title="([^"]+)"', info_line)
            if group_match:
                group = group_match.group(1)
                channel_info['group'] = group
            
            
            name_match = re.search(r',([^,]+)$', info_line)
            if name_match:
                name = name_match.group(1).strip()
                channel_info['name'] = name
            
            
            lang_match = re.search(r'tvg-language="([^"]+)"', info_line)
            country_match = re.search(r'tvg-country="([^"]+)"', info_line)
            
            if lang_match:
                channel_info['language'] = lang_match.group(1)
            else:
                if group_match:
                    eng_country = group_match.group(1)
                    channel_info['language'] = dil_cevirisi.get(eng_country, "Bilinmeyen")
            
            if country_match:
                channel_info['country'] = country_match.group(1)
            else:
                if group_match:
                    eng_country = group_match.group(1)
                    channel_info['country'] = ulke_cevirisi.get(eng_country, eng_country)
            
            
            id_match = re.search(r'tvg-id="([^"]+)"', info_line)
            if id_match:
                current_id = id_match.group(1)
                if current_id.lower() == "test" or not current_id.strip():
                    
                    channel_info['id'] = create_tvg_id(
                        channel_info.get('name', 'Unknown'),
                        channel_info.get('country', '')
                    )
                else:
                    channel_info['id'] = current_id
            else:
                
                channel_info['id'] = create_tvg_id(
                    channel_info.get('name', 'Unknown'),
                    channel_info.get('country', '')
                )
            
            
            logo_match = re.search(r'tvg-logo="([^"]+)"', info_line)
            if logo_match:
                channel_info['logo'] = logo_match.group(1)
            
            channel_info['info_line'] = info_line
            channel_info['url'] = url_line
            
            channels.append(channel_info)
            i += 2
        else:
            i += 1
    
    return channels

def is_bein_sports(channel_name):
    return 'bein' in channel_name.lower() or 'beIN' in channel_name

def is_turkish_bein(channel):
    return is_bein_sports(channel['name']) and ('Turkey' in channel['name'] or 'Türkiye' in channel.get('country', ''))

def format_channel(channel):
    info_line = channel['info_line']
    
   
    if 'id' in channel:
        if re.search(r'tvg-id="[^"]+"', info_line):
            info_line = re.sub(r'tvg-id="[^"]+"', f'tvg-id="{channel["id"]}"', info_line)
        else:
            
            info_line = info_line.replace('#EXTINF:-1 ', f'#EXTINF:-1 tvg-id="{channel["id"]}" ')
    
    
    if 'language' in channel and not re.search(r'tvg-language="', info_line):
        info_line = info_line.replace('#EXTINF:-1 ', f'#EXTINF:-1 tvg-language="{channel["language"]}" ')
    
    if 'country' in channel and not re.search(r'tvg-country="', info_line):
        if 'tvg-language="' in info_line:
            info_line = info_line.replace('tvg-language="' + channel['language'] + '"', 
                                        'tvg-language="' + channel['language'] + '" tvg-country="' + channel['country'] + '"')
        else:
            info_line = info_line.replace('#EXTINF:-1 ', f'#EXTINF:-1 tvg-country="{channel["country"]}" ')
    
    if 'group' in channel and channel['group'] in ulke_cevirisi:
        tr_group = ulke_cevirisi[channel['group']] + " Kanalları"
        info_line = re.sub(r'group-title="[^"]+"', f'group-title="{tr_group}"', info_line)
    
    return info_line + '\n' + channel['url']

def main():
   
    url = "https://ES26-1-daddylive.hf.space/playlist/channels"
    content = get_playlist_from_url(url)
    
    if not content:
        print("İçerik alınamadı, işlem durduruldu.")
        return

    
    channels = parse_m3u(content)
    
    
    turkish_bein = [ch for ch in channels if is_turkish_bein(ch)]
    other_bein = [ch for ch in channels if is_bein_sports(ch['name']) and not is_turkish_bein(ch)]
    other_channels = [ch for ch in channels if not is_bein_sports(ch['name'])]
    
    
    other_channels.sort(key=lambda x: x.get('country', ''))
    
    
    sorted_channels = turkish_bein + other_bein + other_channels
    
    
    new_content = "#EXTM3U url-tvg=\"https://raw.githubusercontent.com/pigzillaaaaa/daddylive/refs/heads/main/epgs/daddylive-channels-epg.xml\"\n"
    for channel in sorted_channels:
        new_content += format_channel(channel) + "\n"
    
    
    filtered_m3u_path = 'daddylive.m3u'
    try:
        with open(filtered_m3u_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Filtrelenmiş M3U dosyası başarıyla oluşturuldu: {filtered_m3u_path}")
    except Exception as e:
        print(f"Dosya yazma hatası: {e}")

if __name__ == "__main__":
    main()
