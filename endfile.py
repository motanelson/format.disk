print ("\033c\033[40;37m\ngive me the file to append end of file? ")
i=input()
f1=open(i,"ab")
f1.write(b"\000")
f1.close()

