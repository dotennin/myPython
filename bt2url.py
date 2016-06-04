#coding: utf-8
# -*- encoding: utf-8 -*-

import bencode, urllib, hashlib, base64
import sys, os, re


def start():
    try:
        #param取得
        torrentName = sys.argv[1]
        if os.path.isfile(torrentName):
            torrent = open(torrentName, 'rb').read()
            printMeta(torrent)

    except:
        #カレントディレクトリのフャイル取得
        files = os.listdir("./")
        for file in files:
            if (re.search(".+[.]+torrent", file) is not None and
                os.path.isfile(file)):
                torrent = open(file, 'rb').read()
                printMeta(torrent)


def printMeta(torrent):
    #メタ計算
    metadata = bencode.bdecode(torrent)
    hashcontents = bencode.bencode(metadata['info'])
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest)
    #プリント
    print 'magnet:?xt=urn:btih:%s' % b32hash

if __name__ == "__main__":
    start()