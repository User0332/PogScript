section .bss
	opt.baz resb 4
	opt.bar resb 4
	opt.foo resb 4
section .text
	global _opt_init.1

_opt_init.1:
	mov eax, 1368
	mov [opt.foo], eax
	mov eax, 84
	mov ebx, eax
	mov eax, [opt.foo]
	add ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 35
	sub ebx, eax
	mov eax, ebx
	mov [opt.bar], eax
	mov eax, [opt.foo]
	mov ebx, eax
	mov eax, [opt.bar]
	add ebx, eax
	mov eax, ebx
	mov ebx, eax
	mov eax, 2
	imul ebx, eax
	mov eax, ebx
	mov [opt.baz], eax