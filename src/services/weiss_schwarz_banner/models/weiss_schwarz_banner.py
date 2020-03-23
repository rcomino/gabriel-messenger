"""Product orm model Model."""
import orm
import sqlalchemy

METADATA = sqlalchemy.MetaData()


class WeissSchwarzBanner(orm.Model):  # pylint: disable=too-many-ancestors
    """Product orm model. This model store what product are processed in the past."""
    __tablename__ = "weiss_schwarz_banner"
    __metadata__ = METADATA

    id = orm.Text(primary_key=True)
