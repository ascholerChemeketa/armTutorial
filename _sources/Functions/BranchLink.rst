.. include:: ../global.rst


Branch and Link
================================

.. index:: BL, return

In assembly, a function is essentially a set of instructions that we can branch to, run and return from. While the ``B`` instruction is sufficient to jump to a new location before running the next instruction, it does not leave us with any information about how to return to where we were. 

Normally, the ``pc`` register stores the address of where we currently are, so if we want to remember a location, we could copy the ``pc`` into another register or to the stack before changing it. Then, we could use that stored value to return to where we had been. (If the goal was to return after taking a branch, we would actually want to return to the instruction that is just after the branch to avoid immediately branching again.)

Rather than do this process by hand every time we want to call a function, we can use the **branch and link** instruction that automates the process:

.. armListing:: BL label

   Branch and Link: Branches to the memory location identified by label and sets the link register, lr, to the address of the instruction after the BL. 

   To return from the branch, MOV the value in lr to the pc register.

.. figure:: TODO BL??

This code sample demonstrates the operation of the ``BL`` instruction. It twice jumps to the location labeled ``myFunction`` and returns from it. Note that BL sets the ``lr`` register as it executes and ``MOV PC, LR`` jumps back to the stored location.

.. armcode::  
   :linenos:

   /*
      Demonstrates behavior of BL instruction
   */

   .text
   .global _start
   _start:
      @do pointless work
      MOV   r0, r0

      @Branch to myFunction
      @set Link register to address of next line after this
      BL    myFunction

      MOV   r1, r0      @copy r0 to r1
      MOV   r0, #0      @clear r0

      @Branch to myFunction
      @set Link register to address of next line after this
      BL    myFunction

      @stop here
   end:
      B     end


   /*
   * Minimal function that just needs to return to
   * where we came from.
   */
   myFunction:
      MOV   r0, #10     @put 10 in r0
      @return to where we came from by copying the Link Register into the PC
      MOV   PC, LR      @return
