#!/usr/bin/env python3
# -*- coding:utf-8 -*-
import sys

s_box=[
    # 0     1    2      3     4    5     6     7      8    9     A      B    C     D     E     F
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

rcon = [0x8d, 0x01, 0x02, 0x04, 0x08,
        0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

class KeySchedule(object):
  def __init__(self, *args, **kwargs):
    self.key=key
    self.key_round=int(key_round)
    self.round_key = [0]*240
    self.nk = len(key) * 4 //32
    self.nr= self.nk+6  # 变换轮数

  def _generate_temp_key(self, i):
    temp_arr = [0]*4
    for j in range(0, 4):
        temp_arr[j] = self.round_key[(i-1) * 4 + j]
    if i % self.nk == 0:
      #列号为4的倍数，进行G函数处理
      k = temp_arr[0]
      temp_arr[0] = temp_arr[1]
      temp_arr[1] = temp_arr[2]
      temp_arr[2] = temp_arr[3]
      temp_arr[3] = k
      temp_arr[0] = s_box[temp_arr[0]]
      temp_arr[1] = s_box[temp_arr[1]]
      temp_arr[2] = s_box[temp_arr[2]]
      temp_arr[3] = s_box[temp_arr[3]]
      temp_arr[0] = temp_arr[0] ^ rcon[i//self.nk]
    elif self.nk > 6 and i % self.nk == 4:
      temp_arr[0] = s_box[temp_arr[0]]
      temp_arr[1] = s_box[temp_arr[1]]
      temp_arr[2] = s_box[temp_arr[2]]
      temp_arr[3] = s_box[temp_arr[3]]
    return temp_arr


  def expansion(self):
    key_bytes = [0]*32
    for index, k in enumerate(bytes.fromhex(self.key)):
      key_bytes[index]=k
    start =self.key_round * 4
    #将现有的key放入数组
    for i in range(start, self.nk+start):
      self.round_key[(i * 4) + 0] = key_bytes[((i-start) * 4) + 0]
      self.round_key[(i * 4) + 1] = key_bytes[((i-start) * 4) + 1]
      self.round_key[(i * 4) + 2] = key_bytes[((i-start) * 4) + 2]
      self.round_key[(i * 4) + 3] = key_bytes[((i-start) * 4) + 3]
    for i in range(self.nk+start, 4 * (self.nr + 1)):
      temp_key = self._generate_temp_key(i)
      for j in range(0,4):
        self.round_key[i * 4 +
                       j] = self.round_key[(i - self.nk) * 4 + j] ^ temp_key[j]
    for i in range(self.nk+start-1, self.nk-1, -1):
      temp_key = self._generate_temp_key(i)
      for j in range(0,4):
        self.round_key[(i - self.nk) * 4 +
                       j] = self.round_key[i * 4 + j] ^ temp_key[j]
    for j in range(0, 16*(self.nr+1)):
      if (j % 16 == 0):
          print("Round %02i: " % int(j/16), end="")
      print("%02X" % self.round_key[j], end="")
      if j % 16 == 15:
        print("")

# python aes_key_schedule.py 31B2998CC1D82E46B1F98F98A215B415 10
if __name__=='__main__':
  if len(sys.argv)<3:
    self_name=sys.argv[0]
    print('请输入待解码的Aes key和所在的轮数')
    print('参数一为生成的Aes key，参数二为生成的轮数')
    print('举个栗子:')
    print('-- Aes-128:(输入16位的key和生成的key的轮数,128只有10轮)')
    print('python %s B1BA2737C83233FE7F7A7DF0FBB01D4A 1 #第1轮生成的key' % self_name)
    print('python %s B1BA2737C83233FE7F7A7DF0FBB01D4A 5 #第5轮生成的key' % self_name)
    print('python %s B1BA2737C83233FE7F7A7DF0FBB01D4A 10 #第10轮生成的key' % self_name)
    print('-- Aes-192:(输入24位的key和生成的key的轮数,192只有12轮)')
    print('python %s B1BA2737C83233FE7F7A7DF0FBB01D4A7835FA62BE9726A1 1 #第1轮生成的key' % self_name)
    print('python %s B1BA2737C83233FE7F7A7DF0FBB01D4A7835FA62BE9726A1 5 #第5轮生成的key' % self_name)
    print('python %s B1BA2737C83233FE7F7A7DF0FBB01D4A7835FA62BE9726A1 12 #第12轮生成的key' % self_name)
    print('Aes-256同理')
  else:
    key=sys.argv[1]
    key_round=sys.argv[2]
    if len(key) not in [32, 48, 64]:
      print('key的长度只能为16,24或32位')
    key_schedule=KeySchedule(key,key_round)
    key_schedule.expansion()



