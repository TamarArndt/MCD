import os, sys
from PyQt5 import QtGui, QtSvg


MAIN_DIR = os.path.dirname(sys.modules['__main__'].__file__)

def UnknownIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_question.png'))


# StopLabelIcons ---------------------------------------------------------------------------

def HomeIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_home.png'))

def EducationIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_education.png'))

def WorkIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_work.png'))

def FriendsFamilyIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_friendsfamily.png'))

def HotelIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_hotel.png'))

def RestaurantIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_restaurant.png'))

def NightlifeIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_nightlife.png'))

def GrocerystoreIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_grocerystore.png'))

def ShopIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_shop.png'))

def SportIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_sport.png'))

def MedicalIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_medical.png'))

def LeisureIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_leisure.png'))

def TransportInfrastructureIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_bus.png'))

def OtherIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_other.png'))

def DetectionOffIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_error.png'))


# MovementLabelIcons -----------------------------------------------------------------------

def SubwayIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_subway.png'))

def TrainIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_train.png'))

def TramIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_tram.png'))

def BusIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_bus.png'))

def CarIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_car.png'))

def PlaneIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_plane.png'))

def WalkingIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_walking.png'))

def CyclingIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_cycling.png'))

def RunningIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_running.png'))

def MotorcycleIcon():
    return QtGui.QIcon(os.path.join(MAIN_DIR , 'res', 'labels', 'ic_motorcycle.png'))






def getStopLabelIcon(name):
    iconfunction = getIconDict("stop").get(name)
    return iconfunction

def getMovementLabelIcon(name):
    iconfunction = getIconDict("movement").get(name)
    return iconfunction

def getIconDict(type):
    if type == "stop":
        stopicons = {
            "Unknown": UnknownIcon(),
            "Home": HomeIcon(),
            "Education": EducationIcon(),
            "Work": WorkIcon(),
            "FriendsFamily": FriendsFamilyIcon(),
            "Friend & Family": FriendsFamilyIcon(),
            "Hotel": HotelIcon(),
            "Restaurant": RestaurantIcon(),
            "Nightlife": NightlifeIcon(),
            "Grocerystore": GrocerystoreIcon(),
            "Grocery Store": GrocerystoreIcon(),
            "Shop": ShopIcon(),
            "Sport": SportIcon(),
            "Medical": MedicalIcon(),
            "Leisure": LeisureIcon(),
            "TransportInfrastructure": TransportInfrastructureIcon(),
            "Transport Infrastructure": TransportInfrastructureIcon(),
            "Other": OtherIcon(),
            "DetectionOff": DetectionOffIcon(),
            "Detection is completely wrong": DetectionOffIcon()
        }
        return stopicons
    elif type == "movement":
        movementicons = {
            "Unknown": UnknownIcon(),
            "Subway" : SubwayIcon(),
            "Train": TrainIcon(),
            "Tram": TramIcon(),
            "Pendelbus": BusIcon(),
            "Bus": BusIcon(),
            "Car": CarIcon(),
            "Plane": PlaneIcon(),
            "Walking": WalkingIcon(),
            "Cycling": CyclingIcon(),
            "Running": RunningIcon(),
            "Motorcycle": MotorcycleIcon(),
            "Detection is completely wrong": DetectionOffIcon()
        }
        return movementicons
    else:
        raise Exception('type for function getIconDict must be either "stop" or "movement"')




def SpeedometerIcon():
    return QtSvg.QSvgWidget(os.path.join(MAIN_DIR, 'res', 'speedometer.svg'))

def ClockIcon():
    return QtSvg.QSvgWidget(os.path.join(MAIN_DIR, 'res', 'ei-clock.svg'))

def DistanceIcon():
    return QtSvg.QSvgWidget(os.path.join(MAIN_DIR, 'res', 'distance.svg'))

