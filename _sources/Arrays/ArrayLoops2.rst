.. include:: ../global.rst


Array Loop Shifted Index
================================

.. index:: arrays, loops

The loop shown on the last page to loop over an array of words works fine, but uses a lot of registers for book keeping. 
We use one register for the base address of the array, another for the index of the array (to test when we are done), and 
another to keep track of the memory offset. 

But, the index and offset are redundant. For word index 0 the offset will always be 0, for word index 1 the offset will be 4, for 
index 2 the offset will be 8,... The offset is always 4x the index. 

The ARM instruction set provides a trick to avoid storing the index and 4x the index. When we go to use the index of an array 
to load data, we can shift it 2 bits. This effectively multiplies it by 4, turning the value 0 into 0, 1 into 4, 2 into 8, etc...


.. armlisting:: LDR rd, [rn, rm, lsl #]

   Access the memory at the byte address rn + (rm shifted left # bits), and store its value into rd. Typically, we will use 
   a shift of 2 to multiply rm  by 4. 

   Similar [rn, rm, lsl #] syntax is available for STR.


This code sample below demonstrates looping through an array using this technique. It copies data from **myArray** to the empty space 
at **doubled** and doubles each element of the array as it copies it. It is roughly equivalent to:

.. code-block:: c++

   int myArraySize = 5;
   int myArray[5] = {10, 20, 30, 40, 50};
   int doubled[5];

   int i = 0;
   while(i < myArraySize) {
      doubled[i] = 2 * myArray[i];
      i++;
   }

In the assembly version, we hold the base address of the original array in ``r2`` and the 
address of doubled in ``r3``. ``r4`` is the index - to use it to find the offset of an element in an array 
we shift it left 2 bits.


.. armcode::  
   :linenos:
   :emphasize-lines: 14, 15, 23, 28

   .data
   @An array of 5 ints
   myArray:    .word    10, 20, 30, 40, 50
   arraySize:  .word    5        @size of myArray

   doubled:    .space   20       @20 bytes = 5 words


   .text
   _start:
   LDR   r1, =arraySize          @ r1 = &arraySize
   LDR   r1, [r1]                @ r1 = arraySize

   LDR   r2, =myArray            @ load myArray start address
   LDR   r3, =doubled            @ load newArray start address

   MOV   r4, #0                  @ r4 = loop counter

   B     looptest                @ jump ahead to loop test

   loopstart:
   @myArray[i]'s address is r2 + (4 * r4) 
   LDR   r5, [r2, r4, lsl #2]    @ r5 = myArray[i]

   LSL   r5, r5, #1              @double r5

   @doubled[i]'s address is r3 + (4 * r4) 
   STR   r5, [r3, r4, lsl #2]    @ doubled[i] = r5

   @go to next step
   ADD   r4, r4, #1              @ add one to counter

   looptest:
   CMP   r4, r1                  @ Compare counter r4 to size of array in r1
   BLT   loopstart               @ If counter Less Than size, go back to start


   end:
   B     end                     @stop here

