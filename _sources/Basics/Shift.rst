.. include:: ../global.rst



Shifts
=====================

.. index:: ! LSL, ! LSR

The **shift** instructions shift all the bits in a register to by a given amount. However, unlike with rotate,
when bits move past position 0 or 31, they disappear. Shifting this pattern:

.. bitpattern::
   :emphasize-bits: 4-11
   :inhex:

   AB0

8 bits to the right would end up "dropping" the 8 rightmost bits:

.. bitpattern::
   :emphasize-bits: 0-3
   :inhex:

   A



Since the bits do not wrap, we can't fake a left shift with a right one.

.. armlisting::  LSL rd, rn, rm / #

   Logical Shift Left. Shift rn to the left the number of bits in rm or #. Result in rd.

.. armlisting::  LSR rd, rn, rm / #

   Logical Shift Right. Shift rn to the right the number of bits in rm or #. Result in rd.


.. armcode::  

   MOV	r1, #0x12     @ r1 = 0000 ... 0000 0001 0010

   @Shift 4 BITS or 1 hex digit to the right
   LSL	r2, r1, #4    @ r2 = 0000 ... 0001 0010 0000

   @Shift 2 BITS to the left
   LSR	r3, r1, #2    @ r3 = 0000 ... 0000 0000 0100

   @Shift r1 by number of bits in r3 (4), result in r5
   LSL   r5, r1, r3


Multiplying and Dividing via Shift
------------------------------------

.. index:: multiply, divide

Shifting bits that represent a binary number to the left one place is equivalent to multiplying it by 2. Here, binary for 5 gets 
shifted and becomes 10 (A):

.. bitpattern::
   :emphasize-bits: 0-2
   :inhex:

   5

.. bitpattern::
   :emphasize-bits: 1-3
   :inhex:

   A

Shifting 2 bits is equivalent to multiplying by 4. Each additional bit shifted represents an additional power of 2. 

.. armcode::  

   MOV   r1, #5
   LSL   r2, r1, #1  @ r6 = 10 or 0xA
   LSL   r3, r1, #2  @ r6 = 20 or 0x14
   LSL   r4, r1, #8  @ r6 = 5 * 256 = 1280 or 0x500

Conversely, each bit shifted to the right divides a binary pattern by 2. Here is 24 (0x18) shifted right to produce 12 (0xC):

.. bitpattern::
   :emphasize-bits: 3-4

   11000

.. bitpattern::
   :emphasize-bits: 2-3

   1100

However, when we shift to the right, and the pattern represents a **two's complement** value, shifting in a 0 for the leftmost bit
can cause an error. Watch what happens if we shift -2 (0xFFFFFFFE) to the right one bit
- we get 0x7FFFFFFF or 2,147,483,647‬:

.. bitpattern::
   :inhex:

   F-E

.. bitpattern::
   :emphasize-bits: 31
   :inhex:

   7F-

To get the right answer, we need to copy the leftmost bit as we shift the pattern. Here is a correct version of -2 / 2 to produce -1 (0xFFFFFFFF):

.. bitpattern::
   :emphasize-bits: 31
   :inhex:

   F-E

.. bitpattern::
   :emphasize-bits: 30-31
   :inhex:

   F-

.. index:: ! ASR

This is the point of the Arithmetic Shift Right instruction - it does a shift that preserves the sign of a two's complement
number:

.. armlisting::  ASR rd, rn, rm / #

   Arithmetic Shift Right. Shift rn to the right the number of bits in rm or #, copying the leftmost bit to fill the void. Result in rd.


.. armcode::  

   MOV   r5, #50
   ASR   r6, r5, #1     @ r6 = r5 / 2
   ASR   r7, r5, #3     @ r7 = r5 / 8
   MOV   r8, #-200 
   ASR   r9, r8, #6     @ r9 = r8 / 64 = 3

   
.. tip::

   Shifting **n** bits to the left multiplies a value by **2^n**. Shifting to the right divides by **2^n** as long as you
   preserve the leftmost bit.