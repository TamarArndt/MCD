from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker


class DatabaseConnection():
    def __init__(self, db_path):
        engine = create_engine("sqlite:///%s" % db_path, echo=False)

        list = ['cluster', 'cluster_type_lookup_table',
                'stops', 'place_type',
                'movement', 'travelMode', 'movementLocation', 'locations',
                'questionnaire_results']
        metadata = MetaData(bind=engine)
        metadata.reflect(engine, only=list)

        Base = automap_base(metadata=metadata)
        Base.prepare()

        self.Cluster = Base.classes.cluster
        self.ClusterTypeLookupTable = Base.classes.cluster_type_lookup_table
        self.Stops = Base.classes.stops
        self.PlaceType = Base.classes.place_type
        self.Movement = Base.classes.movement
        self.TravelMode = Base.classes.travelMode
        self.MovementLocation = Base.classes.movementLocation
        self.Locations = Base.classes.locations
        self.QuestionnaireResults = Base.classes.questionnaire_results

        self.Session = sessionmaker(bind=engine)


