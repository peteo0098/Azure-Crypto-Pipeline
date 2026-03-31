import azure.functions as func
import requests
import json
import os
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential
from datetime import datetime

app = func.FunctionApp()

@app.timer_trigger(schedule="0 0 * * * *", arg_name="myTimer", run_on_startup=True, use_monitor=False) 
def CryptoToBronze(myTimer: func.TimerRequest) -> None:
    
    # 1. Konfigurácia
    url = "https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids=bitcoin,ethereum,solana"
    storage_account_name = "cryptodatalake2026"
    container_name = "crypto-data"
    
    print(f"Spúšťam funkciu CryptoToBronze o {datetime.now()}")

    try:
        # 2. Získanie dát z API
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        print("Dáta z CoinGecko úspešne stiahnuté.")

        # 3. Pripojenie k Azure Storage
        account_url = f"https://{storage_account_name}.blob.core.windows.net"
        token_credential = DefaultAzureCredential()
        blob_service_client = BlobServiceClient(account_url, credential=token_credential)
        
        # 4. Kontrola/Vytvorenie kontajnera
        container_client = blob_service_client.get_container_client(container_name)
        try:
            if not container_client.exists():
                container_client.create_container()
                print(f"Kontajner '{container_name}' bol vytvorený.")
        except Exception as e:
            print(f"Poznámka: Nepodarilo sa overiť/vytvoriť kontajner (možno chýbajú práva): {e}")

        # 5. Definícia cesty a upload
        filename = f"bronze/crypto_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        blob_client = blob_service_client.get_blob_client(container=container_name, blob=filename)
        
        blob_client.upload_blob(json.dumps(data), overwrite=True)
        print(f"Úspešne nahraté do Data Lake: {filename}")

    except requests.exceptions.HTTPError as http_err:
        print(f"API Chyba (CoinGecko): {http_err}")
    except Exception as e:
        print(f"Kritická chyba pri behu funkcie: {e}")
