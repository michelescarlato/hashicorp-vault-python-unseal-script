On the Hashicorp Vault (1.18.2) server:

1. enable approle

```
~$ vault auth enable approle
Success! Enabled approle auth method at: approle/
```

2. create a policy in hashicorp language (hcl):

```
:~$ sudo nano /etc/vault.d/my-policy.hcl
path "secret/data/my-secret" {
  capabilities = ["create", "read", "update", "delete", "list"]
}
```

3. write the policy on vault:

```
:/etc/vault.d$ vault policy write my-policy my-policy.hcl
Success! Uploaded policy: my-policy
```

4. Enable key-value (kv) secret engine at a specific path:

```
$ vault secrets enable -path=secret -version=2 kv
Success! Enabled the kv secrets engine at: secret/
```

5. Check the secret engine version for the `secret/` path under the `Options` column.

```
$ vault secrets list -detailed
```

6. Store a secret message

```
$ vault kv put secret/my-secret value="This is a secret message!"
==== Secret Path ====
secret/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2025-01-12T03:33:39.675883661Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1
```

7. Retrieve the secret using `vault kv get`:

```
(venv) michelescarlato@shredder:~/hvac-hashicorp-vault$ vault kv get secret/my-secret
==== Secret Path ====
secret/data/my-secret

======= Metadata =======
Key                Value
---                -----
created_time       2025-01-12T03:33:39.675883661Z
custom_metadata    <nil>
deletion_time      n/a
destroyed          false
version            1

==== Data ====
Key      Value
---      -----
value    This is a secret message!
```

8. Retrieve it using python:
   
```
$ python3 retrieve_secret.py
Authenticated successfully!
Retrieved secret: This is a secret message!
```

NOTE: 

a. role-id is retrieved with:
```
:/etc/vault.d$ vault read auth/approle/role/my-role/role-id
Key        Value
---        -----
role_id    fc9183ca-c665-9c43-1608-c9e8da5f6c3b
```

b. Secret-id is created with:
```
$ vault write -f auth/approle/role/my-role/secret-id
Key                   Value
---                   -----
secret_id             e48b63a9-6b87-ef27-15e8-eed964736781
secret_id_accessor    30354010-6b95-caf0-e250-5d3856a674b7
secret_id_num_uses    0
secret_id_ttl         24h
```

b1. To increase the TTL of the secret-id:

```
vault write auth/approle/role/my-role secret_id_ttl=48h
```
Replace 48h with the desired TTL (e.g., 72h, 1w, etc.).

Check if the change took place:

```
vault read auth/approle/role/my-role
```

Create a new secret-id
```
vault write -f auth/approle/role/my-role/secret-id
```
e.g.
```
~/hvac-hashicorp-vault$ vault write -f auth/approle/role/my-role/secret-id
Key                   Value
---                   -----
secret_id             09bf0a40-a9e0-3dbd-d7dd-8f1915756436
secret_id_accessor    7e132493-2519-b13b-c7c3-b08e8a2140ba
secret_id_num_uses    0
secret_id_ttl         48h

```
Just use the new value for secret_id in the Python script, and the new TTL will be applied.








