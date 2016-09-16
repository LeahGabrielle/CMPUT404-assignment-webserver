#  coding: utf-8 
import SocketServer
import mimetypes
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 2016 Leah Olexson
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
        self.success = True
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
	self.parse_request(self.data)
        if (self.success):
            #send 200 message
            self.request.sendall("HTTP/1.1 200 OK\r\n")
            #from falsetru at http://stackoverflow.com/questions/21153262/sending-html-through-python-socket-server
            #from Sarah Van Belleghem at https://github.com/vanbelle/CMPUT404-assignment-webserver
            self.request.sendall("Content-Type: "+self.content_type+"\r\n")
            self.request.sendall("Content-Length: "+str(len(self.content))+"\r\n\r\n")
            self.request.sendall(self.content)

    def hasExtension(self):
        print self.path[:9:]
        if self.path[:9:] == "127.0.0.1":
            self.path = self.path[15::]
        try:
            print 'www/'+self.path
            f = open('www/'+self.path)
            self.content = f.read()
            f.close
        except:
           self.error_404()

    def noExtension(self, ext):
        try:
            f = open('www/'+self.path+ext)
            self.content = f.read()
            f.close
        except:
            self.error_404()

    def directory(self):
        try:
            f = open('www/'+self.path+"index.html")
            self.content = f.read()
            f.close
            self.content_type = "text/html"
        except:
            self.error_404()

    def endType(self):
    	reply = False
        extension = mimetypes.guess_type(self.path)[0]
        #this means no .html, .css or file specified
        if (extension == None):
            #This is for paths ending in / or empty paths 
            if (self.path == "" or self.path[-1] == "/"): 
                self.directory()
            #this is files without .html, .css
            else:
                if (self.path[-5::] == "index"):
                    extension = '.html'
                    self.content_type = "text/html"
                    self.noExtension(extension)
                elif (self.path[-4::] == "base" or self.path[-4::] == "deep"):
                    if (self.path == "deep/deep"):
                        self.error_404()
                    if self.path == "deep":
                        self.success = False
                        self.request.sendall("HTTP/1.1 301 MOVED PERMANENTLY\r\n")
                        self.request.sendall("Location: deep/index.html\r\n")
                        #f = open('www/'+self.path+"index.html")
                        #self.content = f.read()
                        #f.close
                        #self.content_type = "text/html"
                        #self.path += "/"
                        #self.directory()
                    else:
                        extension = '.css'
                        self.content_type = "text/css"
                        self.noExtension(extension)
                else:
                    self.error_404() 
                #self.noExtension(extension)
                
        #we got the extension from guess_type
        else:
            if self.path == "deep.css":
                self.error_404()
            else:
                if (self.path =="127.0.0.1:8080/deep/index.html"):
                  f = open("www/deep/index.html")
                  self.content = f.read()
                  f.close
                  self.content_type = "text/html" 
                  self.path = ""
                else:
                    self.content_type = extension
                    self.hasExtension()


    #from sberry at http://stackoverflow.com/questions/18563664/socketserver-python 
    #parses the get request for relevant information
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
        self.path = path.lstrip("/")
        self.method = method
        self.headers = headers
        self.body = body
	self.endType()	

    #error function
    def error_404(self):
        self.request.sendall("HTTP/1.1 404\r\n")
        self.request.sendall("\n404 Error\n")
        self.success = False
    
if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
