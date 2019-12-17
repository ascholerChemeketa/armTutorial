.. include:: ../global.rst


Loops
================================

.. index:: loop

A branch that targets an earlier instruction sets up an assembly loop. In this sample, instruction 4 branches back to instruction 3 
causing an infinite loop that adds 1 to r1.

.. armcode::  
   :linenos:
   :emphasize-lines: 4

      MOV   r1, #0      @init r1

      loopStart:
      ADD   r1, r1, #1   @ r1++
      B     loopStart


To turn this into a counting loop, we can add a conditional branch that checks to see if we should exit the loop. The assembly below is a 
literal translation of:

.. code-block:: text

      r1 = 0
      while(r1 < 5)
            r1++

Lines 4 and 5 check to see if r1 is now greater than or equal to 5. If so, it is time to exit the loop. Otherwise, we add one to r1, and then 
restart the loop:

.. armcode::  
   :linenos:
   :emphasize-lines: 4,5,7

      MOV   r1, #0         @init r1

      loopStart:
      CMP   r1, #5
      BGE   endLoop        @branch to endLoop when r1 >= 5
      ADD   r1, r1, #1     @ r1++  (r1 was < 5)
      B     loopStart      @go back to start of loop

      endLoop:
      MOV   r0, r0         @do nothing... rest of program here


Improving the Counting Loop 
------------------------------------

The sample above requires executing four instructions per loop. Even if we do not take the branch at line 5, we have to execute the instruction.

But, we can rewrite the loop to reduce the amount of work per iteration. The heart of this trick 
if moving the loop test to the end of the loop and having it decide *"do we need to repeat the loop"* instead of *"do we need to exit the 
loop"*. This is done on lines 8 and 9 of the sample below:

To make sure that the loop test is run before executing the body, we jump to the test to begin executing the loop - this is done at line 3. 
Now, every iteration of the loop only requires executing three instructions. If the loop is going to iterate thousands of times, cutting the 
instructions per iteration from four to three could make a significant difference for execution time. So this is the approach compilers take 
when creating a loop.

Improved counting loop:

.. armcode::  
   :linenos:
   :emphasize-lines: 3, 8, 9

      MOV   r1, #0      @init r1

      B     loopTest    @kick start loop by jumping ahead to test

      loopStart:
      ADD   r1, r1, #1  @ r1++
      loopTest:
      CMP   r1, #5      @compare r1 to 5
      BLT   loopStart   @if r1 Less Than 5, go back to loopStart

      MOV   r0, r0      @do nothing... rest of program here
