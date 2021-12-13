import QtQuick 2.0
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.5

RowLayout {
    id: toolbar

    width: parent.width

    Layout.alignment: Qt.AlignBottom

    Button {
        Layout.alignment: Qt.AlignLeft
        Layout.fillWidth: true

        text: "Play"
    }

    Button {
        Layout.alignment: Qt.AlignLeft
        Layout.fillWidth: true

        text: "Details"
    }

    Button {
        Layout.alignment: Qt.AlignLeft
        Layout.fillWidth: true

        text: "Download"
    }

    Row {
        Layout.alignment: Qt.AlignRight

        Repeater{
            model: 5

            ToolButton{
                icon.source: "../../../icons/star.png"
                background: Rectangle {
                    color: "white"
                }
            }
        }
    }
}
