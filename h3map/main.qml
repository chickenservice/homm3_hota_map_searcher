import QtQuick 2.0
import QtQuick.Dialogs 1.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


import "show_my_maps"
import "header/MapSummaryView"


Rectangle {
    required property var importToLibrary

    anchors.fill: parent

    color: '#eeeeee'

    Item {
        id: logger

        Connections {
            target: importToLibrary

            function onApplied(summary) {
                console.log('Filtered items: ', summary["filtered"].length)
            }
        }
    }

    GridLayout{
        id:content

        anchors.fill: parent

        columns: 1
        rows: 3

        rowSpacing: 0
        columnSpacing: 0

        TabBar {
            id: menu

            Layout.fillWidth: true

            TabButton{
                text: qsTr("Library")
            }
            /*
            TabButton{
                text: qsTr("Discover")
            }
            TabButton{
                text: qsTr("Settings")
            }*/
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true

            StackLayout{
                currentIndex: menu.currentIndex
                Layout.fillWidth: true
                Layout.fillHeight: true

                MyMapsView {
                    id: libraryTab
                    libraryModel: MyMaps {
                        libraryActions: importToLibrary
                        delegate: MapSummaryView {}
                    }
                }
            }
        }

        ToolBar {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop

            ProgressBar {
                id: progress

                Connections {
                    target: importToLibrary

                    function onImportingMaps(maxCount) {
                        progress.to = maxCount
                    }

                    function onImportedMap(header) {
                        progress.value += 1
                    }
                }
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}D{i:1}D{i:2}D{i:5}D{i:4}D{i:7}D{i:6}D{i:3}D{i:9}D{i:10}
D{i:11}D{i:8}
}
##^##*/
