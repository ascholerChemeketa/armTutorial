.. include:: ../global.rst


Using the Stack Frame
===============================================

.. index:: stack frame

After the stack frame is built, we use it to store and load from any time a variable needs to be read or written.

We will demonstrate what that might look like for this c++ function:

.. code:: c++

   int bar(int num) {
      int a = num + 1;
      a *= 2;
      return a;
   }

The stack frame for this function would need space for the parameter **num** and the local variable **a**. Since each is an int, they will each require 4 bytes of space. Thus the stack frame will end up looking like this:

.. stackdiagram::
   
   lr , < fp
   old fp  (for bar's caller), (fp - 4)
   num, (fp - 8)
   a , (fp - 12) < sp

Any time we want to access **num**, we will need to load/store from ``[fp, #-8]``. Any time we want to access the variable **a**, we will use the address ``[fp, #-12]``.

The program below has the assembly version of this function. The prologue sets up this stack frame. Line 52 sets up the space for **num** and **a**. After that, the variable **num** needs to be initialized with the value passed in. The parameter was passed in r0, so it is copied to the location in memory  space has been reserved but no values are stored. Line 55 stores r0 into the correct location in memory: ``[fp, #-8]``.

Then, in the body of the function, we use loads and stores to access and modify variables. Something like ``a = num + 1`` would turn into multiple steps: load the value of **num** from the stack frame, add 1 to that value, then store the result back to the location in the stack frame that corresponds to **a**. This process is demonstrated on lines 60-62.

Finally, the epilogue loads the variable to be returned into r0, then cleans up the stack frame.

.. armcode::
   :linenos:
   :emphasize-lines: 52, 55, 60-62

   .text
   .global _start
   _start:
      @call bar(4)
      MOV   r0, #4
      BL    bar

      MOV   r4, r0   @Move returned value to r4

      @stop program
      end:  B     end
      @exit linux style
      @MOV   r7, #1
      @SWI   0



   /*
   Bar function - pointless demonstration function

   int bar(int num) {
      int a = num + 1;
      a *= 2;
      return a;
   }

   Params:
   r0 = num
   Return:
   r0 = a  (2*num + 1)

   Stack Frame:
   -------------------------------
   FramePointer
   Relative
   Address           Contents
   -------------------------------
      -12            a
      -8             num
      -4             old fp
      -0             my lr
   */

   bar:
      @@@ Prologue --------------------------------------------
      PUSH  {fp, lr}       @push necessary registers to stack
                           @if we were using r4+ would need to push those too
                           @sp ends up 4 bytes into stack frame

      ADD   fp, sp, #4     @set frame pointer to top of frame

      SUB   sp, sp, #8     @move stack pointer down 8 bytes
                           @allocates space for num and a

      STR   r0, [fp, #-8]  @store r0 to location reserved for num

      @@@ Body --------------------------------------------

      @@@int a = num + 1
      LDR   r0, [fp, #-8]  @load num into r0
      ADD   r0, r0, #1
      STR   r0, [fp, #-12] @store result into a

      @@@a *= 2
      LDR   r0, [fp, #-12] @load a into r1
      LSL   r0, r0, #1     @ *= 2
      STR   r0, [fp, #-12] @store back into a

      @@@ Epilog --------------------------------------------
      LDR   r0, [fp, #-12] @load a into r0 for return
      ADD   sp, sp, #8     @move stack pointer up to remove 8 bytes
                           @releases space for num and a
      POP   {fp, lr}       @restore all registers
                           @if we were using r4+ would need to pop those too
      BX    lr             @return


It might strike you as a lot of wasted work. Why both storing r0 into memory on line 62 only to load the exact same value from memory back into r0 on line 65? Indeed, when we ask a compiler to optimize code, one of the things it seeks to do is minimize shuffling things back and forth between registers and the stack. But the unoptimized code shown above is the easiest to generate, as what we do on one line does not depend on what is happening on other lines. Each line of c++ code does all of its own loads and stores to guarantee that the current values for variables are stored into the expected places regardless of what code comes next.