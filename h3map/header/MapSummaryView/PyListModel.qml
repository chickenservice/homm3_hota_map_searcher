import QtQuick 2.12
import QtQml.Models 2.1

Item {
    required property ListModel list

    required property var actions

    Connections {
        target: actions

        function onItemAdded(item) {
            //header.idx = maps.count
            list.append(item)
        }
    }

    Component.onCompleted: {
        actions.items()
    }
}
