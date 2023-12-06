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



