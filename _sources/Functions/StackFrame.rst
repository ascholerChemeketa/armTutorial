.. include:: ../global.rst


Stack Frames
===============================================

.. index:: stack frame, calling convention

When high level code from a language like C++ is compiled, memory required for local variables needs to be managed as part of the stack. To do this, each function reserves a chunk of memory sufficient to back up necessary registers as well as to store local variables. This chunk of memory is called a **stack frame**. 

To keep track of where data is within the stack frame, functions set up a **frame pointer** - a register that holds the address where the function's stack frame begins. This register is actually ``r11``. ``fp`` is another name for ``r11`` which is reserved for that purpose. 

.. note:: 

   Some times compilers will omit creating a frame pointer and just address relative to the stack pointer. We are going to focus on the full version with a frame pointer.



Because nested function calls will each try to change the ``fp``, we need to back it up as well. As we start a function, we push the current ``lr`` and ``fp`` values so we can restore them at the end of the function. We then set the ``fp`` to hold the address where the start of the stack frame is (the location of the stored value from the ``lr``). Finally, we allocate space by subtracting from the frame pointer enough bytes to reserve the space required for any variables.

.. tabbed:: sample1

   .. tab:: Start

      .. stackdiagram::
         :empty:
            
          , 
          , 
          , 
          , 
          , 

   .. tab:: Push lr, fp

      .. stackdiagram::
            
         lr , 
         old fp  , < sp
          , 
          , 
          , 

   .. tab:: Set fp

      .. stackdiagram::
            
         lr , < fp
         old fp  , < sp
          , 
          , 
          , 

      The frame pointer is set to ``sp + 4`` to make it hold the address of the start of the stack frame.

   .. tab:: Allocate space

      .. stackdiagram::
            
         lr , < fp
         old fp  , 
         first variable  , 
         second variable  ,
         more??? , < sp

      Space is allocated for all needed variables.

   .. tab:: Use stack frame

      .. stackdiagram::
            
         lr , < fp
         old fp  , (fp - 4) 
         first variable  , (fp - 8)
         second variable  , (fp - 12)
         more??? , < sp

      Items can be found relative to the address stored in ``fp``. Assuming all the variables are a machine word in size (4 bytes), the first variable is always at ``fp - 8``, the second at ``fp - 12``, etc...

To tear down the stack, we reverse the process:

.. tabbed:: sample2

   .. tab:: Current stack frame

      .. stackdiagram::
            
         lr , < fp
         old fp  , (fp - 4) 
         first variable  , (fp - 8)
         second variable  , (fp - 12)
         more??? , < sp


   .. tab:: Deallocate space

      .. stackdiagram::
            
         lr , < fp
         old fp  , < sp
         first variable  , 
         second variable  ,
         more??? , 

      The stack pointer is moved to deallocate the space for variables.

   .. tab:: Pop lr, fp

      .. stackdiagram::
         :empty:
            
         lr , 
         old fp  , 
         first variable  , 
         second variable  ,
         more??? , 

      The ``lr`` and ``fp`` are popped, restoring their old values.


When one function calls another, each new function's stack frame is built on top of the last. As a function exits and its stack frame is removed, the stack pointer and frame pointer are used to restore the previous stack frame:

.. tabbed:: sample3

   .. tab:: foo function

      .. stackdiagram::
         
         lr for foo, < fp
         old fp  (for foo's caller),
         first variable for foo , 
         second variable for foo , < sp
          , 
          , 
          , 
          , 
      
   The foo function's stack frame occupies 0xfffffff0-0xfffffffc

   .. tab:: bar is called from foo

      .. stackdiagram::
         
         lr for foo,
         old fp  (for foo's caller),
         first variable for foo , 
         second variable for foo ,
         lr for bar, < fp
         old fp (for foo), 
         first variable for bar , 
         more??? ,  < sp
      
   Bar's stack frame is built on top of foo's. It occupies 0xffffffe0-0xffffffec
   
   .. tab:: bar is called from foo

      .. stackdiagram::
         
         lr for foo,  < fp
         old fp  (for foo's caller),
         first variable for foo , 
         second variable for foo ,  < sp
         lr for bar,
         old fp (for foo), 
         first variable for bar , 
         more??? ,
      
   When bar's stack frame is torn down, the ``sp`` and ``fp`` are restored to their former positions, restoring foo's stack frame.


This sample shows demonstrates a function ``Bar`` that builds a stack frame with space for a parameter 
