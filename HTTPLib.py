import re
# coding: utf-8

import os
import pdb

class HTTPResponse(object):
    def __init__(self, requested_object_path):
        # ensure request is within root folder
        self.file_path = requested_obect_path

    def generate(self, response_object_path=None):
        # determine whether requested object exists
        if not os.path.exists(response_object_path)
            response = self.build_404_response(response_object_path)

        # determine whether were sending a directory or not
        if os.path.isdir(response_object_path):
            response = self.build_dir_response(response_object_path)
        else:
            response = self.build_file_response(response_object_path)
        return response 

    def build_dir_response(self, response_object_path):
        # return http response string
        pass

    def build_file_response(self, response_object_path):
        # return http response string
        pass

    def build_404_response(self, response_object_path=None):
        # return 404

class HTTPRequest(object):
    def __init__(self, request, root):
        try:
            self.method, self.filename, self.version =  request.splitlines()[0].split()
        except IndexError as e:
            print e.message
        
        self.file_path = os.path.realpath(root) + self.filename
        # regex snippet for parsing headers from:
        # http://stackoverflow.com/questions/4685217/parse-raw-http-headers
        # January 8, 2015
        # Author: mouad
        self.hdr_dict = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n",\
                                request))
