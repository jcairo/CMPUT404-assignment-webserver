import re
# coding: utf-8

import os
import pdb

class HTTPResponse(object):
    def __init__(self, requested_object_path, http_request, abs_server_root):
        # ensure request is within root folder
        self.request = http_request
        self.abs_server_root = abs_server_root

    def generate(self):
        # determine whether file is in server root dir
        if not os.path.commonprefix([self.abs_server_root, os.path.realpath(self.request.file_path)]) == self.abs_server_root: 
            return self.build_404_response()

        # determine whether requested object exists
        if not os.path.exists(self.request.file_path):
            return self.build_404_response()

        # determine whether were sending a directory or not
        if os.path.isdir(self.request.file_path):
            response = self.build_dir_response()
        else:
            response = self.build_file_response()
        return response

    def build_dir_response(self):
        self.headers = self.get_headers('text/html', 200)
        self.line_break = '\r\n'
        self.body = str(os.listdir(self.request.file_path))
        return self.headers + self.line_break + self.body

    def build_file_response(self):
        f = open(self.request.file_path, 'rb')
        self.body = f.read()
        self.headers = self.get_headers(self.get_content_type(), 200)
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
            self.headers = 'HTTP/1.1 200 OK\r\n'
        if code == 404:
            self.headers = "HTTP/1.1 404 Not Found\r\n"
        self.headers += 'Connection: close\r\n'
        self.headers += 'Server: CMPUT404\r\n'
        self.headers += 'Accept-Ranges: bytes\r\n'
        self.headers += 'Content-Type: ' + content_type + '\r\n'
        return self.headers

    def get_content_type(self):
        self.file_type = self.request.file_path.split('.')[-1]
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
