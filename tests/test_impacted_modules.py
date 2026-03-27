from scripts.impacted_modules import closure_with_dependents


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
