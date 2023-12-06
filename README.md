OnvifCamManager Package

Il package OnvifCamManager è una libreria Python progettata per facilitare la gestione e la configurazione delle telecamere ONVIF. Utilizzando l'interfaccia PyQt6, questo package offre un modo semplice e interattivo per connettersi, controllare e gestire le impostazioni delle tue telecamere ONVIF.
Caratteristiche

Connessione Facile: 

Connessione semplice alle telecamere ONVIF usando indirizzo IP, porta, username e password.
    
Gestione delle Impostazioni di Immagine: 

Integrazione con ImageManager per una facile configurazione e gestione delle impostazioni di immagine della telecamera come:

    shutter
    white balance
    focus
    brightness
    contrast
    saturation
    sharpness
    backlight compensation
    wide dynamic range
    
Segnalazione Errori e Messaggi: Utilizzo di segnali PyQt6 per comunicare errori e messaggi di stato.

Installazione

(Le istruzioni per l'installazione verranno aggiunte qui, incluse le dipendenze necessarie e i passaggi per l'installazione.)

to install from this use:
```bash
pip install .
```

Uso

Ecco un esempio di base su come utilizzare OnvifCamManager per connettere una telecamera:

```python
from onvifWrap.onvifManager import OnvifCamManager

# Credenziali della telecamera
credentials = {
    "ip": "127.0.0.1",
    "port": 2000,
    "username": "admin",
    "password": "admin"
}

# Creazione dell'oggetto manager
camManager = OnvifCamManager()

# Connessione alla telecamera
if camManager.connectCamera(credentials):
    print("Connessione riuscita!")
else:
    print("Connessione fallita.")
```

Requisiti

    Python 3.x
    Libreria ONVIF
    PyQt6
