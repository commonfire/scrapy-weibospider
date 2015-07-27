filename = './followflag.txt'
oldflag = open(filename).readline() 
f = open(filename,'w')
f.write('1')

print oldflag

