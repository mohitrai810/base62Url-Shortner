from app.db.database import SessionLocal
from app.services.url_service import create_short_url


def main():
    long_url = input("Enter long URL: ")

    db = SessionLocal()

    try:
        url = create_short_url(db, long_url)

        print()
        print("ID:", url.id)
        print("Short code:", url.short_code)
        print("Long URL:", url.long_url)
        print("Short URL:", f"http://localhost:8000/{url.short_code}")

    finally:
        db.close()


if __name__ == "__main__":
    main()