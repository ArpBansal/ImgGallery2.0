import QtQuick
import QtQuick.Controls.Basic
import QtQuick.Controls
// ApplicationWindow {
//     visible: true
//     width: 600
//     height: 500
//     title: "HelloApp"
//     Text {
//         anchors.centerIn: parent
//         text: "Hello World"
//         font.pixelSize: 24
//     }
// }


ApplicationWindow {
    visible: true
    width: 800
    height: 600
    title: "Image Gallery"

    GridView {
        anchors.fill: parent
        cellWidth: 200
        cellHeight: 200
        model: ListModel {
            ListElement { imageSource: "IMG_1526.JPG" }
            ListElement { imageSource: "IMG_1534.JPG" }
            ListElement { imageSource: "IMG_1536.JPG" }
            // Add more images as needed
        }

        delegate: Item {
            width: 200
            height: 200

            Image {
                anchors.fill: parent
                source: model.imageSource
                fillMode: Image.PreserveAspectCrop
                rotation:90
            }
        }
    }
}

// ImageGallery.qml
# main.py

import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickView
from PyQt6.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    url = QUrl.fromLocalFile("ImageGallery.qml")

    engine.load(url)
    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()


import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: window
    width: 800
    height: 600
    visible: true
    title: "Image Gallery"

    // Navigation Bar
    Rectangle {
        id: navBar
        height: 60
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        color: "#333"

        RowLayout {
            anchors.fill: parent
            anchors.margins: 10
            spacing: 10

            Button {
                text: "Open Folder"
                onClicked: folderDialog.open()
            }

            Button {
                text: "Previous"
                enabled: gridView.currentIndex > 0
                onClicked: gridView.currentIndex--
            }

            Button {
                text: "Next"
                enabled: gridView.currentIndex < gridView.count - 1
                onClicked: gridView.currentIndex++
            }
        }
    }

    // GridView for images
    GridView {
        id: gridView
        anchors.top: navBar.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        cellWidth: 200
        cellHeight: 200
        clip: true
        focus: true

        // Image loading animation
        Component {
            id: imageDelegate

            Rectangle {
                id: imageContainer
                width: gridView.cellWidth
                height: gridView.cellHeight
                color: "#444"

                Image {
                    id: image
                    anchors.fill: parent
                    source: model.source
                    asynchronous: true
                    cache: false

                    onStatusChanged: {
                        if (status == Image.Loading) {
                            loadingAnimation.start();
                        } else if (status == Image.Ready) {
                            loadingAnimation.stop();
                        }
                    }

                    // Loading animation
                    Rectangle {
                        id: loadingRect
                        anchors.centerIn: parent
                        width: 50
                        height: 50
                        radius: 25
                        color: "#666"
                        visible: image.status == Image.Loading

                        RotationAnimation {
                            id: loadingAnimation
                            target: loadingRect
                            from: 0
                            to: 360
                            duration: 1000
                            loops: Animation.Infinite
                        }
                    }
                }

                // Hover effect
                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true

                    onEntered: {
                        imageContainer.color = "#555";
                    }

                    onExited: {
                        imageContainer.color = "#444";
                    }
                }
            }
        }

        // Image model
        model: ListModel {
            id: imageModel

            // Add images to the model here
            // For example:
            // ListElement { source: "image1.jpg" }
            // ListElement { source: "image2.jpg" }
        }

        delegate: imageDelegate
    }

    // Folder dialog for opening image folder
    FileDialog {
        id: folderDialog
        title: "Open Image Folder"
        folder: shortcuts.pictures
        selectFolder: true

        onAccepted: {
            // Load images from the selected folder here
            // For example:
            // imageModel.clear();
            // var files = folderDialog.fileUrls;
            // for (var i = 0; i < files.length; i++) {
            //     imageModel.append({ source: files[i] });
            // }
        }
    }
}