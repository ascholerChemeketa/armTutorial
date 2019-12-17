.. include:: ../global.rst


Bitwise Logic 1
=====================

.. index:: AND

The instructions ``AND``, ``ORR``, ``EOR``, and ``MVN`` function as the bitwise logical operations **and**, **or**, 
**exclusive or**, and **not**. These bitwise operations combine either two registers or a register and an immediate by 
comparing bit 0 of the first to bit 0 of the second, bit 1 of the first to bit 1 of the second, etc...


AND
--------------------------

The ``AND`` instruction compares the individual bits of two patterns using logical **AND**: produce a 1 if both inputs are 1, 0 otherwise.
In these two patterns:

.. bitpattern::
   :emphasize-bits: 2-3,4,5
   :inhex:

   3C


.. bitpattern::
   :emphasize-bits: 0,2-3,4-7
   :inhex:

   FD

Bits 2, 3, and 5 are the only ones that are 1 in both - thus this output is produced:

.. bitpattern::
   :emphasize-bits: 2-3, 5
   :inhex:

   2C


.. armlisting::  AND rd, rn, rm / #

   Combine the bits of rn and the bits of rm or # with AND. Result in rd.


ORR
--------------------------

.. index:: ORR

``ORR`` compares the individual bits of two patterns using logical **OR**: produce a 1 if either or both inputs are 1, 0 otherwise.
In these two patterns:

.. bitpattern::
   :emphasize-bits: 2-3,5,7
   :inhex:

   AC


.. bitpattern::
   :emphasize-bits: 0,4-7
   :inhex:

   F1

Bits 0, 2, 3, and 4-7 are 1 in at least one of of the two inputs - thus this output is produced:

.. bitpattern::
   :emphasize-bits: 0,2,3,4-7
   :inhex:

   FD


.. armlisting::  ORR rd, rn, rm / #

   Combine the bits of rn and the bits of rm or # with OR. Result in rd.


---------------------------------------


.. armcode::  

   @AND keeps 1 if both inputs are 1
   MOV   r1,      #0xac             @ r1 = 0000 ... 1010 1100
   @              #0x3D                    0000 ... 0011 1101
   AND   r2, r1,  #0x3D             @ r2 = 0000 ... 0010 1100

   @ORR keeps 1 from either pattern
   MOV   r4,      #0xac             @ r4 = 0000 ... 1010 1100
   MOV   r5,      #0xF1             @ r5 = 0000 ... 1111 0001  
   ORR   r6, r4, r5                 @ r6 = 0000 ... 1010 1101

