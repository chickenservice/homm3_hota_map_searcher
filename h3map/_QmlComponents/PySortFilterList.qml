import QtQuick 2.0
import QtQuick.Layouts 1.0
import QtQml.Models 2.1
import "../header/MapSummaryView"

Item {
    id: pysort

    required property var pyList

    required property var pyFilter

    property alias model: filteredList

    property alias delegate: filteredList.delegate

    PyListModel {
        list: ListModel {
            id: list
        }
        actions: pyList
    }

    PySortFilterModel {
        pyFilter: pysort.pyFilter
        filtered: DelegateModel {
            id: filteredList
            model: list
            delegate: delegate

            groups: [
                DelegateModelGroup {
                    includeByDefault: true
                    name: "filtered"
                }
            ]

            filterOnGroup: "filtered"
        }
    }
}
