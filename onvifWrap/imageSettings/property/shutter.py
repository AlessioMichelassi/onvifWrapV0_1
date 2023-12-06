from PyQt6.QtCore import *


class ShutterSettings(QObject):

    def __init__(self, imageManager: 'ImageManager', parent=None):
        super().__init__(parent)
        self.imageManager = imageManager
        self.getSettings()
        self.getAllOptions()

    def getSettings(self):
        currentSettings = self.imageManager.currentSettings
        shutter_dict = {}
        if hasattr(currentSettings, 'Exposure'):
            for attr in dir(currentSettings.Exposure):
                if not attr.startswith('_') and hasattr(currentSettings.Exposure, attr):
                    value = getattr(currentSettings.Exposure, attr)
                    shutter_dict[attr] = value
            return shutter_dict
        else:
            self.emitError("getSettings: Error retrieving Dictionary of shutter settings")

    def getAllOptions(self):
        try:
            options = self.imageManager.imagingClient.GetOptions({'VideoSourceToken': self.imageManager.videoToken})
            shutter_dict = {}
            if hasattr(options, 'Exposure'):
                for attr in dir(options.Exposure):
                    if not attr.startswith('_'):
                        value = getattr(options.Exposure, attr)
                        shutter_dict[attr] = value
                return shutter_dict
            else:
                self.emitError("getAllOptions: Error retrieving Dictionary of shutter settings")
                return {}
        except Exception as e:
            self.emitError(f"getAllOptions: Error retrieving Dictionary of shutter settings: {e}")
            return {}

    @property
    def isAuto(self):
        dictionary = self.getSettings()
        if not dictionary:
            self.emitError("isAuto: Error retrieving Dictionary of focus settings")
            return None
        if "Mode" in dictionary:
            if dictionary["Mode"] == "AUTO":
                return True
            else:
                return False
        else:
            self.emitError("isAuto: Error retrieving Dictionary of focus settings")
            return None

    @isAuto.setter
    def isAuto(self, value):
        if value:
            self.setMode("AUTO")
        else:
            self.setMode("MANUAL")

    @property
    def apertureRange(self):
        dictionary = self.getSettings()
        if not dictionary:
            self.emitError("apertureRange: Error retrieving Dictionary of focus settings")
            return None
        if "Iris" in dictionary:
            return dictionary["MinIris"], dictionary["MaxIris"]
        else:
            self.emitError("apertureRange: Error retrieving Dictionary of focus settings")
            return None

    @property
    def gainRange(self) -> list:
        dictionary = self.getAllOptions()
        if not dictionary:
            self.emitError("fainRange: Error retrieving Dictionary of shutter settings")
            return [0,0]
        if 'Gain' in dictionary.keys():
            return [dictionary['Gain']['Min'], dictionary['Gain']['Max']]
        else:
            self.emitError("gainRange: Error retrieving Gain limits from dictionary")
            return [0,0]

    @property
    def shutterRange(self)-> list:
        dictionary = self.getSettings()
        if not dictionary:
            self.emitError("shutterRange: Error retrieving Dictionary of focus settings")
            return [0,0]
        if "ExposureTime" in dictionary:
            return [dictionary["MinExposureTime"], dictionary["MaxExposureTime"]]
        else:
            self.emitError("shutterRange: Error retrieving Dictionary of focus settings")
            return [0,0]

    @property
    def aperture(self):
        currentSettings = self.imageManager.getCurrentSettings()
        if hasattr(currentSettings, 'Exposure'):
            shutterSettings = currentSettings.Exposure
            if hasattr(shutterSettings, 'Iris'):
                return currentSettings.Exposure.Iris
        else:
            return None

    @aperture.setter
    def aperture(self, value):
        if self.isAuto:
            msg = "Cannot set iris in auto mode"
            self.imageManager.emit("error", msg)
            return
        if not self.apertureRange:
            msg = "Cannot set iris, irisRange is None"
            self.imageManager.emit("error", msg)
            return

        try:
            if value < self.apertureRange[0] or value > self.apertureRange[1]:
                msg = f"Iris value out of range. Min: {self.apertureRange[0]}, Max: {self.apertureRange[1]}"
                self.imageManager.emit("error", msg)
                return
            # Assicurati di avere le impostazioni di imaging correnti
            currentSettings = self.imageManager.getCurrentSettings()
            # Aggiorna solo la modalità di bilanciamento del bianco
            if hasattr(currentSettings, 'Exposure'):
                currentSettings.Exposure.Iris = value

                self.imageManager.imagingClient.SetImagingSettings({
                    'VideoSourceToken': self.imageManager.videoToken,
                    'ImagingSettings': currentSettings
                })
                # Ricarica le impostazioni per verificare che l'aggiornamento sia andato a buon fine
                self.checkOperationResult("Iris", value)
            else:
                self.imageManager.emit("error", "Shutter settings not available")
        except Exception as e:
            msg = f"Error setting shutter mode to {value}: {e}"
            self.imageManager.emit("error", msg)

    @property
    def shutterTime(self):
        currentSettings = self.imageManager.getCurrentSettings()
        if hasattr(currentSettings, 'Exposure'):
            shutterSettings = currentSettings.Exposure
            if hasattr(shutterSettings, 'ExposureTime'):
                return currentSettings.Exposure.ExposureTime

    @shutterTime.setter
    def shutterTime(self, value):
        if self.isAuto:
            msg = "Cannot set exposure time in auto mode"
            self.imageManager.emit("error", msg)
            return
        if value < self.shutterRange[0] or value > self.shutterRange[1]:
            msg = f"Shutter value out of range. Min: {self.shutterRange[0]}, Max: {self.shutterRange[1]}"
            self.imageManager.emit("error", msg)
            return
        try:
            # Assicurati di avere le impostazioni di imaging correnti
            currentSettings = self.imageManager.getCurrentSettings()
            # Aggiorna solo la modalità di bilanciamento del bianco
            if hasattr(currentSettings, 'Exposure'):
                currentSettings.Exposure.ExposureTime = value

                self.imageManager.imagingClient.SetImagingSettings({
                    'VideoSourceToken': self.imageManager.videoToken,
                    'ImagingSettings': currentSettings
                })
                # Ricarica le impostazioni per verificare che l'aggiornamento sia andato a buon fine
                self.checkOperationResult("ExposureTime", value)
            else:
                self.imageManager.emit("error", "Shutter settings not available")
        except Exception as e:
            msg = f"Error setting shutter mode to {value}: {e}"
            self.imageManager.emit("error", msg)

    @property
    def gain(self):
        currentSettings = self.imageManager.getCurrentSettings()
        if hasattr(currentSettings, 'Exposure'):
            shutterSettings = currentSettings.Exposure
            if hasattr(shutterSettings, 'Gain'):
                return currentSettings.Exposure.Gain

    @gain.setter
    def gain(self, value):
        if self.isAuto:
            msg = "Cannot set gain in auto mode"
            self.imageManager.emit("error", msg)
            return
        if value < self.gainRange[0] or value > self.gainRange[1]:
            msg = f"Gain value out of range. Min: {self.gainRange[0]}, Max: {self.gainRange[1]}"
            self.imageManager.emit("error", msg)
            return
        try:
            # Assicurati di avere le impostazioni di imaging correnti
            currentSettings = self.imageManager.getCurrentSettings()
            # Aggiorna solo la modalità di bilanciamento del bianco
            if hasattr(currentSettings, 'Exposure'):
                currentSettings.Exposure.Gain = value

                self.imageManager.imagingClient.SetImagingSettings({
                    'VideoSourceToken': self.imageManager.videoToken,
                    'ImagingSettings': currentSettings
                })
                # Ricarica le impostazioni per verificare che l'aggiornamento sia andato a buon fine
                self.checkOperationResult("Gain", value)
            else:
                self.imageManager.emit("error", "Shutter settings not available")
        except Exception as e:
            msg = f"Error setting shutter mode to {value}: {e}"
            self.imageManager.emit("error", msg)

    @property
    def shutterPriority(self):
        currentSettings = self.imageManager.getCurrentSettings()
        if hasattr(currentSettings, 'Exposure'):
            shutterSettings = currentSettings.Exposure
            if hasattr(shutterSettings, 'ExposurePriority'):
                return currentSettings.Exposure.ExposurePriority

    @shutterPriority.setter
    def shutterPriority(self, value):
        try:
            # Assicurati di avere le impostazioni di imaging correnti
            currentSettings = self.imageManager.getCurrentSettings()
            # Aggiorna solo la modalità di bilanciamento del bianco
            if hasattr(currentSettings, 'Exposure'):
                currentSettings.Exposure.ExposurePriority = value

                self.imageManager.imagingClient.SetImagingSettings({
                    'VideoSourceToken': self.imageManager.videoToken,
                    'ImagingSettings': currentSettings
                })
                # Ricarica le impostazioni per verificare che l'aggiornamento sia andato a buon fine
                self.checkOperationResult("ExposurePriority", value)
            else:
                self.imageManager.emit("error", "Shutter settings not available")
        except Exception as e:
            msg = f"Error setting shutter mode to {value}: {e}"
            self.imageManager.emit("error", msg)

    @property
    def priority(self):
        currentSettings = self.imageManager.getCurrentSettings()
        if hasattr(currentSettings, 'Exposure'):
            shutterSettings = currentSettings.Exposure
            return shutterSettings.Priority

    @priority.setter
    def priority(self, value):
        try:
            # Assicurati di avere le impostazioni di imaging correnti
            currentSettings = self.imageManager.getCurrentSettings()
            # Aggiorna solo la modalità di bilanciamento del bianco
            if hasattr(currentSettings, 'Exposure'):
                currentSettings.Exposure.Priority = value

                self.imageManager.imagingClient.SetImagingSettings({
                    'VideoSourceToken': self.imageManager.videoToken,
                    'ImagingSettings': currentSettings
                })
                # Ricarica le impostazioni per verificare che l'aggiornamento sia andato a buon fine
                self.checkOperationResult("Priority", value)
            else:
                self.imageManager.emit("error", "Shutter settings not available")
        except Exception as e:
            msg = f"Error setting shutter mode to {value}: {e}"
            self.imageManager.emit("error", msg)

    def setMode(self, value):
        try:
            # Assicurati di avere le impostazioni di imaging correnti
            currentSettings = self.imageManager.getCurrentSettings()
            # Aggiorna solo la modalità di bilanciamento del bianco
            if hasattr(currentSettings, 'Exposure'):
                currentSettings.Exposure.Mode = value

                self.imageManager.imagingClient.SetImagingSettings({
                    'VideoSourceToken': self.imageManager.videoToken,
                    'ImagingSettings': currentSettings
                })
                # Ricarica le impostazioni per verificare che l'aggiornamento sia andato a buon fine
                self.checkOperationResult("Mode", value)
            else:
                self.emitError("setMode: Shutter settings not available")
        except Exception as e:
            msg = f"Error setting shutter value to {value}: {e}"
            self.emitError(msg)

    def checkOperationResult(self, opType, value):
        settings = self.getSettings()
        if settings[opType] == value:
            msg = f"Shutter {opType} set to {value}"
            self.imageManager.emit("serverMessage", msg)
        else:
            msg = f"Error setting shutter {opType} to {value}, current {opType} is {settings[opType]}"
            self.emitError(msg)

    def emitError(self, errorMsg):
        self.imageManager.emit("error", errorMsg)

