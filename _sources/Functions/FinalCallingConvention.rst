.. include:: ../global.rst


Final Calling Convention
===============================================

.. index:: ! calling convention

Our final version of the calling convention, including setting up and tearing down the stack frame, looks like this:

Calling Procedure (With Stack Frame)
-------------------------------------

Function Call (Done by caller)
   Any data in r0-r3 that needs to be stored is pushed to the stack.
   
   Parameters are placed in r0, r1, r2, and r3 (in order).

   Use ``BL`` to branch to the function.

Function Prologue (Done by called function)
   Push fp and lr to the stack

   Set fp to point to top of the stack frame (where the stored lr is located)

   If the function will use any registers in r4-r9, push the current values to the stack.

   Allocate space for parameters and locals by subtracting the needed number of bytes from the stack pointer.

   Copy parameter values from registers r0+ into appropriate locations in the stack frame.


Function Body (Done by called function)
   Do the work of the function. 
   
   Any time we need to read/write a parameter or local variable, load and/or store it from the stack frame.


Function Epilogue (Done by called function)
   Place any return value(s) in r0, r1, r2, r3. (in C/C++ we only return one value, but there is no reason in assembly you can't return more than one.)

   Deallocate space for parameters and locals by adding the used number of bytes to the stack pointer.

   Pop any stored registers (r4-r9) from the stack to restore their old values.

   Pop the fp and lr to restore frame pointer of caller and the return location of this function.

   Return to the caller with ``BX LR``

Resume Control (Done by caller)
   Any returned value(s) are in registers r0-r3. 

   Pop stored registers (r0-r3) that were preserved before calling. 


.. note::

   Since storing and restoring the ``lr`` is only important if a function will call another function, compilers may omit saving the ``lr`` for functions that call other functions. They also may omit storing the ``fp``. They also may skip using the stack entirely and just do all the work in registers.

