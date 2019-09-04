import sys
import os
import io
import re
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'lib'))
from misc import printdbg


class HatchConfig():

    @classmethod
    def slurp_config_file(self, filename):
        # read hatch.conf config but skip commented lines
        f = io.open(filename)
        lines = []
        for line in f:
            if re.match(r'^\s*#', line):
                continue
            lines.append(line)
        f.close()

        # data is hatch.conf without commented lines
        data = ''.join(lines)

        return data

    @classmethod
    def get_rpc_creds(self, data, network='mainnet'):
        # get rpc info from hatch.conf
        match = re.findall(r'rpc(user|password|port)=(.*?)$', data, re.MULTILINE)

        # python >= 2.7
        creds = {key: value for (key, value) in match}

        # standard Hatch defaults...
        default_port = 8884 if (network == 'mainnet') else 18884

        # use default port for network if not specified in hatch.conf
        if not ('port' in creds):
            creds[u'port'] = default_port

        # convert to an int if taken from hatch.conf
        creds[u'port'] = int(creds[u'port'])

        # return a dictionary with RPC credential key, value pairs
        return creds

    @classmethod
    def tokenize(self, filename):
        tokens = {}
        try:
            data = self.slurp_config_file(filename)
            match = re.findall(r'(.*?)=(.*?)$', data, re.MULTILINE)
            tokens = {key: value for (key, value) in match}
        except IOError as e:
            printdbg("[warning] error reading config file: %s" % e)

        return tokens
