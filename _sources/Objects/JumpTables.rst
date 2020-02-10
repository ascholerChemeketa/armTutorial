.. include:: ../global.rst

Jump Tables
==================================    

.. index:: jump table

A **jump table** is a structure that holds a list of function addresses. 
Each entry in the table corresponds to a different job that might need 
to be done and holds the address of the code that will handle that job. 

Below is what a three entry jump table might look like. There are 
locations for three addresses at 0x100000, 0x100004, and 0x100008 that 
would correspond to three jobs we want to be able to do. (Job A, B, and C). 

To do Job A, we would look at the address ``table + 0`` 
get the address stored there (0x100014), then jump to that location, and  
execute the instructions we find - the code for **function1**. 
To do Job B, we will look at address ``table + 4``, find 0x100034, 
jump to that location, and execute the code we find - that for **function3**.

.. stackdiagram::
   :start-address: 0xffffc
   :no-stack-pointer:
   :buildup:   

   !, 0x100014, table[0] = Job A = function1
   !, 0x100034, table[1] = Job B = function3
   !, 0x100020, table[2] = Job C = function2
   ...
   ... 
   Code for function1
   ...
   ...
   Code for function2
   ...
   ...
   ...
   ...
   Code for function3
   ...
   ...
   ... 


We can use this approach even if we don't know at compile time what function 
we will want to execute for a particular job. If we don't know what code we 
will want to run, we can't set up a direct branch to it. 

The jump table allows us to say *"I don't know where I will be branching too, 
but I know the address I need will be stored in the jump table"*. Our code can 
be written to go load that address and branch to it, even if we don't know what 
it will be. Other code can modify the jump table to make sure that at run time 
the jump table if filled with the correct addresses. 

This approach is used in many places where such flexibility is needed. 
Processors use this technique to handle exceptions - they automatically load 
a value stored at a known address and then branch to the location named by 
that value. The operating system or program running on the hardware has the 
responsibility for providing code to handle such exceptions and making sure 
that the address of their functions are loaded into the correct locations in 
the jump table. It is also used to implment virtual function calls.