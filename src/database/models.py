from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer, String, Date, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Contact(Base):
    __tablename__ = 'contacts'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    additional_info: Mapped[str] = mapped_column(Text, nullable=True)


