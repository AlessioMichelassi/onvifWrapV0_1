"""
    Onvis Wrap can be helpful to use with PyQt6.
usage:

"""

from PyQt6.QtCore import *

from onvif import ONVIFCamera


from onvifWrap.onvifManager import OnvifCamManager

def main():
    credential = {
            "ip": "192.168.1.52",
            "port": 2000,
        }
    onvifCam = OnvifCamManager()
    onvifCam.errorSignal.connect(print)
    onvifCam.serverMessageSignal.connect(print)
    onvifCam.connectCamera(credential)
    IM = onvifCam.imageManager