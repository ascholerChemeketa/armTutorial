.. include:: ../global.rst



Data Movement 
=====================

.. index:: MOV, MVN

The **MOV** and **MVN** instruction copy (move) data from into registers.

-----------
  
.. armlisting::  MOV rd, rn

   MOVe. Copy data from register rn to register rd. Does not modify rn.
  
.. armlisting::  MOV rd, #

   Copy the immediate value # into register rd.

.. armcode::  

    MOV   r1, #100      @Place 100 base 10 in r1
    MOV   r2, #0xff     @Place hex ff (255) in r2
    MOV   r3, #0b1100   @Place 1100 binary in r3 (12 in deciamal, 0xC in Hex)
    MOV   r4, #'A'      @Place char 'A' or 65 in r4
    MOV   r5, r3        @Copy value in r3 into r5

-----------
  
.. armlisting::  MVN rd, rn / #

   MoVe Negated. Places the bitwise negation of the source register or immediate rn / # into register rd. 

.. armcode::  

    @Load r1, then load its negation into r2
    MOV   r1, #1        @ r1 = 0000 0000 ... 0001
    MVN   r2, r1        @ r2 = 1111 1111 ... 1110

    @Load r3, then load its negation into r4
    MOV   r3, #0xA3     @ r3 = 0000 0000 ... 1010 0011
    MVN   r4, r3        @ r4 = 1111 1111 ... 0101 1100

    @Load the negation of 0000 0000 0000 ... 1111 into r5
    MVN   r5, #0xF      @ r5 = 1111 1111 ... 0000