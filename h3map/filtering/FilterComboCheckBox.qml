import QtQuick 2.0
import QtQuick.Controls 2.12
import QtQuick.Layouts 1.12


ComboBox {
    id: control

    required property string filterName

    required property FilterOption options

    model: options.filterOptions

    height: 50

    popup: Popup {
        y: control.height + 10
        width: control.width + 50
        implicitHeight: contentItem.implicitHeight
        padding: 1

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: control.popup.visible ? control.delegateModel : null
            currentIndex: control.highlightedIndex
        }

        background: Rectangle {
            color: 'white'
            radius: 10

            border.width: 3
            border.color: '#dddddd'
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
        text: options.activeOptions
        font: control.font
        color: 'grey'
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignLeft
        elide: Text.ElideRight
    }

    background: Rectangle {
        implicitWidth: 150
        implicitHeight: 40
        border.color: options.color
        border.width: 3
        radius: 10
    }

    delegate: RowLayout {
        width: parent.width
        height: 50
        Layout.fillWidth: true

        CheckBox {
            id: filterSelected
            checked: selected
            enabled: model.enabled
            onClicked: {
                control.activated(index)
            }
        }

        Image {
            source: model.icon
        }

        Label {
            id: filterName
            text: name
            Layout.fillWidth: true
            horizontalAlignment: Qt.AlignBottom
        }

        Label {
            text: count
            color: 'grey'
            Layout.rightMargin: 10
            horizontalAlignment: Qt.AlignBottom
        }
    }
}
