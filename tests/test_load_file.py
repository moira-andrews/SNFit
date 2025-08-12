from SNFit.load_file import file_formatting
from pathlib import Path

def test_file_formatting():
    '''
    Test file_formatting() to make sure files are ingested correctly.
    Should return a dictionary including the new filepath
    '''
    test_dir = (Path(__file__).parent / "test_files").resolve()
    file_dict = file_formatting(str(test_dir))
    assert isinstance(file_dict, dict)
    assert len(file_dict) > 0
    for path in file_dict.values():
        assert Path(path).exists()

