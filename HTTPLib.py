import re
# coding: utf-8

import os
import pdb

class HTTPResponse(object):
    def __init__(self, requested_URI_abspath, abs_server_root):
        # ensure request is within root folder
        self.abs_URI_path = requested_URI_abspath
        self.abs_server_root = abs_server_root

    def generate(self):
        # determine whether file is in server root dir
        if not os.path.commonprefix([self.abs_server_root, self.abs_URI_path]) == self.abs_server_root: 
            return self.build_404_response()

        # determine whether requested object exists
        if not os.path.exists(self.abs_URI_path):
            return self.build_404_response()

        # determine whether were sending a directory or not
        if os.path.isdir(self.abs_URI_path):
            response = self.build_dir_response()
        else:
            response = self.build_file_response()
        return response

    def build_dir_response(self):
        self.headers = self.get_headers('text/html', 200)
        self.line_break = '\r\n'
        self.body = str(os.listdir(self.abs_URI_path))
        return self.headers + self.line_break + self.body

    def build_file_response(self):
        f = open(self.abs_URI_path, 'rb')
        self.body = f.read()
        self.headers = self.get_headers(self.get_content_type(self.abs_URI_path), 200)
        self.line_break = '\r\n'
        return self.headers + self.line_break + self.body

    def build_404_response(self):
        self.headers = self.get_headers('text/html', 404)
        self.line_break = '\r\n'
        self.body = "Nothin here"
        return self.headers + self.line_break + self.body

    def get_headers(self, content_type, code):
        print ("Content Type: " + content_type)
        if code == 200:
            headers = 'HTTP/1.1 200 OK\r\n'
        if code == 404:
            headers = "HTTP/1.1 404 Not Found\r\n"
        headers += 'Connection: close\r\n'
        headers += 'Server: CMPUT404\r\n'
        headers += 'Accept-Ranges: bytes\r\n'
        headers += 'Content-Type: ' + content_type + '\r\n'
        return headers

    def get_content_type(self, abs_URI_path):
        self.file_type = abs_URI_path.split('.')[-1]
        if self.file_type == 'css':
            return 'text/css'

        if self.file_type == 'html':
            return 'text/html'

        if self.file_type == 'jpg':
            return 'image/jpg'
        
        return 'text/html'

class HTTPRequest(object):
    def __init__(self, request, root):
        try:
            self.HTTP_method, self.rel_filepath, self.version =  request.splitlines()[0].split()
        except IndexError as e:
            print e.message

        self.abs_URI_path = os.path.realpath(root + self.rel_filepath)

        # regex snippet for parsing headers from:
        # http://stackoverflow.com/questions/4685217/parse-raw-http-headers
        # January 8, 2015
        # Author: mouad
        self.hdr_dict = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n",\
                                request))
