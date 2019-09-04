import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from hatchd import HatchDaemon
from hatch_config import HatchConfig


def test_hatchd():
    config_text = HatchConfig.slurp_config_file(config.hatch_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'000000fa6116f5d6c6ce9b60bd431469e40b4fe55feeeda59e33cd2f0b863196'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000bf8b02180fa3860e3f4fbfaab76db14fbfd1323d1d3ad06d83b828b6644'

    creds = HatchConfig.get_rpc_creds(config_text, network)
    hatchd = HatchDaemon(**creds)
    assert hatchd.rpc_command is not None

    assert hasattr(hatchd, 'rpc_connection')

    # Hatch testnet block 0 hash == 00000bf8b02180fa3860e3f4fbfaab76db14fbfd1323d1d3ad06d83b828b6644
    # test commands without arguments
    info = hatchd.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert hatchd.rpc_command('getblockhash', 0) == genesis_hash
