.. include:: ../global.rst


A Smarter Function Call
=====================================

.. index:: ! function call


A lot of time is spent in the previous sample pushing and popping values from the stack. This is necessary because the main part of the program is relying on r1 being maintained and the function is making use of r4 and r5 which it is not supposed to modify. We could do the same work with less saving and restoring by using registers in the way the calling convention expects: temporary work should be done in r0-r3 and values we want to preserve are placed in r4-r9. 

This version of the absolute value program uses registers in the way they should. Because it uses r0-r3 for temporaries only and r4-r9 for longer term storage, there is no need to save/restore registers to the stack:

.. armcode::  
   :linenos:
   :emphasize-lines: 13-15, 47, 55-56

   /* 
      Reduces work storing/restoring registers by keeping "local values"
      in r4+
   */

   .text
   .global _start
   _start:
      MOV   r6, #0xAA      @set up some numbers to work with
      MOV   r4, #30
      MOV   r5, #-12

      MOV   r0, r4         @set up parameter for abs call
      BL    abs            @get abs
      MOV   r4, r0         @save result from the function back to r4

      @OK to temporarily use r0-r3 as long as done by next function call
      @Do some random work...
      MOV   r1, #3         @r1 = 3
      MUL   r6, r6, r1     @r6 *= 3
      @done using r1, we are OK if it gets wiped out

      MOV   r0, r5         @setup param
      BL    abs            @get abs
      MOV   r5, r0         @save result back to r5

   end:
      B     end            @stop here

   @----------------------------------------------------------------------
   /*AbsoluteValue

   Calculates absolute value of a value passed in via r0.

   Avoids taking responsibility for registers by doing all work in r0-r3

   int abs(int x) {
      if (x < 0) x = -x;
      return x;
   }

   Params:
   r0 = number
   Return:
   r0 = |number|
   */
   abs:
      @ONLY use registers r0-r3 to do my work
      CMP   r0, #0
      BGE   end_absIf   @check if negative
      MVN   r1, r0      @negative - get bitwise negation
      ADD   r0, r1, #1  @add one to get 2's complement negation

   end_absIf:
      @know that r0 now has abs(r0)
      BX    lr          @return
