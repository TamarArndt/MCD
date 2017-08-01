import logging
import datetime
from PyQt5 import QtCore
from sqlalchemy import and_
from helper import timehelper
from database import dbqueries

logger = logging.getLogger()


class ApplicationStatus():
    def __init__(self, dbConnection, adaptivityMode):
        self.databaseRange_timestamp, self.databaseRange_timestring = dbqueries.determineDatabaseRange(dbConnection)

        # TODO manage timezone
        # currentDate always is a datetime.datetimeobject of the form 2017-06-01 12:31:16.064000+00:00
        self.currentDate = self.databaseRange_timestring[0]
        logging.info('currently selected date: {}'.format(self.currentDate))
        # currentDateEntries contains a list (sorted by startTime) of stops and movements of date
        self.currentDateEntries = self.getEntriesforDate(self.currentDate, dbConnection)
        self.labelingStatusForCurrentDate = LabelingStatusOfDate(self.currentDate, self.currentDateEntries)

        self.adaptivityMode = adaptivityMode
        self.automaticLabelingMode = True

    def updateApplicationStatus(self, dbConnection):
        self.currentDateEntries = self.getEntriesforDate(self.currentDate, dbConnection=dbConnection)
        self.labelingStatusForCurrentDate = LabelingStatusOfDate(self.currentDate, self.currentDateEntries)

    def setCurrentDate(self, date, dbConnection):
        """ sets currentDate to date and updates currentDateEntries to the list of entries for that date """
        if type(date) == QtCore.QDate:
            date = QtCore.QDate.toPyDate(date)
        date = datetime.datetime.combine(date, datetime.datetime.min.time())
        date = timehelper.localizeutc(date)
        if self.currentDate == date:
            pass
        else:
            self.currentDate = date
            self.currentDateEntries = self.getEntriesforDate(date, dbConnection)
            self.labelingStatusForCurrentDate = LabelingStatusOfDate(self.currentDate, self.currentDateEntries)
        logging.info('currently selected date: {}'.format(self.currentDate))

    def getEntriesforDate(self, date, dbConnection):
        if type(date) == QtCore.QDate:
            date = QtCore.QDate.toPyDate(date)
        date = datetime.datetime.combine(date, datetime.datetime.min.time())
        next_date = date + datetime.timedelta(days=1)

        fromTime = timehelper.utcdatetime_to_timestamp(date)
        untilTime = timehelper.utcdatetime_to_timestamp(next_date)

        # STOPS
        stops_list = dbqueries.getStopsBetweenTime(dbConnection, fromTime, untilTime)
        # associate a type with each entry
        stops_list = [{'type': 'Stop', 'value': stop} for stop in stops_list]

        # MOVEMENTS
        movements_list = dbqueries.getMovementsBetweenTime(dbConnection, fromTime, untilTime)
        movements_list = [{'type': 'Movement', 'value': movement} for movement in movements_list]

        sorted_entries = sorted(stops_list + movements_list, key= lambda entry: self.startAndOriginTimeKeyEqualizer(entry))
        return sorted_entries

    def startAndOriginTimeKeyEqualizer(self, entry):
        if entry['type'] == 'Stop':
            return entry['value'].startTime, None
        elif entry['type'] == 'Movement':
            return entry['value'].originTime, entry['value'].position


class LabelingStatusOfDate:
    def __init__(self, date, dateEntries):
        self.date = date
        self.numberOfLabeledStops = 0
        self.totalNumberOfStops = 0
        self.numberOfLabeledMovements = 0
        self.totalNumberOfMovements = 0

        self.setUp(dateEntries)

    def setUp(self, dateEntries):
        for entry in dateEntries:
            if entry['type'] == 'Stop':
                self.totalNumberOfStops += 1
                if entry['value'].flagAutomaticLabeling == 2 or entry['value'].flagAutomaticLabeling == 3:  # 2,3: confirmed
                    self.numberOfLabeledStops += 1
            elif entry['type'] == 'Movement':
                self.totalNumberOfMovements += 1
                if not entry['value'].idType == 13:  # 13: unknown
                    self.numberOfLabeledMovements += 1

    def getTotalProgressPercentage(self):
        total = self.totalNumberOfStops + self.totalNumberOfMovements
        labeled = self.numberOfLabeledStops + self.numberOfLabeledMovements
        percentageOfLabeledEntries = (labeled / total) * 100
        return percentageOfLabeledEntries


