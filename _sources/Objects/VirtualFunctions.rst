.. include:: ../global.rst

Virtual Functions
==================================    

.. index:: virtual functions

We will explore how jump tables are used to implement virtual function 
calls by implementing something similar to this c++ code sample. Note 
that Child extends Parent and that getNum and getBigNum are both 
virtual:

.. code-block:: cpp
   :linenos:

   #include <iostream>

   using namespace std;

   class Parent
   {
   public:
      virtual int getNum() { return 10; }
      virtual int getBigNum() { return 100; }
      int getX() { return x; }
   private:
      int x = 1;
   };

   class Child : public Parent
   {
   public:
      virtual int getNum() { return 5; }
      virtual int getBigNum() { return 5000; }
      int getY() { return y; }
   private:
      int y = 2;
   };


   int main()
   {
      Parent p1;
      Child c1;

      Parent* pp1 = &p1;
      Parent* pp2 = &c1;

      cout << pp1->getNum()    << endl;  //parent version
      cout << pp2->getBigNum() << endl;  //child version
   }


Lines 34 and 35 involve virtual dispatch. We are calling a function on a 
pointer that could be pointing to either a Child or Parent object. To 
enable them to determine which version of getNum or getBigBum to call, we 
need to set up a jump table we can use to load the correct version of 
getNum or getBigNum. A jump table used to determine which virtual 
function to call is known as a **vtables**.

These vtables will each first have the address for getNum, then the address 
for getBugNum. Each class will have its own vtable with pointers for its own 
versions of the functions. But we will always arrange them in the same order. 
Thus, if I have the address of a vtable, I can always know where to look inside 
of it for each function. In the sample below, getNum is the first function 
and getBigNum the second. So we can always load its address + 0 
to find the address of the getNum function and the vtable address + 4 to get 
the the address of the getBugNum function:

.. armcode::
   :no-simulator:

   vtable_for_Parent:
      .word   Parent_getNum      @address of Parent_getNum
      .word   Parent_getBigNum   @address of Parent_getBigNum

   vtable_for_Child:
      .word   Child_getNum       @address of Child_getNum
      .word   Child_getBigNum    @address of Child_getBigNum

   @...

   Parent_getNum:
      MOV   r0, #10
      BX    lr

   Parent_getBigNum:
      MOV   r0, #100
      BX    lr

   Child_getNum:
      MOV   r0, #5
      BX    lr

   Child_getBigNum:
      LDR   r0, =5000
      BX    lr


When assembled, they end up looking something like this:

.. figure:: Images/vtables.png

   The vtable for Parent is at 0xb8. It shows that Parent_getNum is 
   located at address 0x58 and Parent_getBigNum is at 0x60. Child's vtable starts at 
   0xc0. It shows that Child_getNum is at 0x68 
   and Child_getBigNum is at 0x70.

To find the right vtable, every object needs to carry around a pointer to 
the vtable of the class it belongs to. Every Parent object will have a pointer 
to the Parent vtable and every Child object a pointer to the Child vtable. This 
pointer will always be at offset 0 from the start of the object (it will come 
before any member variable data). 

In the memory view shown below, addresses 0xffffffe8-0xffffffec are the storage for 
a Parent object p1, a Child object c1, and two pointers to Parents pp1 and pp2:

.. stackdiagram::
   :no-stack-pointer:

   0xffffffec, pointer pp1 < fp 
   0xfffffff4, pointer pp2
   0x000000c0, Child c1 (vtable)
   0x00000001, Child c1.x
   0x00000002, Child c1.y
   0x000000b8, Parent p1 (vtable)
   0x00000001, Parent p1.x
   ...,
   

Given a call to ``pp2->getBigNum()``, the call would go something like this:

* Load the address pp2 has: **0xfffffff4**.
* We know that the start of that object is the vtable address, so load it: **0x000000c0**
* We know that the getBigNum is always the second function in the vtable 4 bytes in from the start, so load address **0x000000c0 + 4**. 
* 0x000000c4 has the address **0x00000070**. (Refer to the image above) That must be the address of the getBigNum function that goes with this object. 

Notice we are able to find the address for ``Child::getBigNum()`` without ever actually 
knowing what type of object pp2 points at. We just knew to follow 
the pointer, look for the vtable address at the start of the object, then to look for 
the getBigNum function which will always be the second address in the vtable. 

Below is shown the code to do this process assuming memory has already been set up:

.. armcode::
   :no-simulator:

   @r5 = pp2->getBigNum
   LDR   r0, [fp, #-4]  @get address from pp2 (&c1)
   LDR   r1, [r0, #0]   @get &c1 + 0 : the vtable
   LDR   r2, [r1, #4]   @get vtable + 4 : getBigNum
   BLX   r2             @branch with to the address of getBigNum
   MOV   r5, r0         @store return

Notice that this snippet relies on a new instruction ``BLX`` that will branch to 
the address contained in a register (instead of a label defined in the code). This style 
of branch can have its target determined at run time instead of at assemble time. 

.. armlisting:: BLX rd

   Branch and Link eXchange. Branches to the address contained in rd and sets the link 
   register to the address of the next instruction. 

   Used for function calls where the address of the function is in a register. 