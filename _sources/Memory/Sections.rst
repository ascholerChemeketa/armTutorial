.. include:: ../global.rst


Sections
================================

.. index:: section


Assembled code is broken into logical sections that are used in different ways. The bits that represent instructions must be 
executable but should generally not be writable. The bits that represent data should be readable and writable but may not make
sense to execute. 

Some common sections:

* **text** stores the code of the program
* **data** stores global data that can be read or written
* **rodata** stores global information that is Read Only (constants)
* **bss** has uninitialized blank space that we have reserved for use by the program to store data

Directives are used to specify what section various parts of an assembly program belong to:

.. armcode::  

   .section       .data
   myGlobal:      .word   0xC

   .section       .rodata
   MY_CONSTANT:   .word   0x64

   .section       .bss
   uninitializedGlobal:   .space  4

   .text
   .global _start
   _start:
   @Do nothing...
   MOV   r1, #0

   end:  b end       @stop program

That code gets build into what is shown below. Some things to note:

* The sections appear in a specific order: ``text``, ``rodata``, ``data``, then ``bss``.
* Sections may be **padded** with extra 0's to make them occupy a number of bytes that is some specific power of 2. We can see this below at the end of the .data, .bss. and .rodata sections: they have all been padded so that the next section starts at an address that is a multiple of 8.


.. image:: Images/sections.png


.. note:: 

    Most of the time, this tutorial will stick to using just using ``.data`` for 
    all data and ``.text`` for the code. We will generally not use ``.rodata`` or ``.bss``.