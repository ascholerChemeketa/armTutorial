.. include:: ../global.rst


Bitwise Logic 2
=====================

.. index:: EOR

EOR
--------------------------

The ``EOR`` instruction compares the individual bits of two patterns using logical **exclusive or**: 
produce a 1 if one of the two inputs is 1, produce 0 if the input bits are the same.
In these two patterns:

.. bitpattern::
   :emphasize-bits: 2-3,5,7
   :inhex:

   AC

.. bitpattern::
   :emphasize-bits: 1,2,4-7
   :inhex:

   F6

Bits number 1, 3, 4, and 6 are 1 in exactly one of the inputs:

.. bitpattern::
   :emphasize-bits: 1,3,4,6
   :inhex:

   5A


.. armlisting::  EOR rd, rn, rm / #

   Combine the bits of rn and the bits of rm or # with exclusive or. Result in rd.


NOT
--------------------------

.. index:: NOT, MVN

Thgere is no instruction named **NOT**, but the ``MVN`` instruction does the job of logical **NOT**. 
It takes a pattern and flips all the bits so 1's become 0's and vice verse. This pattern:

.. bitpattern::
   :emphasize-bits: 2-3,5,7
   :inhex:

   AC

Produces this when negated: 

.. bitpattern::
   :emphasize-bits: 0,1,4,6,8-31
   :inhex:

   F-53


.. armlisting::  MVN rd, rn / #

   Place the bitwise negation of rm or # in rd. Does logical NOT.



---------------------------------------


.. armcode::  

   @EOR gives 1 if bits are different
   MOV   r7,      #0xac              @ r7 = 0000 ... 1010 1100
   @              #0xFD                     0000 ... 1111 0110
   EOR   r8, r7,  #0xFF              @ r8 = 0000 ... 0101 1010

   MOV   r9,      #0xAC              @ r9 = 0000 ... 1010 1100
   MVN   r10, r9                     @ r10= 1111 ... 0101 0011
   MVN   r11, r10                    @ r11= 0000 ... 1010 1100

