@echo off

echo Running NASM...
nasm -f win32 %1.asm
echo Assembly complete.

echo Running Microsoft Linker...
link /SUBSYSTEM:%2 /ENTRY:start %1.obj *.lib
echo Linking complete.

@echo on
