.. include:: ../global.rst


Nested Function Calls
===============================================

.. index:: calling convention

The basic calling convention introduced earlier does not provide for a function calling another function. When the first function is called, the ``lr`` will be set to point to the return address that function should use. If that function calls a second function using ``BL``, the ``lr`` will be replaced with the address to return to within the first function and wipe out where the first function needs to return to!

To solve this problem, we need to store the current value of the ``lr`` to the stack as we enter the function, and restore it at the end of the function. That way it does not matter if the ``lr`` gets changed during the execution of the function.

Now the calling procedure looks like:

Calling Procedure (With LR storage)
-------------------------------------

Function Call (Done by caller)
   Any data in r0-r3 that needs to be stored is pushed to the stack.
   
   Parameters are placed in r0, r1, r2, and r3 (in order).

   Use ``BL`` to branch to the function.

Function Prologue (Done by called function)
   :red:`Push lr to the stack`

   If the function will use any registers in r4-r9, push the current values to the stack. 


Function Body (Done by called function)
   Do the work of the function. Access passed parameters in r0-r3. Only modify registers r0-r3 and any registers that were saved in the prologue.

Function Epilogue (Done by called function)
   Place any return value(s) in r0, r1, r2, r3. (C/C++ generally only return one value, but there is no reason in assembly you can't return more than one.)

   Pop any stored registers (r4-r9) from the stack to restore their old values.

   :red:`Pop lr from the stack`

   Return to the caller with ``BR LX``

Resume Control (Done by caller)
   Any returned value(s) are in registers r0-r3. 

   Pop stored registers (r0-r3) that were preserved before calling. 


.. note::

   Since storing and restoring the ``lr`` is only important if a function will call another function, compilers will generally use this version of the prologue and epilogue while building a function that calls another function, and the more basic version that skips that when building a function that does not make a call to another function.

-------------------------------------

This simple program demonstrates how saving and restoring the ``lr`` allows a function to call another function and still successfully return to its caller. To see what happens without doing so, try commenting out lines 31 and 41. The simulator will realize something is amiss and give an error message. A real processor would happily "return" at the end of plusTwo back to line 42 (address 0x00000018) (where the last call to plusOne returned to) instead of back to line 10 (0x00000008).

.. armcode:: 
   :linenos:
   :emphasize-lines: 31, 41

   /*
      Main program calls plusTwo(5) and places result in r6
   */
   .text
   .global _start
   _start:
      @save any r0-r3 I need... (none)
      MOV   r0, #5      @load 5 as 
      BL    plusTwo
      MOV   r6, r0      @get my return value, store into r6
      @restore any r0-r3... (none)

      @stop program
      end:  B     end
      @exit linux style
      @MOV   r7, #1
      @SWI   0



   @----------------------------------------------------------------------
   /* plusTwo - adds two to the value passed in by calling plusOne twice

   Params:
   r0 = x
   Return:
   r0 = x + 2
   */
   plusTwo:
      @@@ Prologue ----------------------------------------
      PUSH  {lr}              @store my return address

      @@@ Body --------------------------------------------
      @r0 already has the parameter to pass
      BL   plusOne            
      @r0 has x + 1
      BL   plusOne            
      @r0 has x + 2

      @@@ Epilog --------------------------------------------
      POP   {lr}              @Restore my return address and saved registers
      BX    lr                @return (return value is in r0)
   @----------------------------------------------------------------------


   @----------------------------------------------------------------------
   /* plusOne - adds one to the value passed in

   Params:
   r0 = x
   Return:
   r0 = x + 1
   */
   plusOne:
      @@@ Prologue ----------------------------------------
      PUSH  {lr}              @store my return address

      @@@ Body --------------------------------------------
      ADD   r0, r0, #1          
      @r0 has x + 1

      @@@ Epilog --------------------------------------------
      POP   {lr}              @Restore my return address and saved registers
      BX    lr                @return (return value is in r0)
   @----------------------------------------------------------------------