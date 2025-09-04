def test_truth():
    assert True


def test_shared_python_import():
    # Sanity check: ensure shared python utils importable
    from shared.utils.python import helpers  # noqa: F401
    assert True
