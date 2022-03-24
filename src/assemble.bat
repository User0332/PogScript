@echo off

nasm -f win32 *.asm
link /SUBSYSTEM:WINDOWS /ENTRY:start *.obj *.lib

@echo on