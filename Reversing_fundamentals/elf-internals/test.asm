; tiny.asm
  
BITS 32

    org     0x00010000

    db      0x7F, "ELF"             ; e_ident
    dd      1                                       ; p_type
    dd      0                                       ; p_offset
    dd      $$                                      ; p_vaddr 
    dw      2                       ; e_type        ; p_paddr
    dw      3                       ; e_machine
    dd      _start                  ; e_version     ; p_filesz
    dd      _start                  ; e_entry       ; p_memsz
    dd      4                       ; e_phoff       ; p_flags
_start:
    mov al, 0x0b ; 
    call lol     ; 
    db      0
    dw      0x34                    ; e_ehsize
    dw      0x20                    ; e_phentsize
    dw      1                       ; e_phnum
    dw      0                       ; e_shentsize
    dw      0                       ; e_shnum
    dw      0                       ; e_shstrndx

lol:
    push    0x0068732f
    push    0x6e69622f
    mov ebx, esp 
    int 0x80

filesize      equ     $ - $$