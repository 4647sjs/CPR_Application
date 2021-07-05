import sqlite3

f = open("/workspace/CPR_re/data_input/AED_info.txt", 'r')
data = f.read()
f_con = data.split('b')
s_con = []
for i in f_con:
    s_con.append(i.split('a'))
f.close()

print(s_con)


f_con