#!usr/bin/env python
# -*- coding: utf-8 -*-

import time
import sys
sys.path.append(r'/home/python_worker/moniter')

#import socket
from input import Input
from output import Output
from config import Config


class moniter:
    '''
        cpu net
    '''
    def timer_register(self, interval = 1, type='cpu'):
        if type in ['cpu', 'net']:
            print('aaaaaaa')
        else:
            print('bbbbbbb')
'''
    def _init__(self):
        print("---------init start---------")
        #global _Producer, _Consumer, _Config
        print('---------load import---------')
        self.Producer = Input()
        self.Consumer = Output()
        self.Config = Config()

        print("---------load config---------")
        self.Config.load_config()

        print('---------get system mertrisy---------')
'''



if __name__=='__main__':
    Producer = Input()
    Consumer = Output()

    hostname, ip = Producer.get_ip()
    print(hostname, ip)

    time.sleep(1)
    s = Producer.get_ip_address('ens33')
    print("ens33 ipaddr is %s" % s)

    print('======cpu idle=========')
    print(Producer.cpu_stat)

    print('======disk============')
    print(Producer.disk_stat)

    print('======mem============')
    print(Producer.memory_stat)

    print('======net============')
    print(Producer.networker_stat)
#    print('============%s======' % Producer.get_TotalMemory())
#    print(Producer.Swap_stat())

    print('======out============')
    Consumer.output2kafka()
    #proc