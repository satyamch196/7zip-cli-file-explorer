from re import findall
file="/home/user/7zip_index.txt"
red="\033[31m"
green="\033[32m"
reset="\033[0m"
def file2infotup(file):
    dirs={}
    def split_info(istr):
        result = findall(r'(\s+|\S+)', istr)
        result=result[0::2]
        return result
    def dir_files_sep(f_tup):
        if f_tup[3]=='D....':
            dirs[f_tup[0]]=f_tup[1:3]
        else:
            dirs[f_tup[0]]=f_tup[1:3]+f_tup[4:]
    fh=open(file,mode='r',newline='',encoding='ascii')
    found=0
    _c=0
    global root
    root=""
    for line in fh:
        if line[:4]=="Path":
            archive=line[8:].lstrip("/").split("/")
            for item in range(-1,-(len(archive)+1),-1):
                if archive[item] not in [" ",""]:
                    root=archive[item]
                    break
            root=root.rstrip("\n").rstrip(" ")+"/"
        if line[:8]=='-'*8:
            found=1
            _c+=1
            if _c==2:
                found=0
        elif found==1:
            fi=line.strip('\n')
            fi=split_info(fi)
            date=fi[0]
            time=fi[1]
            attr=fi[2]
            size=int(fi[3])
            compressed=int(fi[4])
            name=fi[-1]
            ft=(name,date,time,attr,size,compressed)
            dir_files_sep(ft)
    fh.close()
    return dirs
def structure_gen(dirs):
#    file2infotup(file)
    dir_list=list(dirs.keys())
    dirdict = {}
    for dir in dir_list:
        parts = dir.split("/")
        if len(parts) > 1:
            pd = ("/".join(parts[:-1]))
            if pd not in dirdict:
                dirdict[pd] = []
            dirdict[pd].append((parts[-1],dirs[dir]))
    return dirdict
def size_format(num):
    def approximate(string):
        try:
            integer_part, decimal_part = string.split('.')
        except ValueError:
            return string
        if len(decimal_part) < 3:
            return string
        if int(decimal_part[2]) >= 5:
            decimal_part = str(int(decimal_part[:2]) + 1)
            if len(decimal_part) > 2:
                integer_part = str(int(integer_part) + 1)
                decimal_part = ""
        else:
            decimal_part = decimal_part[:2]
        if decimal_part!='':
            return f"{integer_part}.{decimal_part}"
        else:
            return integer_part
    if num > 1024**5:
        return approximate(str(num / (1024**5))) + ' PB'
    elif num > 1024**4:
        return approximate(str(num / (1024**4))) + ' TB'
    elif num > 1024**3:
        return approximate(str(num / (1024**3))) + ' GB'
    elif num > 1024**2:
        return approximate(str(num / (1024**2))) + ' MB'
    elif num > 1024:
        return approximate(str(num / 1024)) + ' KB'
    else:
        return str(num) + ' B'
def file_explorer(dirdict=structure_gen(file2infotup(file))):
    def list_contents(cdl):
            for name in cdl:
                if len(name[1]) == 2:
                    print(f"📁 {name[0]} (Directory) - Created on {name[1][0]} at {name[1][1]}")
                else:
                    print(f"📄 {name[0]} (File) - Created on {name[1][0]} at {name[1][1]}, Size: {size_format(name[1][2])}, Compressed: {size_format(name[1][3])}")
    while True:
        c=input('Enter the Command : ')
        for item in dirdict.keys():
            if '/' not in dirdict[item]:
                list_contents(dirdict[item])
            else:
                break
