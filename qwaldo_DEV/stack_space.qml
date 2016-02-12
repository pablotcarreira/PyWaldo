import QtQuick 2.0
import QtQuick.Controls 1.1

Rectangle {
    id: rectangle1
    width: 640
    height: 800

    Grid {
        id: modulos_grid
        objectName: "modulos_grid"
        x: 30
        y: 30
        width: 178
        height: 643
        spacing: 5
        rows: 7

        Modulo {
            objectName: "m1"
            id: modulo1
            transformOrigin: Item.Center
        }

        Modulo {
            objectName: "m2"
            id: modulo2
        }

        Modulo {
            objectName: "m3"
            id: modulo3
        }

        Modulo {
            objectName: "m4"
            id: modulo4
            y: 327
        }

        Modulo {
            objectName: "m5"
            id: modulo5
            y: 407
        }

        Modulo {
            objectName: "m6"
            id: modulo6
            x: 0
            y: 520
        }
    }
}
