#!/usr/bin/env python3
import sys
from tldextract.tldextract import extract

def extract_fqdn(fqdn):
    parts = extract(fqdn)
    if parts.subdomain == '' or parts.subdomain == None:
        return f"{parts.domain}.{parts.suffix}"

    return f"{parts.subdomain}.{parts.domain}.{parts.suffix}"


def list_from_file(filename):
    with open(filename) as file:
        sites = set()
        while (line := file.readline().rstrip()):
            reflow = extract_fqdn(line)
            sites.add(reflow)
    return sites



feed = list_from_file(sys.argv[1])

for site in feed:
    print(site)
