import geopy.distance, datetime
from database import spatiaquery
from sqlalchemy import and_, exists
from helper import timehelper



def getStopsBetweenTime(dbConnection, fromTime, untilTime):
    session = dbConnection.Session()
    stop_query = session.query(dbConnection.Stops).filter(and_(dbConnection.Stops.startTime >= fromTime,
                                                               dbConnection.Stops.startTime < untilTime))
    return stop_query.all()


def getMovementsBetweenTime(dbConnection, fromTime, untilTime):
    session = dbConnection.Session()
    movement_list = session.query(dbConnection.Movement).filter(and_(dbConnection.Movement.originTime >= fromTime,
                                                                      dbConnection.Movement.originTime < untilTime)).all()
    # clean up movements_list
    for movement in list(movement_list):
        if movement.destinationTime <= movement.originTime:
            movement_list.remove(movement)

    return movement_list


def mergeConsecutiveMovementsWithSameTravelMode(dbConnection):
    # need to be consecutive with regard to time!
    session = dbConnection.Session()

    # get movements sorted by origin time and position
    movements = session.query(dbConnection.Movement).filter(dbConnection.Movement.position.isnot(None)).all()
    movements = sorted(movements, key=lambda mvmt: mvmt.originTime)

    from itertools import groupby

    for key, group in groupby(movements, lambda mvmt: mvmt.originTime):
        # sort each group by position
        sorted_group = sorted(group, key=lambda elem: elem.position)
        toBeRemoved = []

        # compare each pair of successors in group
        for first, second in zip(sorted_group, sorted_group[1:]):

            if first.idType == second.idType:
                # eliminate second from sorted_group and rename pos of all consecutive elements in sorted_group
                index = sorted_group.index(second)
                toBeRemoved.append((second, second.id, first.id))

                sec = session.query(dbConnection.Movement).get(second.id)
                session.delete(sec)
                for successor in sorted_group[index:]:
                    setattr(successor, 'position', successor.position - 1)
                session.commit()

        # iterate throug all movement segments that are to be removed and update movementIds in MovementLocation table
        for element in reversed(toBeRemoved):
            sorted_group.remove(element[0])
            idOfMergedMovementSegment = element[1]
            idOfMovementSegmentItIsMergedWith = element[2]
            spatiaquery.spatiaUpdate('UPDATE MovementLocation '
                                     'SET idMovement=' + str(idOfMovementSegmentItIsMergedWith) +
                                     ' WHERE idMovement =' + str(idOfMergedMovementSegment) + ';')


def determineDatabaseRange(dbConnection):
    session = dbConnection.Session()
    query = session.query(dbConnection.Locations.time)
    db_range_timestamp = [query.first()[0], query.order_by(dbConnection.Locations.time.desc()).first()[0]]
    db_range_utc = [timehelper.timestamp_to_utc(db_range_timestamp[0]), timehelper.timestamp_to_utc(db_range_timestamp[1])]
    #db_range_cet = [utc_to_cet(db_range_utc[0]), utc_to_cet(db_range_utc[1])]
    return db_range_timestamp, db_range_utc


def getClusterNameForId(dbConnection, clusterId):
    session = dbConnection.Session()
    clusterName = session.query(dbConnection.Cluster.name).filter(dbConnection.Cluster.id == clusterId).first()[0]
    return clusterName


def getClusterForId(dbConnection, appStatus, clusterId):
    if appStatus.usertestMode:
        session = dbConnection.Session()
        cluster_centroid = session.query(dbConnection.Cluster.centroid).filter(dbConnection.Cluster.id == clusterId).first()[0]
        cluster_centroid = eval(cluster_centroid)
        # in userttest mode this directly returns centroid in needed format [{'coordinates': [long, lat]}]
    else:
        cluster_centroid = spatiaquery.spatiaQuery('SELECT AsGeoJSON(centroid, 6) FROM cluster WHERE id=' + str(clusterId) + ';')[0]
    return cluster_centroid


def TravelModeForId(dbConnection, travelModeId):
    session = dbConnection.Session()
    travelMode = session.query(dbConnection.TravelMode.travelMode).filter(dbConnection.TravelMode.id == travelModeId).first()[0]
    return travelMode


def getMovementPathForMovementId(dbConnection, appStatus, movementId):
    session = dbConnection.Session()
    path = session.query(dbConnection.MovementLocation).filter(dbConnection.MovementLocation.idMovement == movementId).all()
    if not appStatus.usertestMode:
        geoms = spatiaquery.spatiaQuery('SELECT AsGeoJSON(geom, 6) FROM movementLocation WHERE idMovement='+str(movementId)+';')
        pathwithgeoms = []
        for i in range(len(geoms)):
            obj = {'id': path[i].id, 'idMovement': path[i].idMovement, 'time': path[i].time, 'geom': geoms[i]}
            pathwithgeoms.append(obj)

    if appStatus.usertestMode:
        pathwithgeoms = []
        for i in range(len(path)):
            obj = {'id': path[i].id, 'idMovement': path[i].idMovement, 'time': path[i].time, 'geom': path[i].geom}
            pathwithgeoms.append(obj)
        for subpath in pathwithgeoms:
            subpath['geom'] = eval(subpath['geom'])

    return pathwithgeoms


def getMovementAttributesForMovementId(dbConnection, appStatus, movementId):
    path = getMovementPathForMovementId(dbConnection, appStatus, movementId)

    # distance
    distance = 0
    if len(path) > 1:
        for i in range(len(path)-1):
            distance += geopy.distance.vincenty(path[i]['geom']['coordinates'], path[i+1]['geom']['coordinates']).km
    distance = round(distance, 2)

    # duration
    startTime = path[0]['time']
    endTime = path[-1]['time']
    duration_miliseconds = endTime - startTime
    duration_hours = duration_miliseconds / (3.6 * 10**6)
    duration = datetime.timedelta(milliseconds=duration_miliseconds)
    duration = duration - datetime.timedelta(microseconds=duration.microseconds)

    # velocity in km/h
    velocity = 0
    if duration_hours > 0:
        velocity = round(distance / duration_hours, 0)

    return startTime, endTime, distance, duration, velocity


def getClusterIdFromStopId(dbConnection, stopId):
    session = dbConnection.Session()
    clusterId = session.query(dbConnection.Stops.idCluster).filter(dbConnection.Stops.id == stopId).first()[0]
    return clusterId


def isClusterIdAssociatedWithPlaceTypeLabel(dbConnection, clusterId, placeTypeLabel):
    session = dbConnection.Session()
    res = session.query(exists().where(and_(dbConnection.ClusterTypeLookupTable.cluster_id == clusterId,
                                            dbConnection.ClusterTypeLookupTable.place_type_label == placeTypeLabel))).scalar()
    return res


# only used in usertestMode
def getLabelConfidencesForStopId(dbConnection, stopId):
    session = dbConnection.Session()
    labelConfidences = session.query(dbConnection.Stops.labelConfidences).filter(dbConnection.Stops.id == stopId).first()
    return labelConfidences