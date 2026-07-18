#!/usr/bin/env python3
# Copyright    2026  Xiaomi Corp.        (authors:  Han Zhu)
#
# See ../../LICENSE for clarification regarding multiple authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Configuration helper utilities for OmniVoice."""

import json
import os
from pathlib import Path

DEFAULT_MODEL = "k2-fsa/OmniVoice"


def get_default_model() -> str:
    """Resolve the default model ID or local path dynamically.

    Checks sources in the following priority order:
    1. Environment variable `OMNIVOICE_DEFAULT_MODEL` or `OMNIVOICE_MODEL`.
    2. Environment variable `OMNIVOICE_CONFIG` pointing to a config JSON file.
    3. Local `config.json` in the current working directory.
    4. Project root `config.json` (resolving up from this file's location).
    5. Global user config in `~/.config/omnivoice/config.json`.
    6. Fallback default model ("k2-fsa/OmniVoice").
    """
    # 1. Environment variables
    env_model = os.environ.get("OMNIVOICE_DEFAULT_MODEL") or os.environ.get("OMNIVOICE_MODEL")
    if env_model:
        return env_model

    # 2. Environment variable for config file path
    env_config = os.environ.get("OMNIVOICE_CONFIG")
    if env_config and os.path.exists(env_config):
        try:
            with open(env_config, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "default_model" in data:
                    return data["default_model"]
        except Exception:
            pass

    # 3. Local working directory config
    local_config = Path("config.json")
    if local_config.exists():
        try:
            with open(local_config, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "default_model" in data:
                    return data["default_model"]
        except Exception:
            pass

    # 4. Project root config (traverse up parents from this file's directory)
    try:
        current_dir = Path(__file__).resolve().parent
        for parent in [current_dir] + list(current_dir.parents):
            # Check for standard project indicators alongside config.json
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                proj_config = parent / "config.json"
                if proj_config.exists():
                    with open(proj_config, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict) and "default_model" in data:
                            return data["default_model"]
                break  # Don't go beyond project root
    except Exception:
        pass

    # 5. User home config
    home_config = Path.home() / ".config" / "omnivoice" / "config.json"
    if home_config.exists():
        try:
            with open(home_config, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "default_model" in data:
                    return data["default_model"]
        except Exception:
            pass

    return DEFAULT_MODEL


DEFAULT_AVAILABLE_MODELS = [
    {
        "id": "k2-fsa/OmniVoice",
        "name": "OmniVoice (Default)",
        "description": "Massively multilingual zero-shot TTS model supporting over 600 languages."
    }
]


def get_available_models() -> list:
    """Resolve the list of available models from configuration sources.

    Checks sources in the following priority order:
    1. Environment variable `OMNIVOICE_CONFIG` pointing to a config JSON file.
    2. Local `config.json` in the current working directory.
    3. Project root `config.json` (resolving up from this file's location).
    4. Global user config in `~/.config/omnivoice/config.json`.
    5. Fallback default available models.
    """
    # 1. Environment variable for config file path
    env_config = os.environ.get("OMNIVOICE_CONFIG")
    if env_config and os.path.exists(env_config):
        try:
            with open(env_config, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "available_models" in data:
                    return data["available_models"]
        except Exception:
            pass

    # 2. Local working directory config
    local_config = Path("config.json")
    if local_config.exists():
        try:
            with open(local_config, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "available_models" in data:
                    return data["available_models"]
        except Exception:
            pass

    # 3. Project root config (traverse up parents from this file's directory)
    try:
        current_dir = Path(__file__).resolve().parent
        for parent in [current_dir] + list(current_dir.parents):
            if (parent / "pyproject.toml").exists() or (parent / ".git").exists():
                proj_config = parent / "config.json"
                if proj_config.exists():
                    with open(proj_config, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        if isinstance(data, dict) and "available_models" in data:
                            return data["available_models"]
                break
    except Exception:
        pass

    # 4. User home config
    home_config = Path.home() / ".config" / "omnivoice" / "config.json"
    if home_config.exists():
        try:
            with open(home_config, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "available_models" in data:
                    return data["available_models"]
        except Exception:
            pass

    return DEFAULT_AVAILABLE_MODELS

