#!/usr/bin/python3
# coding: utf-8

"""Import the data into the treatment chain
Usage:
    opv-import [options] <campaign>

Arguments:
    campaign              The name of the campaign to import
Options:
    -h --help             Show this screen
    --csv-path=<str>      The path of CSV file for synchro
    --no-clean-sd         Clean SD after copying.
                          /!\\
                            This need sudo rights and you may loose
                            the content of the SD card if something fail !
                          /!\\
    --config-file=<str>   The path to the config file.[default: ./config/main.json]
    --clean-sd            Do NOT clean SD after copying.
    --no-treat            Don't treat files
    --treat               Treat files
    --export              Send files to the celery queue
    --no-export           Don't send files to the celery queue
    --import              Import files
    --no-import           Don't import files
    --data-dir=<str>      Where should be placed file imported from SD
    --lots-output-dir=<str>   Where created lots may be placed
    --id-rederbro=<str>   Id of the rederbro use fot the campaign
    --description=<str>   Description of the campaign
"""
from . import task
from . import managedb
from .treat import treat
from .importSD import Main
from .makeLots import makeLots
from .utils import Config, convert_args

from path import Path
from docopt import docopt


def main():
    """ Import Images from SD """
    # Read the __doc__ and build the Arguments
    args = docopt(__doc__)
    f_args = dict()

    # Convert args
    for n in ['clean-sd', 'import', 'treat', 'export']:
        f_args[n] = convert_args(args, n, True)
    for n in ['config-file', 'data-dir', 'lots-output-dir', 'id-rederbro', 'description', 'csv-path']:
        f_args[n] = convert_args(args, n)
    f_args['campaign'] = args['<campaign>']

    # Remove empty values
    f_args = {k: v for k, v in f_args.items() if v is not None}

    # Create config and update with args
    # !!!!!!!
    # To change : not absolute path
    # !!!!!!!
    conf = Config(f_args.pop('config-file'))
    conf.update(f_args)

    print("=================================================")
    print("===== Let's import the image from SD card =======")

    campaign = managedb.make_campaign(conf['campaign'], conf['id-rederbro'], conf.get('description'))

    # We need to improve this
    # Case 1 : we pass the Arguments
    # Case 2 : Go get the file on rederbro
    srcDir = Path(conf["data-dir"].format(campaign=conf.get('campaign'))).expand()
    csvFile = Path(srcDir) / "pictureInfo.csv"

    if conf.get('import'):
        print("Get data from SD card ...")
        Main().init(conf.get('campaign'), conf).start()
        print("... Done ! Data recover.")

    if conf.get('treat'):
        for l in makeLots(srcDir, csvFile):
            lot = treat(campaign, l)
            # lot object can't be send through network
            if conf.get('export'):
                task.assemble.delay(lot.id)


if __name__ == "__main__":
    main()
