from PyQt6.QtCore import *


class WhiteBalanceSettings(QObject):
    """
        White balance settings

        Definisce le impostazioni di bilanciamento del bianco per una sorgente video.
        Al momento da HappyTime Onvif service è possibile ottenere questi parametri:
        - Mode: modalità di bilanciamento del bianco [Auto, Manual]
        - CrGain: guadagno rosso
        - CbGain: guadagno blu
        - Extension: estensione
    """
    rMin = 0
    rMax = 0
    bMin = 0
    bMax = 0
    rValueY = 0
    bValueY = 0
    rValueC = 0
    bValueC = 0

    def __init__(self, imageManager: 'ImageManager', parent=None):
        super().__init__(parent)
        self.imageManager = imageManager

    def getSettings(self) -> dict:
        white_balance_dict = {}
        currentSettings = self.imageManager.getCurrentSettings()
        settings = self.imageManager.imagingClient.GetImagingSettings({'VideoSourceToken': self.imageManager.videoToken})
        print(settings["WhiteBalance"])
        if hasattr(currentSettings, 'WhiteBalance'):
            white_balance = currentSettings.WhiteBalance
            for attr in dir(white_balance):
                if not attr.startswith('_'):
                    value = getattr(white_balance, attr)
                    white_balance_dict[attr] = value
        else:
            self.imageManager.emit("error", "White balance settings not available")
        return white_balance_dict

    def getMode(self):
        try:
            options = self.imageManager.imagingClient.GetOptions({'VideoSourceToken': self.imageManager.videoToken})
            if hasattr(options, 'WhiteBalance'):
                # Restituisce una lista delle modalità di bilanciamento del bianco supportate
                return options.WhiteBalance.Mode
            else:
                return ["No white balance modes available"]
        except Exception as e:
            self.imageManager.errorSignal.emit(f"Error retrieving white balance modes: {e}")
            return []

    def setMode(self, mode):
        try:
            # Assicurati di avere le impostazioni di imaging correnti
            currentSettings = self.imageManager.getCurrentSettings()
            opType = "Mode"
            # Aggiorna solo la modalità di bilanciamento del bianco
            if hasattr(currentSettings, 'WhiteBalance'):
                currentSettings.WhiteBalance.Mode = mode

                self.imageManager.imagingClient.SetImagingSettings({
                    'VideoSourceToken': self.imageManager.videoToken,
                    'ImagingSettings': currentSettings
                })
                # Ricarica le impostazioni per verificare che l'aggiornamento sia andato a buon fine
                self.checkOperationResult(mode, opType)
            else:
                self.imageManager.emit("error", "White balance settings not available")
        except Exception as e:
            msg = f"Error setting white balance value to {mode}: {e}"
            self.imageManager.emit("error", msg)

    def getRGain(self):
        currentSettings = self.imageManager.getCurrentSettings()
        if hasattr(currentSettings, 'WhiteBalance'):
            wb = currentSettings.WhiteBalance
            if hasattr(wb, 'CrGain'):
                print("CrGain")
                return currentSettings.WhiteBalance.CrGain
            elif hasattr(wb, 'YrGain'):
                print("YrGain")
                return currentSettings.WhiteBalance.YrGain
        else:
            return None

    def setRGain(self, value):
        try:
            # Assicurati di avere le impostazioni di imaging correnti
            currentSettings = self.imageManager.getCurrentSettings()
            opType = "CrGain"
            # Aggiorna solo la modalità di bilanciamento del bianco
            if hasattr(currentSettings, 'WhiteBalance'):
                currentSettings.WhiteBalance.CrGain = value
                self.imageManager.imagingClient.SetImagingSettings({
                    'VideoSourceToken': self.imageManager.videoToken,
                    'ImagingSettings': currentSettings
                })
                # Ricarica le impostazioni per verificare che l'aggiornamento sia andato a buon fine
                self.checkOperationResult(value, opType)
            else:
                self.imageManager.emit("error", "White balance settings not available")
        except Exception as e:
            msg = f"Error setting white balance value to {value}: {e}"
            self.imageManager.emit("error", msg)

    def listAllWhiteBalanceProperties(self, obj, parent_name=""):
        properties = {}

        for attr in dir(obj):
            if not attr.startswith('_'):
                attr_value = getattr(obj, attr)
                full_attr_name = f"{parent_name}.{attr}" if parent_name else attr

                if isinstance(attr_value, (str, int, float, list)):
                    # Se è un tipo base, aggiungilo direttamente
                    properties[full_attr_name] = attr_value
                elif hasattr(attr_value, '__dict__'):
                    # Se è un oggetto complesso, esploralo ricorsivamente
                    properties.update(self.listAllWhiteBalanceProperties(attr_value, full_attr_name))

                if "bGain" in attr:
                    if "Min" in attr:
                        self.bMin = attr_value
                    elif "Max" in attr:
                        self.bMax = attr_value
                elif "rGain" in attr:
                    if "Min" in attr:
                        self.rMin = attr_value
                    elif "Max" in attr:
                        self.rMax = attr_value

        return properties

    def getWhiteBalanceOptions(self):
        try:
            options = self.imageManager.imagingClient.GetOptions({'VideoSourceToken': self.imageManager.videoToken})
            if hasattr(options, 'WhiteBalance'):
                return self.listAllWhiteBalanceProperties(options.WhiteBalance)
            else:
                return {"Info": "No WhiteBalance options available"}
        except Exception as e:
            msg = f"Error retrieving white balance options: {e}"
            self.imageManager.emit("error", msg)
            return {}

    def checkOperationResult(self, opType, value):
        settings = self.getSettings()
        if settings[opType] == value:
            msg = f"WhiteBalance value set to {value}"
            self.imageManager.emit("serverMessage", msg)
        else:
            msg = f"Error setting focus WhiteBalance to {value}, current value is {settings[opType]}"
            self.imageManager.emit("error", msg)