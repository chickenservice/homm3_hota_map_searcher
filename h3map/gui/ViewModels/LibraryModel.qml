import QtQuick 2.12
import QtQml.Models 2.1

import "Library"

Item {
    property alias maps : filtered

    property alias filters: filters

    property alias delegate: filtered.delegate

    property bool configured: false

    required property var libraryActions

    required property var filterActions

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

    FilterModel {
        id: filters
        filter: filterActions
    }

    function importFromFolder(directory) {
        configured = true
        libraryActions.importFromFolder(directory)
    }

    function updateFilter(summary) {
        var toFilter = summary["filtered"]
        filtered.items.removeGroups(0, filtered.items.count, "filtered")
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
            var item = {
                "idx": maps.count,
                "name": header.name,
                "description": header.description,
                "players": header.humans,
                "teams": header.teams,
                "thumbnail": header.thumbnail}
            maps.append(item)
        }
    }

    Connections {
        target: filterActions

        function onApplied(toFilter) {
            updateFilter(toFilter)
        }

        function onCleared() {
            clearFilter()
        }
    }
}
