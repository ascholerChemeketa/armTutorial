.. include:: ../global.rst


Looping Through Arrays
================================

.. index:: arrays, loops

To loop through an array, we need to access successive memory addresses: something like x, x + 4, x + 8,... To use the 
``LDR rd, [rn, #]`` syntax, we would have to list each memory address by hand. Alternatively, we could loading x's address 
into a register, and then modify that address to access new items. But it is often useful to retain the base address of the 
array, so overwriting our copy of its address may not make sense.

To provide a flexible way to access parts of an array, another form of indicating an address for load and store instructions 
is provided for in ARM:

.. armlisting:: LDR rd, [rn, rm]

   Access the memory at the byte address rn + rm, and store its value into rd. 

   Similar [rn, rm] syntax is available for STR, LDRB, LDRSB, and STRB

If rn holds our base address, then rm can hold our offset - any time we access memory, those values will be added together.

This code sample demonstrates looping through an array using this technique. Note that the 

.. armcode::  

      .data
      @an array of 5 ints
      myArray:     .word   10, 20, 30, 40, 50

      arraySize:   .word   5     @size of myArray


      .text
      _start:
      LDR   r1, =arraySize    @ r1 = &arraySize
      LDR   r1, [r1]          @ r1 = arraySize

      LDR   r2, =myArray      @ load myArray start address
                              @ r2 will always point at array start

      MOV   r3, #0            @ r3 = loop counter
      MOV   r5, #0            @ r5 = bytes into array to current element
      MOV   r4, #0            @ r4 = total

      B     looptest          @ jump ahead to loop test

      loopstart:
      @Calculate address of current element by adding offset r5 to base address
      LDR   r6, [r2, r5]      @ r6 = element at address r2 + r5
      ADD   r4, r4, r6        @ total += current value

      @go to next step
      ADD   r3, r3, #1        @ add one to counter
      ADD   r5, r5, #4        @ add 4 to offset value for "current element"

      looptest:
      CMP   r3, r1            @ Compare counter r3 to size of array in r1
      BLT   loopstart         @ If counter Less Than size, go back to start

      end:
      B     end               @stop here


---------------------------------------------------



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