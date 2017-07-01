from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.orm import sessionmaker


class DatabaseConnection():
    def __init__(self, db_path):
        engine = create_engine("sqlite:///%s" % db_path, echo=False)
        metadata = MetaData(engine)
        self.Session = sessionmaker(bind=engine)

        # define table objects
        self.Cluster = Table('cluster', metadata, autoload=True)
        self.ClusterTypeLookupTable = Table('cluster_type_lookup_table', metadata, autoload=True)

        self.Stops = Table('stops', metadata, autoload=True)
        self.PlaceType = Table('place_type', metadata, autoload=True)

        self.Movement = Table('movement', metadata, autoload=True)
        self.TravelMode = Table('travelMode', metadata, autoload=True)
        self.MovementLocation = Table('movementLocation', metadata, autoload=True)
        self.Locations = Table('locations', metadata, autoload=True)

        self.Questionnaire = Table('questionnaire_results', metadata, autoload=True)


