# armTutorial

This is the source code for an interactive ARM v7 assembly tutorial. A live version of the
tutorial can be found here:
http://computerscience.chemeketa.edu/armTutorial/index.html

The goal of the tutorial is to understand assembly well enough to understand how high level code and data
are implemented and develop familiarity with working with assembly and with binary
representations of data.

It is designed for learners who already have basic knowledge of imperative and
object-oriented programming in a high level language. High level code samples are
given in C++, though samples are simple enough that students who know another language
should understand most of what they see.

The tutorial does **not** cover skills related to developing standalone assembly programs or
working with hardware. In the course it was developed for, we typically graduate from the
simulator to real hardware for the end of the course and learn how to do
system calls and build simple full programs.


## Build Instructions

These pages are built using Runestone Components. Start by installing Runestone:
https://github.com/RunestoneInteractive/RunestoneComponents

Once that is done, you should be able to `runestone build` from the main directory of this project.


## Simulator Notes

The tutorial provides interactive samples using web-based ARMv7 simulator:
https://cpulator.01xz.net/doc/
https://cpulator.01xz.net/?sys=arm

The simulator is not open source, but is free to use and the author has explicitly blessed linking to
the simulator from the tutorial.
