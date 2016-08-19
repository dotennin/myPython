# -*-coding:UTF-8 -*-
#!/usr/bin/python

def split(filename, size):
    fp = file(filename, 'rb')
    i = 0 #计算文件切割数
    n = 0 #计算大小
    temp = file(filename+'.part'+str(i),'wb')
    buf = fp.read(1024)
    while(True):
        temp.write(buf)
        buf = fp.read(1024)
        if(buf == ''):
            print filename+'.part'+str(i)
            temp.close()
            fp.close()
            return
        n += 1
        if(n == size):
            n = 0
            print filename+'.part'+str(i)
            i += 1
            temp.close()
            temp = file(filename+'.part'+str(i),'wb')

if __name__ == '__main__':
    name = raw_input('input filename:')
    size = int(raw_input("Please input size(M):"))#输入分割后的大小，以M为单位
    split(name,1024*size)
