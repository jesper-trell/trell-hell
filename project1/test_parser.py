import data_functions


def test_package_parser():
    assert data_functions.package_parser("NAkAALoLAAA=") == (23.56, 30.02,)