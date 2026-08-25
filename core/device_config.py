from copy import deepcopy
from urllib.parse import urlparse


SUPPORTED_LLM_PROVIDERS = {"openai", "anthropic"}


class DeviceConfig:
    DEFAULT = {
        "wifi": {
            "ssid": "",
            "password": "",
        },
        "ap": {
            "enabled": True,
            "ssid": "edge-setup",
            "password": "edge-setup",
            "setup_url": "http://192.168.4.1/setup",
        },
        "backend": {
            "endpoint": "http://localhost:8000",
        },
        "llm": {
            "provider": "openai",
            "base_url": "https://api.openai.com/v1",
            "credentials_ref": "",
        },
    }

    def __init__(self, data=None):
        self._data = deepcopy(self.DEFAULT)
        if data:
            self._merge(self._data, data)
        self.validate(self._data)

    @property
    def data(self):
        return deepcopy(self._data)

    def update(self, patch):
        candidate = self.data
        self._merge(candidate, patch or {})
        self.validate(candidate)
        self._data = candidate
        return self.data

    def public_data(self):
        cfg = self.data
        cfg["wifi"]["password"] = ""
        cfg["wifi"]["password_set"] = bool(self._data.get("wifi", {}).get("password"))
        cfg["llm"]["credentials_ref"] = ""
        cfg["llm"]["credentials_ref_set"] = bool(self._data.get("llm", {}).get("credentials_ref"))
        return cfg

    def validate(self, payload):
        wifi = payload.get("wifi", {})
        ap = payload.get("ap", {})
        backend = payload.get("backend", {})
        llm = payload.get("llm", {})

        if not isinstance(wifi.get("ssid", ""), str):
            raise ValueError("wifi.ssid must be a string")
        if not isinstance(wifi.get("password", ""), str):
            raise ValueError("wifi.password must be a string")
        if not isinstance(ap.get("enabled", True), bool):
            raise ValueError("ap.enabled must be a boolean")

        for field_name in ("setup_url",):
            self._validate_url(ap.get(field_name, ""), f"ap.{field_name}")
        self._validate_url(backend.get("endpoint", ""), "backend.endpoint")

        provider = llm.get("provider")
        if provider not in SUPPORTED_LLM_PROVIDERS:
            raise ValueError("llm.provider must be one of: openai, anthropic")

        base_url = llm.get("base_url", "")
        self._validate_url(base_url, "llm.base_url")

        parsed = urlparse(base_url)
        path = parsed.path or ""
        if provider == "openai" and "/v1" not in path:
            raise ValueError("OpenAI-compatible llm.base_url should include /v1")
        if provider == "anthropic" and "anthropic" not in parsed.netloc:
            raise ValueError("Anthropic-compatible llm.base_url should target an anthropic host")

        if not isinstance(llm.get("credentials_ref", ""), str):
            raise ValueError("llm.credentials_ref must be a string")

    def _merge(self, dest, patch):
        for key, value in patch.items():
            if isinstance(value, dict) and isinstance(dest.get(key), dict):
                self._merge(dest[key], value)
            else:
                dest[key] = value

    @staticmethod
    def _validate_url(value, field_name):
        if not isinstance(value, str):
            raise ValueError(f"{field_name} must be a string")
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError(f"{field_name} must be a valid http/https URL")
