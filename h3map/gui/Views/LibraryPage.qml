import QtQuick 2.0

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

    MapListView {
        id: library
        visible: false
        model: libraryModel.maps
    }

    ChooseLibraryPage {
        id: chooseLibrary
        visible: true
        onLibraryPathChosen: libraryModel.onImportFiles(path)
    }
}
