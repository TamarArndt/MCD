import logging
from database import spatiaquery
from sqlalchemy import and_

logger = logging.getLogger()


""" Cluster-PlaceType-Associations """


def updateStopLabelsWithClusterAssociation(dbConnection, clusterId, associatedPlaceTypeId, associatedPlaceTypeLabel):
    """ update all stops with clusterId, that is not already confirmed (only if flagAutomaticLabeling 0 or 1) """
    session = dbConnection.Session()
    query = session.query(dbConnection.Stops).filter(dbConnection.Stops.idCluster == clusterId,
                                                     dbConnection.Stops.flagAutomaticLabeling <= 1)
    for stop in query:
        setattr(stop, 'placeTypeId', associatedPlaceTypeId)
        setattr(stop, 'placeTypeLabel', associatedPlaceTypeLabel)
        setattr(stop, 'flagAutomaticLabeling', 1)
    session.commit()


def updateClusterTypeLookupTable(dbConnection, clusterId, associatedPlaceTypeId, associatedPlaceTypeLabel):
    session = dbConnection.Session()
    clusterTypeAssoc = session.query(dbConnection.ClusterTypeLookupTable).\
        filter(dbConnection.ClusterTypeLookupTable.cluster_id == clusterId).first()

    # if an association with given clusterId already exists: overwrite
    if clusterTypeAssoc:
        setattr(clusterTypeAssoc, 'place_type_id', associatedPlaceTypeId)
        setattr(clusterTypeAssoc, 'place_type_label', associatedPlaceTypeLabel)
        session.commit()

    # create new row with new cluster-placeType association
    else:
        newClusterPlaceTypeAssociation = dbConnection.ClusterTypeLookupTable(cluster_id = clusterId,
                                                                             place_type_id = associatedPlaceTypeId,
                                                                             place_type_label = associatedPlaceTypeLabel)
        session.add(newClusterPlaceTypeAssociation)
        session.commit()


def newClusterPlaceTypeAssociation(dbConnection, stopId, associatedPlaceTypeLabel):
    session = dbConnection.Session()
    clusterId = session.query(dbConnection.Stops.idCluster).filter(dbConnection.Stops.id == stopId).first()[0]
    associatedPlaceTypeId = session.query(dbConnection.PlaceType.id).filter(dbConnection.PlaceType.place_type == associatedPlaceTypeLabel)
    updateClusterTypeLookupTable(dbConnection, clusterId, associatedPlaceTypeId, associatedPlaceTypeLabel)
    updateStopLabelsWithClusterAssociation(dbConnection, clusterId, associatedPlaceTypeId, associatedPlaceTypeLabel)


""" Label change and confirmation """


def updateStopLabel(dbConnection, appStatus, stopId, newPlaceTypeId, newPlaceTypeLabel):
    session = dbConnection.Session()
    stop = session.query(dbConnection.Stops).get(stopId)

    if stop.flagAutomaticLabeling == 1 and stop.placeTypeId == newPlaceTypeId and appStatus.automaticLabelingMode:
        setattr(stop, 'flagAutomaticLabeling', 2)
    else:
        setattr(stop, 'placeTypeId', newPlaceTypeId)
        setattr(stop, 'placeTypeLabel', newPlaceTypeLabel)
        setattr(stop, 'flagAutomaticLabeling', 3)
    session.commit()


def updateMovementLabel(dbConnection, movementId, newTravelModeId):
    session = dbConnection.Session()
    movement = session.query(dbConnection.Movement).get(movementId)
    setattr(movement, 'idType', newTravelModeId)
    session.commit()


""" Split """


def splitMovementAtTime(dbConnection, movementId, splittime):
    logger.info(" splitting movement %s at time %s.", movementId, splittime)
    session = dbConnection.Session()
    # make two movements from original movement, updating position value
    origMovement = session.query(dbConnection.Movement).get(movementId)

    if origMovement.position == None:
        setattr(origMovement, 'position', 0)
    else:
        # shift position of all consecutive segments
        allConsecutiveSegmentsOfThisMovement = session.query(dbConnection.Movement).\
            filter(and_ (dbConnection.Movement.originTime == origMovement.originTime,
                         dbConnection.Movement.position > origMovement.position)).all()

        for segment in allConsecutiveSegmentsOfThisMovement:
            setattr(segment, 'position', segment.position + 1)

    newMovement = dbConnection.Movement(idType=origMovement.idType,
                                        originId=origMovement.originId,
                                        destinationId=origMovement.destinationId,
                                        originTime=origMovement.originTime,
                                        destinationTime=origMovement.destinationTime,
                                        position=origMovement.position + 1)
    session.add(newMovement)
    session.commit()
    origMovementId = origMovement.id
    newMovementId = newMovement.id
    session.close()

    spatiaquery.spatiaUpdate('UPDATE MovementLocation SET idMovement=' +str(newMovementId) + ' WHERE idMovement ='+ str(origMovementId) +' AND time >' + str(splittime) + ';')
    # can't update MovementLocation Table directly because of geom column
    # and the lack of a spatialite plugin for python3 --> detour via python2

    # TODO split in MovementLocation needs to copy begining and end row
    # otherwise the route is falling apart
    # also: remove copies when split is merged again!