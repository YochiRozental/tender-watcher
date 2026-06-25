import requests

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "text/html,application/pdf,*/*",
    "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
}


def is_url_accessible(url: str) -> bool:
    try:
        response = requests.get(
            url,
            timeout=20,
            allow_redirects=True,
            headers=HEADERS,
            stream=True,
        )

        if response.status_code >= 400:
            print(f"קישור חסום או לא תקין ({response.status_code}): {url}")
            return False

        return True

    except requests.RequestException as error:
        print(f"שגיאה בבדיקת קישור: {url} | {error}")
        return False
