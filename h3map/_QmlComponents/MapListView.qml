import QtQuick 2.0
import QtQuick.Controls.Material 2.12
import QtQuick.Controls 2.15
import QtGraphicalEffects 1.12
import QtQuick.Layouts 1.15
import QtQuick.Shapes 1.10


GridView {
    id: mapListView

    clip: true

    cellWidth: 600
    cellHeight: 400

    flow: GridView.FlowLeftToRight

    ScrollBar.vertical: ScrollBar {}

    function currentPage() {
        var totalHeight = ((height / cellHeight) * (count / (width / cellWidth)))
        var maxRowsPerPage = Math.floor(height / cellHeight)
        return Math.floor(contentY / height)
    }

    function itemsPerPage() {
        var maxRowsPerPage = Math.floor(height / cellHeight)
        var maxColumnsPerPage = Math.floor(width / cellWidth)
        return maxRowsPerPage * maxColumnsPerPage
    }

    function isAtEnd() {
        var totalHeight = ((height / cellHeight) * (count / (width / cellWidth)))
        return (contentY + height) >= totalHeight
    }

    add: Transition {
        NumberAnimation { properties: "scale"; from: 0; to: 1.0; duration: 400 }
        NumberAnimation { properties: "opacity"; from: 0; to: 1.0; duration: 400 }
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.66}
}
##^##*/
