# SPDX-License-Identifier: MIT
import os
import krita
import re

def saveNextJpeg():
    document = krita.Krita.instance().activeDocument()
    fileName = document.fileName()
    filePrefix = re.sub(r'\.\w+$', '', fileName)
    fileDirname = os.path.dirname(fileName)

    latestIndex = 0
    existingFileRegex = re.compile('(?i)^{}(\d+)\.(?:png|jpe?g)$'.format(filePrefix))

    for f in os.listdir(fileDirname):
        match = existingFileRegex.search(os.path.join(fileDirname, f))
        if match:
            index = int(match.group(1))
            if index > latestIndex:
                latestIndex = index

    outputFileName = '{}{:03d}.jpg'.format(filePrefix, latestIndex + 1)
    exportConfiguration = krita.InfoObject()
    exportConfiguration.setProperties({
        'baseline': True,
        'exif': True,
        'filters': [],
        'iptc': True,
        'optimize': True,
        'progressive': False,
        'quality': 100,
        'saveProfile': True,
        'smoothing': 0,
        'subsampling': 0,
        'transparencyFillColor': [255, 255, 255],
        'xmp': True,
    })

    document.exportImage(outputFileName, exportConfiguration)

class SaveNextJpegExtension(krita.Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("save_next_jpeg", "Save next JPEG")
        action.triggered.connect(saveNextJpeg)


instance = krita.Krita.instance()
instance.addExtension(SaveNextJpegExtension(instance))
