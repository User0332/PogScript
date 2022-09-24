section .bss
	reg.baz resb 4
	reg.bar resb 4
	reg.foo resb 4
section .text
	global _reg_init.1

_reg_init.1:
	mov eax, 342
	mov ebx, eax
	mov eax, 4
	imul ebx, eax
	mov eax, ebx
	mov [reg.foo], eax
	mov eax, 84
	mov ebx, eax
	mov eax, [reg.foo]
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
	mov [reg.bar], eax
	mov eax, [reg.foo]
	mov ebx, eax
	mov eax, [reg.bar]
	add ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 2
	imul ebx, eax
	mov eax, ebx
	mov [reg.baz], eax