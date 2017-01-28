import datetime

from importData import managedb

def test_fill_client():
    campaign = managedb.make_campaign("campaign_name", 1, "a description")
    sensors = managedb.make_sensors(0, 0, 0, 0, 0)
    lot = managedb.make_lot(campaign.id, 0, sensors.id, 0, datetime.datetime.now(), None)

    cp = managedb.make_cp("", 5, True, lot.id)
    pano = managedb.make_panorama(0, cp.id)
    managedb.make_tile(0, 0, '', 0, 0, 0, pano.id)
