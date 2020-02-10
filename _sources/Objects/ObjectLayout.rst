.. include:: ../global.rst

Objects Data
==================================    

Since our Time class consists of three ints, it occupies 3 words or 
12 bytes of memory. If we have:

.. code:: c++

   Time time1(12, 45, 00);

We will need to 
allocate 12 bytes of space in which to store the second, minute, and 
hour. Then, we need to place the 3 words into those bytes in a 
consistent way so that if we need to find the *hour*, we know where to 
look for it.

Here, we have decided to place the *second* variable first, then *minute* 
then *hour*. If we keep track of the address where the data for time1 starts, 
0xfffffffc in this case, we can find *second* at that address, *minute* at 
that address - 4, and *hour* at that address - 8:


.. stackdiagram::
   :no-stack-pointer:
   
   00, address of time1 (time1.second)
   45, address of time1 - 4 (time1.minute)
   12, address of time1 - 8 (time1.hour)

Each Time object will be laid out the same way, so any time we want to find 
the *hour* of a Time, we just need to know where the Time object is located 
and then subtract 8 bytes. These two objects:

.. code:: c++

   Time time1(12, 45, 00);
   Time time2(8, 30, 00);

Would be laid out like this:

.. stackdiagram::
   :no-stack-pointer:
   

   00, address of time1 (time1.second)
   45, address of time1 - 4 (time1.minute)
   12, address of time1 - 8 (time1.hour)
   00, address of time1 (time2.second)
   30, address of time1 - 4 (time2.minute)
   8, address of time1 - 8 (time2.hour)

As long as we keep track that **time1** is at 0xfffffffc and **time2** is at 
0xfffffff0, we can find the members of each object: **time1.minute** is at 
0xfffffffc - 4 = 0xfffffff8. **time2.hour** is at 
0xfffffff0 - 8 = 0xffffffe8. 