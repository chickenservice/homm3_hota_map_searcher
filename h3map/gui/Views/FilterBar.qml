import QtQuick 2.0
import QtQuick.Dialogs 1.0
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "../ViewModels"
import "../ViewModels/Library"
import "Components"

Row {

    required property FilterModel filterModel

    id: filterBar

    spacing: 10

    FilterComboCheckBox {
        filterName: "Players"

        model: filterModel.amountOfPlayerOptions

        onActivated: {
            filterModel.toggleAmountOfPlayers(index)
        }
    }

    FilterComboCheckBox {
        filterName: "Teams"

        model: filterModel.teamSizeOptions

        onActivated: {
            filterModel.toggleTeamSize(index)
        }
    }

    FilterComboCheckBox {
        filterName: "Map Size"

        model: filterModel.mapSizeOptions

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
