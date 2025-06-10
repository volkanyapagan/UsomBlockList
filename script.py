import requests
import re

# USOM verisini al
url = "https://www.usom.gov.tr/url-list.txt"
response = requests.get(url)
data = response.text

# IP ve domain regex
ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
domain_pattern = re.compile(
    r"^(?!:\/\/)([a-zA-Z0-9-_]+\.)+[a-zA-Z]{2,11}$"  # sade domain (www.example.com gibi)
)

# Ayıklanmış listeler
ip_list = []
domain_list = []

# Verileri satır satır ayıkla
for line in data.splitlines():
    entry = line.strip().split(";")[0].strip()  # URL kısmı
    entry = entry.replace("http://", "").replace("https://", "").split("/")[0]  # sadece host

    if ip_pattern.match(entry):
        ip_list.append(entry)
    elif domain_pattern.match(entry):
        domain_list.append(entry)

# IP adreslerini dosyaya yaz (tek dosya)
with open("UsomIPBlockList.txt", "w", encoding="utf-8") as ip_file:
    ip_file.write("\n".join(sorted(set(ip_list))))

# Domainleri 4 parçaya bölerek yaz
chunk_size = 100000
sorted_domains = sorted(set(domain_list))

for i in range(4):
    start = i * chunk_size
    end = start + chunk_size
    chunk = sorted_domains[start:end]
    filename = f"UsomDomainBlockList_Part{i + 1}.txt"
    with open(filename, "w", encoding="utf-8") as domain_file:
        domain_file.write("\n".join(chunk))
