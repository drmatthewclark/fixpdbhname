import sys
#
# verify that pdb file atom names match those in the amber parameter files
amber='amber03.dat'
amberdata=[]

pdb=sys.argv[1]

with open(amber, 'r') as a:
	for line in a:
		
		dat = line.split('\t')
		if len(dat) > 1:
			amberdata.append([dat[0].strip(), dat[2].strip()])


with open(pdb, 'r') as p:
	for i, line in enumerate(p):
		matched = False
		res = line[17:21].strip()
		name = line[12:17].strip()
		for r in amberdata:
			if res == r[0] and name == r[1]:
				matched = True
				continue
		if not matched:
			print("not matched", name, res, 'line', i)
