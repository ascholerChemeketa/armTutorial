.. include:: ../global.rst


A Simple Function Call
=====================================

.. index:: function call

Calling and returning from a function always involves five phases. Control starts at the caller, which has to possibly save information it has in registers r0-r3 and then call the function. The called function needs to gather and save information (the **prologue**), execute its code, and then clean up and return (the **eplogue**). Finally, the caller needs to restore any saved values and then work with any returned value. Here is a summary of what happens:

Calling Procedure (Basic)
-------------------------------------

Function Call (Done by caller)
   Any data in r0-r3 that needs to be stored is pushed to the stack.
   
   Parameters are placed in r0, r1, r2, and r3 (in order).

   Use ``BL`` to branch to the function.

Function Prologue (Done by called function)
   If the function will use any registers in r4-r9, push the current values to the stack. 

Function Body (Done by called function)
   Do the work of the function. Access passed parameters in r0-r3. Only modify registers r0-r3 and any registers that were saved in the prologue.

Function Epilogue (Done by called function)
   Place any return value(s) in r0, r1, r2, r3. (C/C++ generally only return one value, but there is no reason in assembly you can't return more than one.)

   Pop any stored registers (r4-r9) from the stack to restore their old values.

   Return to the caller with ``MOV PC, LR``

Resume Control (Done by caller)
   Any returned value(s) are in registers r0-r3. 

   Pop stored registers (r0-r3) that were preserved before calling. 

A Sample Function
---------------------------------

The code sample below demonstrates a program that replace r4 and r5 with their absolute values. To do this, it uss an ``abs`` function. To call the function, the main part of the program stores r1, which is in use, then places the parameter (value to take absolute value of) in r0. The function preserves, r4 and r5 so it can use them, then does its work. It finishes up by placing the answer in r0, restoring r4 and r5 and branching back. Then the main part of the program moves the returned value out of r0 and restores r1.

Here is how the stack is used to store values along the way:

.. tabbed:: sample2


   .. tab:: Start

      .. stackdiagram::
         :empty:

          , 
          ,
          ,
          
   .. tab:: At line 12

      .. stackdiagram::

         r1 from main, < sp 
          ,
          ,
      
      main part of program pushes r1 for safe keeping.
          
   .. tab:: At line 51

      .. stackdiagram::

         r1 from main, 
         r5 from abs,
         r4 from abs, < sp 
      
      abs pushes r4 and r5 for safe keeping.
          
   .. tab:: At line 62

      .. stackdiagram::

         r1 from main, < sp 
         r5 from abs,
         r4 from abs,

      abs restores previous values of r4 and r5
          
   .. tab:: At line 16

      .. stackdiagram::
         :empty:

         r1 from main,
         r5 from abs,
         r4 from abs,

      main part of program restores r1
          


.. armcode::  
   :linenos:

   /*
      Main program is using registers 1, 4 and 5
      It is responsible for storing/restoring r1 while calling function
   */
   .text
   .global _start
   _start:
      MOV   r1, #0xAA
      MOV   r4, #30
      MOV   r5, #-12

      PUSH  {r1}        @I want to keep r1 safe, so save it
      MOV   r0, r4      @set up parameter for abs call
      BL    abs
      MOV   r4, r0      @save result from the function back to r4
      POP   {r1}        @restore r1

      PUSH  {r1}        @I want to keep r1 safe, so save it
      MOV   r0, r5      @setup param
      BL    abs
      MOV   r5, r0      @save result
      POP   {r1}        @restore r1

   end:
      B     end         @stop here



   @----------------------------------------------------------------------
   /*AbsoluteValue
   Calculates absolute value of a value passed in via r0.

   Demonstrates register responsibility:
   Uses r0, r1, r4, r5 - must preserve existing values in r4/r5

   Equivelent to:
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
      @store any registers 4+ I want to use
      PUSH  {r4, r5}

      @do work, using 
      MOV   r1, #0
      CMP   r0, r1         @compare parameter in r0 to 0
      BGE   end_absIf      @if r0 was >= jump ahead
      MVN   r4, r0         @r0 was negative... copy its bitwise negation to r4
      ADD   r5, r4, #1     @add 1 to get 2's complement negation into r5
      MOV   r0, r5         @move negated version into r0

   end_absIf:
      @r0 has correct answer at this point
      @restore any registers 4+ I used
      POP   {r4, r5}
      MOV   PC, LR         @return


         
