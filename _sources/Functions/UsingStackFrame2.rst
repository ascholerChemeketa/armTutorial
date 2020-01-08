.. include:: ../global.rst


Using the Stack Frame - Continued
===============================================

.. index:: stack frame

This more elaborate example has code for two functions, one of which calls 
the other. 

The first function is closeEnough, which has two parameters and two int 
variables, thus requiring 16 bytes of space in addition to the room for 
lr and fp:

.. stackdiagram::
   :no-stack-pointer:
   
   lr , < fp
   old fp (for closeEnough's caller), (fp - 4)
   x , (fp - 8) 
   y , (fp - 12) 
   diff , (fp - 16) 
   diffMagnitude , (fp - 20) 

The ``abs`` function only has one parameter and no local variables, 
so its stack frame only requires 4 bytes beyond the lr and fp:

.. stackdiagram::
   :no-stack-pointer:
   :start-address: 0xffffffe8
   
   lr , < fp
   old fp  (for abs's caller), (fp - 4)
   x, (fp - 8) 

As you watch the code run, have both the disassembly and memory panes open so you can pay attention to how the ``fp`` (``r11``) is keeping track of the current stack frame and loads and stores are addressing memory relative to it.

.. armcode::
   :linenos:

   .data
   a:      .word   25
   b:      .word   26

   /*
      Main program sets r6 to 1 if a and b are within 1 of each other
      otherwise set r6 to 0

      Calls closeEnough function to help do the job
   */
   .text
   .global _start
   _start:
      @load a and b into "permanent" registers
      LDR   r4, =a
      LDR   r4, [r4]
      LDR   r5, =b
      LDR   r5, [r5]

      @save any r0-r3 I need... (none)
      MOV   r0, r4      @load the parameters
      MOV   r1, r5
      BL    closeEnough
      MOV   r6, r0      @get my return value, store into r6
      @restore any r0-r3... (none)

      @stop program
      end:  B     end
      @exit linux style
      @MOV   r7, #1
      @SWI   0



   @----------------------------------------------------------------------
   /* CloseEnough - determine if two numbers are within one of each other
      Calls abs to help do the job.

   bool closeEnough(int x, int y) {
         int diff = x - y;
         int diffMagnitude = abs(diff);
         return (diffMagnitude <= 1);
   }

   Params:
   r0 = x
   r1 = y
   Return:
   r0 = 1 if within 1, 0 otherwise

   Stack Frame:
   -------------------------------
   FramePointer
   Relative
   Address           Contents
   -------------------------------
   -20              diffMagnitude
   -16              diff
   -12              y
   -8               x
   -4               old fp
   0                my lr
   */
   closeEnough:
      @@@ Prologue ----------------------------------------
      PUSH  {fp, lr}          @store my return address and previous fp
                              @If we were going to use r4+ would need to store
                              @sp now points at address 0x04 relative to frame
      ADD   fp, sp, #4        @set fp to point at addres 0x00 relative to frame
      SUB   sp, sp, #16       @Make 16 bytes space for four local variables/parameters
      STR   r0, [fp, #-8]     @store r0 to x in stack frame
      STR   r1, [fp, #-12]    @store r1 to y in stack frame

      @@@ Body --------------------------------------------
      @int diff = x - y;
      LDR   r0, [fp, #-8]     @r0 = x
      LDR   r1, [fp, #-12]    @r1 = y
      SUB   r0, r0, r1        @r0 = x - y
      STR   r0, [fp, #-16]    @store answer to diff in stack frame

      @int diffMagnitude = abs(diff);
      LDR   r0, [fp, #-16]    @get diff into r0
      @save any r0-r3 I care about...none
      BL   abs                @get abs of difference of x and y
      @answer of abs(x - y) is in r0
      @restore any r0-r3 I saved...none
      STR   r0, [fp, #-20]    @store answer to diffMagnitude in stack frame

      @return (diffMagnitude <= 1);
      LDR   r0, [fp, #-20]    @get diffMagnitude into r0
      CMP   r0, #1            @compare diffMagnitude with 1
      MOVLE r0, #1            @set r0 to true/false based on result
      MOVGT r0, #0            @ 1 if diff is <= 1; 0 if diff is > 1

      @@@ Epilog --------------------------------------------
      ADD   sp, sp, #16       @Remove 16 bytes for local variables
      POP   {fp, lr}          @Restore my return address and saved registers
      BX    lr                @return
   @----------------------------------------------------------------------


   @----------------------------------------------------------------------
   /* AbsoluteValue
      Does not call another function

   int abs(int x) {
      if (x < 0)
         x = -x;
      return x;
   }

   Params:
   r0 = number
   Return:
   r0 = |number|

   Stack Frame:
   -------------------------------
   FramePointer
   Relative
   Address           Contents
   -------------------------------
   -8               x
   -4               old fp
   0                my lr
   */
   abs:
      @@@ Prologue ----------------------------------------
      PUSH  {fp, lr}          @store previous fp and our lr
                              @If we were going to use r4+ would need to store
      ADD   fp, sp, #4        @set fp to point at addres 0x00 relative to frame
      SUB   sp, sp, #4        @Make 4 bytes space for one local variable/param
      STR   r0, [fp, #-8]     @store r0 to x in stack frame

      @@@ Body --------------------------------------------

      @if (x < 0)
      LDR   r0, [fp, #-8]     @r0 = x
      CMP   r0, #0            @check against 0
      BGE   end_absIf         @if >= 0, skip ahead
      @   x = -x;
      MVN   r0, r0            @was negative, so negate bitwise
      ADD   r0, r0, #1        @add one to get 2's complement negation
      STR   r0, [fp, #-8]     @store back to x in stack frame

   end_absIf:
      @@@ Epilog --------------------------------------------
      LDR   r0, [fp, #-8]     @get x into r0
      ADD   sp, sp, #4        @Remove 4 bytes for local variables
      POP   {fp, lr}          @Restore old fp and lr
      BX    lr                @return
   @----------------------------------------------------------------------
