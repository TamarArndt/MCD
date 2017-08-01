import geopy.distance, datetime
from database import spatiaquery
from sqlalchemy import and_, exists
from helper import timehelper


""" for application set up """


def determineDatabaseRange(dbConnection):
    session = dbConnection.Session()
    # query = session.query(dbConnection.Locations.time)
    # db_range_timestamp = [query.first()[0], query.order_by(dbConnection.Locations.time.desc()).first()[0]]
    # db_range_utc = [timehelper.timestamp_to_utc(db_range_timestamp[0]), timehelper.timestamp_to_utc(db_range_timestamp[1])]
    # #db_range_cet = [utc_to_cet(db_range_utc[0]), utc_to_cet(db_range_utc[1])]
    #
    # return db_range_timestamp, db_range_utc

    locationquery = spatiaquery.spatiaQuery('SELECT AsGeoJSON(point, 6) FROM Locations ORDER BY time;')
    timequery = session.query(dbConnection.Locations.time)

    # range start
    location = locationquery[0]['coordinates']
    timestamp = timequery.first()[0]
    pytzTimezone = timehelper.getPytzTimezoneFromLocation(latitude=location[1], longitude=location[0])
    timestring_tzaware = timehelper.timestamp_to_givenPytzTimezone(timestamp, pytzTimezone)
    dbRangeStart_timestring = timestring_tzaware.replace(hour=0, minute=0, second=0, microsecond=0)
    dbRangeStart_timestamp = timehelper.tzawareTimestring_to_timestamp(dbRangeStart_timestring)

    # range end
    location = locationquery[-1]['coordinates']
    timestamp = timequery.order_by(dbConnection.Locations.time.desc()).first()[0]
    pytzTimezone = timehelper.getPytzTimezoneFromLocation(latitude=location[0], longitude=location[1])
    timestring_tzaware = timehelper.timestamp_to_givenPytzTimezone(timestamp, pytzTimezone)
    dbRangeEnd_timestring = timestring_tzaware.replace(hour=0, minute=0, second=0, microsecond=0)
    dbRangeEnd_timestamp = timehelper.tzawareTimestring_to_timestamp(dbRangeEnd_timestring)

    dbRange_timestamp = [dbRangeStart_timestamp, dbRangeEnd_timestamp]
    dbRange_timestring = [dbRangeStart_timestring, dbRangeEnd_timestring]

    return dbRange_timestamp, dbRange_timestring




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

        # iterate through all movement segments that are to be removed and update movementIds in MovementLocation table
        for element in reversed(toBeRemoved):
            sorted_group.remove(element[0])
            idOfMergedMovementSegment = element[1]
            idOfMovementSegmentToBeMergedWith = element[2]
            # delete duplicateRow
            duplicateRow = getMovementPathForMovementId(dbConnection, idOfMergedMovementSegment)[0]['id']
            spatiaquery.spatiaUpdate('DELETE FROM MovementLocation WHERE id ='+str(duplicateRow)+';')
            # change membership of MovementLocation entries that are merged
            spatiaquery.spatiaUpdate('UPDATE MovementLocation '
                                     'SET idMovement=' + str(idOfMovementSegmentToBeMergedWith) +
                                     ' WHERE idMovement =' + str(idOfMergedMovementSegment) + ';')


""" timeline detection """


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


def getClusterNameForId(dbConnection, clusterId):
    session = dbConnection.Session()
    clusterName = session.query(dbConnection.Cluster.name).filter(dbConnection.Cluster.id == clusterId).first()[0]
    return clusterName


def getClusterForId(clusterId):
    cluster_centroid = spatiaquery.spatiaQuery('SELECT AsGeoJSON(centroid, 6) FROM cluster WHERE id=' + str(clusterId) + ';')[0]
    return cluster_centroid


def TravelModeForId(dbConnection, travelModeId):
    session = dbConnection.Session()
    travelMode = session.query(dbConnection.TravelMode.travelMode).filter(dbConnection.TravelMode.id == travelModeId).first()[0]
    return travelMode


def getMovementPathForMovementId(dbConnection, movementId):
    session = dbConnection.Session()
    path = session.query(dbConnection.MovementLocation).filter(dbConnection.MovementLocation.idMovement == movementId).all()

    geoms = spatiaquery.spatiaQuery('SELECT AsGeoJSON(geom, 6) FROM movementLocation WHERE idMovement='+str(movementId)+';')
    pathwithgeoms = []
    for i in range(len(geoms)):
        obj = {'id': path[i].id, 'idMovement': path[i].idMovement, 'time': path[i].time, 'geom': geoms[i]}
        pathwithgeoms.append(obj)

    pathwithgeoms_sorted = sorted(pathwithgeoms, key= lambda entry: entry['time'])
    return pathwithgeoms_sorted


def getMovementAttributesForMovementId(dbConnection, appStatus, movementId):
    path = getMovementPathForMovementId(dbConnection, movementId)

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
    fullhours = duration_miliseconds // (1000 * 60 * 60)
    fullminutes = duration_miliseconds // (1000 * 60) - fullhours * 60
    if fullhours == 0:
        duration_formatted = str(fullminutes) + ' min'
    else:
        duration_formatted = str(fullhours) + ' h ' + str(fullminutes) + ' min'

    # velocity in km/h
    velocity = 0
    if duration_hours > 0:
        velocity = round(distance / duration_hours, 0)

    return startTime, endTime, distance, duration_formatted, velocity


def getClusterIdFromStopId(dbConnection, stopId):
    session = dbConnection.Session()
    clusterId = session.query(dbConnection.Stops.idCluster).filter(dbConnection.Stops.id == stopId).first()[0]
    return clusterId


def isClusterIdAssociatedWithPlaceTypeLabel(dbConnection, clusterId, placeTypeLabel):
    session = dbConnection.Session()
    res = session.query(exists().where(and_(dbConnection.ClusterTypeLookupTable.cluster_id == clusterId,
                                            dbConnection.ClusterTypeLookupTable.place_type_label == placeTypeLabel))).scalar()
    return res


def getQuestionnaireResultsForDate(dbConnection, date_timestamp):
    ''' the given date is the timestamp of that date at 00:00 in utc '''
    # TODO timezone ! -> date_timestamp needs to be tz aware for given date
    session = dbConnection.Session()
    res = session.query(dbConnection.QuestionnaireResults).filter(dbConnection.QuestionnaireResults.time == date_timestamp).first()
    return res