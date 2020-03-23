"""Product orm model module"""
import orm
import sqlalchemy

METADATA = sqlalchemy.MetaData()


class Product(orm.Model):  # pylint: disable=too-many-ancestors
    """Product orm model. This table store what product are processed in the past."""
    __tablename__ = "product"
    __metadata__ = METADATA

    id = orm.Integer(primary_key=True)
