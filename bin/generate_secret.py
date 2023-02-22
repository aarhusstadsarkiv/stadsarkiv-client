#!/usr/bin/env python
import secrets

# Generate a secret key for use in the app
if __name__ == "__main__":
    print(secrets.token_hex(32))
