import QtQuick 2.0

import ".."

Item {
    required property ListModel filterOptions

    required property string name

    property string color: "#dddddd"

    property color activeFilter: Theme.primary

    property string activeOptions: name

    function toggleFilter(index) {
        var status = filterOptions.get(index).selected
        filterOptions.setProperty(index, "selected", !status)
        toggleActive()
    }

    function clearAll() {
        for(var i = 0; i < filterOptions.count; i++) {
            filterOptions.setProperty(i, "selected", false)
        }
        toggleActive()
        setAvailableOptions()
    }

    function toggleActive() {
        let active = getActiveOptions()
        if(active.length > name.length) {
            color = activeFilter
            activeOptions = active
        }
        else {
            color = "#dddddd"
            activeOptions = name
        }
    }

    function setAvailableOptions() {
        for(var i = 0; i < filterOptions.count; i++) {
            let count = filterOptions.get(i).count
            if(count > 0) {
                filterOptions.setProperty(i, "enabled", true)
            }
            else {
                filterOptions.setProperty(i, "enabled", false)
                filterOptions.setProperty(i, "selected", false)
            }
        }
    }

    function getActiveOptions() {
        let activated = name
        var count = 0
        for(var i = 0; i < filterOptions.count; i++) {
            if(filterOptions.get(i).selected) {
                let active = filterOptions.get(i).name
                if(activated.length === name.length) {
                    activated += ": " + active
                }
                else {
                    count++
                    activated = activated.split("  +")[0]
                    activated += "  +" + count
                }
            }
        }

        return activated
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

    Component.onCompleted: setAvailableOptions()
}
