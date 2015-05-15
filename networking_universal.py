"""
The DTScripts Universal Networking script

I made this as a base for communication for my upcoming racing game. I hope that you find this useful for your project as well. :)

The DTScripts Universal Networking script is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

The DTScripts Universal Networking script is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with the DTScripts Universal Networking script.  If not, see <http://www.gnu.org/licenses/>.
"""

import bge
from bge import logic
from GameLogic import *
from socket import *
from pickle import *

def networkInitServer():
    cont = bge.logic.getCurrentController()
    globaldict = bge.logic.globalDict
    obj = cont.owner
    
    host = '127.0.0.1'
    ServerPort = 45000
    globaldict['sServer'] = socket(AF_INET, SOCK_DGRAM)
    globaldict['sServer'].setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    globaldict['sServer'].bind((host,ServerPort))
    globaldict['sServer'].setblocking(0)
    globaldict['connection_type'] = 'server'
        
def networkInitClient():
    cont = bge.logic.getCurrentController()
    obj = cont.owner
    globaldict = bge.logic.globalDict
    
    ServerIP = '127.0.0.1'
    ServerPort = 45000
    Clientname = ''
    ClientPort = 45001
    globaldict['sClient'] = socket(AF_INET, SOCK_DGRAM)
    globaldict['sClient'].setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    globaldict['sClient'].bind((Clientname,ClientPort))
    globaldict['host'] = (ServerIP,ServerPort)
    globaldict['sClient'].setblocking(0)
    globaldict['connection_type'] = 'client'

def updateData(cont):
    cont = bge.logic.getCurrentController()
    obj = cont.owner
    globaldict = bge.logic.globalDict
    PosYou = [obj.position[0], obj.position[1], obj.position[2]]
    scene = getCurrentScene()
    if globaldict['connection_type'] == "server":
        Client = scene.objects['OBClient']
        try:
            #print('stuff received?')
            Data, CLIP = globaldict['sServer'].recvfrom(1024)
            #print(Data) #data coming in confirmed
            UPData = loads(Data)
            PosClient = [UPData[0], UPData[1], UPData[2]]
            Client.worldPosition = PosClient
            Data = dumps((PosYou))
            #print("wtf: " + str(Data))
            globaldict['sServer'].sendto(Data, CLIP)
            #print(Data)
        except:
            pass
    if globaldict['connection_type'] == "client":
        Server = scene.objects['OBServer']
        Data = dumps((PosYou))
        globaldict['sClient'].sendto(Data, globaldict['host'])
        try:
            Data1, SRIP = globaldict['sClient'].recvfrom(1024)
            UPData = loads(Data1)
            #print(SRIP)
            #print("woot" + str(UPData))
            PosServer = [UPData[0], UPData[1], UPData[2]]
            Server.worldPosition = PosServer
        except:
            pass
