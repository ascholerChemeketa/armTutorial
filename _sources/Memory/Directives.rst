.. include:: ../global.rst


Directives and Identifiers
================================

.. index:: directive, identifier


.. pseudo_h2:: Directives

Directives are instructions for the assembler about what to do with the information that comes after them. Directives
always start with a . like: ``.word`` or ``.section``. We can use directives to say things like "here is a word (32-bit pattern) to place into memory":


.. armcode::  

    .word   0xABCDABCD


.. pseudo_h2:: Identifiers

Identifiers are how we name lines of code. They do not become code, they are just labels we can use later on to refer
to a particular piece of data or instruction. Identifiers always need to end with a : and follow normal rules for naming 
things in programming - no spaces or odd characters, first character must be alphabetical - like ``X:`` or ``milesPerHour:`` or ``input1:``.
The identifier may be on the same line as the thing it names or on the preceding line:

.. armcode::  

   @This word of memory can be referred to as X
   X: .word   0xABCDABCD
   
   @This word of memory can be referred to as pattern
   pattern:
   .word   0x12345678
