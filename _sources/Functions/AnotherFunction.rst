.. include:: ../global.rst


Another Function
=====================================

The sample below has a second demonstration of using the calling conventions - it contains an unsigned division function ``udiv`` that is used to figure out the coins to use to make change. The ``udiv`` function takes two parameters, the number to divide and the divisor, passed in ``r0`` and ``r1`` and returns two values, the quotient and the remainder, in ``r0`` and ``r1``.

.. note:: 

   Since parameters are just register numbers, documentation of how the registers are being used is critical! 

Like the last one, this program avoids storing and reloading registers by keeping long term values in r4+ and using r0-r3 for all the temporary work in the function.


.. armcode::  
   :linenos:

   /*
      Demonstrates using unsigned division function to make ideal change for 
      the number of cents loaded in r0.
      
      Answer provided as:
         r6: quarters
         r7: dimes
         r8: nickles
         r9: pennies
   */

   .text
   .global _start
   _start:

      @Initial number of cents
      MOV   r0, #92

      @25 cents per quarter
      MOV   r1, #25
      BL    udiv           @ cents / 25
      @r0 now has quarters and r1 leftover cents
      MOV   r6, r0         @r6 = num quarters
      MOV   r0, r1         @put leftover cents back into r0

      @10 cents per dime
      MOV   r1, #10
      BL    udiv           @leftover cents / 10
      @r0 now has dimes needed and r1 leftover cents
      MOV   r7, r0         @r7 = num dimes
      MOV   r0, r1         @put leftover cents back into r0

      @5 cents per nickle
      MOV   r1, #5
      BL    udiv           @leftover cents / 5
      @r0 now has nickles needed and r1 leftover cents
      MOV   r8, r0         @r8 = num nickles

      MOV   r9, r1         @r9 = pennies = leftover cents

   end:
      B     end            @stop here

   @----------------------------------------------------------------------
   /*Unsigned division - assumes both values are unsigned integers
   Params:
   r0 = number
   r1 = divisor
   Return:
   r0 = quotient
   r1 = remainder
   */
   udiv:
      MOV   r2, #0            @temp_quotient
      B     udiv_test
   udiv_loop_start:
      SUB   r0, r0, r1        @number -= divisor
      ADD   r2, r2, #1        @quotient++
   udiv_test:
      CMP   r0, r1            @is remaining value > divisor?
      @Can't use GE for unsigned values
      BCS   udiv_loop_start   @if higher or same continue loop

      MOV   r1, r0            @remainder = leftover part of number
      MOV   r0, r2            @quotient = temp_quotient
      MOV   pc, lr            @return
