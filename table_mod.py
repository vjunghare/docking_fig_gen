import glob

files=glob.glob('*.pdb')
files.sort()
print files
#files=['6lu7-2qiq.pdb']
res_no=[]
f_2=open("table_all.csv","w+")
for complex_pdbs in files:
	table_f_t=complex_pdbs.split('.')
	table_f=table_f_t[0]+ '.csv'
	f_2.write("%s\n"%table_f_t[0])
	f_2.write("Ligand,Residue_No,Atom_Name,Chain,Atom_No,,Residue_Name,Residue_No,Atom_Name,Chain,Atom_No,,Distance\n")
	int_table='mod_'+table_f_t[0]+ '.csv'
	f_1= open(table_f,"r")
	f=open (int_table, "w+")
	res_data=[]
	with f_1 as ine:
		ine = [lin.rstrip('\n') for lin in ine]
		for lin in ine:
			lin = lin.rstrip(' ')
			res_data.append(lin)
	for i in res_data:
		i_s=i.split(" ")
		flag_2=i_s[2].find("C")
		print i_s[6]
		flag_8=i_s[6].find("C")
		print flag_8
		flag_0=i_s[6].find("CA")
		print flag_0
		if( flag_8==-1 and flag_0==-1 and flag_2==-1):
			f.write("%s\n"%i)
			f_2.write("%s\n"%i)
	f_2.write("\n")
print "DONE !"
