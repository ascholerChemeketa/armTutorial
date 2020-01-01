.. include:: ../global.rst


Calling Conventions
=====================================

.. index:: calling conventions

As control is transferred from one location to another, we also need to transfer information and coordinate register use. We want to be able to pass parameters to functions and have them return values. As those functions do work, they will be using the same registers that the rest of the program does - we need to make sure that one part of the program does not overwrite an important piece of information stored in a register by another part of the program.

If we were hand coding an entire program in assembly, we could manage registers however we wanted. But keeping track of which ones were in use at every point of a large program would be a complex undertaking. And we generally don't sit down to write an entire program by hand. We use tools to compile code and make use of code that others have written. For arbitrary pieces of code to work together, they can't count on any special knowledge (*\ "I know that register r8 is not being used right now, so I'll put my data there"*\ ). Instead, we need an agreed on set of rules for how to pass information from function to function and who gets to use which registers. 

**Calling conventions** are the rules for how functions transmit information and use registers and memory. They will necessarily differ between architectures (ARM and Intel have different registers available) but also may differ between operating systems and even different compilers for the same platform. We will focus on the calling conventions generally used in ARM v7 by the GNU C/C++ compiler - they are a fairly representative set of rules.

In general, register 0-9 are used for program data. r0-r3 are used for temporary storage and information passing. There is never any expectation that other code will preserve values in these registers. r4-r9 are used for longer term storage and functions are expected to not destroy values in them: 

Register Use:
---------------------

.. csv-table::
   :header: "Register(s)", "Use"
   :widths: 20, 50
   :class: "register-table"

   **r0 - r3**, Parameters and return values. |br|  Also used for temporary values - any function can change these at will.
   **r4 - r9**, Stored values. Any values stored in these must be preserved by functions.
   **r10 - r15**, Special purpose. These have assigned roles (like **pc** or **lr**). Not all the roles are always used.

The stack is used to back up  the values in registers when needed as well as for situations too complex for the normal conventions (like passing more than 4 parameters to a function). When a value needs to be preserved so a register can be reused for a new job, we push the old value to the stack and then later pop it off to restore it.

