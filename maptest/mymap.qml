import QtQuick 2.0
import QtQuick.Controls 1.2
import QtLocation 5.5
import QtPositioning 5.5


Rectangle {
    width: 600
    height: 400
    visible: true

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
    }

}


