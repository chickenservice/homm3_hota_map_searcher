import QtQuick 2.12
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.0
import QtQml.Models 2.1
import "../../_QmlComponents"
import "../../filtering"

Item {
    id: comp

    required property var pyFilter;

    required property var libraryModel;

    required property var table;

    anchors.fill: parent

    /*
    PySortFilterList {
        id: filtered
        pyList: libraryModel
        pyFilter: comp.pyFilter
        delegate: MapSummaryView {}
    }
    */

    ColumnLayout {
        anchors.fill: parent

        ToolBar {
            id: toolBar
            Layout.fillWidth: true
            padding: 20

            background: Rectangle {
                color: '#eeeeee'
            }

            FilterBar {
                filterModel: Filter {
                    filter: pyFilter
                }
            }
        }


        MapListView {
            id: listview

            Layout.fillWidth: true
            Layout.fillHeight: true

            model: comp.table
            delegate: MapSummaryView {}

            Connections {
                target: pyFilter

                function onApplying(summary) {
                    table.applyFilter(summary)
                }
            }
        }
    }
}


