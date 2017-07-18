import QtQuick 2.0
import QtQuick.Controls 1.2
import QtLocation 5.5
import QtPositioning 5.5


Rectangle {
    // width and height are overwritten by Map: anchors.fill: parent
    width: 600
    height: 400
    visible: true

    // markerModel provides all positions (lat, long) where markers should be placed
    ListModel{
        id: markerModel
        ListElement{
            latitude: 52.46714
            longitude: 13.4
        }
    }
    // splitMarkerModel stores all positions where split markers are to be placed
    ListModel{
        id: splitMarkerModel
        ListElement{
            latitude: 48.534950
            longitude: 9.071802
        }
    }


    Plugin {
        id: mapboxPlugin
        name: "mapbox"
        PluginParameter { name: "mapbox.map_id"; value: "mapbox.streets" }
        PluginParameter { name: "mapbox.access_token"; value: "pk.eyJ1IjoidGFtYXJhcm5kdCIsImEiOiJjajRpOHoyb2MwNjFnMzNzZXNwMHRldzAwIn0.fDH3VtBeCN5F-eUybyx1_w" }
    }

    Map {
        id: mymap
        anchors.fill: parent
        plugin: mapboxPlugin
        center {
           latitude: -41.271233 //48.534950
           longitude: 174.785786 //9.071802
        }
        maximumZoomLevel: 18.5
        zoomLevel: 15 //10
        MapPolyline{
            id: mPath
            line.width: 4
            line.color: '#FBC02D'
            path: []
        }

        MapItemView{
            id: mMarkers
            model: markerModel
            delegate: MapQuickItem {
                anchorPoint.x: locationmarker.width/2
                anchorPoint.y: locationmarker.height/2
                coordinate: QtPositioning.coordinate(latitude, longitude) // uses lat, long from List Model

                sourceItem: Image {
                    id: locationmarker
                    source: "../../res/location_marker.svg"
                }
            }
        }

        MapItemView{
            id: mSplitMarker
            model: splitMarkerModel
            delegate: MapQuickItem {
                anchorPoint.x: locationmarker.width/2
                anchorPoint.y: locationmarker.height/2
                coordinate: QtPositioning.coordinate(latitude, longitude) // uses lat, long from List Model

                sourceItem: Image {
                    id: locationmarker
                    source: "../../res/location_marker_split.svg"
                }
            }
        }

    }

    // functions to interact with map and map overlays

    // CLEAR
    function clearAll() {
        mymap.clearMapItems()
    }

    // dictpoint has the format: {"latitude": 30.5, "longitude": 40.2}
    // dictpointlist is a list of dictpoints: [dictpoint, dictpoint, ...]

    // MARKER
    function setMarker(dictpoint) {
        markerModel.append( dictpoint )
    }
    function setMarkers(dictpointlist) {
        for (var i = 0; i < dictpointlist.length; i++) {
            setMarker(dictpointlist[i])
        }
    }
    function clearMarkers() {
        markerModel.clear()
    }

    // PATH
    function setPath(dictpointlist){
        //to ensure that no path corpses stay on map when only markers are to be put on the map
        if (dictpointlist.length > 0) {
            mymap.addMapItem(mPath)
            mPath.path = dictpointlist
        }
    }

    // set center and zoomLevel according to overlay items
    function fitMap() {
        mymap.fitViewportToMapItems()
    }


    // SPLIT MARKER
    function setSplitMarker(dictpoint) {
        splitMarkerModel.clear()
        splitMarkerModel.append(dictpoint)
    }
    function clearSplitMarker() {
        splitMarkerModel.clear()
    }

}


