from faker import Faker
from sqlalchemy.orm import Session

from src.database.connect import SessionLocal
from src.database.models import Contact
from src.schemas import ContactModel

fake = Faker()
database = SessionLocal()


def create_contacts(body: ContactModel, db: Session = database):
    contact = Contact(**body.dict())
    print(contact, db)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


if __name__ == "__main__":
    for _ in range(100):
        random_contact = ContactModel(
            name=fake.first_name(),
            surname=fake.last_name(),
            email=fake.email(),
            phone=fake.msisdn(),
            birthday=fake.date(),
            additionally=fake.paragraph(nb_sentences=2),
        )
        create_contacts(body=random_contact, db=database)
