import re
import os
file='/sdcard/7z_list.txt'#Download/Quick Share/neth7z.txt'
def file2infotup(file):
    dirs={}
    def split_info(istr):
        result = re.findall(r'(\s+|\S+)', istr)
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
    for line in fh:
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
            size=fi[3]
            compressed=fi[4]
            name=fi[5]
            ft=(name,date,time,attr,size,compressed)
            dir_files_sep(ft)
    fh.close()
    print(dirs)
    exit()
    return dirs
def structure_gen(dirs):
    file2infotup(file)
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
def file_explorer(dirdict=structure_gen(file2infotup(file))):
    for i in dirdict.keys():
        if '/' not in i:
            for name in dirdict[i]:
                if len(name[1]) == 2:
                    print(f"📁 {name[0]} (Directory) - Created on {name[1][0]} at {name[1][1]}")
                else:
                    print(f"📄 {name[0]} (File) - Created on {name[1][0]} at {name[1][1]}, Size: {name[1][2]}, Compressed: {name[1][3]}")
    while True:
        c=input('Enter the Command : ')
        break
        if c in dirdict.keys():
            break
#file_explorer()
def list_contents(directory_structure, current_path):
    """List the contents of the current directory."""
    #print(list(directory_structure.keys())[0])
    current_dir = directory_structure[current_path]#list(directory_structure.keys())[0]]#get_current_directory(directory_structure, current_path)
    if not current_dir:
        print("Invalid directory.")
        return

    print(f"Contents of '{current_path if current_path else 'root'}':")
    #print(f"Contents of '{'/'.join(current_path) if current_path else 'root'}':")
    for item in current_dir:
        if isinstance(item, tuple) and len(item) == 2:  # Ensure the item is a tuple of (name, metadata)
            name, metadata = item
            if isinstance(metadata, tuple):  # Ensure metadata is a tuple
                if len(metadata) == 2:
                    print(f"📁 {name} (Directory) - Created on {metadata[0]} at {metadata[1]}")
                elif len(metadata) == 4:
                    print(f"📄 {name} (File) - Created on {metadata[0]} at {metadata[1]}, Size1: {metadata[2]}, Size2: {metadata[3]}")
                else:
                    print(f"⚠️ {name} - Unknown metadata format: {metadata}")
            else:
                print(f"⚠️ {name} - Invalid metadata format: {metadata}")
        else:
            print(f"⚠️ Invalid item format: {item}")
def navigate(directory_structure, current_path, target):
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

def run_file_explorer(directory_structure):
    """Run the file explorer CLI."""
    current_path =list(directory_structure.keys())
    while True:
        list_contents(directory_structure, current_path[0])
        #command = input("\nEnter a command (navigate <name>, back, exit): ").strip().split()
        break
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

run_file_explorer(structure_gen(file2infotup(file)))