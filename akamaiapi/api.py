#!/usr/custom/python-2.7.6/bin/python

import os, sys, re, datetime, logging
import hmac, hashlib, base64
import json
import uuid
import ssl

if sys.version_info[0] == 3:
    import urllib.request as URL
    import configparser as ConfigParser
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
else:
    import urllib2 as URL
    import ConfigParser
    ctx = None


logger = logging.getLogger(__name__)

class API:

    def __init__(self, file=os.environ['HOME'] + '/.edgerc'):

        self.config = ConfigParser.ConfigParser()
        self.config.read(file)
        self.defaults = self.config.defaults()
        self.client_secret = self.defaults['client_secret']
        self.client_token = self.defaults['client_token']
        self.access_token = self.defaults['access_token']
        self.host = self.defaults['host']
        #self.http = httplib.HTTPSConnection(self.host)

    def _hmac_sha256(self, key, data):
        digest = hmac.new(
            key.encode('utf8'),data.encode('utf8'),digestmod=hashlib.sha256
        ).digest()
        return base64.b64encode(digest).decode('utf8')

    def _nonce(self):
        nonce = uuid.uuid4()
        return nonce

    def _timestamp(self):
        try:
            tmp = os.environ['TZ']
        except KeyError:
            tmp = None
        os.environ['TZ'] = 'UTC'
        now = datetime.datetime.now()
        ts = now.strftime("%Y%m%dT%H:%M:%S+0000")
        if tmp is None:
            del os.environ['TZ']
        else:
            os.environ['TZ'] = tmp
        return ts

    def get(self,path):
        timestamp = self._timestamp()
        nonce = self._nonce()
        signing_key = self._hmac_sha256(self.client_secret,timestamp)
        data_to_sign = 'EG1-HMAC-SHA256 client_token={0};access_token={1};timestamp={2};nonce={3};'.format(self.client_token,self.access_token,timestamp,nonce)
        data = '\t'.join([
            'GET','https',
            self.host,
            path,
            '',
            '',
            data_to_sign
        ])
        signature = self._hmac_sha256(signing_key,data)
        data_to_sign += "signature={0}".format(signature)
        headers = {'Authorization': data_to_sign}
        req = URL.Request(
            "https://{0}{1}".format(self.host,path),
            None,
            headers
        )
        if sys.version_info[0] == 3:
            u = URL.urlopen(req,context=ctx)
        else:
            u = URL.urlopen(req)
        response_json = u.read().decode('utf8')
        result = json.loads(response_json)
        return result

