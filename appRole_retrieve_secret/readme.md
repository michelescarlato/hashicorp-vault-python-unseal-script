On the vault server:

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











