#!usr/bin/env python
# -*- coding: utf-8 -*-

import time
import os
import socket
import fcntl
import struct

from multiprocessing import cpu_count


class Input:
    ''' 获取主机名、ip'''
    def get_ip(self):
    #    hostname = socket.getfqdn(socket.gethostname())
    #    ip = socket.gethostbyname(hostname)
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return hostname, ip

    ''' 获取指定网卡ip地址'''
    def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,
            struct.pack('256s', ifname[:15]))[20:24])

    ''' 返回百分占比 '''
    def usage_percent(self,use, total):
        try:
            ret = int(float(use)/ total * 100)
        except ZeroDivisionError:
            raise Exception("ERROR - zero division error")
        return '%s%%'%ret

    # Total returns total CPU time[
    def get_CpuTotalTime():
        return cpu['user'] + cpu['Nice'] + cpu['Sys'] + cpu['Idle'] + cpu['Wait'] + cpu['Irq'] + cpu['SoftIrq'] + cpu['Stolen']

    '''
    name   user  nice   system      idle      iowait  irrq  softirq  steal guest guest_nice 
    cpu    60382   1     80032     198934063   2349     0     109      0     0       0
    cpu0   2405    0     2084      4140924     682      0     6        0     0       0
    '''
    @property
    def cpu_stat(self,interval = 1, idle_old = 0):
        cpu_num = cpu_count()
        with open("/proc/stat", "r") as f:
            line = f.readline()
            spl = line.split(" ")
            worktime_1 = sum([int(i) for i in spl[2:]])
            idletime_1 = int(spl[5])
        time.sleep(interval)
        with open("/proc/stat", "r") as f:
            line = f.readline()
            spl = line.split(" ")
            worktime_2 = sum([int(i) for i in spl[2:]])
            idletime_2 = int(spl[5])

        dworktime = (worktime_2 - worktime_1)
        didletime = (idletime_2 - idletime_1)
        cpu_percent = self.usage_percent(dworktime - didletime,didletime)
        return {'cpu_count':cpu_num,'cpu_percent':cpu_percent}


    @property
    def disk_stat(self):
        hd = {}
        disk = os.statvfs("/")
        hd['available'] = disk.f_bsize * disk.f_bfree
        hd['capacity'] = disk.f_bsize * disk.f_blocks
        hd['used'] =  hd['capacity'] - hd['available']
        hd['used_percent'] = self.usage_percent(hd['used'], hd['capacity'])
        return hd

    @property
    # 字节
    def memory_stat(self):
        mem = {}
        with open("/proc/meminfo", "r") as f:
            for line in f:
                line = line.strip()
                if len(line) < 2: continue
                name = line.split(':')[0]
                var = line.split(':')[1].split()[0]
            #    print("name-var=%s:%s") % (name,var)
                # KB => B
                mem[name] = long(var) * 1024.0
            mem['MemUsed'] = mem['MemTotal'] - mem['MemFree'] - mem['Buffers'] - mem['Cached']
        mem['used_percent'] = self.usage_percent(mem['MemUsed'],mem['MemTotal'])
        mem['swap_use'] = mem['SwapTotal'] - mem['SwapFree']
        return {'MemTotal':mem['MemTotal'],'MemUsed':mem['MemUsed'],'MemFree':mem['MemFree'],'used_percent':mem['used_percent'],'swap_total':mem['SwapTotal'],'swap_use':mem['swap_use'],'swap_free':mem['SwapFree']}

    ''' 获取Linux系统的总物理内存 '''
    def get_TotalMemory(self):
        with open('/proc/meminfo', "r") as fd:
            for line in fd:
                if line.startswith('MemTotal'):
                    mem = int(line.split()[1].strip())
                    break
        mem = '%.f' % (mem / 1024.0) + ' MB'
        fd.close()
        return {'Memory': mem}

    def networker_stat(self,interface='eth0'):
        net = {}
        with open('/proc/net/dev', "r") as fd:
            for line in fd:
                if interface in line:
                    stat = float(interface.split()[1])
                    STATS[0:] = [stat]

        return
'''
    def Swap_stat(self):
        swap = {}
        with open('/proc/swaps') as fd:
            for line in fd:
                if line.startswith('/'):
                    print("line is :%s") % line
                    spl = line.split(" ")
                    # spl[31] = partition	3145724	2889940	-2
                    print("spl len =%d; %s" % (len(spl),spl[31]))
                    sw = spl[len(spl)-1:].split('\t')
                    print(sw)

      
                    swap['name'] = spl[0]
                    swap['total'] = long(spl[2])
                    swap['use'] = long(spl[3])
                    swap['free'] = swap['total'] - swap['use']
                    break
        return {'name':swap['name'], 'total':swap['total'], 'use':swap['use'], 'free':swap['free']}
'''




