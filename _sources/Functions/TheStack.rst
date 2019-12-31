.. include:: ../global.rst


The Stack
================================

.. index:: stack

The stack is a region of memory typically used by compilers for managing the memory required by functions within a program. It is used by compilers to allocate space for local variables in functions, other book keeping information (like where a function returns to), and to store values from registers when we need to use that register for some new purpose.

The stack gets its name because of the way memory is allocated within it. Memory is never added or removed from the middle of the stack - it is strictly managed by adding or removing to the top. When memory is required, space is allocated at the top of the stack. When that memory is no longer required, it is removed from the stack. 

A register is used to keep track of the memory address for the top of the stack. ``TODO`` is usually referred to as the ``sp`` or **stack pointer**. Although programs are free to use this register for any purpose, it is assumed that it will be used to track the top of the stack. When a program starts up, the stack pointer will` be initialized to a memory address where the program can start building the stack. In the simulator, when we load any program, the ``sp`` is set to TODO:

.. figure:: TODO

.. tip::

   Different environments will have different initial addresses for the top of the stack. When you are programming on real Linux hardware, do not assume it will use the same address for the stack.


In most implementations, the stack actually grows down in memory - the bottom of the stack is the highest address in the stack and the top of the stack is the lowest address. When we refer to the **top** of the stack, we will be talking about the lowest memory address. This is called a **descending** stack. (We will not be looking at the alternative: **ascending** stack.)


Working with the stack
------------------------------------

The ``sp`` always points to the top byte of memory on the stack (which is the lowest memory address). Thus, to add memory to the stack, we first have to subtract the number of bytes desired from the ``sp`` to find the address of the new memory. When we are done with memory and are ready to remove it from the stack, we add a number of bytes to the ``sp``. The stack is most commonly used to store register values. Since each register is 4 bytes, we typically add or subtract 4 from the ``sp``.

To actually load and store the values from memory, we use ``LDR`` and ``STR`` just like we were accessing any other data in memory. This sample demonstrates storing the values from ``r1`` and ``r2`` to the stack, then wiping out the registers, before restoring them from memory. Note that we add ``r1`` and then ``r2``, meaning that ``r2`` is on the top of the stack (lowest memory address). When we go to remove them, we have to start with the top of the stack - we have to remove ``r2`` before ``r1``.

TODO TABS

.. stackdiagram::
   :empty:

    ,
    ,


.. stackdiagram::

    , < sp
    , 


.. stackdiagram::

   r1 , < sp
    , 


.. stackdiagram::

   r1 ,
    , < sp


.. stackdiagram::

   r1 ,
   r2 , < sp


As we restore values from the stack to registers, we add to ``sp`` to remove words from the stack. The values that were placed in memory remain there, but we no longer consider them to be part of the stack and will reuse the space they are in next time we add something to the stack.

TODO TABS

.. stackdiagram::

   r1 ,
   r2 , < sp

.. stackdiagram::

   r1 , < sp
   r2 , 
   
.. stackdiagram::
   :empty:

   r1 ,
   r2 ,





.. tip::

   Stacks always work in a Last In, First Out (LIFO) fashion. You must remove things in the opposite order you add them.

.. armcode::  

   .text 
   .global _start
   _start:
   @Some initial values
   MOV   r1, #0xAA
   MOV   r2, #0xBB

   @Store r1 to the stack
   SUB   sp, sp, #4     @Move stack pointer down 4 bytes
   STR   r1, [sp]       @Copy r1 to that address

   @Store r2 to the stack
   SUB   sp, sp, #4     @Move stack pointer down 4 bytes
   STR   r2, [sp]       @Copy r2 to that address

   @Wipe out registers
   MOV   r1, #0x0
   MOV   r2, #0x0

   @r2 is at the top of the stack, it must be removed before r1
   LDR   r2, [sp]       @Restore r2 from stack
   ADD   sp, sp, #4     @Move stack pointer up 4 bytes

   @restore r1 from stack and remove it
   LDR   r1, [sp]       @Restore r1 from stack
   ADD   sp, sp, #4     @Move stack pointer up 4 bytes


TODO MEMORY IMAGES