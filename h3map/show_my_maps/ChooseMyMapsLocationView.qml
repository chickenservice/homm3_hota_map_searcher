import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.0


Item {
    id: libraryEmpty
    anchors.fill: parent

    signal libraryPathChosen(string path)

    ColumnLayout {
        Layout.alignment: Qt.AlignCenter

        Button {
            Layout.alignment: Qt.AlignCenter

            text: "Choose folder"

            onClicked: fileDialog.setVisible(true)
        }
    }

    FileDialog {
        id: fileDialog
        visible: false
        title: "Please choose a folder"
        folder: shortcuts.home
        selectFolder: true
        onAccepted: {
            console.log("You chose: " + fileDialog.folder)
            libraryEmpty.libraryPathChosen(fileDialog.folder)
        }
        onRejected: {
            console.log("Canceled")
        }
    }
}
