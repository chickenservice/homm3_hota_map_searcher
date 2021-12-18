import QtQuick 2.0
import QtQuick.Dialogs 1.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Row {

    required property Filter filterModel

    id: filterBar

    spacing: 10

    FilterComboCheckBox {
        filterName: "Players"

        options: filterModel.amountOfPlayerOptions

        onActivated: {
            filterModel.toggleAmountOfPlayers(index)
        }
    }

    FilterComboCheckBox {
        filterName: "Teams"

        options: filterModel.teamSizeOptions

        onActivated: {
            filterModel.toggleTeamSize(index)
        }
    }

    FilterComboCheckBox {
        filterName: "Map Size"

        options: filterModel.mapSizeOptions

        onActivated: {
            filterModel.toggleMapSize(index)
        }
    }

    Button {
        text: "Clear"

        onClicked: {
            filterModel.clear()
        }
    }


}
