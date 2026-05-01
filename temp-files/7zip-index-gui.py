def load_file2var():
    file=input('Enter File Address : ')
    file=open(file)
    data=file.readlines()
    file.close()
    print(data)
while True:
    i=int(input())
    t=i-(i*0.7)
    print(t)