# SPDX-License-Identifier: MIT
import os
import krita
import re

def saveNextPng():
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

    outputFileName = '{}{:03d}.png'.format(filePrefix, latestIndex + 1)
    exportConfiguration = krita.InfoObject()
    exportConfiguration.setProperties({
        'alpha': False,
        'compression': 9,
        'forceSRGB': True,
        'indexed': False,
        'interlaced': False,
        'saveSRGBProfile': False,
        'transparencyFillcolor': [255, 255, 255],
    })

    document.exportImage(outputFileName, exportConfiguration)

class SaveNextPngExtension(krita.Extension):

    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction("save_next_png", "Save next PNG")
        action.triggered.connect(saveNextPng)


instance = krita.Krita.instance()
instance.addExtension(SaveNextPngExtension(instance))
