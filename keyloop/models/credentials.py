import sqlalchemy as sa

import cryptacular.bcrypt
from sqlalchemy import CheckConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableDict

from .base import Base

__all__ = [
    "Credential",
]

bcrypt = cryptacular.bcrypt.BCRYPTPasswordManager()


class Credential(Base):
    __tablename__ = "credentials"

    def __init__(self, *args, **kwargs):
        password = kwargs.pop("password", None)
        super(Credential, self).__init__(*args, **kwargs)
        if password:
            self.password = password

    email = sa.Column(sa.Text, unique=True, nullable=True)
    _password = sa.Column(sa.Text, nullable=False)
    name = sa.Column(sa.Text)
    username = sa.Column(sa.Text, unique=True, nullable=True)
    msisdn = sa.Column(sa.Text, nullable=True)
    citizen_id = sa.Column(sa.Text, nullable=True)
    _metadata = sa.Column(MutableDict.as_mutable(JSONB), nullable=True, default=dict)

    def _set_password(self, value):
        self._password = bcrypt.encode(value)

    password = property(fset=_set_password)

    def password_check(self, value):
        return bcrypt.check(self._password, value)

    __table_args__ = (
        CheckConstraint("coalesce(email , username, msisdn, citizen_id ) is not null"),
    )
