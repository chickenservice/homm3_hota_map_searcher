import QtQuick 2.0
import QtQuick.Controls 2.12


ComboBox {
    id: control

    required property string filterName

    height: 50

    popup: Popup {
        y: control.height - 10
        width: control.width
        implicitHeight: contentItem.implicitHeight
        padding: 1

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex

            ScrollIndicator.vertical: ScrollIndicator { }
        }

        background: Rectangle {
            color: 'white'
            radius: 10

            border.width: 3
            border.color: '#dddddd'

            Rectangle {
                width: parent.width - 6
                height: parent.height - 6
                x: parent.x + 3
                y: parent.y - 5

                radius: 10
            }
        }
    }

    indicator: Canvas {
        id: canvas
        x: control.width - width - control.rightPadding
        y: control.topPadding + (control.availableHeight - height) / 2
        width: 12
        height: 8
        contextType: "2d"

        Connections {
            target: control
            function onPressedChanged() { canvas.requestPaint(); }
        }

        onPaint: {
            context.reset();
            context.moveTo(0, 0);
            context.lineTo(width, 0);
            context.lineTo(width / 2, height);
            context.closePath();
            context.fillStyle = 'grey';
            context.fill();
        }
    }

    contentItem: Text {
        text: control.filterName
        font: control.font
        color: 'grey'
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        elide: Text.ElideRight
    }

    background: Rectangle {
        implicitWidth: 120
        implicitHeight: 40
        border.color: '#dddddd'
        border.width: 3
        radius: 10
    }

    delegate: Item {
        width: parent.width
        height: 50

        Row {
            CheckBox {
                id: filterSelected
                checked: selected
                onClicked: {
                    control.activated(index)
                }
            }

            Image {
                source: model.icon
            }

            Label {
                text: name
                verticalAlignment: Qt.AlignVCenter
                horizontalAlignment: Qt.AlignHCenter
            }

            Label {
                text: count
                padding: { left: 5; right: 5 }
                horizontalAlignment: Qt.AlignRight
            }
        }
    }
}
