"""Tworzy pierwsze konto MANAGEMENT.
Użycie na serwerze: docker compose exec backend python create_admin.py
"""
import getpass
import sys

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.forecast import Forecast  # noqa: F401 (wymagane przez relację User -> Forecast)
from app.models.user import User, UserRole


def main():
    email = input("Email: ").strip().lower()
    full_name = input("Imię i nazwisko: ").strip()
    password = getpass.getpass("Hasło (min. 12 znaków): ")
    if len(password) < 12 or password != getpass.getpass("Powtórz hasło: "):
        sys.exit("Hasło za krótkie lub hasła się różnią.")

    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == email).first():
            sys.exit("Użytkownik o takim emailu już istnieje.")
        db.add(User(
            email=email,
            full_name=full_name,
            hashed_password=get_password_hash(password),
            role=UserRole.MANAGEMENT,
        ))
        db.commit()
        print(f"Utworzono konto MANAGEMENT: {email}")
    finally:
        db.close()


if __name__ == "__main__":
    main()