import QtQuick 2.0

Row {
    id: header

    spacing: 2

    Image {
        source: "../../_QmlComponents/img/" + model.thumbnail
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
                    source: "../../_QmlComponents/icons/players.gif"
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
