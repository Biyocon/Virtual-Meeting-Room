"""AgentProfile loader and MeetingAgentInstance lifecycle tests."""

from pathlib import Path

import pytest
import yaml

from agent_sidecar.contracts import AgentProfile
from agent_sidecar.runtime.instance import (
    InstanceNotFound,
    close_instance,
    create_instance,
    get_instance,
    list_instances_for_meeting,
    reset_instances,
    update_instance_status,
)
from agent_sidecar.runtime.profile_loader import load_profiles, reset_profile_cache
from agent_sidecar.runtime.state import now_iso


@pytest.fixture(autouse=True)
def reset_state():
    reset_profile_cache()
    reset_instances()
    yield
    reset_profile_cache()
    reset_instances()


class TestProfileLoader:
    """YAML profile loading and validation."""

    def test_loads_builtin_profiles(self):
        profiles = load_profiles()
        assert "pm" in profiles
        assert "analyst" in profiles
        assert "facilitator" in profiles

        pm = profiles["pm"]
        assert pm.name == "Projektleder Maria"
        assert pm.role == "Projektleder"
        assert pm.model == "gpt-4o-mini"
        assert "facilitation" in pm.skills

    def test_invalid_profile_raises_clear_error(self, tmp_path: Path):
        bad_dir = tmp_path / "bad_profiles"
        bad_dir.mkdir()
        (bad_dir / "bad.yaml").write_text(
            yaml.safe_dump({"name": "Missing ID", "role": "test"})
        )

        with pytest.raises(ValueError) as exc_info:
            load_profiles(bad_dir)
        assert "Missing ID" in str(exc_info.value) or "id" in str(exc_info.value)

    def test_duplicate_profile_id_raises(self, tmp_path: Path):
        dup_dir = tmp_path / "dup_profiles"
        dup_dir.mkdir()
        (dup_dir / "a.yaml").write_text(yaml.safe_dump({"id": "pm", "name": "A", "role": "r"}))
        (dup_dir / "b.yaml").write_text(yaml.safe_dump({"id": "pm", "name": "B", "role": "r"}))

        with pytest.raises(ValueError) as exc_info:
            load_profiles(dup_dir)
        assert "duplicate profile id" in str(exc_info.value)

    def test_empty_profile_directory_raises(self, tmp_path: Path):
        empty_dir = tmp_path / "empty"
        empty_dir.mkdir()
        with pytest.raises(ValueError) as exc_info:
            load_profiles(empty_dir)
        assert "no *.yaml profiles found" in str(exc_info.value)


class TestMeetingAgentInstance:
    """MeetingAgentInstance lifecycle."""

    def test_create_and_get_instance(self):
        profile = AgentProfile(id="pm", name="PM", role="Projektleder")
        instance = create_instance(
            tenant_id="t1",
            meeting_id="m1",
            agent_instance_id="agent-1",
            profile=profile,
            role="chair",
        )
        assert instance.agentInstanceId == "agent-1"
        assert instance.meetingId == "m1"
        assert instance.tenantId == "t1"
        assert instance.agentProfileId == "pm"
        assert instance.status == "idle"

        found = get_instance("t1", "m1", "agent-1")
        assert found.agentInstanceId == "agent-1"

    def test_get_unknown_instance_raises(self):
        with pytest.raises(InstanceNotFound):
            get_instance("t1", "m1", "agent-404")

    def test_update_status(self):
        profile = AgentProfile(id="pm", name="PM", role="Projektleder")
        create_instance("t1", "m1", "agent-1", profile, "chair")

        updated = update_instance_status("t1", "m1", "agent-1", "thinking")
        assert updated.status == "thinking"

        found = get_instance("t1", "m1", "agent-1")
        assert found.status == "thinking"

    def test_close_instance(self):
        profile = AgentProfile(id="pm", name="PM", role="Projektleder")
        create_instance("t1", "m1", "agent-1", profile, "chair")

        removed = close_instance("t1", "m1", "agent-1")
        assert removed is not None

        with pytest.raises(InstanceNotFound):
            get_instance("t1", "m1", "agent-1")

    def test_list_instances_for_meeting(self):
        profile = AgentProfile(id="pm", name="PM", role="Projektleder")
        create_instance("t1", "m1", "agent-1", profile, "chair")
        create_instance("t1", "m1", "agent-2", profile, "observer")
        create_instance("t1", "m2", "agent-3", profile, "chair")

        m1_instances = list_instances_for_meeting("t1", "m1")
        assert len(m1_instances) == 2
        assert {i.agentInstanceId for i in m1_instances} == {"agent-1", "agent-2"}

    def test_instances_isolated_by_tenant(self):
        profile = AgentProfile(id="pm", name="PM", role="Projektleder")
        create_instance("t1", "m1", "agent-1", profile, "chair")

        # Same meetingId, different tenant is a separate instance.
        create_instance("t2", "m1", "agent-1", profile, "chair")

        assert get_instance("t1", "m1", "agent-1").tenantId == "t1"
        assert get_instance("t2", "m1", "agent-1").tenantId == "t2"
