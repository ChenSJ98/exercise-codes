#!/usr/bin/env python3
"""
check the security and functionability of uploaded code 
- forbid from importing os (although not a good way compared to sandbox)
- scanning for 'import os' and 'exec'
- random chessboard check
"""
import imp
import traceback

import numpy as np
from timeout_decorator import timeout

FORBIDDEN_LIST = ['import os', 'exec']

class CodeCheck():
    def __init__ (self, script_file_path, chessboard_size):
        self.time_out = 1
        self.script_file_path = script_file_path
        self.chessboard_size = chessboard_size
        self.agent = None
        self.test_color = 1
        self.errormsg = 'Error'
        # print(self.chessboard)
        
    
    def check_code(self):
        if self.__check_forbidden_import() == False:
            return False
        try:
            self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, 1, self.time_out)
            self.agent = imp.load_source('AI', self.script_file_path).AI(self.chessboard_size, -1, self.time_out)
        except Exception:
            self.errormsg = "Fail to init"
            return False
        if not self.__check_simple_chessboard():
            self.errormsg = "Can not pass usability test."
            return False
        if not self.__check_advance_chessboard():
            self.errormsg = "Your code is too weak, fail to pass base test."
            return False
        return True


    def __check_forbidden_import(self):
        '''
        :return 1: ok
        :return 0: import error 
        '''
        with open(self.script_file_path, 'r') as myfile:
            data = myfile.read()
            for keyword in FORBIDDEN_LIST:
                idx = data.find(keyword)
                if idx != -1:
                    self.errormsg = "import forbidden"
                    return False
        return True
    
    def __check_go (self, chessboard):
        try:
            timeout(1)(self.agent.go)(np.copy(chessboard))
        except Exception:
            self.errormsg = "Error:" + traceback.format_exc()
            return False
        return True
    
    def __check_result (self, chessboard, result):
        if not self.__check_go(chessboard):
            print("enter check_go")
            return False
        if not self.agent.candidate_list or list(self.agent.candidate_list[-1]) not in result:
            print("enter 2")
            return False
        return True
        
    def __check_simple_chessboard(self):
        if not self.__check_go(np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)):
            print("not pass check go")
            return False
    
        tmp0 = [1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1]
        tmp1 = np.stack([tmp0] * 3)
        tmp2 = -tmp1
        chessboard = np.concatenate([tmp1, tmp2, tmp1, tmp2, tmp1], axis=0)
        idx = np.random.choice(15 * 15, 10)
        chessboard = np.reshape(chessboard, [15 * 15])
        chessboard[idx] = 0
        chessboard = np.reshape(chessboard, [15, 15])
    
        if not self.__check_go(chessboard):
            return False
        # print("valid")
        ## check validity
        try:
            # print("-----------------")
            # print(self.agent.candidate_list[-1])
            # print(chessboard)
            # print()
            # print(chessboard[self.agent.candidate_list[-1]])
            if chessboard[self.agent.candidate_list[-1]] == 0:
                return True
            else:
                return False
        except ValueError:
            return False
        except IndexError:
            return False
    
    def __check_advance_chessboard (self):
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        f = open("./chess_log.txt",'r')
        i = 0
        lines = f.readlines()
        for x in lines:
            i = i + 1
            if (i == len(lines) - 1):
                break
            s = x.split(',')
            # print(s,i,len(lines)-1)
            chessboard[int(s[0])][int(s[1])]=int(s[2][:-1])
        
        self.__check_result(chessboard,[0,0])
        # 冲5
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:4] = -1
        chessboard[1, 0:4] = 1
        if not self.__check_result(chessboard, [[0, 4]]):
            return False
        
        # 防守冲5
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:3] = -1
        chessboard[0, 7] = -1
        chessboard[1, 0:4] = 1
        if not self.__check_result(chessboard, [[1, 4]]):
            return False
        
        # 三三
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[1, 1:3] = -1
        chessboard[2:4, 3] = -1
        chessboard[1, 6:8] = 1
        chessboard[2:4, 8] = 1
        if not self.__check_result(chessboard, [[1, 3]]):
            return False
        
        # 防守三三
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0,1] = -1
        chessboard[0,6] = -1
        chessboard[1,1:5] = -1
        chessboard[2,5] = -1
        chessboard[2,7] = -1
        chessboard[3,8] = -1
        chessboard[4,7:9] = -1
        chessboard[5,6] = -1
        # chessboard[6,5] = -1

        chessboard[0:2, 0] = 1
        chessboard[0, 2:6] = 1
        chessboard[1,5] = 1
        chessboard[2,6] = 1
        chessboard[3,4:8] = 1
        chessboard[4,6] = 1
        # chessboard[2:4, 8] = 1
        if not self.__check_result(chessboard, [[3, 3]]):
            return False
        
        
        return True
