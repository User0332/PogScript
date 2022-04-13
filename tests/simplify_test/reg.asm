section .bss
	__NOACCESS.mainmem.1 resb 12

section .text
	global _start

_start:
	mov eax, 4
	mov ebx, eax
	mov eax, 234
	imul ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 3
	imul ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 234
	add ebx, eax
	mov eax, ebx
	mov [__NOACCESS.mainmem.1+0], eax
	mov eax, 23
	mov ebx, eax
	mov eax, 3
	imul ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 234
	mov ebx, eax
	mov eax, 234
	add ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 34
	imul ebx, eax
	mov eax, ebx
	add ebx, eax
	mov eax, ebx
	mov [__NOACCESS.mainmem.1+4], eax
	mov eax, 32
	mov ebx, eax
	mov eax, 324
	imul ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 34
	imul ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 32
	mov ebx, eax
	mov eax, 4
	imul ebx, eax
	mov eax, ebx
	add ebx, eax
	mov eax, ebx
	mov [__NOACCESS.mainmem.1+8], eax