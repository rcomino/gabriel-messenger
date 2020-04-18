import orm
import sqlalchemy

METADATA = sqlalchemy.MetaData()


class Identifier(orm.Model):  # pylint: disable=too-many-ancestors
    """Indetifier orm model. This table store what product was processed in the past."""
    __tablename__ = "identifier"
    __metadata__ = METADATA

    id = orm.Text(primary_key=True)
