@echo off

nasm -f win32 %1.asm
link /SUBSYSTEM:WINDOWS /ENTRY:start %1.obj

@echo on