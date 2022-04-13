section .bss
	__NOACCESS.mainmem.1 resb 12

section .text
	global _start

_start:
	mov eax, 1368
	mov [__NOACCESS.mainmem.1+0], eax
	mov eax, 84
	mov ebx, eax
	mov eax, [__NOACCESS.mainmem.1+0]
	add ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 35
	sub ebx, eax
	mov eax, ebx
	mov [__NOACCESS.mainmem.1+4], eax
	mov eax, [__NOACCESS.mainmem.1+0]
	mov ebx, eax
	mov eax, [__NOACCESS.mainmem.1+4]
	add ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 2
	imul ebx, eax
	mov eax, ebx
	mov [__NOACCESS.mainmem.1+8], eax