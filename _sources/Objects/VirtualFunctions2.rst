.. include:: ../global.rst

Virtual Functions Sample
==================================    

.. index:: virtual functions

Below is the full listing to implement virtual function calls in a code 
sample designed to emulate the c++ shown on the previous page. Notice that 
the "constructors" for Parent and Child store the address of the appropriate 
vtable into the object as it is constructed (lines 141 and 159).

.. armcode::
   :linenos:
   :emphasize-lines: 13-15, 29-31, 141, 159

   .data
   /*
   Parent structure:
      8 bytes total space
         address - 4 : x
         address + 0 : vtable

   VTable:
      0 : Parent_getNum
      4 : Parent_getBigNum
   */

   vtable_for_Parent:
      .word   Parent_getNum
      .word   Parent_getBigNum

   /*
   Child structure:
      12 bytes total space
         address - 8 : y
         address - 4 : Parent.x
         address + 0 : vtable

   VTable:
      0 : Child_getNum
      4 : Child_getBigNum
   */

   vtable_for_Child:
      .word   Child_getNum
      .word   Child_getBigNum


   .text

   /*
   Translation of:

   Parent p1;
   Child c1;

   Parent* pp1 = &p1;
   Parent* pp2 = &c1;

   cout << pp1->getNum()    << endl;  //parent version
   cout << pp2->getBigNum() << endl;  //child version

   Stack in main:
   -------------------------------
   FramePointer
   Relative
   Address       Contents
   -------------------------------
      -20     = Parent p1
      -8     = Child c1
      -4     = pp2
   fp +  0     = pp1

   */

   _start:
      @Set FP to bottom of empty space
      SUB   fp, sp, #4
      @Allocate space on the stack for Child, Parent, 2 pointers
      SUB   sp, sp, #28

      @Parent p1
      SUB   r0, fp, #20    @calculate p1's address to r0
      BL    Parent_Parent

      @Child c1
      SUB   r0, fp, #8     @calculate c1's address to r0
      BL    Child_Child

      @pp1 = &p1
      SUB   r0, fp, #20    @calculate p1's address to r0
      STR   r0, [fp]       @store to pp1

      @pp2 = &c1
      SUB   r0, fp, #8     @calculate c1's address to r0
      STR   r0, [fp, #-4]  @store to pp2

      @r4 = pp1->getNum
      LDR   r0, [fp]       @get address from pp1 (&p1)
      LDR   r1, [r0, #0]   @get &p1 + 0 : the vtable
      LDR   r2, [r1, #0]   @get vtable + 0 : getNum
      BLX   r2             @branch with address in r2
      MOV   r4, r0         @store return

      @r5 = pp2->getBigNum
      LDR   r0, [fp, #-4]  @get address from pp2 (&c1)
      LDR   r1, [r0, #0]   @get &c1 + 0 : the vtable
      LDR   r2, [r1, #4]   @get vtable + 4 : getBigNum
      BLX   r2             @branch with address in r2
      MOV   r5, r0         @store return

      ADD   sp, sp, #28    @remove space for local variables

   end:
      B     end



   /*
   Simple implementation - no stack - just return 10
   */
   Parent_getNum:
      MOV   r0, #10
      BX    lr

   /*
   Simple implementation - no stack - just return 100
   */
   Parent_getBigNum:
      MOV   r0, #100
      BX    lr


   /*
   Simple implementation - no stack - just return 5
   */
   Child_getNum:
      MOV   r0, #5
      BX    lr

   /*
   Simple implementation - no stack - just return 5000
   */
   Child_getBigNum:
      LDR   r0, =5000
      BX    lr

   /*
   Simple implementation - no stack
   Sets up vtable and initializes x

   r0 = this
   */
   Parent_Parent:
      @setup vtable at this + 0
      LDR   r1, =vtable_for_Parent  @vtable address
      STR   r1, [r0, #0]            @store to this + 0
      MOV   r1, #1
      STR   r1, [r0, #-4]           @store 1 to this.x (this - 4)
      BX    lr

   /*
   Simple implementation - only saves lr to stack
   Calls parent constructor, then overides vtable and inits y

   r0 = this
   */
   Child_Child:
      PUSH  {lr}
      @setup parent part of this object
      BL    Parent_Parent

      @change vtable address to be one for Child class
      LDR   r1, =vtable_for_Child   @vtable address
      STR   r1, [r0, #0]            @store to this + 0
      MOV   r1, #2
      STR   r1, [r0, #-8]           @store 2 to this.y (this - 8)

      POP  {lr}
      BX    lr
