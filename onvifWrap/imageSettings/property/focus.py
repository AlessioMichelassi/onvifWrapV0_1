from PyQt6.QtCore import *


class FocusSettings(QObject):

    def __init__(self, imageManager, parent=None):
        super().__init__(parent)
        self.imageManager = imageManager

    def getSettings(self):
        currentSettings = self.imageManager.getCurrentSettings()
        focusDict = {}
        if hasattr(currentSettings, 'Focus'):
            for attr in dir(currentSettings.Focus):
                if not attr.startswith('_') and hasattr(currentSettings.Focus, attr):
                    value = getattr(currentSettings.Focus, attr)
                    focusDict[attr] = value
            return focusDict
        else:
            self.imageManager.emit("error", "Focus settings not available")

    def getAllOptions(self):
        """
                Recupera tutte le opzioni di focus disponibili.
                :return:
                """
        try:
            options = self.imageManager.imagingClient.GetOptions({'VideoSourceToken': self.imageManager.videoToken})
            if hasattr(options, 'Focus'):
                focusDict = {}
                for attr in dir(options.Focus):
                    if not attr.startswith('_') and hasattr(options.Focus, attr):
                        value = getattr(options.Focus, attr)
                        focusDict[attr] = value
                return focusDict
            else:
                msg = "No focus options available"
                self.emitError(msg)
                return {}
        except Exception as e:
            msg = f"Error retrieving focus options: {e}"
            self.imageManager.emit("error", msg)
            return {}

    @property
    def isAuto(self):
        dictionary = self.getSettings()
        if not dictionary:
            self.emitError("isAuto: Error retrieving Dictionary of focus settings")
            return None
        if 'AutoFocusMode' in dictionary:
            if dictionary['AutoFocusMode'] == 'AUTO':
                return True
            else:
                return False
        else:
            errorMsg = f"Error retrieving focus value {dictionary}"
            self.imageManager.emit("error", errorMsg)
            return None

    @isAuto.setter
    def isAuto(self, value):
        if value:
            self.setMode("AUTO")
        else:
            self.setMode("MANUAL")

    @property
    def defaultSpeed(self):
        dictionary = self.getSettings()
        if not dictionary:
            self.emitError("defaultSpeed: Error retrieving Dictionary of focus settings")
            return None
        if 'DefaultSpeed' in dictionary:
            return dictionary['DefaultSpeed']
        else:
            self.emitError("Error retrieving default speed")

    @defaultSpeed.setter
    def defaultSpeed(self, value: float):
        """
            Imposta il valore di default speed.
            :param value:
            :return:
        """
        speedRange = self.speedRange
        if not speedRange:
            self.emitError("defaultSpeed: Error retrieving speed range")
            return
        if not self.isAuto:
            return
        min_speed = speedRange[0]
        max_speed = speedRange[1]
        if value < min_speed or value > max_speed:
            self.emitError(f"Error setting default speed to {value}, value must be between {min_speed} and {max_speed}")
        else:
            try:
                currentSettings = self.imageManager.getCurrentSettings()
                opType = "DefaultSpeed"
                if hasattr(currentSettings, 'Focus'):
                    currentSettings.Focus.DefaultSpeed = value
                    self.imageManager.imagingClient.SetImagingSettings({
                        'VideoSourceToken': self.imageManager.videoToken,
                        'ImagingSettings': currentSettings
                    })
                    self.checkOperationResult(opType, value)
                else:
                    self.imageManager.emit("error", "Focus settings not available")
            except Exception as e:
                msg = f"Error setting default speed to {value}: {e}"
                self.imageManager.emit("error", msg)

    @property
    def speedRange(self):
        dictionary = self.getAllOptions()
        if not dictionary:
            self.emitError("speedRange: Error retrieving Dictionary of focus settings")
            return None
        if 'DefaultSpeed' in dictionary:
            return dictionary['DefaultSpeed']['Min'], dictionary['DefaultSpeed']['Max']
        else:
            self.emitError("Error retrieving default speed range")
            return None

    @property
    def focusNearRange(self):
        dictionary = self.getAllOptions()
        if not dictionary:
            self.emitError("focusNearRange: Error retrieving Dictionary of focus settings")
            return None
        if 'NearLimit' in dictionary:
            return dictionary['NearLimit']['Min'], dictionary['NearLimit']['Max']
        else:
            self.emitError("Error retrieving focus near range")
            return None

    @property
    def focusFarRange(self):
        dictionary = self.getAllOptions()
        if not dictionary:
            self.emitError("focusFarRange: Error retrieving Dictionary of focus settings")
            return None
        if 'FarLimit' in dictionary:
            return dictionary['FarLimit']['Min'], dictionary['FarLimit']['Max']
        else:
            self.emitError("Error retrieving focus far range")
            return None

    @property
    def focusNearLimit(self):
        dictionary = self.getSettings()
        if not dictionary:
            self.emitError("focusNearLimit: Error retrieving Dictionary of focus settings")
            return None
        if 'NearLimit' in dictionary:
            return dictionary['NearLimit']
        else:
            self.emitError("Error retrieving focus near limit")
            return None

    @focusNearLimit.setter
    def focusNearLimit(self, value: float):
        """
            Imposta il valore di focus near limit.
            :param value:
            :return:
        """
        focusRange = self.focusNearRange
        if not focusRange:
            self.emitError("focusNearLimit: Error retrieving focus near range")
            return
        if not self.isAuto:
            return
        min_focus = focusRange[0]
        max_focus = focusRange[1]
        if value < min_focus or value > max_focus:
            self.emitError(f"Error setting focus near limit to {value}, value must be between {min_focus} and {max_focus}")
        else:
            try:
                currentSettings = self.imageManager.getCurrentSettings()
                opType = "NearLimit"
                if hasattr(currentSettings, 'Focus'):
                    currentSettings.Focus.NearLimit = value
                    self.imageManager.imagingClient.SetImagingSettings({
                        'VideoSourceToken': self.imageManager.videoToken,
                        'ImagingSettings': currentSettings
                    })
                    self.checkOperationResult(opType, value)
                else:
                    self.imageManager.emit("error", "Focus settings not available")
            except Exception as e:
                msg = f"Error setting focus near limit to {value}: {e}"
                self.imageManager.emit("error", msg)

    @property
    def focusFarLimit(self):
        dictionary = self.getSettings()
        if not dictionary:
            self.emitError("focusFarLimit: Error retrieving Dictionary of focus settings")
            return None
        if 'FarLimit' in dictionary:
            return dictionary['FarLimit']
        else:
            self.emitError("Error retrieving focus far limit")
            return None

    @focusFarLimit.setter
    def focusFarLimit(self, value: float):
        """
            Imposta il valore di focus far limit.
            :param value:
            :return:
        """
        focusRange = self.focusFarRange
        if not focusRange:
            self.emitError("focusFarLimit: Error retrieving focus far range")
            return
        if not self.isAuto:
            return
        min_focus = focusRange[0]
        max_focus = focusRange[1]
        if value < min_focus or value > max_focus:
            self.emitError(f"Error setting focus far limit to {value}, value must be between {min_focus} and {max_focus}")
        else:
            try:
                currentSettings = self.imageManager.getCurrentSettings()
                opType = "FarLimit"
                if hasattr(currentSettings, 'Focus'):
                    currentSettings.Focus.FarLimit = value
                    self.imageManager.imagingClient.SetImagingSettings({
                        'VideoSourceToken': self.imageManager.videoToken,
                        'ImagingSettings': currentSettings
                    })
                    self.checkOperationResult(opType, value)
                else:
                    self.imageManager.emit("error", "Focus settings not available")
            except Exception as e:
                msg = f"Error setting focus far limit to {value}: {e}"
                self.imageManager.emit("error", msg)

    @property
    def extensions(self):
        dictionary = self.getSettings()
        if not dictionary:
            self.emitError("extensions: Error retrieving focus settings")
            return None
        if 'Extension' in dictionary:
            return dictionary['Extension']
        else:
            self.emitError("Error retrieving focus extensions")

    def emitError(self, errorMsg):
        self.imageManager.emit("error", errorMsg)

    def setMode(self, value):
        """
        Imposta la modalità di focus.
        :param value:
        :return:
        """
        try:
            currentSettings = self.imageManager.getCurrentSettings()
            opType = "AutoFocusMode"
            if hasattr(currentSettings, 'Focus'):
                currentSettings.Focus.AutoFocusMode = value
                self.imageManager.imagingClient.SetImagingSettings({
                    'VideoSourceToken': self.imageManager.videoToken,
                    'ImagingSettings': currentSettings
                })
                self.checkOperationResult(opType, value)
            else:
                self.imageManager.emit("error", "Focus settings not available")
        except Exception as e:
            msg = f"Error setting focus value to {value}: {e}"
            self.imageManager.emit("error", msg)

    def checkOperationResult(self, opType, value):
        settings = self.getSettings()
        if settings[opType] == value:
            msg = f"Focus {opType} set to {value}"
            self.imageManager.emit("serverMessage", msg)
        else:
            msg = f"Error setting focus {opType} to {value}, current value is {settings[opType]}"
            self.imageManager.emit("error", msg)
