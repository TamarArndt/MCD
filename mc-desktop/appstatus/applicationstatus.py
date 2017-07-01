import logging
import datetime
from PyQt5 import QtCore
from sqlalchemy import and_
from helper import timehelper

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logging.basicConfig()



class ApplicationStatus():
    def __init__(self, dbConnection):
        self.databaseRange_timestamp, self.databaseRange_utc = determineDatabaseRange(dbConnection)

        # TODO manage timezone
        # currentDate always is a datetime.datetimeobject of the form 2017-06-01 12:31:16.064000+00:00
        self.currentDate = self.databaseRange_utc[0]

        # currentDateEntries contains a list (sorted by startTime) of stops and movements of date
        self.currentDateEntries = getEntriesforDate(self.currentDate, dbConnection)

        # TODO
        # self.numberOfLabeledStops
        # self.numberOfLabeledMovements


    def setCurrentDate(self, date, dbConnection):
        ''' sets currentDate to date and updates currentDateEntries to the list of entries for that date'''
        if type(date) == QtCore.QDate:
            date = QtCore.QDate.toPyDate(date)
        date = datetime.datetime.combine(date, datetime.datetime.min.time())
        if self.currentDate == date:
            pass
        else:
            self.currentDate = date
            self.currentDateEntries = getEntriesforDate(date, dbConnection)
        logging.info('currently selected date: {}'.format(self.currentDate))




def determineDatabaseRange(dbConnection):
    session = dbConnection.Session()
    query = session.query(dbConnection.Locations.columns.time)
    db_range_timestamp = [query.first()[0], query.order_by(dbConnection.Locations.columns.time.desc()).first()[0]]
    db_range_utc = [timehelper.timestamp_to_utc(db_range_timestamp[0]), timehelper.timestamp_to_utc(db_range_timestamp[1])]
    #db_range_cet = [utc_to_cet(db_range_utc[0]), utc_to_cet(db_range_utc[1])]

    return db_range_timestamp, db_range_utc



def getEntriesforDate(date, dbConnection):
    if type(date) == QtCore.QDate:
        date = QtCore.QDate.toPyDate(date)
    date = datetime.datetime.combine(date, datetime.datetime.min.time())
    next_date = date + datetime.timedelta(days=2)

    dayrange_timestamp = [timehelper.cetdatetime_to_timestamp(date), timehelper.cetdatetime_to_timestamp(next_date)]
    session = dbConnection.Session()

    # STOPS
    stop_query = session.query(dbConnection.Stops).filter(and_(dbConnection.Stops.columns.startTime >= dayrange_timestamp[0],
                                                               dbConnection.Stops.columns.startTime < dayrange_timestamp[1]))
    stops_list = stop_query.all()
    # associate a type with each entry
    stops_list = [{'type': 'Stop', 'value': stop} for stop in stops_list]


    # MOVEMENTS
    movement_query = session.query(dbConnection.Movement).filter(and_(dbConnection.Movement.columns.originTime >= dayrange_timestamp[0],
                                                                      dbConnection.Movement.columns.originTime < dayrange_timestamp[1]))
    movements_list = movement_query.all()
    # clean up movements_list
    for movement in list(movements_list):
        if movement.destinationTime <= movement.originTime:
            movements_list.remove(movement)
    # associate a type with each entry
    movements_list = [{'type': 'Movement', 'value': movement} for movement in movements_list]


    sorted_entries = sorted(stops_list + movements_list, key= (lambda entry: startAndOriginTimeKeyEqualizer(entry)))
    return sorted_entries



def startAndOriginTimeKeyEqualizer(entry):
    if entry['type'] == 'Stop':
        return entry['value'].startTime
    else:
        return entry['value'].originTime

