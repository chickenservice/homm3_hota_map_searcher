import QtQuick 2.0
import QtQuick.Dialogs 1.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "ViewModels"
import "Views"
import "Views/Components"

Rectangle {
    required property var app

    anchors.fill: parent

    color: '#eeeeee'

    Item {
        id: logger

        Connections {
            target: app

            function onFiltered(summary) {
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
            TabButton{
                text: qsTr("Discover")
            }
            TabButton{
                text: qsTr("Settings")
            }
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.fillHeight: true

            StackLayout{
                currentIndex: menu.currentIndex
                Layout.fillWidth: true
                Layout.fillHeight: true

                LibraryPage {
                    id: libraryTab
                    application: app
                }

                DiscoverPage {
                    id: discoverTab
                    model: app
                }
            }
        }

        ToolBar {
            Layout.fillWidth: true
            Layout.alignment: Qt.AlignTop

            ProgressBar {
                id: progress

                Connections {
                    target: app

                    function onStarting(maxCount) {
                        progress.to = maxCount
                    }

                    function onAddMap(header) {
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
