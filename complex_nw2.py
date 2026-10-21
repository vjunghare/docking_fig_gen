import pymol
from pymol import cmd, stored

import glob

files=glob.glob('*.pdb')

#files =['FTU-WT-cefotaxime.pdb', 'FTU_wt-cefaperazone.pdb', 'FTU_wt-ampicillin.pdb', 'FTU_wt-cephalothin.pdb', 'FTU_wt-piperacillin.pdb', 'FTU-WT-carbenicillin.pdb']
aln_obj = cmd.get_unused_name('_aln')
print files
base=files[0].strip()
cmd.load(base, 'base')
modelName1='base'
atmsel_base=[ ]
res_no=[]
for complex_pdbs in files:
	table_f_t=complex_pdbs.split('.')
	table_f='mod_'+table_f_t[0]+ '.csv'
	f_1= open(table_f,"r")
	res_data=[]
	with f_1 as ine:
		ine = [lin.rstrip('\n') for lin in ine]
		for lin in ine:
			lin = lin.rstrip(' ')
			res_data.append(lin)
	for rd in res_data:
		flag_kt=0
		rd_v=rd.split()
		#print rd_v
		if len(res_no)>1:
			for kt in res_no:
				if (kt==rd_v[7]):
					flag_kt=1
		if (flag_kt==0):
			res_no.append(rd_v[7])
			#print res_no
	res_no.append(res_data[0].split()[1])
print res_no
atmsel2_1_1=[ ]
for complex_files in files:
	base_no=0
	print complex_files
	if (complex_files==files[0]):
		base_no=1
	print base_no
	table_file_t=complex_files.split('.')
	table_file='mod_' + table_file_t[0]+ '.csv'
	print table_file
	file_1= open(table_file,"r")
	data_lig=[]
	with file_1 as ins:
		ins = [line.rstrip('\n') for line in ins]
		for line in ins:
			line = line.rstrip(' ')
			data_lig.append(line)
	variable=complex_files.strip()
	cmd.load(variable, 'variable')
	modelName2='variable'
	cmd.bg_color('white')
	atmsel1=[ ]
	atmsel2=[ ]
	atmsel2_1=[ ]
	
	atmsel_mc= [ ]
	if(base_no==1):
		for i_res_no in res_no:
			atmsel2_1_1.append('(%s and resi %s)'%(modelName1, i_res_no))
	for i in data_lig:		
		b=[]
		b=i.split()
		#print b
		atmsel1.append('(%s and resn %s and resi %s and chain A and name %s)'%(modelName2,b[0], b[1], b[2] ))
		atmsel2.append('(%s and resn %s and resi %s and chain A and name %s)'%(modelName2, b[6], b[7], b[8]))
		atmsel2_1.append('(%s and resn %s and resi %s)'%(modelName2, b[6], b[7]))
		
		if(base_no==1):
			#atmsel2_1_1.append('(%s and resi %s)'%(modelName1, b[6], b[7]))
			atmsel_base.append('(%s and resn %s and resi %s)'%(modelName1, b[6], b[7]))
		if(b[8]=='O' or b[8]=='N'):
			atmsel_mc.append('(%s and resn %s and resi %s)'%(modelName2, b[6], b[7]))            
	t_n=0

	print atmsel1
	print '\n'
	print atmsel2
	#print len(data_lig)
	cmd.deselect()
	names=cmd.get_names('objects')
	#print "%s"%names
	cmd.show_as('cartoon','%s'%modelName2)
	#cmd.set_color("ty", "cyan")
	cmd.color('cyan', '%s'%modelName2)
	if (len(atmsel_mc) != 0):
		cmd.select('atms_mc', ' '.join('%s' % u1 for u1 in atmsel_mc))
	#cmd.select('atms2', ' '.join('%s' % u2 for u2 in atmsel2))
	#print atmsel_base
	cmd.select('atms_base', ' '.join('%s' % u2 for u2 in atmsel_base))
	cmd.select('atms2_1', ' '.join('%s' % u2 for u2 in atmsel2_1))
	cmd.select('atms2_1_1', ' '.join('%s' % u2 for u2 in atmsel2_1_1))
	#cmd.hide('cartoon','atms2_1 and %s'%modelName)
	cmd.show('sticks','atms2_1 and %s'%modelName2)
	cmd.set("stick_radius",0.2,'atms2_1' )
	#cmd.set("stick_radius", 0.008,'atms2_1')
	cmd.show_as('sticks','%s and HETATM'%modelName2)
	cmd.set("stick_radius",0.25,'%s and HETATM'%modelName2)
	cmd.show("sphere",'%s and HETATM'%modelName2)
	cmd.set("sphere_scale",0.25)
	cmd.spectrum('count','magenta_cyan','%s and HETATM'%modelName2)
	cmd.remove('hydrogen and %s'%modelName2)
	cmd.util.cbao(selection='%s and HETATM'%modelName2)
	cmd.util.cbap(selection='%s and atms2_1'%modelName2)
	cmd.label("name CA and atms2_1", "resn + resi")
	cmd.align(modelName2,modelName1,object=aln_obj)
	while t_n< (len(data_lig)):
		#print t_n
		cmd.select('atms12', atmsel1[t_n])
		cmd.select('atms22', atmsel2[t_n])
		cmd.distance('pairs', 'atms12','atms22')
		#cmd.set('label_size',9)
		cmd.set ('label_font_id', 10)
		cmd.set ('dash_color', 'ruby')
		cmd.set("label_color","black")
		cmd.set ("label_size", 12)
		cmd.set("label_position",(1.5,0,8))
		#cmd.delete("atms12")
		#cmd.delete("atms22")
		t_n=t_n+1
	cmd.set('cartoon_transparency',0.4)
	#cmd.orient("%s and "%modelName2)
	#cmd.zoom(("%s"%modelName2), 10)
	#cmd.orient("%s and HETATM"%modelName1)
	#cmd.orient("%s"%modelName1)
	#cmd.center("%s and atms_base"%modelName1)
	#cmd.align(modelName2,modelName1,object=aln_obj)
	png_name =complex_files[:-4] + '.png'
	cmd.orient("%s and atms2_1_1"%modelName1)
	cmd.hide('everything',"base")
	cmd.delete("%s"%aln_obj)
	#cmd.center("%s"%modelName2)
	cmd.set('cartoon_side_chain_helper',1)
	if (len(atmsel_mc) != 0):
		cmd.set('cartoon_side_chain_helper', 0,'atms_mc')
	cmd.hide('label','all')
	cmd.ray(2560,1440)
	cmd.png(("%s")%png_name)
	pse_name=complex_files[:-4] + '.pse'
	cmd.save(pse_name)
	cmd.delete("%s"%modelName2)
	cmd.delete("pairs")
	cmd.delete("atms12")
	cmd.delete("atms22")
	cmd.delete("variable")
	#cmd.delete("center")
	#cmd.show('lines','%s'%modelName1)
print "DONE !"
