import QtQuick 2.0
import QtQuick.Dialogs 1.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "ViewModels"
import "Views"

Rectangle {
    required property var app

    anchors.fill: parent

    color: '#eeeeee'

    GridLayout{
        anchors.fill: parent

        columns: 1
        rows: 3

        rowSpacing: 10

        TabBar {
            id: menu

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

        StackLayout{
            currentIndex: menu.currentIndex

            Layout.alignment: Qt.AlignTop

            LibraryPage {
                id: libraryTab
                model: app
            }

            DiscoverPage {
                id: discoverTab
                model: app
            }
        }

        ToolBar {
            Layout.fillWidth: true

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
