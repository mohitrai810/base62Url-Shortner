from sqlalchemy.orm import Session

from app.models.url import URL
from app.services.base62 import encode


def create_short_url(db: Session, long_url: str) -> URL:
    url = URL(
        long_url=long_url,
        short_code="",
    )

    db.add(url)
    db.flush()

    url.short_code = encode(url.id)

    db.commit()
    db.refresh(url)

    return url