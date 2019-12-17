.. include:: ../global.rst


If Else Implementation
================================

.. index:: if else

You may have noticed that the logic for conditionals in assembly is the reverse of high level languages. In high level languages 
we use conditionals to specify extra code to run under certain circumstances:

.. code-block:: c++

      if(x < 2)
            y = 5;
      //rest of program

In assembly, a branch always skips code. So our branch logic has to be written to decide when to skip a group of instructions, 
not when to run them. Instead of asking "is x less than 2", the compare and branch statement in the code below effectively say 
*"if the value in r1 is greater than or equal to 2 don't set y to 5"*\ :

.. armcode::  
   :linenos:
   :emphasize-lines: 10, 11

      .data
      x:      .word   2
      y:      .word   0

      .text
      _start:
      LDR     r1, =x      @load x's address
      LDR     r1, [r1]    @r1 = x

      CMP     r1, #2      @test r1 vs 2 (calculate r1 - 2)
      BGE     endIf       @branch past "if body" if r1 Not Equal to 2

      @These instructions only executed if r1 was == 2
      MOV     r2, #5
      LDR     r3, =y      @load y's address
      STR     r2, [r3]    @y = 5

      endIf:
      MOV     r0, r0      @do nothing... rest of program here

------------------------------------------------------------

To write an if else in assembly, we generally use the form: 

.. code-block:: text

      test whether to skip to else
      ...if code...
      skip to end else
      else: 
      ...else code...
      endElse:


So this C++:

.. code-block:: c++

      if(x < 2)
            y = 5;
      else
            y = 3;

Would become: 

.. armcode::  
   :linenos:
   :emphasize-lines: 10, 11, 15, 17, 21

      .data
      x:      .word   1
      y:      .word   0

      .text
      _start:
      LDR     r1, =x       @load x's address
      LDR     r1, [r1]     @load x

      CMP     r1, #2       @test x vs 2 (x - 2)
      BGE     else         @branch to else if x Greater or Equal

      @if part
      MOV     r2, #5
      B       endElse      @done with if part... get past else

      else:
      @else part
      MOV     r2, #3

      endElse:
      @done with if/else
      LDR     r3, =y       @load y's address
      STR     r2, [r3]     @y = value set in if/else