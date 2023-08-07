import sys
import math
import re

residues = {}
def parse(line):
	aname = line[12:16]
	res   = line[17:29]
	x     = line[31:38]
	y     = line[39:46]
	z     = line[47:54]

	return (aname, res, x, y, z )


def dist(r1, r2):
	x  = float(r1[2]) - float(r2[2])
	y  = float(r1[3]) - float(r2[3])
	z  = float(r1[4]) - float(r2[4])

	d = math.sqrt(x**2 + y**2 + z**2 )
	return d

	

def create_residues(fname):
	with open(fname, 'r') as file:
		for line in file:
			aname, res, x, y, z = parse(line)
			d = (aname, res, x, y, z, line.strip() ) 
			if res not in residues:
				new= [ d, ]
				residues[res] =  new
			else:
				residues[res].append(d)
	
def rename_hydrogens(fname):
	create_residues(fname)
	for item in residues:
		vals = residues[item]
		sublist = []
		cmap = {}
		for i, atom1 in enumerate(vals):
			line = atom1[5]
			for j in range(i+1, len(vals)):
				atom2 = vals[j]
				d = dist(atom1, atom2)
				test = abs(d-1.0)
				if test < 0.10 and (not atom1[0].strip().startswith('H') and 
					atom2[0].strip().startswith('H')):
	
					assert atom1[1] == atom2[1]
					newname = 'H'
					bb = atom1[0].strip()
					resname = atom1[1][0:3]
	
					if len(bb) > 1:
						suffix = bb[1:].strip()
						if suffix not in cmap:
							if suffix == 'A':
								if resname in 'GLY':
									cmap[suffix] = 2
								else:	
									cmap[suffix] = ''
	
							elif suffix == 'B':
								if resname in 'ILE THR VAL':
									cmap[suffix] = ''
								elif resname in 'ALA PHE LEU':
									cmap[suffix] = 1
								else:
									cmap[suffix] = 2
							elif suffix == 'D':
								if resname in 'HID HIS HIP PHE TYR TRP':
									cmap[suffix] = 1
								else:
									cmap[suffix] = 2;
	
							elif suffix == 'E':
								if resname in 'HID HIS HIP MET PHE TRP TYR':
									cmap[suffix] = 1
								elif resname in 'ARG':
									cmap[suffix] = '' 
								else:
									cmap[suffix] = 2
							elif suffix == 'G':
								if resname in 'SER':
									cmap[suffix] = ''
								elif resname in 'ILE THR VAL':
									cmap[suffix] = 1
								elif resname in 'LEU':
									cmap[suffix] = ''
								else:
									cmap[suffix] = 2
							elif suffix == 'G2':
								if resname in 'CYX LEU SER':
									cmap[suffix] = ''
								elif resname in 'PRO LYS MET ARG GLN GLU':
									cmap[suffix] = 2
								else:
									cmap[suffix] = 1
							elif suffix == 'Z':
								if resname in 'LYS':
									cmap[suffix] = 1
								elif resname in 'PHE':
									cmap[suffix] = ''
								else:
									cmap[suffix] = 2
	
							elif suffix == 'G1':
								if resname in 'THR':
									cmap[suffix] = ''
								elif resname in 'VAL':
									cmap[suffix] = 1
								else:
									cmap[suffix] = 2
	
							elif suffix == 'D1':
								if resname in 'ILE LEU':
									cmap[suffix] = 1
								elif resname in 'TYR PHE':
									suffix = 'D'
									if suffix in cmap:
										cmap[suffix] = 2
									else:
										cmap[suffix] = 1
								elif resname in 'TRP':
									cmap[suffix] = ''
								else:
									cmap[suffix] = 2
	
							elif suffix == 'D2':
								if resname in 'TYR HID HIS HIP HIE PHE':
									suffix = 'D'
									cmap[suffix] = 2
								else:
									cmap[suffix] = 1
	
							elif suffix == 'E1':
								if resname in 'TYR HIS HIP HIE PHE':
									suffix = 'E'
									cmap[suffix] = 1
								elif resname in 'TRP':
									cmap[suffix] = ''
								else:
									cmap[suffix] = 1
								
								
							elif suffix == 'E2':
								if resname in 'TYR PHE TRP':
									suffix = 'E'
									cmap[suffix] = 2
								elif resname in 'HIS HIP HIE HID':
									suffix = 'E'
									cmap[suffix] = 1
								else:
									cmap[suffix] = 1
	
							elif suffix == 'H':
								cmap[suffix] = ''
	
							elif suffix == 'H2':
								if resname in 'ARG':
									cmap[suffix] = 1
								else:
									cmap[suffix] = ''
	
							elif suffix == 'Z3':
								cmap[suffix] = ''
	
							elif suffix == 'Z2':
								cmap[suffix] = ''
	
							elif suffix == 'E3':
								cmap[suffix] = ''
							else:
								cmap[suffix] = 1
							
	
						else:
							if cmap[suffix] == '':
								cmap[suffix] = 1
							else:
								cmap[suffix] += 1
	
						newname = 'H' + suffix + str(cmap[suffix])
						#if suffix == 'H1':  print(suffix, cmap[suffix], atom2[0], newname )
							
					#if atom1[0].strip() == 'N' : newname = 'H  '
					sublist.append( (atom2[0].strip(), newname ) )
					#print(atom1[1], atom1[0], atom2[0], newname)
	
			for xx in sublist:
				orig, new = xx
				if orig in line:
					rep = new.strip()
					# make the column look "standard"
					if len(rep) < 4:
						fix = ' %-3s ' % (rep)
					else:
						fix = '%-4s ' % (rep)
						
					line = line[:12] + fix + line[17:]
					break
	
			print(line)


if __name__ == "__main__":
	fname = sys.argv[1]
	rename_hydrogens(fname) 
