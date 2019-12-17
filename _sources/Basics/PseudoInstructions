.. include:: ../global.rst

Pseudo Instructions
=====================

.. index:: pseudo instruction

Some instructions which the processor does not actually support can be modified by the assembler
to produce instructions that do make sense. Assembly instructions that are not actually supported
by the hardware are referred to as **pseudo instructions**. 

A typical use of pseudo instructions is to work around the fact that the immediate value in an arm
instruction can't use more than 8 significant bits. That means it should be impossible to use the value
11111111111111111111111111111111 as an immediate. But, since that is -1, it is a useful value. Assemblers
will support the value -1 by converting the instruction that uses it into an equivalent one that works with
the bitwise negation of 0 or positive 1:

.. armcode::  

   @This should be illegal... too many bits
   MOV   r6, #0b11111111111111111111111111111111    @ r6 = #0xFFFFFFFF or #-1

   @But this is legal and has same effect
   MVN   r6, #0             @ r6 = 1111 1111 ...

   @These all assemble to same instruction:
   MOV   r6, #-1            @ r6 = 1111 1111 ...
   MOV   r6, #0xffffffff    @ r6 = 1111 1111 ...
   MVN   r6, #0             @ r6 = 1111 1111 ...

   @So do these:
   ADD   r6, r6, #-1    
   SUB   r6, r6, #1       
