section .bss
	__NOACCESS.mainmem.1 resb 12

section .text
	global _start

_start:
	mov eax, 3042
	mov [__NOACCESS.mainmem.1+0], eax
	mov eax, 15981
	mov [__NOACCESS.mainmem.1+4], eax
	mov eax, 352640
	mov [__NOACCESS.mainmem.1+8], eax