.. include:: ../global.rst

Member Functions
==================================    

.. note:: 

   To focus on just the new ideas, all the sample functions will omit 
   PUSHing lr and we will skip building a stack frame and just do all 
   our work in registers.


Member functions in assembly work just like any other function, only 
we need to pass in the address of *this* as an extra parameter. In ARM, 
the convention is to pass *this* in ``r0``. 

Below is a sample implementation of ``int Time::getHour()``. Notice that 
line 11 assumes r0 already has the address of **this**. From our definition 
of the time class, we also know that the *hour* field is 8 bytes into 
the object. So, to access **this->minute** line 11 uses the memory address ``r0 - 8``.

.. armcode::
   :linenos:
   :no-simulator:
   :emphasize-lines: 3, 11, 14

   /*
   int Time::getHour() {
      return this->hour;
   }

   Params:
      r0 = address of this
   */
   Time_getMinute:
      @r0 has address of this object
      LDR   r1, [r0, #-8]  @r1 = this->hour

      @place return value in r0
      MOV   r0, r1

      BX    lr


Because ``r0`` is used for **this**, if the function 
requires normal parameters, they will be in ``r1``, ``r2``,... This sample 
shows an implementation of  ``void Time::setHour(int )``. On line 12, 
we take the value *m* that was passed in using ``r1`` and store it to 
the location of **this->minute** which is ``r0 - 4``


.. armcode::
   :linenos:
   :no-simulator:
   :emphasize-lines: 3, 12

   /*
   void Time::setMinute(int m) {
      this->minute = m;
   }

   Params:
      r0 = address of this
      r1 = m
   */
   Time_setMinute:
      @r0 has address of this object, minute is 4 bytes into this
      STR   r1, [r0, #-4]  @this->minute = r1

      BX    lr


Constructors
----------------------------------

Constructors are nothing more than functions that are expected to initialize 
the members of the object. Our time object might have a no-argument constructor 
that initializes each variable to 0:

.. armcode::
   :linenos:
   :no-simulator:

   /*
   Time::Time() {
      this->second = 0;
      this->minute = 0;
      this->hour = 0;
   }

   Params:
      r0 = address of this
   */
   Time_Time:
      @r0 has address of this object
      MOV   r1, #0
      STR   r1, [r0, #0]   @this->second = 0
      STR   r1, [r0, #-4]  @this->minute = 0
      STR   r1, [r0, #-8]  @this->hour   = 0

      BX    lr

And a constructor that accepts 3 arguments that are used to specify values 
for *hour*, *minute*, and *second*:

.. armcode::
   :linenos:
   :no-simulator:

   /*
   Time::Time(int h, int m, int s) {
      this->second = s;
      this->minute = m;
      this->hour = h;
   }

   Params:
      r0 = address of this
      r1 = h
      r2 = m
      r3 = s
   */
   Time_Time_int_int_int:
      @r0 has address of this object
      STR   r3, [r0, #0]   @this->second = s
      STR   r2, [r0, #-4]  @this->minute = m
      STR   r1, [r0, #-8]  @this->hour   = h

      BX    lr