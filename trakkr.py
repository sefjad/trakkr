import requests
import time


WALLETS = [
    "6ejbdRMhgkdMDZmDyZKJMjyL41wef8vYM13AWg8JfwwwhhG",
    "7SynfTQzCVuU6YhpbaVQzHFWjnmN4sTcjaot63Nm7wwwzGz",
    "EccxYg7rViwYfn9EMoNu7sUaV82QGyFt6ewiQaH1GwwwYjv"
]

r
RPC_URL = "https://api.mainnet-beta.solana.com"

def get_transactions(wallet, limit=10):
    """Fetch recent transactions for a specific wallet."""
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getConfirmedSignaturesForAddress2",
        "params": [wallet, {"limit": limit}]
    }
    response = requests.post(RPC_URL, json=payload)
    if response.status_code == 200:
        return response.json().get("result", [])
    else:
        print(f"Failed to fetch transactions for {wallet}")
        return []

def track_wallets():
    """Monitor and display recent transactions for tracked wallets."""
    print("Tracking wallets...\n")
    while True:
        for wallet in WALLETS:
            transactions = get_transactions(wallet)
            print(f"\nTransactions for Wallet: {wallet}")
            for tx in transactions:
                print(f"  - Signature: {tx['signature']}, Slot: {tx['slot']}")
        print("\nWaiting for the next poll...\n")
        time.sleep(60)  

if __name__ == "__main__":
    track_wallets()
