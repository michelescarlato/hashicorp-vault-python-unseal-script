import hvac

# Vault server address and port
VAULT_ADDR = "http://127.0.0.1:8200"

# AppRole credentials
ROLE_ID = "fc9183ca-c665-9c43-1508-c9e8da5f6c3b"  # Replace with your actual Role ID
SECRET_ID = "e48b63a9-6b87-ef27-1508-eed964736781"  # Replace with your actual Secret ID

# Initialize the Vault client
client = hvac.Client(url=VAULT_ADDR)

# Authenticate using AppRole
auth_response = client.auth.approle.login(
    role_id=ROLE_ID,
    secret_id=SECRET_ID
)

# Check if authenticated
if client.is_authenticated():
    print("Authenticated successfully!")

    # Retrieve the secret
    try:
        secret = client.secrets.kv.v2.read_secret_version(path="my-secret",
                                                          raise_on_deleted_version=True)
        print("Retrieved secret:", secret["data"]["data"]["value"])
    except hvac.exceptions.InvalidPath as e:
        print("Invalid path. Ensure the secret exists at the specified location.")
    except Exception as e:
        print("Failed to retrieve the secret:", e)
else:
    print("Failed to authenticate.")

