import re
# coding: utf-8

class HTTPResponse(object):
    def __init__(self):
        pass

class HTTPRequest(object):
    def __init__(self, request):
        try:
            self.request_method, self.request_path, self.http_version = \
                                request.splitlines()[0].split()
        except IndexError as e:
            print e.message

        # regex snippet for parsing headers from:
        # http://stackoverflow.com/questions/4685217/parse-raw-http-headers
        # January 8, 2015
        # Author: mouad
        self.request_dict = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n",\
                                request))
