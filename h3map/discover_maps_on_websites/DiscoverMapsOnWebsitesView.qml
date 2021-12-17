import QtQuick 2.0


import "../_QmlComponents"


Item {
    required property var model

    DiscoverMapsOnWebsites {
        id: onlineModel
        dispatcher: model
    }

    MapListView {
        id: discover
        model: onlineModel.maps

        anchors.fill: parent

        onContentYChanged: {
            if(isAtEnd()) {
                var requestedAmountOfItems = itemsPerPage()
                onlineModel.discover(requestedAmountOfItems)
            }
        }
    }

    onVisibleChanged: {
        if(visible)
            onlineModel.discover(10)
    }
}
