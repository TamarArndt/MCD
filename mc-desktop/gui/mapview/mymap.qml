import QtQuick 2.0
import QtQuick.Controls 1.2
import QtLocation 5.5
import QtPositioning 5.5


Rectangle {
    // width and height are overwritten by Map: anchors.fill: parent
    width: 600
    height: 400
    visible: true

    //property variant fitRect

    // markerModel provides all positions (lat, long) where markers should be placed
    ListModel{
        id: markersEntireDayModel
        ListElement{
            latitude: 52.46714
            longitude: 13.4
        }
    }

    ListModel{
        id: markersSelectedEntryModel
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
           latitude: -41.271233
           longitude: 174.785786
        }
        maximumZoomLevel: 18.5
        zoomLevel: 15 //10
        MapPolyline{
            id: pathEntireDay
            line.width: 3
            line.color: '#FFDF80' //'#FFBC40'
            path: []
        }

        MapItemView{
            id: markersEntireDay
            model: markersEntireDayModel
            delegate: MapQuickItem {
                anchorPoint.x: locationmarker.width/2
                anchorPoint.y: locationmarker.height
                coordinate: QtPositioning.coordinate(latitude, longitude) // uses lat, long from List Model

                sourceItem: Image {
                    id: locationmarker
                    source: projectDirectory + "/res/location_marker_small.svg" // TODO path
                }
            }
        }

        MapPolyline{
            id: pathSelectedEntry
            line.width: 6
            line.color: '#FFCB3B' //0A75C2'
            path: []
        }

        MapItemView{
            id: markersSelectedEntry
            model: markersSelectedEntryModel
            delegate: MapQuickItem {
                anchorPoint.x: locationmarker.width/2
                anchorPoint.y: locationmarker.height
                coordinate: QtPositioning.coordinate(latitude, longitude) // uses lat, long from List Model

                sourceItem: Image {
                    id: locationmarker
                    source: projectDirectory + "/res/location_marker.svg" // TODO path
                }
            }
        }

        MapItemView{
            id: splitMarker
            model: splitMarkerModel
            delegate: MapQuickItem {
                anchorPoint.x: locationmarker.width/2
                anchorPoint.y: locationmarker.height
                coordinate: QtPositioning.coordinate(latitude, longitude) // uses lat, long from List Model

                sourceItem: Image {
                    id: locationmarker
                    source: projectDirectory + "/res/location_marker_split.svg" // TODO path
                }
            }
        }

    }

    // functions to interact with map and map overlays

    // CLEAR
    function clearAll() {
        mymap.clearMapItems()
    }
    function clearOnlyPathAndMarkersOfSelectedEntry() {
        markersSelectedEntryModel.clear()
        mymap.removeMapItem(pathSelectedEntry)
    }

    // dictpoint has the format: {"latitude": 30.5, "longitude": 40.2}
    // dictpointlist is a list of dictpoints: [dictpoint, dictpoint, ...]

    // MARKER
    function setMarkersEntireDay(dictpointlist) {
        for (var i = 0; i < dictpointlist.length; i++) {
            markersEntireDayModel.append(dictpointlist[i])
        }
    }
    function setMarkersSelectedEntry(dictpointlist) {
        for (var i = 0; i < dictpointlist.length; i++) {
            markersSelectedEntryModel.append(dictpointlist[i])
        }
    }

    // PATH
    function setPathEntireDay(dictpointlist){
        //to ensure that no path corpses stay on map when only markers are to be put on the map
        if (dictpointlist.length > 0) {
            mymap.addMapItem(pathEntireDay)
            pathEntireDay.path = dictpointlist
        }
    }
    function setPathSelectedEntry(dictpointlist){
        //to ensure that no path corpses stay on map when only markers are to be put on the map
        if (dictpointlist.length > 0) {
            mymap.addMapItem(pathSelectedEntry)
            pathSelectedEntry.path = dictpointlist
        }
    }

    // FIT MAP
    // set center and zoomLevel according to overlay items
    function fitMap() {
        mymap.fitViewportToMapItems()
    }

    function fitMapToSelectedItems(lat1, long1, lat2, long2) {
        mymap.visibleRegion = QtPositioning.rectangle([QtPositioning.coordinate(lat1, long1), QtPositioning.coordinate(lat2, long2)])
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


