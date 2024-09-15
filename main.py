import requests
import time

def load_proxies(filename):
    with open(filename, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

def fetch_wallet_data(wallet_address, proxy, counters):
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

                if rank < 50000:
                    counters['rank_50k'] += 1
                    counters['total_rank_100k'] += 1
                elif 50000 <= rank < 100000:
                    counters['rank_50k_100k'] += 1
                    counters['total_rank_100k'] += 1

                if top_percent < 5:
                    counters['top_5'] += 1
                    counters['total_10'] += 1
                elif 5 <= top_percent < 10:
                    counters['top_5_10'] += 1
                    counters['total_10'] += 1

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

counters = {
    'rank_50k': 0,
    'rank_50k_100k': 0,
    'total_rank_100k': 0,
    'top_5': 0,
    'top_5_10': 0,
    'total_10': 0
}

with open(wallets_file, 'r') as file:
    wallets = [line.strip() for line in file if line.strip()]

for wallet in wallets:
    if proxies:
        for proxy in proxies:
            fetch_wallet_data(wallet, proxy, counters)
            time.sleep(1)
            break
    else:
        print("No proxies found.")
        break

print("\nFinal Results:")
print(f"Rank < 50,000: {counters['rank_50k']}")
print(f"Rank 50,000 - 100,000: {counters['rank_50k_100k']}")
print(f"\nTop < 5%: {counters['top_5']}")
print(f"Top 5% - 10%: {counters['top_5_10']}")
print(f"\nTotal < 100,000: {counters['total_rank_100k']}")
print(f"Total < 10%: {counters['total_10']}")
