import QtQuick 2.0

ListModel {
    id: mapList

     QtObject {
         property string name: "Ariane"
     }

     ListElement {

         name: "Bella"
         description: "Lorem ipsum dolor"
         thumbnail: "default.gif"
         teams: 0
         humans: 1
     }

     ListElement {

         name: "Corinna"
         description: "Lorem ipsum dolor"
         thumbnail: "default.gif"
         teams: 0
         humans: 1
     }

}
