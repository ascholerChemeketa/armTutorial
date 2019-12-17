.. include:: ../global.rst


Conditional Branches
================================

.. index:: branch; conditional


.. index:: condition codes

To use the condition bits in the ``CPSR``, we can use **condition codes** that correspond to various logical combinations 
of the bits. Here are the most common codes:

.. csv-table:: 
   :header: "Code", "Meaning", "Bits"
   :widths: 10, 35, 30
   :class: "list-table"

   **EQ** , Equal, Z set
   **NE** , Not Equal, Z clear 
   **GE** , Greater or Equal, N and V both set or both clear
   **LT** , Greater Than, N set and V clear OR N clear and V set
   **GT** , Greater Than, Z clear AND either N set and V clear or N clear and V set
   **LE** , Less or Equal, Z set OR N set and V clear OR N clear and V set

.. tip:: 

      You are not responsible for memorizing the bits associated with each code. Focus on making sure you recognize the codes.

There are also some less common codes:

.. csv-table:: 
   :header: "Code", "Meaning", "Bits"
   :widths: 10, 30, 30
   :class: "list-table"

   **MI** , Negative (MInus), N set 
   **PL** , Positive or zero (PLus), N clear
   **VS** , Overflow, V set
   **VC** , No overflow, V clear
   **HI** , Unsigned higher, C set and Z clear
   **LS** , Unsigned lower or same, C clear or Z set
   **CS** , Unsigned higher or same, C set
   **CC** , Unsigned lower, C clear


These codes can be added to a ``B`` instruction to modify the circumstances under which it branches. 
Like  ``BEQ`` for "branch if equal" or ``BGT`` for "branch if greater than". 

The ARM sample below uses a conditional branch to approximate this C++ code:

.. code-block:: c++

      if(x == 2)
            y = 5;


On line 10, the assembly does a comparison between r1, where x has been loaded, and 2. Then, on line 11, the branch checks the condition bits 
set by that operation. If they indicate that the values were not equal to each other, it skips down to the label on line 18. If the 
values were equal, it continues on after line 11 to the next instruction at 14.


.. armcode::  
   :linenos:
   :emphasize-lines: 10, 11, 18

      .data
      x:      .word   2
      y:      .word   0

      .text
      _start:
      LDR     r1, =x      @load x's address
      LDR     r1, [r1]    @r1 = x

      CMP     r1, #2      @test r1 vs 2 (calculate r1 - 2)
      BNE     endIf       @branch past "if body" if r1 Not Equal to 2

      @These instructions only executed if r1 was == 2
      MOV     r2, #5
      LDR     r3, =y      @load y's address
      STR     r2, [r3]    @y = 5

      endIf:
      MOV     r0, r0      @do nothing... rest of program here


.. warning::

      Before using the comparison codes, you need to do a comparison to set the condition bits!