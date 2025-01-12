import requests
import json
import time

# Vault server address
VAULT_ADDRESS = "http://localhost:8200"

# Path to unseal keys
UNSEAL_KEYS_FILE = "/etc/vault.d/unseal_keys.json"


# Function to load unseal keys from a file
def load_unseal_keys():
    with open(UNSEAL_KEYS_FILE, 'r') as file:
        data = json.load(file)
    return data["keys"]


# Function to unseal Vault
def unseal_vault():
    keys = load_unseal_keys()
    for key in keys:
        response = requests.put(f"{VAULT_ADDRESS}/v1/sys/unseal", json={"key": key})
        if response.status_code == 200:
            print("Unseal step successful")
        else:
            print("Error in unsealing step:", response.json())
            return
    # Check if Vault is already unsealed
    if not requests.get(f"{VAULT_ADDRESS}/v1/sys/seal-status").json()["sealed"]:
        print("Vault is unsealed.")
        return
    print("All keys applied, Vault should be unsealed now.")


# Function to check if Vault is sealed
def is_vault_sealed():
    response = requests.get(f"{VAULT_ADDRESS}/v1/sys/seal-status")
    return response.json()["sealed"]


# Main function to auto-unseal Vault
def main():
    # Wait until Vault is accessible
    while True:
        try:
            if not is_vault_sealed():
                print("Vault is already unsealed.")
                return
            print("Vault is sealed, starting unseal process...")
            unseal_vault()
            break
        except requests.exceptions.ConnectionError:
            print("Vault is not reachable, retrying in 5 seconds...")
            time.sleep(5)


if __name__ == "__main__":
    main()
