#!/usr/bin/env python3

base = 16
'''
for i in range(0,base+1):
    numbers = []
    for x in range(0,16):
        count = i
        for z in range(1,x+1):
            count = count + (((base*base)**z)*i)
        numbers.append(count)
    print("{0}:\n".format(i))
    for num in numbers:
        print("\t",hex(num),num)
'''

for i in range(0,base+1):
    last = i
    for x in range(0,base+1):
        print(hex(last))
        last = i + ((base*base)*last)

'''
6
(6*256)+6
606
(6*257*256)+6
60606
(6*257*256*256)+(6*256)+6
6060606
(6*257*256*256*256)+(6*256*256)+(6*256)+6
606060606

6
(6*256)+6
606
(6*256*256)+(256*6)+6
60606
(6*256*256*256)+(256*6*256)+(256*6)+6
6060606
(6*256*256*256*256)+(256*6*256*256)+(6*256*256)+(6*256)+6
606060606
(6*256*256*256*256*256)+(256*6*256*256*256)+(6*256*256*256)+(6*256*256)+(6*256)+6
60606060606

'''
