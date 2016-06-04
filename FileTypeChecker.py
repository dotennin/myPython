#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
# ファイルタイプ
# 16進数からバイト数の計算が簡単に行える
def typeList():
    return {
        "FFD8FF": "JPEG",
        "89504E47": "PNG",
        "47494638": "GIF",
        "49492A00": "TIFF",
        "424D": "BMP",
        "41433130": "DWG",
        "38425053": "PSD",
        "7B5C727466": "RTF",
        "3C3F786D6C": "XML",
        "68746D6C3E": "HTML",
        "44656C69766572792D646174653A": "EML",
        "CFAD12FEC5FD746F": "DBX",
        "2142444E": "PST",
        "D0CF11E0": "MS Word/Excel",
        "5374616E64617264204A": "MDB"
    }

# バイトから16進数に変換
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
          hexstr += u"0"
        hexstr += t
    return hexstr.upper()


def filetype(filename):
    # 二進数
    binfile = open(filename, 'rb')
    tl = typeList()
    ftype = 'unknown'
    for hcode in tl.keys():
        # 読み込むバイト数
        numOfBytes = len(hcode) / 2
        # ファイルの最後まで読み込む必要がないため、HEADERに戻る、
        binfile.seek(0)
        # 「B」はバイト数を表す、バイトの配列を返す
        hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes))

        f_hcode = bytes2hex(hbytes)
        if f_hcode == hcode:
            ftype = tl[hcode]
            break
    binfile.close()
    return ftype

if __name__ == '__main__':
    print filetype('./sample.png')