.. include:: ../global.rst



Arithmetic
=====================

.. index:: ADD, SUB, RSB

Arithmetic instructions combine two values via addition or subtraction, placing the results into a destination register.


.. tip::
    
    All of the arithmetic instructions only support an immediate value as the last parameter.



-----------
  

.. armlisting::  ADD rd, rn, rm / #

   Add rn to either register rm or immediate #, place the results in rd.

.. armcode::  

    MOV   r1, #100
    MOV   r2, #200
    ADD   r3, r1, r2        @r3 = r1 + r2
    ADD   r4, r1, #1        @r4 = r1 + 1
    ADD   r4, r4, #1        @r4++


-----------
  

  
.. armlisting::  SUB rd, rn, rm / #

   Subtracts either register rm or immediate # from rn and places answer in rd.

.. armcode::  

    @Load some starting values
    MOV   r1, #50
    MOV   r2, #200
    SUB   r2, r2, r1     @r2 = r2 - r1
    SUB   r3, r1, r2     @r3 = r1 - r2
    SUB   r4, r1, #10    @r4 = r1 - 10
    @SUB   r4, #10, r1   @Invallid! Immediate value must be last

    
-----------
  
Because only the final operand for SUB can be an immediate, we cannot write ``SUB r2, #10, r1`` to subtract r1 from 10. 
Instead, there is a **reverse subtract** instruction **RSB** that subtracts the first parameter from the second.

.. armlisting::  RSB rd, rn, rm / #

   Reverse SuBtract. Subtracts rn from either register rm or immediate # and places answer in rd.

.. armcode::  

    @Load some starting values
    MOV   r1, #50
    MOV   r2, #200
    RSB   r3, r2, r1    @r3 = r1 - r2 using RSUB
    RSB   r5, r1, #10   @r5 = 10 - r1