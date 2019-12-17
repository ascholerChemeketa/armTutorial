.. include:: ../global.rst


Operand Shifts
=====================

.. index:: LSL, LSR, ASR, ROR

The architecture of the ARM processor provides a shift unit in the data path between the registers and the ALU.
Because of its location, it is possible to shift one of the operands (always the second one) as it is brought to
the ALU from the register file. 

We do this by using ``ROR``, ``ASR``, ``LSL``, or ``LSR``

Since the bits do not wrap, we can't fake a left shift with a right one.

.. armlisting::  INSTRUCTION rd, rn, rm, LSL/LSR/ASR/ROR #

   Perform a basic INSTRUCTION like MOV or ADD. However, do the given shift to the value from rm before using it.
    rm itself is not affected.


.. armcode::  

   MOV   r1, #0x5
   @Take r1, left shift value by 1 bit (multiplies by 2) and move into r2
   MOV   r2, r1, LSL #1       @r2 = r1 * 2
   LSL   r2, r1, #1           @Same!!!


   @Use ASR 2 bits to divide by 4 while moving value
   MOV   r3, #-100
   MOV   r4, r3, ASR #2       @r4 = r3 / 4

   @Use use LSL 2 bits to multiply value of r8 by 4 while adding to itself
   @  to produce 5 * r8
   MOV   r8, #3
   ADD   r9, r8, r8, LSL #2   @r9 = r8 + r8 * 4
                              @   = 5 * r8

   @Calculate (2 * r5) - r6 in one line using LSL and ReverseSuBtract
   MOV   r5, #6
   MOV   r6, #9
   RSB   r7, r6, r5, LSL #1   @r7 = r5 * 2 - r6

