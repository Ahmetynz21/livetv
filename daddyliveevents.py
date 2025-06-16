import re
from urllib.request import urlopen
from collections import defaultdict


url = "https://ES26edt-daddyliveevents.hf.space/playlist/events"
response = urlopen(url)
data = response.read().decode("utf-8")

entries = re.findall(r'(#EXTINF:[\s\S]*?)(?=\n#EXTINF:|\Z)', data)


def get_group_title(entry):
    match = re.search(r'group-title="([^"]+)"', entry)
    return match.group(1) if match else "Unknown"


def get_title(entry):
    match = re.search(r',(.+)', entry)
    return match.group(1).strip() if match else ""


def replace_logo(entry):
    old_logo = "https://raw.githubusercontent.com/pigzillaaaaa/iptv-scraper/main/imgs/cfl-logo.png"
    new_logo = "https://raw.githubusercontent.com/pigzillaaaaa/iptv-scraper/refs/heads/main/imgs/cfb-logo.png"
    return entry.replace(old_logo, new_logo)


groups = defaultdict(list)
for entry in entries:
    entry = replace_logo(entry)  
    group = get_group_title(entry)
    groups[group].append(entry)


for group in groups:
    groups[group] = sorted(groups[group], key=get_title)



header = '#EXTM3U url-tvg="https://raw.githubusercontent.com/pigzillaaaaa/daddylive/refs/heads/main/epgs/daddylive-events-epg.xml"\n\n'

sorted_content = header
for group in sorted(groups.keys()):
    sorted_content += "\n".join(groups[group]) + "\n"


with open("daddyliveevents.m3u", "w", encoding="utf-8") as f:
    f.write(sorted_content)

print("daddylive.m3u dosyası kontrol edildi")
