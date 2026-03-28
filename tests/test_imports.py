def test_import_main():
    from tactical_manager.main import main
    assert callable(main)