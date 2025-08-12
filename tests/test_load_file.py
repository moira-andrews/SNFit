from SNFit.load_file import load_dir
import os
import glob

def test_directory_add():
    '''
    Test load_dir() to make sure files are ingested correctly if given as a directory input.
    Should return nothing if successful.
    '''
    test_dir = os.path.join(os.path.dirname(__file__), "test_files")
    files = glob.glob(os.path.join(test_dir, '*'))
    file_dict = load_dir(files)
    assert isinstance(file_dict, dict)
    assert len(file_dict) > 0
    for path in file_dict.values():
        assert os.path.exists(path)

if __name__ == "__main__":
    test_directory_add()
