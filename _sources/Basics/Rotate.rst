.. include:: ../global.rst



Rotation
=====================

.. index:: ROR

The **rotate** instruction shifts all the bits in a register to the right by a given amount. If we take this pattern:


.. bitpattern::
   :emphasize-bits: 8-15

   0110 1111 0000 0000

And shift it right 1 bit, we get:

.. bitpattern::
   :emphasize-bits: 7-14

   0110 1111 0000 000

Notice that shifting one bit completely changes the hex version of the pattern. If we want to shift by one hex digit, 
we should shift the original pattern 4 bits. 

.. bitpattern::
   :emphasize-bits: 4-11

   0110 1111 0000

   
.. tip::

   Each 4-bits of rotation shifts the hex digits by 1


Bits that shift past position 0 wrap around to bit 31. Here is the pattern shifted 6 more bits:

.. bitpattern::
   :emphasize-bits: 0-5, 30-31 

   110-0110 11

-----------
  

.. armlisting::  ROR rd, rn, rm / #

   ROtate Right. Rotate rn to the right the number of bits in rm or #. Result in rd.

.. armcode::  

   MOV   r1, #0x12      @ r1 = 0000 0000 ... 0000 0001 0010

   @Rotate r1 right by 1 bit
   ROR   r2, r1, #1     @ r2 = 0010 0000 ... 0000 0000 1001

   @Rotate r1 right by 4 bits - one hex char
   ROR   r3, r1, #4     @ r3 = 0010 0000 ... 0000 0000 0001


There is no **rotate left** instruction, because we do not need one. A 31-bit rotate is the same as rotating left 1 bit,
a 30-bit rotate the same as rotating left 2 bits, .... If we want to rotate left 12 bits, we could instead rotate 20 to the right:

.. armcode::  

   MOV   r1, #0x12      @ r1 = 0x00000012

   @Rotate r1 left 12 bits by ROR 20 bits (32 - 20 = 12); answer in r6
   ROR   r6, r1, #20    @ r6 = 0x00012000


.. tip::

   To rotate left X bits, we rotate 32 - X to the right