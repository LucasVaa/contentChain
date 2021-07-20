# -*- coding:UTF-8 -*-
import json
import random
import time
import urllib.parse
import urllib.request
import os
import sys
sys.path.append(os.pardir)

from contentp2p import udp as pu
from globalArgs import glo
from contentDb import createTable, databaseSync
from contentCore import transaction, block
from contentConsensusStorage import levelDBStorage
from contentConsensus import pbftMsg, tools


def rootReceive(udp_socket):
    """"Start a receiving thread to process information from the other node."""
    while 1:
        data, addr = pu.recembase(udp_socket)
        action = json.loads(data)
        # A new node joins.
        if action['type'] == 'addNode':
            print("A new node is added!")
            print(action['data'])
            peerInfoList = createTable.getPeerList()
            peerList = []
            for i in peerInfoList:
                peerList.append(i['nid'])
            try:
                createTable.NodeInformation.create(
                    nid = action['data']['nid'],
                    public_key = action['data']['public_key'],
                    node_type = action['data']['node_type'],
                    capacity = action['data']['capacity'],
                    score = action['data']['score'],
                    pid = action['data']['pid'],
                    createdAt = action['data']['createdAt'],
                    updatedAt = action['data']['updatedAt'],
                )
            except Exception as e:
                print('Catch a exception', e)
            pu.broadcastJS(udp_socket, {
                "type": "addNode",
                "data": action['data']
            }, peerList)
            
            pu.sendJS(udp_socket, addr[0],{
                "type": "addList",
                "data": peerInfoList
            })
            # choose a leaderNode & broadcast id
            leaderNid = ''
            peerInfoList = createTable.getPeerList()
            peerList = []
            for i in peerInfoList:
                peerList.append(i['nid'])
            leaderNid = random.choice(peerList)
            glo.set_value("leaderNid", leaderNid)
            pu.broadcastJS(udp_socket, {
                "type": "leaderNid",
                "data": leaderNid
            }, peerList)
        elif action['type'] == 'startRoot':
            url = 'http://' + action['data']['oldRoot'] + ':8888/getLatestState'
            result = ""
            with urllib.request.urlopen(url) as f:
                result = f.read().decode('utf-8')
                result = json.loads(result)
            print(result)
            # MySQL存储ContentObjectLocation
            for value in result['location']:
                location = value
                try:
                    createTable.ContentObjectLocation.create(
                        cid=location['cid'],
                        nid1=location['nid1'],
                        nid2=location['nid2'],
                        nid3=location['nid3'],
                        createdAt=location['createdAt'],
                        updatedAt=location['updatedAt']
                    )
                except Exception as e:
                    print('Catch a exception', e)

            # MySQL存储NodeInformation
            for value in result['node_list']:
                node = value
                try:
                    createTable.NodeInformation.create(
                        nid=node['nid'],
                        public_key=node['public_key'],
                        node_type=node['node_type'],
                        capacity=node['capacity'],
                        score=node['score'],
                        pid=node['pid'],
                        createdAt=node['createdAt'],
                        updatedAt=node['updatedAt']
                    )
                except Exception as e:
                    print('Catch a exception', e)


            

