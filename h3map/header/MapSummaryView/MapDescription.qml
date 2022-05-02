import QtQuick 2.0
import QtQuick.Layouts 1.3

import "../../"

ColumnLayout {
    Layout.fillHeight: true
    Layout.preferredWidth: parent.width

    Text {
        id: description

        Layout.fillHeight: true
        Layout.preferredWidth: parent.width

        text: model.description
        maximumLineCount: 15
        wrapMode: Text.Wrap
    }
}
