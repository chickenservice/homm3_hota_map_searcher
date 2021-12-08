import QtQuick 2.12

Item {
    property alias maps : maps

    property alias dispatcher: mapsActions.target

    ListModel {
        id: maps
    }

    function discover(page) {
        dispatcher.discover(page)
    }

    Connections {
        id: mapsActions

        function onRetrievedMaps(headers) {
            for (var i in headers){
                var header = headers[i]
                var item = {
                    "name": header.name,
                    "description": header.description,
                    "players": header.humans,
                    "teams": header.teams,
                    "thumbnail": header.thumbnail
                }
                maps.append(item)
            }
        }
    }

}
