from onvifWrap.onvifManager import OnvifCamManager

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