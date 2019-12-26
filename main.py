# -*- coding: utf-8 -*-
'''
LH SELF-BOT V1.0 2019/07/27
            V1.1 2019/08/02
            V1.2 2019/08/15
'''
import os, sys
def run():
     if sys.version_info[0] == 2:
          print('This software does not support on python2.')
          return
try:
     os.system("python ./libs/main.py")
except:
     pass
exit()

if __name__ == '__main__':
    run()
