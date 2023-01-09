#!/usr/bin/env python3
import configparser
import json
import logging
import os.path
import pprint
import time
import typing
from typing import List

import requests
import yaml

from protocol_backup import blogger
from protocol_backup.item import Item

"""Python wrapper protocols.io REST API"""


class BackupProtocols:

    def __init__(self,config):
        self.group = config['group']
        afile = config['auth file']
        if os.path.exists(afile):
            with open(afile) as f:
                authconfig = yaml.safe_load(f)
                self.client_id = authconfig['client']
                self.client_secret = authconfig['secret']
                self.public = authconfig['public']
                self.private = authconfig['private']
        else:
            raise ValueError(f"auth file {afile} specified by [auth] file not found")
        self.pagesize = int(config.get('page size',10))
        self.output_directory = config.get('output directory','storehere')

    @property
    def output_directory(self)->str:
        return self._output_dir

    @output_directory.setter
    def output_directory(self,value:str)->None:
        """Set output directory, attempting creation if not present"""
        # let Python raise error if problem per EAFP
        if value is not None:
            candidate = os.path.join(os.getcwd(),value)
            if not os.path.isdir(candidate):
                os.makedirs(candidate)
            self._output_dir = candidate
        else:
            raise ValueError("output_directory may not be None")

    def filename(self,item:Item)->str:
        """Return filename base on state of self (as_draft)"""
        n = f"protocol{item.id}.txt"
        return os.path.join(self.output_directory,n)

    def get(self,*args,**kwargs):
        """requests.get wrapper"""
        if blogger.isEnabledFor(logging.DEBUG):
            start = time.monotonic_ns()
            r = requests.get(*args,**kwargs)
            stop = time.monotonic_ns()
            blogger.debug(f"{r.url} took {(stop - start ) /1_000_000_000} seconds")
            return r
        else:
            return requests.get(*args,**kwargs)

    @property
    def private_header(self):
        return {"Authorization": f"Bearer {self.private}"}

    @property
    def public_header(self):
        return {"Authorization": f"Bearer {self.public}"}


    def _read_list(self, r, storage: List[Item]):
        """Convert response into list of protocols"""
        self._validate(r)
        plist = json.loads(r.text)
        items = plist['items']
        for itemjson in items:
            id = itemjson['id']
            storage.append(Item(itemjson))
            with open(os.path.join(self.output_directory,f'p{id}.txt'),'w') as f:
                pp = pprint.PrettyPrinter()
                text = pp.pformat(itemjson)
                print(text, file=f)
        return plist


    def _validate(self,r)->None:
        """Valid response"""
        if r.status_code == 200:
            return
        raise ValueError(f"Error {r.status_code} {r.text} reading {r.url}")

    def workspace_protocols(self):
        self.protocols : List[Item]  = []
        url = f"https://www.protocols.io/api/v3/workspaces/{self.group}/protocols"
        params = {'page_size':'100'}
        r = self.get(url,params=params,headers=self.private_header)
        print(len(self.protocols))
        self._read_list(r,self.protocols)
        for p in self.protocols:
            with open(self.filename(p),'w') as f:
                self.get_protocol(p.id,f)



    def get_protocol(self, id: int, output: typing.TextIO) -> None:
        """Get protocol by id. Pretty print to output"""
        url = f"https://www.protocols.io/api/v4/protocols/{id}"
        params = {'content_format':'json'}
        r = self.get(url, params=params,headers=self.private_header)
        self._validate(r)
        pdata = json.loads(r.text)
        # TODO. parse this out, recursively?
        pp = pprint.PrettyPrinter()
        text = pp.pformat(pdata)
        print(text, file=output)





