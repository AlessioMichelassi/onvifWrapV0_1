from onvif import ONVIFCamera
from PyQt6.QtCore import QObject, pyqtSignal

from onvifWrap.imageSettings.imageManager import ImageManager


class OnvifCamManager(QObject):
    ip = "127.0.0.1"
    port = 2000
    username = "admin"
    password = "admin"
    cam: ONVIFCamera
    ptz = None
    mediaService = None  # Serve per ottenere il profilo di streaming
    mediaProfile = None  # Profilo di streaming
    imageManager: ImageManager = None
    errorSignal = pyqtSignal(str)
    serverMessageSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def _connectCamera(self, credentialDictionary: dict):
        """
        Credential deve essere un dizionario con le chiavi ip e port
        username e password.
        credential = {
                        "ip": "127.0.0.1",
                        "port": 2000,
                        "username": "admin",
                        "password": "admin"
                    }
        :param credentialDictionary:
        :return:
        """
        self.ip = credentialDictionary["ip"]
        self.port = credentialDictionary["port"]
        if "username" in credentialDictionary.keys():
            self.username = credentialDictionary["username"]
        if "password" in credentialDictionary.keys():
            self.password = credentialDictionary["password"]
        try:
            self.cam = ONVIFCamera(self.ip, self.port, self.username, self.password)
            self.cam.devicemgmt.GetServices(False)
            self.serverMessageSignal.emit(f"Connected to {self.ip}:{self.port}")
            return True
        except Exception as e:
            errorString = f"From onvifCam.connectCam:\n\tThere is an issue trying connecting\n\t{e}"
            self.errorSignal.emit(errorString)
            return False

    def connectCamera(self, credentialDictionary: dict):
        if self._connectCamera(credentialDictionary):
            self.createMediaService()

            return True
        else:
            return False

    def createMediaService(self):
        """
        Crea il media service che serve per ottenere il profilo di streaming.
        :return:
        """
        self.mediaService = self.cam.create_media_service()
        self.mediaProfile = self.mediaService.GetProfiles()[0]
        self.imageManager = ImageManager(self)


# test class

if __name__ == '__main__':
    credential = {
        "ip": "192.168.1.52",
        "port": 2000,
    }
    onvifCam = OnvifCamManager()
    onvifCam.errorSignal.connect(print)
    onvifCam.serverMessageSignal.connect(print)
    onvifCam.connectCamera(credential)
    IM = onvifCam.imageManager

    print(f"Focus isAuto: {IM.focus.isAuto}")
    print(f"Focus defaultSpeed: {IM.focus.defaultSpeed}")
    print(f"Focus speedRange: {IM.focus.speedRange}")
    print(f"Focus focusNearRange: {IM.focus.focusNearRange}")
    print(f"Focus focusFarRange: {IM.focus.focusFarRange}")
    print(f"Focus extensions: {IM.focus.extensions}")
    IM.focus.isAuto = False
    IM.focus.defaultSpeed = 10
    print(f"Focus {IM.focus.getSettings()}")
    IM.focus.focusNearLimit = 200
    IM.focus.focusFarLimit = 200
    print(f"Focus {IM.focus.getSettings()}")

    #print(IM.shutter.getAllOptions())
    print(f"Shutter isAuto: {IM.shutter.gainRange}")
    IM.shutter.isAuto = False
    IM.shutter.aperture = 20
    IM.shutter.aperture = 5
    IM.shutter.shutterTime = 100
    IM.shutter.gain = 100
    IM.shutter.isAuto = True
    IM.shutter.priority = "FrameRate"
    print(f"Shutter Priority {IM.shutter.priority}")

    print(f"Shutter {IM.shutter.getSettings()}")
    IM.color.brightness = 50
    IM.color.contrast = 50
    IM.color.saturation = 50
    IM.color.sharpness = 50

    print(f"backLightCompensation {IM.color.backlightCompensation}")
    IM.color.isBacklightCompensation = "ON"
    IM.color.backlightCompensation = 10

    print(f"irCutFilter {IM.color.irCutFilter}")

    #IM.color.irCutFilter = "OFF"
