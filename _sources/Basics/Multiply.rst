.. include:: ../global.rst

Multiply
=====================

.. index:: MUL, multiply

Shifts are efficient ways to multiply and divide by powers of 2, but sometimes we want to multiply by 
other values. Fortunately, there is a multiply instruction:

.. armlisting::  MUL rd, rn, rm

   Multiply rn by rm. Result in rd. An immediate value cannot be used - all operands must be registers.

.. armcode::  

   MOV   r1, #5
   MOV   r2, #2

   MUL   r3, r1, r2     @r3 = r1 * r2
   MUL   r3, r3, r3     @r3 = r3 * r3


.. index:: MLA

The design of the ARM processor (at least historically) allowed for the data path to efficiently add a value to
a product that had just been calculated. Being able to multiply two values and immediately sum them with something
can be useful for accumulating a total while performing a loop over a series of calculations. This operation is
handled by the MLA instruction:


.. armlisting::  MLA rd, rn, rm, ra

   Multiply rn by rm and add to ra. Result in rd. An immediate value cannot be used - all operands must be registers.

.. armcode::  

   MOV   r5, #2
   MOV   r6, #3
   MOV   r7, #7

   MOV   r8, #0x100
   MOV   r9, #0x10
   MOV   r10, #0x1

   @set r11 to (r5*r8) + (r6*r9) + (r7*r10)
   MUL   r11, r5, r8          @(r5*r8)
   MLA   r11, r6, r9, r11     @(r6*r9) + (r5*r8)
   MLA   r11, r7, r10, r11    @(r7*r10) + (r6*r9) + (r5*r8)


------------------------------

What about division? Not all ARM processors have division hardware. So the unsigned division ``UDIV`` and signed division ``SDIV`` 
instructions are only available if the hardware supports them. For processors without hardware division, programmers need to code the
process by hand or rely on an assembler macro that implements division using a series of other instructions.