import QtQuick 2.0

Item {
    required property var filterMock

    FilterBar {
        filterModel: Filter {
            filter: filterMock
        }
    }
}
