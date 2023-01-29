import QtQuick 2.12
import QtQml.Models 2.1

Item {

    required property var pyFilter

    required property DelegateModel filtered

    function updateFilter(summary) {
        var toFilter = summary["filtered"]
        for(var i = 0; i < toFilter.length; i++) {
            filtered.items.addGroups(toFilter[i], 1, "filtered")
        }
    }

    function clearFilter() {
        filtered.items.addGroups(0, filtered.items.count, "filtered")
    }

    Connections {
        target: pyFilter

        function onApplying() {
            filtered.items.removeGroups(0, filtered.items.count, "filtered")
        }

        function onApplied(toFilter) {
            updateFilter(toFilter)
        }

        function onCleared() {
            clearFilter()
        }
    }
}
