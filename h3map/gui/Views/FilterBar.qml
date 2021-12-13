import QtQuick 2.0
import QtQuick.Dialogs 1.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../ViewModels"
import "Components"

Row {

    required property var app

    id: filterBar

    spacing: 10

    signal cleared

    FilterComboCheckBox {
        filterName: "Players"

        model: options.filterOptions

        FilterModel {
            id: options
            filterOptions: ListModel {
                ListElement { name: 0; selected: false; value: 0; count: 0}
                ListElement { name: 1; selected: false; value: 1; count: 0}
                ListElement { name: 2; selected: false; value: 2; count: 0 }
                ListElement { name: 3; selected: false; value: 3; count: 0 }
                ListElement { name: 4; selected: false; value: 4; count: 0 }
                ListElement { name: 5; selected: false; value: 5; count: 0 }
                ListElement { name: 6; selected: false; value: 6; count: 0 }
                ListElement { name: 7; selected: false; value: 7; count: 0 }
                ListElement { name: 8; selected: false; value: 8; count: 0 }
            }
        }

        onActivated: {
            options.toggleFilter(index)
            app.applyFilter({playerNumberOptions: options.getSelection(), teamSizeOptions: teamSize.getSelection(), mapSizeOptions: mapSizeRules.getSelection()})
        }

        Connections {
            target: filterBar

            function onCleared() {
                options.clearAll()
            }
        }

        Connections {
            target: app

            function onFiltered(summary) {
                var data = summary["playerNumber"]
                options.filterOptions.setProperty(0, 'count', data[0])
                options.filterOptions.setProperty(1, 'count', data[1])
                options.filterOptions.setProperty(2, 'count', data[2])
                options.filterOptions.setProperty(3, 'count', data[3])
                options.filterOptions.setProperty(4, 'count', data[4])
                options.filterOptions.setProperty(5, 'count', data[5])
                options.filterOptions.setProperty(6, 'count', data[6])
                options.filterOptions.setProperty(7, 'count', data[7])
                options.filterOptions.setProperty(8, 'count', data[8])
            }
        }
    }

    FilterComboCheckBox {
        filterName: "Teams"

        model: teamSize.filterOptions

        FilterModel {
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
        }

        onActivated: {
            teamSize.toggleFilter(index)
            app.applyFilter({playerNumberOptions: options.getSelection(), teamSizeOptions: teamSize.getSelection(), mapSizeOptions: mapSizeRules.getSelection()})
        }

        Connections {
            target: filterBar

            function onCleared() {
                teamSize.clearAll()
            }
        }

        Connections {
            target: app

            function onFiltered(summary) {
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
        }
    }

    FilterComboCheckBox {
        id: mapSizeFilter
        filterName: "Map Size"

        model: mapSizeRules.filterOptions

        FilterModel {
            id: mapSizeRules
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
        }

        onActivated: {
            mapSizeRules.toggleFilter(index)
            app.applyFilter({playerNumberOptions: options.getSelection(), teamSizeOptions: teamSize.getSelection(), mapSizeOptions: mapSizeRules.getSelection()})
        }

        Connections {
            target: filterBar

            function onCleared() {
                mapSizeRules.clearAll()
            }
        }

        Connections {
            target: app

            function onFiltered(summary) {
                var data = summary["mapSize"]
                mapSizeRules.filterOptions.setProperty(0, 'count', data['XL'])
                mapSizeRules.filterOptions.setProperty(1, 'count', data['L'])
                mapSizeRules.filterOptions.setProperty(2, 'count', data['M'])
                mapSizeRules.filterOptions.setProperty(3, 'count', data['S'])
            }
        }
    }

    Button {
        text: "Clear"

        onClicked: {
            app.clearFilter()
            filterBar.cleared()
        }
    }


}
