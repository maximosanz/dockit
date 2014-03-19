def extract_interactions(writecon_filepath,one_pdb):
	#finds 5A and 10A interacting residues from the writecon files, and creates command to draw 5A contact lines
	#load interactions from interaction file
	#one_pdb says whether input file is input as one pdb (4.1 --> 3.1) or two - it is boolean
	in_file = open(writecon_filepath)
	lines = in_file.readlines()
	lines = lines[4:]

	ref_rec_5A_contacts = []
	ref_lig_5A_contacts = []
	ref_rec_5A_int_residues = []
	ref_lig_5A_int_residues = []
	ref_rec_10A_int_residues = []
	ref_lig_10A_int_residues = []

	inp_rec_5A_contacts = []
	inp_lig_5A_contacts = []
	inp_rec_5A_int_residues = []
	inp_lig_5A_int_residues = []
	inp_rec_10A_int_residues = []
	inp_lig_10A_int_residues = []

	#finds reference 5A contacts
	for line in lines:
		if (line=="\n"):
			break
		#add residue to list of residues that appear in at least one 5A interaction
		ref_rec_5A_int_residues.append(line[0:4].strip()+':'+line[6]+'/1.1')
		ref_lig_5A_int_residues.append(line[14:18].strip()+':'+line[20]+'/2.1')
		#add particular 5A contact to list of contacts
		ref_rec_5A_contacts.append(line[0:4].strip()+':'+line[6]+'.CA/1.1')
		ref_lig_5A_contacts.append(line[14:18].strip()+':'+line[20]+'.CA/2.1')

	#slice reference contacts off lines
	lines = lines[len(ref_rec_5A_contacts)+4:]

	#finds input 5A contacts
	for line in lines:
		if (line=="\n"):
			break
		#add residue to list of residues that appear in at least one 5A interaction
		inp_rec_5A_int_residues.append(line[0:4].strip()+':'+line[6]+'/3.1')
		inp_lig_5A_int_residues.append(line[14:18].strip()+':'+line[20]+'/4.1')
		#account for the fact that the model may be one pdb by changing the 4.1 --> 3.1
		if (one_pdb==True):
			inp_lig_5A_int_residues[len(inp_lig_5A_int_residues)-1]=inp_lig_5A_int_residues[len(inp_lig_5A_int_residues)-1][:-3]+"3.1"
		#add particular 5A contact to list of contacts
		inp_rec_5A_contacts.append(line[0:4].strip()+':'+line[6]+'.CA/3.1')
		inp_lig_5A_contacts.append(line[14:18].strip()+':'+line[20]+'.CA/4.1')
		#account for the fact that the model may be one pdb by changing the 4.1 --> 3.1
		if (one_pdb==True):
			inp_lig_5A_contacts[len(inp_lig_5A_contacts)-1]=inp_lig_5A_contacts[len(inp_lig_5A_contacts)-1][:-3]+"3.1"

	for line in lines:
		if (line[0:6]=="INT10A"):
			#add reference residue to list of residues that appear in at least one 10A interaction
			ref_rec_10A_int_residues.append(line[7:11].strip()+':'+line[13]+'/1.1')
			ref_lig_10A_int_residues.append(line[21:25].strip()+':'+line[27]+'/2.1')
			#do similar for input complex but only if the NoEquivRes flag is absent
			if (line[37:47]!="NoEquivRes"):
				inp_rec_10A_int_residues.append(line[37:41].strip()+':'+line[43]+'/3.1')
			if (line[51:61]!="NoEquivRes"):
				inp_lig_10A_int_residues.append(line[51:55].strip()+':'+line[57]+'/4.1')
				#account for the fact that the model may be one pdb by changing the 4.1 --> 3.1
				if (one_pdb==True):
					inp_lig_10A_int_residues[len(inp_lig_10A_int_residues)-1]=inp_lig_10A_int_residues[len(inp_lig_10A_int_residues)-1][:-3]+"3.1"

	#remove duplicates from residue lists
	ref_rec_5A_int_residues = list(set(ref_rec_5A_int_residues))
	ref_lig_5A_int_residues = list(set(ref_lig_5A_int_residues))
	ref_rec_10A_int_residues = list(set(ref_rec_10A_int_residues))
	ref_lig_10A_int_residues = list(set(ref_lig_10A_int_residues))
	inp_rec_5A_int_residues = list(set(inp_rec_5A_int_residues))
	inp_lig_5A_int_residues = list(set(inp_lig_5A_int_residues))
	inp_rec_10A_int_residues = list(set(inp_rec_10A_int_residues))
	inp_lig_10A_int_residues = list(set(inp_lig_10A_int_residues))

	#construct commands to draw 5A contacts
	ref_draw_5A_contacts = ""
	for i in range(len(ref_rec_5A_contacts)):
		ref_draw_5A_contacts += "draw arrow"+str(i)+"r arrow ("+ref_rec_5A_contacts[i]+") ("+ref_lig_5A_contacts[i]+"); color $arrow"+str(i)+"r TRANSLUCENT 0.5;"

	inp_draw_5A_contacts = ""
	for i in range(len(inp_rec_5A_contacts)):
		inp_draw_5A_contacts += "draw arrow"+str(i)+"m arrow ("+inp_rec_5A_contacts[i]+") ("+inp_lig_5A_contacts[i]+"); color $arrow"+str(i)+"m TRANSLUCENT 0.5 purple;"

	#construct list of 5A interface residues for reference
	ref_int_5A_residues = ""
	for res in ref_rec_5A_int_residues:
		ref_int_5A_residues += res+" or "

	for res in ref_lig_5A_int_residues:
		ref_int_5A_residues += res+" or "

	ref_int_5A_residues = ref_int_5A_residues[:-4]

	#construct list of 5A interface residues for input
	inp_int_5A_residues = ""
	for res in inp_rec_5A_int_residues:
		inp_int_5A_residues += res+" or "

	for res in inp_lig_5A_int_residues:
		inp_int_5A_residues += res+" or "

	inp_int_5A_residues = inp_int_5A_residues[:-4]

	#construct list of 10A interface residues for reference
	ref_int_10A_residues = ""
	for res in ref_rec_10A_int_residues:
		ref_int_10A_residues += res+" or "

	for res in ref_lig_10A_int_residues:
		ref_int_10A_residues += res+" or "

	ref_int_10A_residues = ref_int_10A_residues[:-4]

	#construct list of 10A interface residues for input
	inp_int_10A_residues = ""
	for res in inp_rec_10A_int_residues:
		inp_int_10A_residues += res+" or "

	for res in inp_lig_10A_int_residues:
		inp_int_10A_residues += res+" or "

	inp_int_10A_residues = inp_int_10A_residues[:-4]

	in_file.close()
	return {'ref_draw_5A_contacts':ref_draw_5A_contacts,'ref_int_5A_residues':ref_int_5A_residues,'ref_int_10A_residues':ref_int_10A_residues,'inp_draw_5A_contacts':inp_draw_5A_contacts,'inp_int_5A_residues':inp_int_5A_residues,'inp_int_10A_residues':inp_int_10A_residues}
