.. include:: ../global.rst


Array Access
================================

.. index:: arrays

We access information in arrays in the same way we do any other piece of memory. First we use a ``LDR`` instruction to load the address of the 
memory, then we use an ``LDR`` with that address to load the data itself. 

What is different about arrays is that we expect to find multiple units of storage starting at the address we are working with. To access elements other 
than the first, we need to calculate the correct address by adding a number of bytes to the base address - an **offset**. The **offset** will be the index 
number of the element we desire times the size of each element in bytes. For example: if we want the 10th item in an array of words, we would add 10 * 4 = 40 bytes.

As programmers, we have to do the math to calculate the right **offset**. But we don't have to add it to the base address ourselves. Instead, we can specify 
it as a value to add to the address found in a register using this syntax:

.. armlisting:: LDR rd, [rn, #]

   Access the memory at the address rn + #, and store its value into rd. # should be i * element_size where i is the index of the element desired 
   and element_size is the number of bytes per element.

   Similar [rn, #] syntax is available for STR, LDRB, LDRSB, and STRB

This code sample demonstrates setting myArray[4] = myArray[0] + myArray[1]:

.. armcode::  

   .data
   @An array of 4 words
   myArray:      .word   5, 10, 15, 20, 0
   @myArray will store address of first word
   @ each additional one if 4 bytes after the last

   .text
   LDR   r1, =myArray   @ load myArray start address

   LDR   r2, [r1]       @ r2 = value at address of myArray
                        @    = myArray[0]

   LDR   r3, [r1, #4]   @ r2 = value at address of myArray + 4 bytes
                        @    = myArray[1]

   ADD   r4, r2, r3     @ r4 = myArray[0] + myArray[1]

   STR   r4, [r1, #16]  @ store r4 (sum) to 16 bytes after start of myArray
                        @ myArray[4] = r4


.. tip::

   To see the ``STR`` instruction's effects, you will have to have the Memory tab of the simulator showing. You can dock it next to the Diasassembly tab 
   so that both views are visible.

   Also, when you restart the simulator, the memory does not get reset - make sure to Reload if you want to watch it run again.


If we are working with bytes of memory, the strategy will be the same, but the size of each element is 1 and we need to use LDRB/LDRSB and STRB to load and 
store the values:


.. armcode::  

   .data
   @an array of 4 SIGNED bytes
   myArray:    .byte   -3, 4, 10, 0

   .align   @make sure we are padded to a full word
   @not needed here, but good to always do it

   .text
   _start:
      LDR   r1, =myArray      @ load arrays start address

      LDRSB r2, [r1]          @ r2 = myArray[0] as Signed Byte

      LDRSB r3, [r1, #1]      @ r3 = myArray[1] (1 byte from start)

      ADD   r4, r2, r3        @ r4 = myArray[0] + myArray[1]

      @STore Register r4 back to array as Byte
      STRB  r4, [r1, #3]      @ myArray[2] (2 bytes from start) = r4 (sum)