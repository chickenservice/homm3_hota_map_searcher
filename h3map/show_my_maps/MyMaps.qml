import QtQuick 2.12
import QtQml.Models 2.1

import "../filtering"

Item {
    property alias maps : filtered

    property alias filters: filters

    property alias delegate: filtered.delegate

    property bool configured: libraryActions.mapsDirectoryConfigured

    required property var libraryActions

    ListModel {
        id: maps
    }

    DelegateModel {
        id: filtered
        model: maps

        groups: [
            DelegateModelGroup {
                includeByDefault: true
                name: "filtered"
            }
        ]

        filterOnGroup: "filtered"
    }

    Filter {
        id: filters
        filter: libraryActions
    }

    function importFromFolder(directory) {
        libraryActions.importMaps(directory)
    }

    function updateFilter(summary) {
        var toFilter = summary["filtered"]
        for(var i = 0; i < toFilter.length; i++) {
            filtered.items.addGroups(toFilter[i], 1, "filtered")
        }
    }

    function clearFilter() {
        filtered.items.addGroups(0, filtered.items.count, "filtered")
    }

    Connections {
        target: libraryActions

        function onImportedMap(header) {
            header.idx = maps.count
            maps.append(header)
        }

        function onImportedMaps() {
            filters.apply()
        }

        function onApplying() {
            filtered.items.removeGroups(0, filtered.items.count, "filtered")
        }

        function onApplied(toFilter) {
            updateFilter(toFilter)
        }

        function onCleared() {
            clearFilter()
        }
    }

    Component.onCompleted: {
        libraryActions.maps()
    }
}
