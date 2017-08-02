==========================
Mobility Companion Desktop
==========================

About
-----
This package provides a desktop application to label data collected by the Android/iOS Mobility Companion App.


Dependencies
------------

* OS: runs on Linux, Mac OS and Windows

* supported Python versions: **Python3 >= 3.5**

* **Python 2** (<< 2.8, >= 2.7) needs to be installed on your system, because the application uses a subprocess with Python 2


Installation
------------

1. for the installation make sure you have **pip and pip3** installed

   :code:`apt-get install python3-pip`

   :code:`apt-get install python-pip`



.. 2. install **PyQt5**

     .. :code:`pip3 install pyqt5`

     .. * **probably not neccessary anymore:**
     .. on Linux: the PyQt5 installation must be complemented by the following modules:
     PyQt5.QtSvg, PyQt5.QtQuick, QtQuick.Controls, QtPositioning, QtLocation.
     install them with:

     .. :code:`pip3 install <modulename in lowercase>`


2. install **pyspatialite** for python2

   :code:`pip install pyspatialite`

   * if this error occurs:

     :code:`__main__.HeaderNotFoundException: cannot find proj_api.h, bailing out`

     you can follow the steps below, that are described in the comments of `this issue <https://github.com/lokkju/pyspatialite/issues/18>`  in the pyspatialite repository

     * for Linux:

       :code:`$ CFLAGS=-I/usr/include .env/bin/pip install pyspatialite`

     * for Mac OS:

       * install the Proj and GEOS libraries: :code:`brew install proj geos`

       * find the install loaction:  :code:`brew info geos proj`

       * specify the include folder in the CFLAGS option with the found location. Alter the following command given your install location

         :code:`CFLAGS="-I/usr/local/Cellar/proj/4.9.2/include -I/usr/local/Cellar/geos/3.5.0/include" / pip install pyspatialite`


3. all **other requirements** can be installed with:

   :code:`pip3 install -r requirements.txt`



Run program
-----------

To execute the program run the following from within the project:

   :code:`./bin/mobility-companion-desktop`
