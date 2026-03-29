# Weather App

App Python per consultare le condizioni meteo attuali di qualsiasi
città, usando l'API gratuita Open-Meteo.

## Funzionalità

- Ricerca meteo tramite nome della città
- Geocodifica automatica (nome città → coordinate)
- Caching in-memory dei risultati (validità: 60 minuti)
- Gestione degli errori per input non validi e problemi di rete

## Requisiti

- Python 3.10+
- Libreria `requests`

Installazione dipendenze:
pip install requests

## Come usare l'app

python weather_app.py

Esempio di chiamata nel codice:
from weather_app import get_weather
print(get_weather("Napoli"))

## Output di esempio

{
  "city": "Naples, Italy",
  "temperature": "18.5°C",
  "wind_speed": "12.3 km/h",
  "weather_code": 1,
  "source": "api"
}

## Gestione degli errori

- Città non trovata  → {"error": "Città 'X' non trovata."}
- Input vuoto        → {"error": "Il nome della città non può essere vuoto."}
- Timeout rete       → {"error": "Richiesta scaduta. Riprova più tardi."}
- Nessuna connessione → {"error": "Nessuna connessione a internet."}

## API utilizzate

- Geocoding: https://geocoding-api.open-meteo.com/v1/search
- Forecast:  https://api.open-meteo.com/v1/forecast
- Documentazione: https://open-meteo.com/en/docs

## Miglioramenti futuri

- Interfaccia grafica con icone meteo
- Previsione a 5 giorni
- Salvataggio delle ultime città cercate
