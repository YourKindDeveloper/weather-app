import requests
from cache import get_from_cache, save_to_cache

def get_weather(city: str) -> dict:
    """
    Recupera le condizioni meteo attuali per una città.

    Args:
        city (str): Nome della città da cercare.

    Returns:
        dict: Dizionario con city, temperature, wind_speed,
              weather_code e source ("api" o "cache").
              In caso di errore: {"error": str}.

    Example:
        >>> get_weather("Napoli")
        {"city": "Naples, Italy", "temperature": "18.5°C",
         "wind_speed": "12.3 km/h", "weather_code": 1, "source": "api"}

        >>> get_weather("")
        {"error": "Il nome della città non può essere vuoto."}
    """
    if not city or not city.strip():
        return {"error": "Il nome della città non può essere vuoto."}

    city = city.strip()
    cache_key = f"weather_{city.lower()}"

    cached = get_from_cache(cache_key)
    if cached:
        return {**cached, "source": "cache"}

    try:
        geo_data = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": city, "count": 1, "format": "json"},
            timeout=10
        ).json()

        if "results" not in geo_data or not geo_data["results"]:
            return {"error": f"Città '{city}' non trovata."}

        r = geo_data["results"][0]
        lat, lon = r["latitude"], r["longitude"]
        city_label = f"{r['name']}, {r.get('country', '')}"

        weather_data = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": lat,
                "longitude": lon,
                "current": "temperature_2m,weather_code,wind_speed_10m",
                "timezone": "auto"
            },
            timeout=10
        ).json()

        current = weather_data.get("current", {})
        output = {
            "city": city_label,
            "temperature": f"{current.get('temperature_2m')}°C",
            "wind_speed": f"{current.get('wind_speed_10m')} km/h",
            "weather_code": current.get("weather_code"),
            "source": "api"
        }

        save_to_cache(cache_key, output)
        return output

    except requests.exceptions.Timeout:
        return {"error": "Richiesta scaduta. Riprova più tardi."}
    except requests.exceptions.ConnectionError:
        return {"error": "Nessuna connessione a internet."}
    except requests.exceptions.RequestException as e:
        return {"error": f"Errore di rete: {str(e)}"}


if __name__ == "__main__":
    city = input("Inserisci il nome della città: ")
    result = get_weather(city)
    print(result)
