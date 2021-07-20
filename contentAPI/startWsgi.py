# -*- coding:UTF-8 -*-
import threading
from wsgiref.simple_server import make_server

import os
import sys
sys.path.append(os.pardir)

from contentAPI.admin.command import route as adminRoute
from contentAPI.app.command import route as appRoute
from contentAPI.node.command import route as nodeRoute
from globalArgs import glo

def startNodeServer(ip):
	with make_server(ip, 8888, nodeRoute.routeMiddleware) as nodeHttpd:
		print("Serving HTTP on port 8888...")
		# Respond to requests until process is killed
		nodeHttpd.serve_forever()

def startAdminServer(ip):
	with make_server(ip, 5555, adminRoute.routeMiddleware) as nodeHttpd:
		print("Serving HTTP on port 5555...")
		# Respond to requests until process is killed
		nodeHttpd.serve_forever()

def startAppServer(ip):
	with make_server(ip, 80, appRoute.routeMiddleware) as nodeHttpd:
		print("Serving HTTP on port 80...")
		# Respond to requests until process is killed
		nodeHttpd.serve_forever()

if __name__ == "__main__":
	glo._init()
	t1 = threading.Thread(target=startNodeServer, args=())
	t2 = threading.Thread(target=startAdminServer, args=())
	t3 = threading.Thread(target=startAppServer, args=())
	t1.start()
	t2.start()
	t3.start()