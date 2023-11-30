[BITS 64]
global main

section .text
main: 
	;openat(AT_FDCWD, "/", O_RDONLY)
	mov edx, 0
	lea rsi, [rel s_root]
	mov rdi, -100
	mov eax, 257
	syscall

	;getdents(fd, dirent, 0x1000)
	mov rdi, rax
	mov rsi, rsp
	mov rdx, 0x1000
	mov rax, 78
	syscall

	mov r15, rax

	xor r14, r14
	xor edx, edx
	jmp rec 

rec:
	mov dx, [rsp+r14+16] ; rsp is our dirent
	sub edx, 20
	lea rsi, [rsp+r14+18]
	mov edi, 1
	mov eax, 1
	syscall

	mov edx, 1
	lea rsi, [rel s_newline]
	mov edi, 1
	mov eax, 1
	syscall

	mov dx, [rsp+r14+16]
	add r14d, edx
	cmp r14, r15
	jl rec

	xor edi, edi
	mov eax, 60
	syscall

section .data
	s_root: db "/home/ctf",0
	s_newline: db 0x0a