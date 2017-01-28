import pytest
from collections import namedtuple

import tempfile
from path import Path

from importData import managedb
from importData import treat


Photo = namedtuple("Photo", ["timestamp", "path"])
Csv = namedtuple("Csv", ["timestamp", "data"])

@pytest.fixture()
def campaign():
    return managedb.make_campaign('test3', 1, 'descr').id

def test_treat(campaign, capsys):
    with tempfile.NamedTemporaryFile(suffix='.jpg') as path1:
        with tempfile.NamedTemporaryFile(suffix='.jpg') as path2:
            path1 = Path(path1.name)
            path2 = Path(path2.name)
            l = {
                'csv': Csv(0, {'gps': {'lat': 0, 'lon': 0, 'alt': 0},
                               'compass': {'degree': 0, 'minutes': 0},
                               'takenDate': 0,
                               'goproFailed': 0}),
                0: Photo(0, path1),
                1: Photo(0, path1),
                2: Photo(0, path1),
                3: Photo(0, path1),
                4: Photo(0, path2),
                5: Photo(0, path2)}

            lot = treat.treat(campaign, l)
            out, _ = capsys.readouterr()
            assert out == "Lot n°{} generated\n".format(lot.id)

            del l[0]

            lot = treat.treat(campaign, l)
            out, _ = capsys.readouterr()
            assert out == "Malformed lot n°{0}\nLot n°{0} generated\n".format(lot.id)
