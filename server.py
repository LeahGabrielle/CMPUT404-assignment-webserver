#  coding: utf-8 
import SocketServer
import mimetypes
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
	self.parse_request(self.data)

    def hasExtension(self):
        try:
            f = open('www/'+self.path)
            self.request.sendall(f.read())
            f.close
        except:
           self.error_404()

    def noExtension(self, ext):
        try:
            f = open('www/'+self.path+ext)
            self.request.sendall(f.read())
            f.close
        except:
            self.error_404()

    def directory(self):
        try:
            f = open('www/'+self.path+"index.html")
            self.request.sendall(f.read())
            f.close
        except:
            self.error_404()

# http://www.acmesystems.it/python_httpd
    def endType(self):
    	reply = False
        print "PATH: "+self.path
        extension = mimetypes.guess_type(self.path)[0]
        end = self.path.split(".")
        print extension
        if (extension == None):
            #This means no .html, .css
            if (self.path == "" or self.path[-1] == "/"): 
                self.directory()
            else:
                if (self.acceptTypes[0] == "text/html"):
                    extension = '.html'
                elif (self.acceptTypes[0] == "text/css"):
                    extension = '.css'
                else:
                    self.error_404()
            
                self.noExtension(extension)
        else: # we got the extension from guess_type
            self.hasExtension()
        
        '''
    	if (self.acceptTypes[0] == "text/html"):
	   mimetype = 'text/html'
	   extension = '.html'
	   reply = True
	elif (self.acceptTypes[0] == "text/css"):
	   mimetype = 'text/css'
           extension = '.css'
	   reply = True;
        if reply:
            print end
            if (len(end) == 1):
                self.noExtension(extension)
            else:
                self.hasExtension()
        '''
#from sberry at http://stackoverflow.com/questions/18563664/socketserver-python 
    def parse_request(self, req):
        headers = {}
        lines = req.splitlines()
        inbody = False
        body = ''
        for line in lines[1:]:
            if line.strip() == "":
                inbody = True
            if inbody:
                body += line
            else:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
        method, path, _ = lines[0].split()
	self.acceptTypes = headers.get('Accept').split(",")
	#print self.acceptTypes
        self.path = path.lstrip("/")
        self.method = method
        self.headers = headers
        self.body = body
	#print self.headers
	#print self.path
	print "parse self.path: " + self.path
	#print self.method
	#print self.body	
	
	self.endType()	

    def error_404(self):
        self.request.sendall("Error 404")
    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
