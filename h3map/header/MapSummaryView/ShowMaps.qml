import QtQuick 2.0
import QtQuick.Layouts 1.0

import "../../_QmlComponents"

Item {
    required property Maps m;

    anchors.fill: parent

    ColumnLayout {
        anchors.fill: parent

        MapListView {
            id: listview
            Layout.fillWidth: true
            Layout.fillHeight: true
            model: m.maps
            delegate: MapSummaryView {}
        }
    }

}
