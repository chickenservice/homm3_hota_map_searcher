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
                ListElement { name: 0; selected: false; value: 0 }
                ListElement { name: 1; selected: false; value: 1 }
                ListElement { name: 2; selected: false; value: 2 }
                ListElement { name: 3; selected: false; value: 3 }
                ListElement { name: 4; selected: false; value: 4 }
                ListElement { name: 5; selected: false; value: 5 }
                ListElement { name: 6; selected: false; value: 6 }
                ListElement { name: 7; selected: false; value: 7 }
                ListElement { name: 8; selected: false; value: 8 }
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
    }

    FilterComboCheckBox {
        filterName: "Teams"

        model: teamSize.filterOptions

        FilterModel {
            id: teamSize
            filterOptions: ListModel {
                ListElement { name: 0; selected: false; value: 0 }
                ListElement { name: 1; selected: false; value: 1 }
                ListElement { name: 2; selected: false; value: 2 }
                ListElement { name: 3; selected: false; value: 3 }
                ListElement { name: 4; selected: false; value: 4 }
                ListElement { name: 5; selected: false; value: 5 }
                ListElement { name: 6; selected: false; value: 6 }
                ListElement { name: 7; selected: false; value: 7 }
                ListElement { name: 8; selected: false; value: 8 }
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
                }
                ListElement {
                    name: "L"
                    selected: false
                    value: "L"
                }
                ListElement {
                    name: "M"
                    selected: false
                    value: "M"
                }
                ListElement {
                    name: "S"
                    selected: false
                    value: "S"
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
    }

    Button {
        text: "Clear"

        onClicked: {
            app.clearFilter()
            filterBar.cleared()
        }
    }


}
