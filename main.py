import requests
import time

def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def fetch_wallet_data(wallet_address, proxy):
    url = f"https://layerhub.xyz/be-api/protocol_wallets/movement/{wallet_address}"
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}"
    }
    retry_attempts = 3
    
    for attempt in range(retry_attempts):
        try:
            response = requests.get(url, proxies=proxies)
            if response.status_code == 200:
                data = response.json()
                
                top_percent = data["walletPerformance"]["topPercent"]
                better_than = data["walletPerformance"]["betterThan"]
                total_count = data["walletPerformance"]["totalCount"]
                
                rank = int(total_count - better_than)
                
                print(f"Wallet: {wallet_address} | Top: {top_percent:.2f}% | Rank: {rank}")
                break
            
            elif response.status_code == 429:
                print(f"Rate limit exceeded for wallet: {wallet_address}. Retrying in 10 seconds...")
                time.sleep(10)

            elif response.status_code == 500:
                print(f"Wallet: {wallet_address} | Not participated")
                break

            else:
                print(f"Failed to fetch data for wallet: {wallet_address}. Status Code: {response.status_code}")
                break

        except requests.exceptions.RequestException as e:
            print(f"Request failed for wallet: {wallet_address}. Error: {e}")
            break

        if attempt < retry_attempts - 1:
            time.sleep(3)

wallets_file = 'wallets.txt'
proxies_file = 'proxies.txt'

wallets = []
proxies = load_proxies(proxies_file)

with open(wallets_file, 'r') as file:
    wallets = [line.strip() for line in file if line.strip()]

for wallet in wallets:
    if proxies:
        for proxy in proxies:
            fetch_wallet_data(wallet, proxy)
            time.sleep(1)
            break
    else:
        print("No proxies found.")
        break