import geopy.distance, datetime
from database import spatiaquery


def getClusterNameForId(dbConnection, clusterId):
    session = dbConnection.Session()
    clusterName = session.query(dbConnection.Cluster.columns.name).filter(dbConnection.Cluster.columns.id == clusterId).first()[0]
    return clusterName

def getClusterForId(dbConnection, clusterId):
    session = dbConnection.Session()
    #cluster_area = spatiaquery.spatiaQuery('SELECT AsGeoJSON(cluster_area, 6) FROM cluster WHERE id=' + str(clusterId) + ';')
    cluster_centroid = spatiaquery.spatiaQuery('SELECT AsGeoJSON(centroid, 6) FROM cluster WHERE id=' + str(clusterId) + ';')
    return cluster_centroid

def TravelModeForId(dbConnection, travelModeId):
    session = dbConnection.Session()
    travelMode = session.query(dbConnection.TravelMode.columns.travelMode).filter(dbConnection.TravelMode.columns.id == travelModeId).first()[0]
    return travelMode


def getMovementPathForMovementId(dbConnection, movementId):
    session = dbConnection.Session()
    path = session.query(dbConnection.MovementLocation).filter(dbConnection.MovementLocation.columns.idMovement == movementId).all()
    geoms = spatiaquery.spatiaQuery('SELECT AsGeoJSON(geom, 6) FROM movementLocation WHERE idMovement='+str(movementId)+';')
    pathwithgeoms = []
    for i in range(len(geoms)):
        obj = {'id': path[i].id, 'idMovement': path[i].idMovement, 'time': path[i].time, 'geom': geoms[i]}
        pathwithgeoms.append(obj)
    return pathwithgeoms


def getMovementAttributesForMovementId(dbConnection, movementId):
    path = getMovementPathForMovementId(dbConnection, movementId)

    # distance
    distance = 0
    if len(path) > 1:
        for i in range(len(path)-1):
            distance += geopy.distance.vincenty(path[i]['geom']['coordinates'], path[i+1]['geom']['coordinates']).km
    distance = round(distance, 2)

    # duration
    begin = path[0]['time']
    end = path[-1]['time']
    duration_miliseconds = end-begin
    duration_hours = duration_miliseconds / (3.6 * 10**6)
    duration = datetime.timedelta(milliseconds=duration_miliseconds)
    duration = duration - datetime.timedelta(microseconds=duration.microseconds)

    # velocity in km/h
    velocity = 0
    if duration_hours > 0:
        velocity = round(distance / duration_hours, 0)

    return distance, duration, velocity
