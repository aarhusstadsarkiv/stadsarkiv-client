import httpx
import asyncio


async def verify_token(token):
    http_path = "https://demo.openaws.dk"
    # http_path = "http://localhost:5555"
    url = f"{http_path}/webhook/mail/token/verify"
    headers = {"Content-Type": "application/json"}
    payload = {"token": token}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            response.raise_for_status()

            data = response.json()
            print("Response data:", data)

    except httpx.HTTPStatusError as http_error:
        print(f"HTTP error occurred: {http_error}")
    except Exception as error:
        print(f"An error occurred: {error}")


asyncio.run(verify_token("some-test-token"))