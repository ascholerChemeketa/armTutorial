.. include:: global.rst


ARM Tutorial
####################

Introduction
==================================

This reader introduces the basics of ARM v7 assembly. The primary goal is to 
help students who already know how to program in a high level language learn about
the form their programs take after compiling - the kinds of instructions a 
computer really processes information. These materials provide examples of basic ARM instructions,
assembly programming constructs, and how high level languages constructs are represented
in assembly.

Things this reader is NOT: a standalone course - it is a resource for a class; focused on "real" ARM programming - the goal
is to understand how assembly works, not become a working assembly developer.

.. pseudo_h3:: Assumed background knowledge:

* High-level programming experience (preferably C++)
* Basic `binary <http://computerscience.chemeketa.edu/cs160Reader/Binary/index.html>`__ and `data representation in binary <http://computerscience.chemeketa.edu/cs160Reader/DataRepresentation/index.html>`_
* `Boolean logic <http://computerscience.chemeketa.edu/cs160Reader/LogicCircuits/index.html>`_ - AND / OR/ XOR

.. pseudo_h3:: Conventions:

Samples will sometimes end with an infinite loop: 

.. armcode::  
   :no-simulator:

   end:     b  end

This is provided to prevent the simulator from running invalid instructions or data. Often times, this will be omitted for brevity, 
in which case the simulator will report an error after attempting to run past the last instruction. 

All code should start with:

.. armcode::  
   :no-simulator:

   .text                @identifies this is code
   .global _start       @declare _start symbol to be globally visible
   _start:              @identify this location as entry point for the program

It is often omitted as the simulator will assume that it should start at the first line of code it encounters.

Topics
==================================


.. toctree::
   :includehidden:
   :numbered:
   :maxdepth: 2

   Basics/index.rst
   Memory/index.rst
   Bitwise/index.rst
   Control/index.rst
   Arrays/index.rst
   Functions/index.rst
   