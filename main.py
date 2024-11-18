import requests
import time
import logging
from retrying import retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("coin_trading.log"),
        logging.StreamHandler()
    ]
)

# Constants
AMOUNT = 0.2  # Replace with your desired amount in sol
TARGET_WALLET = "WALLET TO MONITOR"
WALLET = "YOUR WALLET FROM MEVX"
TOKEN = "AUTH TOKEN FROM MEVX"
BUY_COIN_URL = "https://api-fe.mevx.io/api/trade/buy"  # API endpoint for buying coins

HEADERS = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "authorization": f"Bearer {TOKEN}",
    "content-type": "application/json",
    "origin": "https://mevx.io",
    "priority": "u=1, i",
    "referer": "https://mevx.io/",
    "sec-ch-ua": '"Chromium";v="130", "Microsoft Edge";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.0.0",
}


@retry(stop_max_attempt_number=3, wait_fixed=500)
def get_first_pool_id(token_address):
    """
    Fetch the first pool ID for a given token address.
    Retries up to 3 times if an error occurs.
    """
    url = f"https://api.mevx.io/api/v1/pools/{token_address}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    pools = response.json()
    if pools:
        logging.info(f"Found pool for token {token_address}: {pools[0]['poolId']}")
        return pools[0]["poolId"]
    logging.warning(f"No pools found for token address: {token_address}")
    return None


@retry(stop_max_attempt_number=3, wait_fixed=500)
def buy_coin(address, pool_id, amount, chain="sol", ref_code=""):
    """
    Send a request to buy a coin.
    Retries up to 3 times if an error occurs.
    """
    payload = {
        "addresses": [address],
        "poolId": pool_id,
        "amount": amount,
        "chain": chain,
        "refCode": ref_code,
    }
    response = requests.post(BUY_COIN_URL, headers=HEADERS, json=payload)
    response.raise_for_status()
    data = response.json()
    if data.get("data", {}).get("transactions", [{}])[0].get("code") == -1:
        logging.error("Insufficient balance for transaction.")
        return None
    logging.info(f"Successfully purchased coin: {data}")
    return data


def fetch_and_buy_new_coins(last_checked_timestamp):
    """
    Fetch new coin listings and attempt to buy.
    """
    API_URL = f"https://frontend-api.pump.fun/coins/user-created-coins/{TARGET_WALLET}"
    params = {"offset": 0, "limit": 10, "includeNsfw": "true"}

    try:
        response = requests.get(API_URL, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching coin listings: {e}")
        return last_checked_timestamp

    for coin in data:
        if coin.get("created_timestamp", 0) > last_checked_timestamp:
            start_time = time.time_ns() // 1_000_000  # Start time in milliseconds

            # Extract token address and fetch pool ID
            address = coin.get("mint")
            if address:
                pool_id = get_first_pool_id(address)
                if pool_id:
                    buy_coin(WALLET, address, AMOUNT)
                    end_time = time.time_ns() // 1_000_000  # End time in milliseconds
                    elapsed_time = end_time - start_time
                    logging.info(f"Time from spotting to buying: {elapsed_time} ms")
                else:
                    logging.warning(f"No valid pool ID found for address: {address}")
            else:
                logging.warning(f"Skipping coin due to missing mint address: {coin}")

    # Update the last checked timestamp
    return max((coin.get("created_timestamp", last_checked_timestamp) for coin in data), default=last_checked_timestamp)


def main():
    """
    Main loop to continuously check for new coins and buy them.
    """
    last_checked_timestamp = int(time.time() * 1000)

    try:
        while True:
            last_checked_timestamp = fetch_and_buy_new_coins(last_checked_timestamp)
            time.sleep(1)  # Adjust polling interval for speed
    except KeyboardInterrupt:
        logging.info("Script terminated by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
