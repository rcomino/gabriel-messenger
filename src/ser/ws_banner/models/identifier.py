"""Product orm model Model."""

import orm
import sqlalchemy

METADATA = sqlalchemy.MetaData()


class Identifier(orm.Model):  # pylint: disable=too-many-ancestors
    """Product orm model. This model store what product are processed in the past."""
    __tablename__ = "identifier"
    __metadata__ = METADATA

    id = orm.Text(primary_key=True)
