import gzip


#f = gzip.open('C:\\Users\\ia.kudryashov\\PycharmProjects\\brocade\\SN6000B-SW1-SANA-S0cp-201805311510.SSHOW_AG.txt.gz','rb')
"""temp = gzip.open('C:\\Users\\ia.kudryashov\\PycharmProjects\\brocade\\SN6000B-SW1-SANA-S0cp-201805311510.SSHOW_AG.txt.gz','r')
print(temp)

temp1 = temp.read().splitlines()
print(temp1)
#for line in f:
 #   line = line.strip('\r\n')
 #   print(line)"""

#with gzip.open('C:\\Users\\ia.kudryashov\\PycharmProjects\\brocade\\SN6000B-SW1-SANA-S0cp-201805311510.SSHOW_AG.txt.gz', 'rb') as f:




f=gzip.open('C:\\Users\\ia.kudryashov\\PycharmProjects\\brocade\\SN6000B-SW1-SANA-S0cp-201805311510.SSHOW_AG.txt.gz', 'rt')
print(f.read())



