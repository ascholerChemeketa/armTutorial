.. include:: ../global.rst

Objects in High Level Languages
==================================    

.. index:: objects

When we declare a class in a high level programming language, we define a 
collection of data and some ways to manipulate that data. We write something 
like the **Time** class below to indicate that a Time consists of there
integers and that we can do things with a Time object like change the 
minute value and retrieve the hour value.

.. code:: c++

   class Time {
   private:
      int second;
      int minute;
      int hour;

   public:
      Time();
      Time(int h, int m, int s);
      int getMinute();
      void setMinute(int m);
      void incrHour();
      int getHour();
   };


Every Time has its own data (hours, minutes, seconds), but they all share 
the same functions. There is only one ``Time::getMinute()`` function. The same 
code will execute no matter which Time object we call getMinute on. However, 
the data that code operates on will depend on what object is executing the 
code. In the sample below, we call getMinute() on **time1**, so as the 
``Time::getMinute()`` will be operating on the data of time1.

.. code:: c++

   Time time1(12, 45, 00);
   Time time2(8, 30, 00);
   int x = time1.getMinute();

To access the data of the object that the function was called on, the 
function accesses **this** meaning *"the current object"*. **this** is not 
passed explicitly as a parameter, it is implicit in the way the function 
was called.

.. code:: c++

   int Time::getHour() {
      return this->hour;
   }

