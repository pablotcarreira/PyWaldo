import QtQuick 2.0

Rectangle {
    width: 110
    height: 110
    color: "#000000"
    visible: true

    Behavior on y {
        SequentialAnimation{
            //colocar outros passos, ex: mudar a imagem.
           NumberAnimation { duration: 100 }
        }
    }

    Image {
        id: image1
        x: 0
        y: 0
        source: "imagens/waldo.svg"
    }

    function mudarPosicao(newY) {
        y = y + newY
    }

}
