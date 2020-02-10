.. include:: ../global.rst


Stack Frames
===============================================

.. index:: stack frame, calling convention

When high level code from a language like C++ is compiled, memory required 
for local variables needs to be managed as part of the stack. To do this, 
each function reserves a chunk of memory sufficient to back up necessary 
registers as well as to store local variables. This chunk of memory is 
called a **stack frame**. 

To keep track of where data is within the stack frame, we need a fixed 
reference point. The stack pointer can be tricky to use for this as it 
may change during the function if more memory is allocated.  So in ARM, 
functions set up a **frame pointer** - a register that holds the address 
where the function's stack frame begins. By convention, this register 
is ``r11`` - ``fp`` is another name for ``r11``. 

.. note:: 

   Some times compilers will omit creating a frame pointer and just address relative to the stack pointer. We are going to focus on the full version with a frame pointer.


In the same way that nested function calls need to worry about backing 
up the link register, each function is going to want its own value in 
the *fp*. Unlike the *lr*, which each function is responsible for backing 
up on its own, the *fp* is assumed to not be modified by other functions. 
So when a function does want to place a new value in *fp*, it is 
responsible fo backing up the *fp* of the previous function and restoring 
it before returning.

As we start a function, we push the current ``lr`` (this function's 
return address) and ``fp`` (the caller's frame pointer) values so we 
can restore them at the end of the function. We then set the ``fp`` 
to hold the address where the start of the stack frame is. Finally, we 
allocate space for any variables in the function by subtracting from the 
stack pointer enough bytes to reserve the space required.

Here is what the process looks like:

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

To tear down the stack, we reverse the process. We add to the stack pointer 
to deallocate the space reserved for variables, then pop the ``lr`` and ``fp`` to 
restore the values we started with:

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

   .. tab:: foo calls bar

      .. stackdiagram::
         
         lr for foo,
         old fp  (for foo's caller),
         first variable for foo , 
         second variable for foo ,
         lr for bar, < fp
         0xfffffff8 (fp for foo), 
         first variable for bar , 
         more??? ,  < sp
      
      Bar's stack frame is built on top of foo's. It occupies 0xffffffe0-0xffffffec. 
      It stores foo's ``fp`` - 0xfffffff8 - into its stack frame so that it can 
      be restored.
   
   .. tab:: bar returns to foo

      .. stackdiagram::
         
         lr for foo,  < fp
         old fp  (for foo's caller),
         first variable for foo , 
         second variable for foo ,  < sp
         lr for bar,
         0xfffffff8 (fp for foo), 
         first variable for bar , 
         more??? ,
      
      When bar's stack frame is torn down, ``sp`` ends up at the end of foo's 
      stack frame and 0xfffffff8 is popped back into ``fp``, which restores 
      the frame pointer for foo.

      Note that ``fp`` and ``sp`` both end up in the same position they were 
      before bar was called.
