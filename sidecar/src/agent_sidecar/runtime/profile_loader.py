"""AgentProfile loader from sidecar/profiles/*.yaml.

Static persona configuration is loaded once at startup. Invalid profiles fail
fast with a clear error message instead of a traceback.
"""

from pathlib import Path

import yaml

from agent_sidecar.contracts import AgentProfile


PROFILE_DIR = Path(__file__).parent.parent.parent.parent / "profiles"


def load_profiles(profile_dir: Path | str | None = None) -> dict[str, AgentProfile]:
    """Load all *.yaml profiles from disk and return a dict keyed by profile id.

    Raises:
        ValueError: if the directory is missing, empty, or contains invalid profiles.
    """
    directory = Path(profile_dir) if profile_dir is not None else PROFILE_DIR

    if not directory.exists():
        raise ValueError(f"profile directory does not exist: {directory}")

    files = sorted(directory.glob("*.yaml"))
    if not files:
        raise ValueError(f"no *.yaml profiles found in {directory}")

    profiles: dict[str, AgentProfile] = {}
    errors: list[str] = []

    for path in files:
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as exc:
            errors.append(f"{path.name}: invalid YAML ({exc})")
            continue
        except OSError as exc:
            errors.append(f"{path.name}: cannot read file ({exc})")
            continue

        if not isinstance(data, dict):
            errors.append(f"{path.name}: profile must be a mapping, got {type(data).__name__}")
            continue

        try:
            profile = AgentProfile(**data)
        except ValueError as exc:
            errors.append(f"{path.name}: {exc}")
            continue

        if profile.id in profiles:
            errors.append(
                f"{path.name}: duplicate profile id '{profile.id}' "
                f"(already defined in {profiles[profile.id].id})."
            )
            continue

        profiles[profile.id] = profile

    if errors:
        raise ValueError(
            "failed to load agent profiles:\n" + "\n".join(f"  - {err}" for err in errors)
        )

    return profiles


# Lazy singleton: loaded on first access so tests can override PROFILE_DIR.
_profile_cache: dict[str, AgentProfile] | None = None


def get_profiles(profile_dir: Path | str | None = None) -> dict[str, AgentProfile]:
    """Return cached profiles, loading them on first call."""
    global _profile_cache
    if _profile_cache is None or profile_dir is not None:
        _profile_cache = load_profiles(profile_dir)
    return _profile_cache


def reset_profile_cache() -> None:
    """Test-only: force reload on next access."""
    global _profile_cache
    _profile_cache = None
