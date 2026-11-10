
import os
import sys
import requests

PAYPAL_API = "https://api-m.sandbox.paypal.com"
GEMINI_API = (
    "https://generativelanguage.googleapis.com/v1beta/"
    "models/gemini-3.1-flash-lite:generateContent"
)


def get_secret(name):
    value = os.getenv(name)

    if not value:
        try:
            from google.colab import userdata
            value = userdata.get(name)
        except (ImportError, Exception):
            pass

    if not value:
        raise RuntimeError(f"Missing credential: {name}")

    return value


def verify_payment(order_id):
    token_response = requests.post(
        f"{PAYPAL_API}/v1/oauth2/token",
        auth=(
            get_secret("PAYPAL_CLIENT_ID"),
            get_secret("PAYPAL_CLIENT_SECRET")
        ),
        data={"grant_type": "client_credentials"},
        timeout=20
    )
    token_response.raise_for_status()
    token = token_response.json()["access_token"]

    response = requests.get(
        f"{PAYPAL_API}/v2/checkout/orders/{order_id}",
        headers={"Authorization": f"Bearer {token}"},
        timeout=20
    )
    response.raise_for_status()

    order = response.json()

    captures = [
        capture
        for unit in order.get("purchase_units", [])
        for capture in unit.get(
            "payments", {}
        ).get("captures", [])
    ]

    return (
        order.get("id") == order_id
        and order.get("status") == "COMPLETED"
        and any(
            capture.get("status") == "COMPLETED"
            and capture.get("amount", {}).get("value") == "1.00"
            and capture.get("amount", {}).get("currency_code") == "USD"
            for capture in captures
        )
    )


def generate_passport(analysis):
    response = requests.post(
        GEMINI_API,
        headers={
            "x-goog-api-key": get_secret("GEMINI_API_KEY"),
            "Content-Type": "application/json"
        },
        json={
            "contents": [{
                "parts": [{
                    "text": (
                        "You are CodeGraph AI. Generate a "
                        "professional Smart Code Passport "
                        "based only on this repository "
                        "analysis. Explain important files, "
                        "relationships, and suggest three "
                        "improvements. Do not invent "
                        "security findings.\n\n"
                        + analysis
                    )
                }]
            }]
        },
        timeout=60
    )
    response.raise_for_status()

    return response.json()[
        "candidates"
    ][0]["content"]["parts"][0]["text"]


def main():
    if len(sys.argv) != 3:
        print(
            "Usage: python smart_passport.py "
            "ORDER_ID ANALYSIS_FILE"
        )
        return

    order_id = sys.argv[1]
    analysis_file = sys.argv[2]

    if not verify_payment(order_id):
        print("LOCKED: Verified payment required.")
        return

    with open(analysis_file, encoding="utf-8") as file:
        analysis = file.read()

    passport = generate_passport(analysis)

    print("PREMIUM SMART CODE PASSPORT UNLOCKED")
    print(passport)


if __name__ == "__main__":
    main()
