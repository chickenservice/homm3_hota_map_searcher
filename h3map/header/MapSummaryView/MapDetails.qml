import QtQuick 2.0

Row {
    id: header

    spacing: 2

    Image {
        source: "../../_QmlComponents/img/"// + model.thumbnail
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

        Row {
            spacing: 15
        Column{
            Text {
                text: "Teams: "// + model.teams
                font.italic: true
            }

            Text {
                text: "Players: "// + model.players
                font.italic: true
            }

            Text {
                text: "Humans: "// + model.humans
                font.italic: true
            }

            Text {
                text: "Winning condition: " + model.victory_condition
                font.italic: true
            }

            Text {
                text: "Loss condition: " + model.loss_condition
                font.italic: true
            }

            }
        Column {

            Text {
                text: "Map size: " + model.map_size
                font.italic: true
            }

            Text {
                text: "Difficulty: " + model.difficulty
                font.italic: true
            }
        }

        }

    }
}
