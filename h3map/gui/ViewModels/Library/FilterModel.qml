import QtQuick 2.0

import "../"

Item {
    required property var filter

    property alias amountOfPlayerOptions: amountOfPlayers.filterOptions

    property alias teamSizeOptions: teamSize.filterOptions

    property alias mapSizeOptions: mapSize.filterOptions

    FilterOptionModel {
        id: amountOfPlayers
        filterOptions: ListModel {
            ListElement { name: 0; selected: false; value: 0; count: 0 }
            ListElement { name: 1; selected: false; value: 1; count: 0 }
            ListElement { name: 2; selected: false; value: 2; count: 0 }
            ListElement { name: 3; selected: false; value: 3; count: 0 }
            ListElement { name: 4; selected: false; value: 4; count: 0 }
            ListElement { name: 5; selected: false; value: 5; count: 0 }
            ListElement { name: 6; selected: false; value: 6; count: 0 }
            ListElement { name: 7; selected: false; value: 7; count: 0 }
            ListElement { name: 8; selected: false; value: 8; count: 0 }
        }

        Connections {
            target: filter

            function onApplied(summary) {
                var data = summary["playerNumber"]
                amountOfPlayers.filterOptions.setProperty(0, 'count', data[0])
                amountOfPlayers.filterOptions.setProperty(1, 'count', data[1])
                amountOfPlayers.filterOptions.setProperty(2, 'count', data[2])
                amountOfPlayers.filterOptions.setProperty(3, 'count', data[3])
                amountOfPlayers.filterOptions.setProperty(4, 'count', data[4])
                amountOfPlayers.filterOptions.setProperty(5, 'count', data[5])
                amountOfPlayers.filterOptions.setProperty(6, 'count', data[6])
                amountOfPlayers.filterOptions.setProperty(7, 'count', data[7])
                amountOfPlayers.filterOptions.setProperty(8, 'count', data[8])
            }

            function onCleared() {
                amountOfPlayers.clearAll()
            }
        }
    }

    FilterOptionModel {
        id: teamSize
        filterOptions: ListModel {
            ListElement { name: 0; selected: false; value: 0;  count: 0}
            ListElement { name: 1; selected: false; value: 1;  count: 0}
            ListElement { name: 2; selected: false; value: 2;  count: 0}
            ListElement { name: 3; selected: false; value: 3;  count: 0}
            ListElement { name: 4; selected: false; value: 4;  count: 0}
            ListElement { name: 5; selected: false; value: 5;  count: 0}
            ListElement { name: 6; selected: false; value: 6;  count: 0}
            ListElement { name: 7; selected: false; value: 7;  count: 0}
            ListElement { name: 8; selected: false; value: 8;  count: 0}
        }

        Connections {
            target: filter

            function onApplied(summary) {
                var data = summary["teamSize"]
                teamSize.filterOptions.setProperty(0, 'count', data[0])
                teamSize.filterOptions.setProperty(1, 'count', data[1])
                teamSize.filterOptions.setProperty(2, 'count', data[2])
                teamSize.filterOptions.setProperty(3, 'count', data[3])
                teamSize.filterOptions.setProperty(4, 'count', data[4])
                teamSize.filterOptions.setProperty(5, 'count', data[5])
                teamSize.filterOptions.setProperty(6, 'count', data[6])
                teamSize.filterOptions.setProperty(7, 'count', data[7])
                teamSize.filterOptions.setProperty(8, 'count', data[8])
            }

            function onCleared() {
                teamSize.clearAll()
            }
        }
    }

    FilterOptionModel {
        id: mapSize
        filterOptions: ListModel {
            ListElement {
                name: "XL"
                selected: false
                value: "XL"
                count: 0
            }
            ListElement {
                name: "L"
                selected: false
                value: "L"
                count: 0
            }
            ListElement {
                name: "M"
                selected: false
                value: "M"
                count: 0
            }
            ListElement {
                name: "S"
                selected: false
                value: "S"
                count: 0
            }
        }

        Connections {
            target: filter

            function onApplied(summary) {
                var data = summary["mapSize"]
                mapSize.filterOptions.setProperty(0, 'count', data['XL'])
                mapSize.filterOptions.setProperty(1, 'count', data['L'])
                mapSize.filterOptions.setProperty(2, 'count', data['M'])
                mapSize.filterOptions.setProperty(3, 'count', data['S'])
            }

            function onCleared() {
                mapSize.clearAll()
            }
        }
    }

    function toggleAmountOfPlayers(index) {
        amountOfPlayers.toggleFilter(index)
        apply()
    }

    function toggleTeamSize(index) {
        teamSize.toggleFilter(index)
        apply()
    }

    function toggleMapSize(index) {
        mapSize.toggleFilter(index)
        apply()
    }

    function apply() {
        filter.apply({
            playerNumberOptions: amountOfPlayers.getSelection(),
            teamSizeOptions: teamSize.getSelection(),
            mapSizeOptions: mapSize.getSelection()
         })
    }

    function clear() {
        filter.clear()
    }
}
