from PyQt6.QtCore import *

from zeep import helpers

import logging

"""logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('zeep.transports')
logger.setLevel(logging.DEBUG)"""


class ColorSettings(QObject):

    def __init__(self, imageManager, parent=None):
        super().__init__(parent)
        self.imageManager = imageManager

    def getSettings(self):
        settings = {}
        currentSettings = self.imageManager.imagingClient.GetImagingSettings(
            {'VideoSourceToken': self.imageManager.videoToken})
        settings_dict = helpers.serialize_object(currentSettings)
        # print(settings_dict)

        for attr in dir(currentSettings):
            if not attr.startswith('_'):
                value = getattr(currentSettings, attr)
                settings[attr] = value
        return settings

    def getAllOptions(self):
        colorDictionary = {}
        options = self.imageManager.imagingClient.GetOptions({'VideoSourceToken': self.imageManager.videoToken})
        if hasattr(options, 'Brightness'):
            colorDictionary['Brightness'] = options.Brightness
        if hasattr(options, 'Contrast'):
            colorDictionary['Contrast'] = options.Contrast
        if hasattr(options, 'ColorSaturation'):
            colorDictionary['ColorSaturation'] = options.ColorSaturation
        if hasattr(options, 'Sharpness'):
            colorDictionary['Sharpness'] = options.Sharpness
        if hasattr(options, 'BacklightCompensation'):
            colorDictionary['BacklightCompensation'] = options.BacklightCompensation
        if hasattr(options, 'IrCutFilterModes'):
            colorDictionary['IrCutFilterModes'] = options.IrCutFilterModes
        if hasattr(options, 'WideDynamicRange'):
            colorDictionary['WideDynamicRange'] = options.WideDynamicRange
        return colorDictionary

    @property
    def brightness(self):
        currentSettings = self.imageManager.currentSettings
        if hasattr(currentSettings, "Brightness"):
            return currentSettings.Brightness
        else:
            return 999

    @brightness.setter
    def brightness(self, value):
        if not self.brightnessRange:
            msg = "Cannot set iris, irisRange is None"
            self.imageManager.emit("error", msg)
            return
        try:
            self.imageManager.imagingClient.SetImagingSettings(
                {"VideoSourceToken": self.imageManager.videoToken,
                 "ImagingSettings": {"Brightness": value}})
            self.checkOperationResult("Brightness", value)
        except Exception as e:
            msg = f"Error setting brightness to {value}: {e}"
            self.imageManager.emit("error", msg)

    @property
    def brightnessRange(self) -> tuple:
        dictionary = self.getAllOptions()
        if 'Brightness' in dictionary:
            return dictionary['Brightness']['Min'], dictionary['Brightness']['Max']
        else:
            return None, None

    @property
    def contrast(self):
        currentSettings = self.imageManager.currentSettings
        if hasattr(currentSettings, "Contrast"):
            return currentSettings.Contrast
        else:
            return 999

    @contrast.setter
    def contrast(self, value):
        if not self.contrastRange:
            msg = "Cannot set iris, irisRange is None"
            self.imageManager.emit("error", msg)
            return
        try:
            self.imageManager.imagingClient.SetImagingSettings(
                {"VideoSourceToken": self.imageManager.videoToken,
                 "ImagingSettings": {"Contrast": value}})
            self.checkOperationResult("Contrast", value)
        except Exception as e:
            msg = f"Error setting contrast to {value}: {e}"
            self.imageManager.emit("error", msg)

    @property
    def contrastRange(self) -> tuple:
        dictionary = self.getAllOptions()
        if 'Contrast' in dictionary:
            return dictionary['Contrast']['Min'], dictionary['Contrast']['Max']
        else:
            return 999, 999

    @property
    def saturation(self):
        currentSettings = self.imageManager.currentSettings
        if hasattr(currentSettings, "ColorSaturation"):
            return currentSettings.ColorSaturation
        else:
            return 999

    @saturation.setter
    def saturation(self, value):
        if not self.saturationRange:
            msg = "Cannot set iris, irisRange is None"
            self.imageManager.emit("error", msg)
            return
        try:
            self.imageManager.imagingClient.SetImagingSettings(
                {"VideoSourceToken": self.imageManager.videoToken,
                 "ImagingSettings": {"ColorSaturation": value}})
            self.checkOperationResult("ColorSaturation", value)
        except Exception as e:
            msg = f"Error setting saturation to {value}: {e}"
            self.imageManager.emit("error", msg)

    @property
    def saturationRange(self) -> tuple:
        dictionary = self.getAllOptions()
        if 'ColorSaturation' in dictionary:
            return dictionary['ColorSaturation']['Min'], dictionary['ColorSaturation']['Max']
        else:
            return None, None

    @property
    def detail(self):
        currentSettings = self.imageManager.currentSettings
        if hasattr(currentSettings, "Sharpness"):
            return currentSettings.Sharpness
        else:
            return 999

    @detail.setter
    def detail(self, value):
        if not self.detailRange:
            msg = "Cannot set iris, irisRange is None"
            self.imageManager.emit("error", msg)
            return
        try:
            self.imageManager.imagingClient.SetImagingSettings(
                {"VideoSourceToken": self.imageManager.videoToken,
                 "ImagingSettings": {"Sharpness": value}})
            self.checkOperationResult("Sharpness", value)
        except Exception as e:
            msg = f"Error setting detail to {value}: {e}"
            self.imageManager.emit("error", msg)

    @property
    def detailRange(self) -> tuple:
        dictionary = self.getAllOptions()
        if 'Sharpness' in dictionary:
            return dictionary['Sharpness']['Min'], dictionary['Sharpness']['Max']
        else:
            return None, None

    @property
    def backlightCompensation(self):
        currentSettings = self.imageManager.currentSettings
        if hasattr(currentSettings, "BacklightCompensation"):
            return currentSettings.BacklightCompensation
        else:
            return 999

    @backlightCompensation.setter
    def backlightCompensation(self, value):
        if not self.isBacklightCompensation:
            self.emitError("Cannot set backlight compensation, backlight compensation is OFF")
            return
        try:
            # Assumi che il modo sia ON o OFF. Verifica la documentazione della tua telecamera per i valori corretti.
            mode = "ON" if self.isBacklightCompensation  else "OFF"

            self.imageManager.imagingClient.SetImagingSettings({
                "VideoSourceToken": self.imageManager.videoToken,
                "ImagingSettings": {
                    "BacklightCompensation": {
                        "Level": value,
                        "Mode": mode
                    }
                }
            })

            # Verifica se l'impostazione è stata cambiata con successo
            if self.backlightCompensationLevel == value:
                msg = f"Backlight compensation level set to {value}"
                self.imageManager.emit("serverMessage", msg)
            else:
                msg = f"Error setting backlight compensation level to {value}, current level is {self.backlightCompensationLevel}"
                self.imageManager.emit("error", msg)
        except Exception as e:
            # Gestisci l'eccezione qui
            self.imageManager.emit("error", f"Error setting backlight compensation level: {e}")

    @property
    def isBacklightCompensation(self):
        currentSettings = self.imageManager.currentSettings
        if hasattr(currentSettings, "BacklightCompensation"):
            if currentSettings.BacklightCompensation.Mode == "OFF":
                return False
            return True
        else:
            return False

    @isBacklightCompensation.setter
    def isBacklightCompensation(self, value):
        try:
            # Assumi che il modo sia ON o OFF. Verifica la documentazione della tua telecamera per i valori corretti.
            mode = "ON" if self.isBacklightCompensation else "OFF"

            self.imageManager.imagingClient.SetImagingSettings({
                "VideoSourceToken": self.imageManager.videoToken,
                "ImagingSettings": {
                    "BacklightCompensation": {
                        "Level": value,
                        "Mode": mode
                    }
                }
            })

            # Verifica se l'impostazione è stata cambiata con successo
            if self.backlightCompensationLevel == value:
                msg = f"Backlight compensation level set to {value}"
                self.imageManager.emit("serverMessage", msg)
        except Exception as e:
            # Gestisci l'eccezione qui
            self.imageManager.emit("error", f"Error setting backlight compensation level: {e}")


    @property
    def backlightCompensationLevel(self):
        currentSettings = self.imageManager.currentSettings
        if hasattr(currentSettings, "BacklightCompensation"):
            return currentSettings.BacklightCompensation.Level
        else:
            return 999


    @property
    def backlightCompensationRange(self) -> tuple:
        dictionary = self.getAllOptions()
        if 'BacklightCompensation' in dictionary:
            return dictionary['BacklightCompensation']['Level']['Min'], dictionary['BacklightCompensation']['Level']['Max']
        else:
            return None, None

    @property
    def irCutFilter(self):
        currentSettings = self.imageManager.currentSettings
        if hasattr(currentSettings, "IrCutFilter"):
            return currentSettings.IrCutFilter
        else:
            return 999

    @property
    def wideDynamicRange(self):
        currentSettings = self.imageManager.currentSettings
        if hasattr(currentSettings, "WideDynamicRange"):
            return currentSettings.WideDynamicRange
        else:
            return 999

    def checkOperationResult(self, opType, value):
        settings = self.getSettings()
        if settings[opType] == value:
            msg = f"color {opType} set to {value}"
            self.imageManager.emit("serverMessage", msg)
        else:
            msg = f"Error setting color {opType} to {value}, current {opType} is {settings[opType]}"
            self.emitError(msg)

    def emitError(self, errorMsg):
        self.imageManager.emit("error", errorMsg)
