import QtQuick 2.12

Item {
    property alias maps : maps

    property alias dispatcher: mapsActions.target

    property bool configured: false

    ListModel {
        id: maps
    }

    function onImportFiles(directory) {
        dispatcher.load(directory)
        configured = true
    }

    Connections {
        id: mapsActions

        function onFiltered(headers) {
            maps.clear()
            for(var i in headers) {
                var header = headers[i]
                var item = {"name": header.name, "description": header.description, "players": header.humans, "teams": header.teams, "thumbnail": header.thumbnail}
                maps.append(item)
            }
        }

        function onAddMap(header) {
            var item = {"name": header.name, "description": header.description, "players": header.humans, "teams": header.teams, "thumbnail": header.thumbnail}
            maps.append(item)
        }
    }

}
