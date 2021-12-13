import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0
import QtQml.Models 2.1

import "../ViewModels"
import "Components"
import "Components/MapCard"

Item {
    required property var application

    LibraryModel {
        id: libraryModel
        dispatcher: application
    }

    states: [
        State {
            name: "libraryUnconfigured"
            when: !libraryModel.configured
            PropertyChanges {
                target: chooseLibrary
                visible: true
            }
            PropertyChanges {
                target: library
                visible: false
            }
        },
        State {
            name: "libraryConfigured"
            when: libraryModel.configured
            PropertyChanges {
                target: library
                visible: true
            }
            PropertyChanges {
                target: chooseLibrary
                visible: false
            }
        }
    ]

    ColumnLayout {
        id: library
        visible: false
        anchors.fill: parent

        ToolBar {
            id: toolBar
            Layout.fillWidth: true
            padding: 20

            background: Rectangle {
                color: '#eeeeee'
            }

            FilterBar {
                app: application
            }
        }

        MapListView {
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: viewList

            Connections {
                target: application

                function onFiltered(filtered) {
                    viewList.updateFilter(filtered)
                }

            }
        }

        DelegateModel {
            id: viewList
            model: libraryModel.maps
            delegate: MapCard {
            }

            groups: [
                DelegateModelGroup {
                    includeByDefault: true
                    name: "filtered"
                }

            ]

            function updateFilter(filtered) {
                viewList.items.removeGroups(0, viewList.items.count, "filtered")
                for(var i = 0; i < filtered.length; i++) {
                    var toUpdate = filtered[i].idx
                    viewList.items.addGroups(toUpdate, 1, "filtered")
                }
            }

            filterOnGroup: "filtered"
        }
    }


    ChooseLibraryPage {
        id: chooseLibrary
        visible: true
        onLibraryPathChosen: libraryModel.onImportFiles(path)
    }
}
