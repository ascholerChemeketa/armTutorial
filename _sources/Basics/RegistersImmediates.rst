.. include:: ../global.rst



Instruction format
=================================

.. index:: immediate, register

ARM instructions generally take the form:
  
.. armlisting::  ADD rd, rn, #

Things like **rd** or **rn** are shorthand for **register**. They may normally be any of the 
general purpose registers like r1, r2, r3,.... **rd** stands for "destination" register -
it is typically the register that gets modified by the instruction. The other letters, like n or m in rn or rm 
are meaningless placeholders. It is usually possible for the destination register to be the same as one (or multiple) of the source registers.

The **#** stands for an **immediate** value - a literal number. Litterals always start with a # and may be written as:

* Signed integers : #10, #-5
* Hexadecimal values : #0xFF
* Binary values : #0b110
* ascii chars : #'A'

Samples:

.. armcode::

    ADD     r1, r1, #10
    ADD     r3, r4, #0xFF
    ADD     r5, r5, #0b11111111
    ADD     r6, r6, #'A'

-----------


Comments
------------------------------------------------

Multiline comments are surrounded by /\* \*/ and single line comments start with @:

.. armcode::  

    /* This is a 
       multiline comment 
    */

    ADD     r1, r2, #10  @line comment
    @line comment
    ADD     r1, r2, #10 