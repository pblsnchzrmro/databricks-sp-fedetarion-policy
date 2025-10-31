#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import requests
import sys

def load_config(path: str ="config.json"):
    with open(path, "r") as f:
        config = json.load(f)
    return config

def exchange_token(cfg: dict) -> dict:
    url = f"{cfg['databricks_host']}/oidc/v1/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "client_id": cfg["databricks_client_id"],
        "subject_token": cfg["jwt"],
        "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
        "scope": "all-apis"
    }

    print(f"Requesting token exchange from {url}...\n")
    response = requests.post(url, headers=headers, data=data)

    print("Status code:", response.status_code)
    try:
        result = response.json()
        print(json.dumps(result, indent=2))
    except Exception:
        print(response.text)
        raise

    if response.status_code != 200:
        sys.exit("Token exchange failed.")
    return result


def validate_token(host: str, access_token: str) -> None:
    url = f"{host}/api/2.0/preview/scim/v2/Me"
    headers = {"Authorization": f"Bearer {access_token}"}
    print("\nValidating token against Databricks API...\n")
    response = requests.get(url, headers=headers)
    print("HTTP", response.status_code)
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception:
        print(response.text)

def main():
    cfg = load_config()
    token_data = exchange_token(cfg)
    access_token = token_data.get("access_token")

    if access_token:
        print("\nAccess token obtained successfully.\n")
        validate_token(cfg["databricks_host"], access_token)
    else:
        print("Warning: 'access_token' not found in Databricks response.")

if __name__ == "__main__":
    main()
