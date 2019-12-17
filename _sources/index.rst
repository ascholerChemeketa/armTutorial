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

Samples will sometimes end with an infinite loop: ``end: b end`` - 
this is provided to prevent the simulator from running invalid instructions or data.


Topics
==================================

.. toctree::
   :includehidden:
   :maxdepth: 2

   Basics/index.rst
   Memory/index.rst
   Bitwise/index.rst
   Control/index.rst
   Arrays/index.rst