#file_explorer()
def list_contents(directory_structure, current_path):
    """List the contents of the current directory."""
    current_dir = directory_structure[current_path]# get_current_directory(directory_structure, current_path)
    if not current_dir:
        print("Invalid directory.")
        return

    print(f"Contents of '{(current_path) if current_path else 'root'}':")
    #print(f"Contents of '{'/'.join(current_path) if current_path else 'root'}':")
    #for item in current_dir:
    for item in range(len(current_dir)):
        it=current_dir[item]
        if isinstance(it, tuple) and len(it) == 2:  # Ensure the item is a tuple of (name, metadata)
            name, metadata = it
            if isinstance(metadata, tuple):  # Ensure metadata is a tuple
                if len(metadata) == 2:
                    print(f"📁 {name} (Directory) - Created on {metadata[0]} at {metadata[1]}")
                elif len(metadata) == 4:
                    print(f"📄 {name} (File) - Created on {metadata[0]} at {metadata[1]}, Size: {size_format(metadata[2])}, Compressed: {size_format(metadata[3])}")
                else:
                    print(f"⚠️ {name} - Unknown metadata format: {metadata}")
            else:
                print(f"⚠️ {name} - Invalid metadata format: {metadata}")
        else:
            print(f"⚠️ Invalid item format: {item}")
'''def navigate(directory_structure, current_path, target):
    """Navigate to a subdirectory or file."""
    current_dir = get_current_directory(directory_structure, current_path)
    if not current_dir:
        print("Invalid directory.")
        return current_path

    for item in current_dir:
        if isinstance(item, tuple) and len(item) == 2:  # Ensure the item is a tuple of (name, metadata)
            name, metadata = item
            if name == target:
                if isinstance(metadata, tuple) and len(metadata) == 2:  # Directory
                    current_path.append(target)
                    print(f"Navigated to '{'/'.join(current_path)}'")
                else:
                    print(f"'{target}' is a file. Cannot navigate into a file.")
                return current_path

    print(f"'{target}' not found in the current directory.")
    return current_path

def go_back(current_path):
    """Navigate back to the parent directory."""
    if current_path:
        current_path.pop()
        print(f"Navigated back to '{'/'.join(current_path) if current_path else 'root'}'")
    else:
        print("Already at the root directory.")
    return current_path

def get_current_directory(directory_structure, current_path):
    """Get the current directory based on the current path."""
    current_dir = directory_structure
    for part in current_path:
        found = False
        for item in current_dir:
            if isinstance(item, tuple) and len(item) == 2:  # Ensure the item is a tuple of (name, metadata)
                name, metadata = item
                if name == part:
                    current_dir = directory_structure.get('/'.join(current_path + [part]), [])
                    found = True
                    break
        if not found:
            return None
    return current_dir
'''
def run_file_explorer(directory_structure):
    """Run the file explorer CLI."""
    current_path = list(directory_structure.keys())
    while True:
        #print(current_path[0])
        list_contents(directory_structure, current_path[0])
        break
        command = input("\nEnter a command (navigate <name>, back, exit): ").strip().split()
        if not command:
            continue

        if command[0] == "navigate" and len(command) > 1:
            current_path = navigate(directory_structure, current_path, command[1])
        elif command[0] == "back":
            current_path = go_back(current_path)
        elif command[0] == "exit":
            print("Exiting the file explorer.")
            break
        else:
            print("Invalid command. Use 'navigate <name>', 'back', or 'exit'.")

#(run_file_explorer(structure_gen(file2infotup(file))))
dict=structure_gen(file2infotup(file))
"""for key in dict.keys():
	print(red,key,reset," = ",green,dict[key],reset)"""
def change_current_dir(dir):
	global cur_path
	if dir=="..":
		if cur_path==root:
			return root
		path_list=cur_path.split("/")
		cur_path=""
		for item in range(len(path_list)-2):
			cur_path=cur_path+path_list[item]+"/"
	elif dir==".":
		cur_path=cur_path
	elif dir not in ["..","."]:
		cur_path=cur_path+dir+"/"
	return cur_path
def file_explorer():
	global cur_path
	cur_path=root
	while True:
		print("╭─ \033[44m"+cur_path+reset)
		print("╰─ ",end="")
		cmd=input().split()
		clear_cmd=[]
		for item in cmd:
			if item != " ":
				clear_cmd.append(item)
		cmd=clear_cmd
		if cmd[0]=="cd":
			if len(cmd)==2:
				cur_path=change_current_dir(cmd[1])
			elif len(cmd)==1:
				cur_path=root
		elif cmd[0] in ["ls","pwd","find"]:
			pass
		elif cmd[0] in ["exit","quit"]:
			print(green+"Exiting..."+reset)
			break
		else:
			print("Help Message")
file_explorer()
