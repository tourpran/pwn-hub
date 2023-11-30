op = [0x14, 0x00, 0x01, 0x0F, 0x04, 0x15, 0x0F, 0x0E, 0x53, 0x14, 0x01, 0x14, 0x02, 0x14, 0x03, 0x14, 0x04, 0x01, 0x08, 0x13, 0x01, 0x09, 0x37, 0x01, 0x0A, 0x01, 0x01, 0x0B, 0xF0, 0x01, 0x0C, 0x0F, 0x01, 0x0D, 0x90, 0x01, 0x07, 0xAD, 0x15, 0x27, 0x0E, 0x2C, 0x03, 0xEA, 0x07, 0x19, 0x01, 0x07, 0xE9, 0x15, 0x17, 0x0E, 0x37, 0x03, 0xEA, 0x07, 0x48, 0x07, 0x49, 0x01, 0x07, 0xCB, 0x15, 0x47, 0x0E, 0x44, 0x03, 0xEA, 0x07, 0x3D, 0x07, 0x3C, 0x07, 0x39, 0x01, 0x07, 0x16, 0x15, 0x37, 0x0E, 0x53, 0x03, 0xEA, 0x16, 0x0E]

pc = 0 # Program counter
flag1 = flag2 = flag3 = 0 # flags
d_word = 0 # a 4 byte thingy

reg = [] # Registers assuming length 15
our_input = [] #our input 4 bytes ?

def shr(arg):
    return arg>>4

def and_15(arg):
    return arg&15

main_op = []

while(pc < 85):
    ins = op[pc]
    arg0 = op[pc + 1]
    main_op.append(ins)
    rs_arg0 = shr(arg0)
    and_arg0 = and_15(arg0)
    
    if(ins == 1):
        print(f"reg[{arg0}] = {op[pc+2]}")
        pc += 1

    elif(ins == 2):
        print(f"reg[{rs_arg0}] = reg[{and_arg0}]")
    elif(ins == 3):
        print(f"reg[{rs_arg0}] += reg[{and_arg0}]")
    elif(ins == 4):
        print(f"reg[{rs_arg0}] -= reg[{and_arg0}]")
    elif(ins == 5):
        print(f"reg[{rs_arg0}] *= reg[{and_arg0}]")
    elif(ins == 6):
        print(f"reg[{rs_arg0}] /= reg[{and_arg0}]")
    elif(ins == 7):
        print(f"reg[{rs_arg0}] ^= reg[{and_arg0}]")
    elif(ins == 8):
        print(f"reg[{rs_arg0}] |= reg[{and_arg0}]")
    elif(ins == 9):
        print(f"reg[{rs_arg0}] &= reg[{and_arg0}]")
    elif(ins == 10):
        print(f"if reg[{and_arg0}] == 0: reg[{rs_arg0}] = 1")
        print(f"else reg[{rs_arg0}] = 0")
    elif(ins == 11):
        print(f"reg[{rs_arg0}] << reg[{and_arg0}]")
    elif(ins == 12):
        print(f"reg[{rs_arg0}] >> reg[{and_arg0}]")

    elif(ins == 13):
        print(f"if (flag1:{flag1} == 1): ", end="")
        print(f"je {arg0}")
    elif(ins == 14):
        print(f"if (flag1:{flag1} == 0): ", end="")
        print(f"je {arg0}")
    elif(ins == 15):
        print(f"if (flag2:{flag2} == 1):", end="")
        print(f"je {arg0}")
    elif(ins == 16):
        print(f"if (flag2:{flag2} == 0): ", end="")
        print(f"je {arg0}")
    elif(ins == 17):
        print(f"if (flag3:{flag3} == 1): ", end="")
        print(f"je {arg0}")
    elif(ins == 19):
        print(f"our_input[{d_word}] = reg[{arg0}]")
        print(f"inc d_word")
        d_word+=1
    elif(ins == 20):
        print(f"reg[{arg0}] = our_input[{d_word}]")
        print(f"dec d_word")
        d_word-=1
    else:
        if(ins == 18):
            print(f"if (flag3:{flag3}== 0): ", end="")
            print(f"je {arg0}")

    if(ins == 21):
        print(f"reg[15] = reg[16] = reg[17] = 0")
        print(f"flag1 = 1; if reg[{rs_arg0}]==reg[{and_arg0}]")
        print(f"flag3 = 1; if reg[{rs_arg0}]<reg[{and_arg0}]")
        print(f"flag2 = 1; if reg[{rs_arg0}]>reg[{and_arg0}]")

    elif(ins == 22):
        print(f"ret reg[{arg0}]")
    pc += 2

print(main_op)