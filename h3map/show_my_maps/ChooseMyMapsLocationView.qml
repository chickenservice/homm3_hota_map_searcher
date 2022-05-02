import QtQuick 2.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Dialogs 1.0


Item {
    id: libraryEmpty
    anchors.fill: parent
    anchors.margins: Qt.AlignCenter

    signal libraryPathChosen(string path)

    ColumnLayout {
        Layout.fillWidth: true
        Layout.fillHeight: true
        Layout.alignment: Qt.AlignCenter

        Text {
            text: "Frohe Weihnachten du Nette!🎄🎁\nSodass wir noch viele tolle Spieleabende miteinander verbringen ♥"
        }

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