def seedReceive(udp_socket):
    """"Start a receiving thread to process information from the other node."""
    while 1:
        data, addr = pu.recembase(udp_socket)
        action = json.loads(data)
        # A new node joins.
        if action['type'] == 'addNode':
            try:
                createTable.NodeInformation.create(
                    nid = action['data']['nid'],
                    public_key = action['data']['public_key'],
                    node_type = action['data']['node_type'],
                    capacity = action['data']['capacity'],
                    score = action['data']['score'],
                    pid = action['data']['pid'],
                    createdAt = action['data']['createdAt'],
                    updatedAt = action['data']['updatedAt'],
                )
            except Exception as e:
                print('Catch a exception', e)
        elif action['type'] == 'addList':
            peerList = []
            for i in action['data']:
                peerList.append(i['nid'])
                try:
                    createTable.NodeInformation.create(
                        nid = i['nid'],
                        public_key = i['public_key'],
                        node_type = i['node_type'],
                        capacity = i['capacity'],
                        score = i['score'],
                        pid = i['pid'],
                        createdAt = i['createdAt'],
                        updatedAt = i['updatedAt'],
                    )
                except Exception as e:
                    print('Catch a exception', e)
            if (len(peerList) <= 1):
                peerList = ["1111"]
            glo.set_value("peerList", peerList)
        elif action['type'] == 'leaderNid':
            print("leaderNid", action['data'])
            glo.set_value("leaderNid", action['data'])
        elif action['type'] == 'requestConsensus':
            evidence = ''
            if len(action['data']) == 6:
                evidence = transaction.Trade(
                    nid = action['data']['nid'],
                    evidence_time = action['data']['evidence_time'],
                    cid = action['data']['cid'],
                    uid = action['data']['uid'],
                    value = action['data']['value'],
                    state = action['data']['state']
                )
            elif len(action['data']) == 13:
                evidence = transaction.Evidences(
                    nid = action['data']['nid'],
                    evidence_time = action['data']['evidence_time'],
                    cid = action['data']['cid'],
                    uid = action['data']['uid'],
                    pid = action['data']['pid'],
                    title = action['data']['title'],
                    author = action['data']['author'],
                    description = action['data']['description'],
                    publisher = action['data']['publisher'],
                    publishid = action['data']['publishid'],
                    isencrypt = action['data']['isencrypt'],
                    content_hash = action['data']['content_hash'],
                    create_time = action['data']['create_time'],
                )
            elif len(action['data']) == 4:
                evidence = transaction.Takeoff(
                    nid = action['data']['nid'],
                    evidence_time = action['data']['evidence_time'],
                    cid = action['data']['cid'],
                    state = action['data']['state']
                )
            transactions = transaction.Transaction(evidence)
            glo.get_value("sealer").consensus_pool.enqueue(transactions)
            print('evidence is added')
        elif action['type'] == 'result':
            # return TransactionHash to the userEnd
            glo.set_value("txHash", action['data'])

        elif action['type'] == 'broadcastPrePrepare':
            peerInfoList = tools.get_seed_list()
            peerList = []
            for i in peerInfoList:
                peerList.append(i['nid'])
            pu.broadcastJS(udp_socket, {
                "type": "prePrepare",
                "data": action['data']
            }, peerList)

        elif action['type'] == 'prePrepare':
            prePrepare = pbftMsg.PBFTMsg('prePrepare')
            prePrepare.message_body = action['data']['message_body']
            glo.get_value("engine").handlePrePrepare(prePrepare)

        elif action['type'] == 'broadcastPrepare':
            peerInfoList = tools.get_seed_list()
            peerList = []
            for i in peerInfoList:
                peerList.append(i['nid'])
            pu.broadcastJS(udp_socket, {
                "type": "prepare",
                "data": action['data']
            }, peerList)

        elif action['type'] == 'prepare':
            prepare = pbftMsg.PBFTMsg('prepare')
            prepare.message_body = action['data']['message_body']
            glo.get_value("engine").handlePrepare(prepare)

        elif action['type'] == 'broadcastCommit':
            peerInfoList = tools.get_seed_list()
            peerList = []
            for i in peerInfoList:
                peerList.append(i['nid'])
            pu.broadcastJS(udp_socket, {
                "type": "commit",
                "data": action['data']
            }, peerList)

        elif action['type'] == 'commit':
            commit = pbftMsg.PBFTMsg('commit')
            commit.message_body = action['data']['message_body']
            glo.get_value("engine").handleCommit(commit)

        elif action['type'] == 'reply':
            glo.set_value("consensusBlock", action['data'])

        elif action['type'] == 'reportBlock':
            peerInfoList = createTable.getPeerList()
            peerList = []
            for i in peerInfoList:
                peerList.append(i['nid'])
            report_block = action['data']
            pu.broadcastJS(udp_socket, {
                "type": "getBlock",
                "data": report_block
            }, peerList)

        elif action['type'] == 'getBlock':
            report_block = action['data']
            blocks = block.load_block(report_block)
            levelDBStorage.storage(blocks, glo.get_value("leveldb"))
            databaseSync.sync(report_block)

def seedSend():
    """"Start a sending thread to process information from the terminal."""
    time.sleep(1)
    while 1:
        msg_input = input("$:")
        if (msg_input == "exit"):
            parm = {
                "nid": glo.get_value("ip")
            }

            data = urllib.parse.urlencode(parm)
            url = 'http://' + glo.get_value('root') + ':5555/deleteNode?%s' % data
            result = ''
            with urllib.request.urlopen(url) as f:
                result = f.read().decode('utf-8')
                result = json.loads(result)
            os._exit(1)

def rootSend():
    """"Start a sending thread to process information from the terminal."""
    time.sleep(1)
    while 1:
        msg_input = input("$:")
        if (msg_input == "exit"):
            rootlist = ["10.10.1.117", "10.10.1.118"]

            root = random.choice(rootlist)

            # 1.通知根结点启动并同步根结点的mysql数据

            parm = {
                "oldRoot": glo.get_value("ip")
            }
            pu.sendJS(
                glo.get_value("udp_socket"),
                root,
                {
                    "type": "startRoot",
                    "data": parm
                }
            )
            # 2.通知结点网络更新根结点
            data = {
                "root": root,
            }
            glo.set_value("node_type", type)
            data = json.dumps(data)
            data = data.encode('utf-8')
            nidList = createTable.getAll()
            for i in nidList:
                url = 'http://' + i + ':8888/changeRoot'
                result = ''    
                with urllib.request.urlopen(url, data) as f:
                    result = f.read().decode('utf-8')
                    result = json.loads(result)
            time.sleep(10)
            os._exit(1)