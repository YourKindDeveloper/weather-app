import time

_weather_cache = {}
CACHE_DURATION_SECONDS = 3600  # 1 ora

def get_from_cache(city_key: str) -> dict | None:
    record = _weather_cache.get(city_key)
    if record is None:
        return None
    if time.time() - record["timestamp"] < CACHE_DURATION_SECONDS:
        return record["data"]
    return None

def save_to_cache(city_key: str, data: dict) -> None:
    _weather_cache[city_key] = {
        "data": data,
        "timestamp": time.time()
    }
