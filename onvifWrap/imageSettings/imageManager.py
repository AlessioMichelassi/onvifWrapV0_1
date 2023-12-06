from onvif import ONVIFCamera
from PyQt6.QtCore import QObject, pyqtSignal

from onvifWrap.imageSettings.property.color import ColorSettings
from onvifWrap.imageSettings.property.focus import FocusSettings
from onvifWrap.imageSettings.property.shutter import ShutterSettings
from onvifWrap.imageSettings.property.whiteBalance import WhiteBalanceSettings


class ImageManager(QObject):
    mediaClient = None
    videoToken = None
    profiles = None
    imagingClient = None
    currentSettings = None

    # Imaging settings
    whiteBalance: WhiteBalanceSettings = None
    shutter: ShutterSettings = None
    focus: FocusSettings = None
    color: ColorSettings = None

    canAccessImagingSettings = False

    def __init__(self, cameraManager, parent=None):
        super().__init__(parent)
        self.cameraManager = cameraManager
        self.initImagingSettings()

    def initImagingSettings(self):
        try:
            self.mediaClient = self.cameraManager.cam.create_media_service()
            self.profiles = self.mediaClient.GetProfiles()
            if self.profiles:
                self.videoToken = self.profiles[0].VideoSourceConfiguration.SourceToken
                self.imagingClient = self.cameraManager.cam.create_imaging_service()
                self.cameraManager.serverMessageSignal.emit("Imaging settings initialized.")
                self.currentSettings = self.imagingClient.GetImagingSettings({"VideoSourceToken": self.videoToken})
            else:
                self.cameraManager.errorSignal.emit("No profiles found on the camera.")
        except Exception as e:
            self.cameraManager.errorSignal.emit(f"Error getting imaging settings: {e}")
        self.initImageProperties()

    def initImageProperties(self):
        self.whiteBalance = WhiteBalanceSettings(self, self.cameraManager)
        self.shutter = ShutterSettings(self, self.cameraManager)
        self.focus = FocusSettings(self, self.cameraManager)
        self.color = ColorSettings(self, self.cameraManager)

    def updateCurrentSettings(self):
        """
        Aggiorna le impostazioni correnti.
        ImagingService in Onvif Zeep crea un client per il servizio Imaging e lo interroga
        aggiornando le impostazioni correnti.
        :return:
        """
        self.currentSettings = self.imagingClient.GetImagingSettings({"VideoSourceToken": self.videoToken})
        try:
            pass
        except Exception as e:
            self.cameraManager.errorSignal.emit(f"Error retrieving imaging settings: {e}")

    def getCurrentSettings(self):
        if self.currentSettings is None:
            self.updateCurrentSettings()
        return self.currentSettings

    def emit(self, signal, message):
        if signal == "error":
            self.cameraManager.errorSignal.emit(message)
        elif signal == "serverMessage":
            self.cameraManager.serverMessageSignal.emit(message)

    def getAllOption(self):
        try:
            options = self.imagingClient.GetOptions({'VideoSourceToken': self.videoToken})
            return options
        except Exception as e:
            self.cameraManager.errorSignal.emit(f"Error retrieving imaging settings: {e}")
            return None
