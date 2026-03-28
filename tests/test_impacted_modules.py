import pytest

from scripts.impacted_modules import (
    closure_with_dependents,
    detect_modules_from_paths,
    validate_graph,
)


def test_closure_with_dependents():
    reverse = {
        "lib-common": ["svc-a", "svc-b"],
        "svc-a": [],
        "svc-b": [],
    }
    impacted = closure_with_dependents({"lib-common"}, reverse)
    assert impacted == {"lib-common", "svc-a", "svc-b"}

    impacted2 = closure_with_dependents({"svc-a"}, reverse)
    assert impacted2 == {"svc-a"}


def test_detect_modules_from_paths_avoids_prefix_collision():
    modules = {
        "svc-a": {"path": "services/a"},
        "svc-ab": {"path": "services/ab"},
    }
    changed = ["services/ab/main.py"]
    assert detect_modules_from_paths(modules, changed) == {"svc-ab"}


def test_validate_graph_rejects_unknown_dependency():
    modules = {
        "svc-a": {"deps": ["missing-lib"]},
        "svc-b": {"deps": []},
    }
    with pytest.raises(ValueError, match="unknown dependency"):
        validate_graph(modules)
