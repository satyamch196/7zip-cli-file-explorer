def change_current_dir(cmd):
	if len(cmd)==1:
		return root
	elif cmd[1]=="-":
		return old_wrk_dir
	else:
		dir=" ".join(cmd[1:])
	global old_wrk_dir,PWD,empty_dir
	empty_dir=0
	def check_for_empty_dir():
		try:
			global empty_dir
			dir_not_in_dict=PWD[len(root):len(PWD)-1]
			prv_dir_in_dict=old_wrk_dir[len(root):len(old_wrk_dir)-1]
			if prv_dir_in_dict=="":
				return
			dirs_in_prv_dir=[]
			for dir_index in range(len(dict[prv_dir_in_dict])):
				if len(dict[prv_dir_in_dict][dir_index][1])==2:
					dirs_in_prv_dir.append(prv_dir_in_dict+"/"+dict[prv_dir_in_dict][dir_index][0])
			if (dir_not_in_dict not in dict.keys()) and (dir_not_in_dict in dirs_in_prv_dir):
				empty_dir=1
		except KeyError:
			return
	def double_dot_handling():
		if PWD==root:
			return PWD
		path_list=PWD.split("/")
		pwd=""
		for item in range(len(path_list)-2):
			pwd=pwd+path_list[item]+"/"
		return pwd
	def triple_dot_handling():
		path_list=PWD.split("/")
		if len(path_list)<3:
			return pwd
		pwd=""
		for item in range(len(path_list)-3):
			pwd=pwd+path_list[item]+"/"
		return pwd
	dirs_list=dir.split("/")
	for dirs in dirs_list:
		if dir[0] in ["~","/"]:
			PWD=root
		elif dirs=="..":
			PWD=double_dot_handling()
		elif dirs==".":
			return PWD
		elif dirs=="...":
			PWD=triple_dot_handling()
		elif "*" in dir:
			print(red+"Wildcards aren't supported !"+reset)
			return old_wrk_dir
		else:
			PWD=PWD+dir
	if PWD[-1]!="/":
		PWD=PWD+"/"
	PWD = re.sub(r'/+', '/', PWD)
	check_for_empty_dir()
	if (empty_dir==1) or (PWD[len(root):len(PWD)-1] in dict.keys()) or (PWD==root):
		return PWD
	else:
		print(red+"cd : Directory",dir,"does not exists !"+reset)
		return old_wrk_dir
