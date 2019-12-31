.. include:: ../global.rst


Calling Conventions
=====================================

.. index:: calling conventions

As control is transferred from one location to another, we also need to transfer information and coordinate register use. We want to be able to pass parameters to functions and have them return values. As those functions do work, they will be using the same registers that the rest of the program does - we need to make sure that one part of the program does not overwrite an important piece of information stored in a register by another part of the program.

If we were hand coding an entire program in assembly, we could manage registers however we wanted. But keeping track of which ones were in use at every point of a large program would be a complex undertaking. And we generally don't sit down to write an entire program by hand. We use tools to compile code and make use of code that others have written. For arbitrary pieces of code to work together, they can't count on any special knowledge (*\ "I know that register r8 is not being used right now, so I'll put my data there"*\ ). Instead, we need an agreed on set of rules for how to pass information from function to function and who gets to use which registers. 

**Calling conventions** are the rules for how functions transmit information and use registers and memory. They will necessarily differ between architectures (ARM and Intel have different registers available) but also may differ between operating systems and even different compilers for the same platform. We will focus on the calling conventions generally used in ARM v7 by the GNU C/C++ compiler - they are a fairly representative set of rules.

In general, register 0-9 are used for program data. r0-r3 are used for temporary storage and information passing. There is never any expectation that other code will preserve values in these registers. r4-r9 are used for longer term storage and functions are expected to not destroy values in them: 

Register Use:
---------------------

.. csv-table::
   :header: "Register(s)", "Use"
   :widths: 20, 50
   :class: "register-table"

   **r0 - r3**, Parameters and return values. |br|  Also used for temporary values - any function can change these at will.
   **r4 - r9**, Stored values. Any values stored in these must be preserved by functions.
   **r10 - r15**, Special purpose. These have assigned roles (like **pc** or **lr**). Not all the roles are always used.

The stack is used to back up  the values in registers when needed as well as for situations too complex for the normal conventions (like passing more than 4 parameters to a function). When a value needs to be preserved so a register can be reused for a new job, we push the old value to the stack and then later pop it off to restore it.

A function call always involves 5 steps:

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

This code sample below demonstrates a program that replace r4 and r5 with their absolute values. To do this, it uss an ``abs`` function. To call the function, the main part of the program stores r1, which is in use, then places the parameter (value to take absolute value of) in r0. The function preserves, r4 and r5 so it can use them, then does its work. It finishes up by placing the answer in r0, restoring r4 and r5 and branching back. Then the main part of the program moves the returned value out of r0 and restores r1:

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


A Smarter Version
---------------------------------

A lot of time is spent in the previous sample pushing and popping values from the stack. This is necessary because the main part of the program is relying on r1 being maintained and the function is making use of r4 and r5 which it is not supposed to modify.

We could do the same work with less saving and restoring by using registers in the way the calling convention expects: temporary work should be done in r0-r3 and values we want to preserve are placed in r4-r9. This version of the absolute value program uses registers in this more appropriate way:

.. armcode::  
   :linenos:

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
      MOV   PC, LR      @return
