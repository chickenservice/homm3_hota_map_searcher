import QtQuick 2.0

Item {
    required property var filterOptions

    signal filterSelected

    function toggleFilter(index) {
        var status = filterOptions.get(index).selected
        filterOptions.setProperty(index, "selected", !status)
    }

    function clearAll() {
        for(var i = 0; i < filterOptions.count; i++) {
            filterOptions.setProperty(i, "selected", false)
        }
    }

    function getRule(index) {
        return filterOptions.get(index).rule()
    }

    function getSelection() {
        var selectedOptions = {}
        for(var i = 0; i < filterOptions.count; i++) {
            var option = filterOptions.get(i)
            selectedOptions[option.name] = {selected: option.selected, value: option.value}
        }

        return selectedOptions
    }
}
