import requests
import time
import pandas as pd
from tabulate import tabulate
from dune_client.client import DuneClient  # Import DuneClient from dune_client

# Dune API key and query ID
DUNE_API_KEY = "oAgSGElXrvOPJgmhefc75CDIC1OylnTe"  # Replace with your actual API key
DUNE_QUERY_ID = 3536881

# Initialize DuneClient
dune = DuneClient(DUNE_API_KEY)

# List of wallets to track
WALLETS = [
    "3wr7N8qQmGBz8jiicoC3634QCuYfmjLjyAidg9YnUaFq",
    "3wr7N8qQmGBz8jiicoC3634QCuYfmjLjyAidg9YnUaFq",
    "6rXTgb8dp7FaavXt11qjRd9KzGHzCJtgBxupo9phS4Sg",
    "3dNTS4e2pwtQsTLgdKNm3p6vVijAfM6c57EajDY4zrpt",
    "4kWbtFRCoJFgbMpFqBzKYN3MsFcUwaL8t1ysB6ADq2ye"
]

# Solana RPC endpoint
RPC_URL = "https://api.mainnet-beta.solana.com"

def fetch_dune_data():
    """Fetch the latest result from Dune using DuneClient."""
    try:
        # Fetch the latest result using the DuneClient
        query_result = dune.get_latest_result(DUNE_QUERY_ID)
        
        # Print the entire query result to understand its structure
        print("Dune query result structure:", query_result)
        
        # Try accessing the result data based on what the structure shows
        data = query_result  # Adjust this line if you see a specific attribute holding the data
        print("Dune Analytics data fetched successfully.")
        return pd.DataFrame(data)
    except Exception as e:
        print(f"Failed to fetch data from Dune API: {e}")
        return pd.DataFrame()


# Function to get recent transactions for a specific wallet
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

def get_top_tokens():
    """Fetch top-performing tokens from Dexscreener."""
    url = "https://api.dexscreener.com/token-boosts/latest/v1"  # Adjust with Dexscreener's actual API
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        print(data[0]["tokenAddress"])
        return None  # Get top 10 tokens
    else:
        print("Failed to fetch top tokens from Dexscreener.")
        return []

# Function to track and display transactions with Solscan links
def track_wallets():
    """Monitor and display recent transactions for tracked wallets."""
    print("Tracking wallets...\n")
    
    while True:
        dune_data = fetch_dune_data()
        get_top_tokens()
        
        for wallet in WALLETS:
            transactions = get_transactions(wallet)
            
            print(f"\nTransactions for Wallet: {wallet}")
            for tx in transactions:
                signature = tx['signature']
                slot = tx['slot']
                
                # Generate a Solscan link for the transaction
                solscan_link = f"https://solscan.io/tx/{signature}?cluster=mainnet"
                
                # Display transaction details with a clickable Solscan link
                print(f"  - Signature: {signature}, Slot: {slot}")
                print(f"    Solscan: {solscan_link}")
        
        # Display Dune Analytics data if available
        if not dune_data.empty:
            print("\nDune Analytics Data:")
            print(tabulate(dune_data, headers="keys", tablefmt="pretty"))  # Using tabulate for a styled table
        
        print("\nWaiting for the next poll...\n")
        time.sleep(60)  # Polling interval (in seconds)

if __name__ == "__main__":
    track_wallets()
