.. include:: ../global.rst


ARM Trick - Set Bits
=========================================

.. index:: set bits

Another little trick that ARM assembly allows is for instructions that do arithmetic or logic to set the condition bits 
while calculating their answer. We do this by adding ``S`` to the end of the instruction:

.. armlisting:: xxxS ??, ??, ??

      Set condition bits. Does the instruction xxx but also updates the condition bits depending on the result of the instruction.


Say we want to implement this logic:

.. code:: text

      r1 = r1 - 10
      if( r1 < 0 )
            r1 = 0

Normally, we would subtract 10, then do a comparison, then do a branch or conditional execution of the r1 = 0. Using this trick, 
we can do the following where only two instructions total are needed for the subtraction and if:

.. armcode::  

      MOV      r1, #5         @init r1

      SUBS     r1, r1, #10    @r1 -= 10
                              @Update status flags based on result

      MOVMI    r1, #0         @set r1 to 0
                              @If status flags show MInus (negative)

      MOV      r0, r0         @do nothing... rest of program here

We can do a similar thing to make a counting loop where changing the counter also does the comparison that will help us determine 
whether the loop is done:


.. armcode::  

      MOV      r1, #5         @init r1

      B        loopTest       @branch to test
      loopStart:
      SUBS     r1, r1, #1     @r1--
                              @Set the status flags based on result
      loopTest:
      BPL      loopStart      @branch to start
                              @If status flags indicate PLus (zero or positive)