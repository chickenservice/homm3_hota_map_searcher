import QtQuick 2.0
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0

import "../ViewModels"
import "Components"

Item {
    required property var model

    LibraryModel {
        id: libraryModel
        dispatcher: model
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
                app: model
            }
        }

        MapListView {
            model: libraryModel.maps
            Layout.fillWidth: true
            Layout.fillHeight: true
        }
    }


    ChooseLibraryPage {
        id: chooseLibrary
        visible: true
        onLibraryPathChosen: libraryModel.onImportFiles(path)
    }
}
