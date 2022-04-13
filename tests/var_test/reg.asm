section .bss
	__NOACCESS.mainmem.1 resb 12

section .text
	global _start

_start:
	mov eax, 342
	mov ebx, eax
	mov eax, 4
	imul ebx, eax
	mov eax, ebx
	mov [__NOACCESS.mainmem.1+0], eax
	mov eax, 84
	mov ebx, eax
	mov eax, [__NOACCESS.mainmem.1+0]
	add ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 7
	mov ebx, eax
	mov eax, 5
	imul ebx, eax
	mov eax, ebx
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