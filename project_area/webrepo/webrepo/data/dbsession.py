import sqlalchemy
import sqlalchemy.orm
from webrepo.data.modelbase import SqlAlchemyBase
# noinspection PyUnresolvedReferences
import webrepo.data.album
# noinspection PyUnresolvedReferences
import webrepo.data.track
# noinspection PyUnresolvedReferences
import webrepo.data.account
# noinspection PyUnresolvedReferences
import webrepo.data.passwordreset


class DbSessionFactory:
    factory = None

    @staticmethod
    def global_init(db_file):
        # If DbSessionFactory already exists, don't run this again
        if DbSessionFactory.factory:
            return

        if not db_file:
            raise Exception("You must specify a data file.")

        conn_str = "sqlite:///" + db_file
        print("Connecting to db with conn string: {}".format(conn_str))

        engine = sqlalchemy.create_engine(conn_str, echo=False)
        SqlAlchemyBase.metadata.create_all(engine)
        DbSessionFactory.factory = sqlalchemy.orm.sessionmaker(bind=engine)

    @staticmethod
    def create_session():
        return DbSessionFactory.factory()

