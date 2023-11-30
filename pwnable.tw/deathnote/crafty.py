# int 0x80 -> \xcd\x80
for i in range(48, 122):
	for j in range(48, 122):
		if(i^j == 0xcd):
			print(i,j)

for i in range(48, 122):
	for j in range(48, 122):
		if(i^j == 0x80):
			print(i,j)
