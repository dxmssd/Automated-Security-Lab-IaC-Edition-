import requests
from bs4 import BeautifulSoup
import json
import ipaddress
import random
import time

# 1. FUNCTION TO FIND THE MOST RECENT DOWNLOAD LINK
def get_latest_azure_url():
    # This is the official Microsoft download landing page
    download_page = "https://www.microsoft.com/en-us/download/details.aspx?id=56519"
    try:
        response = requests.get(download_page)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Search for the anchor tag containing the .json file link
        for link in soup.find_all('a'):
            url = link.get('href')
            if url and '.json' in url:
                return url
        return None
    except Exception as e:
        print(f"[X] Error searching for the link: {e}")
        return None

# 2. FUNCTION TO PROCESS AZURE IP RANGES
def scan_azure_network():
    url = get_latest_azure_url()
    if not url:
        # Fallback link in case scraping fails
        url = "https://download.microsoft.com/download/7/1/D/71D86715-5596-4529-9B13-DA13A5DE5B63/ServiceTags_Public_20251208.json"

    print(f"[*] Downloading IP database from: {url}")
    
    try:
        data = requests.get(url).json()
        
        # Filtering for specific region prefixes
        azure_ranges = []
        for region in data['values']:
            if "eastus2" in region['name']:
                azure_ranges.extend(region['properties']['addressPrefixes'])
        
        print(f"[+] Network map loaded! {len(azure_ranges)} segments found in East US 2.")
        print("-" * 50)

        # 3. SCANNING SIMULATION
        # Testing 40 random IPs from the gathered ranges
        for _ in range(40): 
            random_segment = random.choice(azure_ranges)
            network = ipaddress.ip_network(random_segment)
            
            # Get the first usable host IP from the segment
            target_ip = str(next(network.hosts())) 
            
            print(f"   [Scanning] IP: {target_ip} | Port: 22 (SSH) | Status: TIMEOUT")
            time.sleep(0.4)

        print("-" * 50)
        print("[!] SIMULATION COMPLETED")
        print("[*] Note: In a real-world attack, if an IP responds, the bot automatically triggers the Brute Force module.")

    except Exception as e:
        print(f"[X] Error during execution: {e}")

if __name__ == "__main__":
    scan_azure_network()