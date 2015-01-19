# coding: utf-8
import re

#    Copyright 2015 Jonathan Cairo
#    
#    This file is part of CMPUT404-assignment-webserver
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import pdb

class HTTPResponse(object):
    def __init__(self, requested_URI_abspath, abs_server_root, request):
        # ensure request is within root folder
        self.abs_URI_path = requested_URI_abspath
        self.abs_server_root = abs_server_root
        
        # parse the first line of the http request
        try:
            self.HTTP_req_method, self.req_rel_filepath, self.HTTP_req_version =  request.splitlines()[0].split()
        except IndexError as e:
            print e.message

    def generate(self):
        # ensure valid http request line
        if self.HTTP_req_version != 'HTTP/1.1' and self.HTTP_req_version != 'HTTP/1.0':
            return self.build_404_response()

        if self.req_rel_filepath == None:
            return self.build_404_response()
        
        if self.HTTP_req_method != 'GET':
            return self.build_404_response()

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
        self.body = self.build_file_links(os.listdir(self.abs_URI_path))
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

    def build_file_links(self, file_list):
        file_contents_html = ''
        for el in file_list:
            file_contents_html += '<a href=/' + el + '/>' + el + '<a>' + '<br>'
        return file_contents_html

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
