import QtQuick 2.0
import QtQuick.Layouts 1.3

import "../../_QmlComponents"

Card {
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

        MapDetails {

        }

        MapDescription {

        }

        Toolbar {

        }
    }
}
