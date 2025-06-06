import requests
import pandas as pd
import sqlite3
import logging
from datetime import datetime

API_URL = "https://api.tradedoubler.com/1.0/products.json;page=1;pageSize=100;fid=20968?token=92D3529CA3144687BF4A2CA750EAAD9993033983"
DB_PATH = "products.db"
LOG_FILE = "product_pipeline_log.txt"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def fetch_products(api_url):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        logging.info("Data hämtad från API.")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Fel vid hämtning av data från API: {e}")
        return None

def process_products(data):
    try:
        rows = []
        for product in data.get('products', []):
            price_raw = product.get("price", 0)
            try:
                price = float(str(price_raw).replace(",", "."))
            except (ValueError, TypeError):
                logging.warning(f"Felaktigt prisformat: {price_raw}, sätts till 0.0")
                price = 0.0

            rows.append({
                "productId": product.get("productId"),
                "name": product.get("name"),
                "price": price,
                "currency": product.get("currency"),
                "updated": datetime.now().isoformat()
            })
        logging.info(f"{len(rows)} produkter bearbetade.")
        return pd.DataFrame(rows)
    except Exception as e:
        logging.error(f"Fel vid bearbetning av produkter: {e}")
        return pd.DataFrame()

def save_to_sqlite(df, db_path=DB_PATH):
    try:
        with sqlite3.connect(db_path) as conn:
            df.to_sql("products", conn, if_exists="replace", index=False)
        logging.info(f"{len(df)} produkter sparade till databasen.")
    except Exception as e:
        logging.error(f"Fel vid skrivning till SQLite: {e}")

def main():
    logging.info("Produkt-pipeline startad.")
    data = fetch_products(API_URL)
    if not data:
        logging.warning("Ingen data att behandla.")
        return

    df = process_products(data)
    if not df.empty:
        save_to_sqlite(df)
    else:
        logging.warning("Ingen giltig produktdata att spara.")
    logging.info("Produkt-pipeline avslutad.")

if __name__ == "__main__":
    main()
