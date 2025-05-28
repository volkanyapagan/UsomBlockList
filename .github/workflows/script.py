
import requests
import re

URL = "https://www.usom.gov.tr/url-list.txt"

def is_ip(line):
    return re.match(r"^\\d{1,3}(\\.\\d{1,3}){3}$", line.strip())

def main():
    response = requests.get(URL)
    lines = response.text.strip().splitlines()

    ip_list = []
    domain_list = []

    for line in lines:
        clean_line = line.strip()
        if not clean_line:
            continue
        if is_ip(clean_line):
            ip_list.append(clean_line)
        else:
            domain_list.append(clean_line)

    with open("UsomIPBlockList.txt", "w") as f:
        f.write("\n".join(ip_list))

    with open("UsomDomainBlockList.txt", "w") as f:
        f.write("\n".join(domain_list))

if __name__ == "__main__":
    main()
