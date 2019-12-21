.. include:: ../global.rst


Looping Through Arrays
================================

.. index:: arrays, loops

To loop through an array, we need to access successive memory addresses: something like x, x + 4, x + 8, ... To use the 
``LDR rd, [rn, #]`` syntax, we would have to list each memory address by hand. Alternatively, we could load x's address 
into a register, and then modify that address each time we were ready to access the next item. 
But it is often useful to retain the base address of the array, so overwriting our copy of its address may not make sense.

To provide a flexible way to access parts of an array, another form of indicating an address for load and store instructions 
is provided for in ARM:

.. armlisting:: LDR rd, [rn, rm]

   Access the memory at the byte address rn + rm, and store its value into rd. 

   Similar [rn, rm] syntax is available for STR, LDRB, LDRSB, and STRB

If rn holds our base address, then rm can hold our offset - any time we access memory, those values will be added together.

This code sample demonstrates looping through an array using this technique. Note that we calculate the address of items in the array 
on line 24 by adding the base address stored in ``r2`` with the offset stored in ``r5`` and every time through the loop we add 4 to the 
offset (on line 29).

.. armcode::  
   :linenos:
   :emphasize-lines: 24,29

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



Looping over byte arrays
---------------------------


If we are working with bytes of memory, the index (loop counter) and offet will always be the same, so we can use one 
register to represent both. Index 2 will be 2 bytes in, index 5, will be 5 bytes in, etc...

The code sample below totals the values in myArray using a loop. It is just like the sample above except that r3 serves 
as both the array counter (index) and the memory offset for each element. And as we load elements of the array we have to use 
``LDRSB`` to load them as bytes.

.. armcode::  
   :linenos:
   :emphasize-lines: 22

   .data
   @an array of 4 SIGNED bytes
   myArray:       .byte   4, 2, -1, 10
   .align   @make sure we are padded to a full word
   myArraySize:   .word   4

   .text
   _start:
   LDR   r1, =myArraySize     @ r1 = &myArraySize
   LDR   r1, [r1]             @ r1 = myArraySize - it is a word, use LRB

   LDR   r2, =myArray         @ load myArray start address
                              @ r2 will always point at array start

   MOV   r3, #0               @ r3 = loop counter
   MOV   r4, #0               @ r4 = total

   B     looptest             @ jump ahead to loop test

   loopstart:
   @Load array item - it is a byte so use LDRSB
   LDRSB r6, [r2, r3]         @ r6 = element at address r2 + r3 
   ADD   r4, r4, r6           @ total += current value

   @go to next step
   ADD   r3, r3, #1           @ add one to index

   looptest:
   CMP   r3, r1               @ Compare counter r3 to size of array in r1
   BLT   loopstart            @ If counter Less Than size, go back to start

   end:
   B     end                  @stop here
