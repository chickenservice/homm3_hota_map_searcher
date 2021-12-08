import QtQuick 2.0
import QtQuick.Controls.Material 2.12
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.12
import QtQuick.Layouts 1.15
import QtQuick.Shapes 1.10


Rectangle {
        id: card

        anchors.leftMargin: 20
        anchors.rightMargin: 20

        width: 540
        height: 360

        border.color: '#dddddd'
        border.width: 2

        ColumnLayout {
            width: parent.width

            anchors {
                left: parent.left
                right: parent.right
                top: parent.top
                bottom: parent.bottom

                leftMargin: 20
                rightMargin: 20
                topMargin: 20
                bottomMargin: 20
            }

            spacing: 2

            Row {
                id: header

                spacing: 2

                Image {
                    source: model.thumbnail
                    sourceSize.width: 128
                    fillMode: Image.PreserveAspectFit
                }

                Column{

                    spacing: 2

                    Text {

                        width: 280

                        text: model.name
                        font.bold: true
                        font.pointSize: 12
                        wrapMode: Text.WordWrap
                    }

                    Column {
                        Row {
                            Image {
                                source: "icons/players.gif"
                            }

                            Text {
                                text: "Teams: " + model.teams
                                font.italic: true
                            }
                        }

                        Text {
                            text: "Human Players: " + model.humans
                            font.italic: true
                        }
                    }
                }
            }


            Text {
                id: description

                Layout.fillHeight: true
                Layout.preferredWidth: parent.width
                //Layout.preferredHeight: parent.height - header.height - toolbar.height - lastPlayed.height

                text: model.description
                maximumLineCount: 15
                wrapMode: Text.Wrap
            }

            Text {
                id: lastPlayed

                text: qsTr("Last played: Never")
                color: 'grey'
            }

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
                            icon.source: "star.png"
                            background: Rectangle {
                                color: "white"
                            }
                        }
                    }
                }
            }
        }
    }
