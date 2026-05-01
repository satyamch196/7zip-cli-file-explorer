import sys
def size_format(num):
    if num[0] not in "0123456789":
        return "NULL"
    num=int(num)
    def approximate(string):
#        return string
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
#fh=open("/storage/6BFF-EB00/ses-packs.txt")
#fl=fh.readlines()
fl=sys.stdin.readlines()
#print(fl)
print("SIZE","COMPRESSED","NAME",sep="\t")
"""sum=0
for item in fl:
	sum+=int(item.split()[3])
#	print(item.split()[-1])

print(size_format(str(sum)))
"""
l=[]
for index in range(len(fl)):
	line=fl[index].split()
#	if int(line[3])<(100*1024*1024):
#		continue
	l.append(int(line[3]))
l.sort(reverse=True)
#print(l)
subtotal=0
for i in l:
	for index in range(len(fl)):
		line=fl[index].split()
		if str(i) == line[3]: # and i>(100*1024*1024):
			subtotal+=i
			print(size_format(line[3]),size_format(line[4]),"\t"+line[-1],sep="\t")
#			print(line[-1])
			break
#		elif i<(100*1024*1024*1024):
#			break
#print(subtotal)
print("Sub Total :",size_format(str(subtotal)))
grandtotal=0
for item in fl:
	grandtotal+=int(item.split()[3])
#	print(item.split()[-1])

#print(size_format(str(grandtotal)))
print("Grand Total :",size_format(str(grandtotal)))
#	print(index)
'''	if index in range(2,10): #index>4 or index<11: #c>2:
		for char in range(len(fl[index])):
			if fl[index][char]=="/":
				print("Github"+fl[index][char+18:-1],fl[index][:5])
				break
	if c>4 or c<11:
		pass
	elif index[1]=="#":
		break
'''
#fh.close()
