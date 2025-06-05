from name_matching.main import main

def test_main_output(capsys):
    main()
    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello from name-matching!"
