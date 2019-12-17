.. include:: ../global.rst


Masking
=====================

.. index:: mask

Masking is the process of using bitwise operations to isolate part of a binary pattern. As an example, here are the
bits that represent the ARM machine code for ``ADD r1, r2, r3``. Bits 12-15 have the destination register:

.. bitpattern::
   :emphasize-bits: 12-15
   :inhex:

   E0821003

To isolate that register from the pattern, we could ``AND`` with 0xF000 (hex for 1111 0000 0000 0000):

.. bitpattern::
   :emphasize-bits: 12-15
   :inhex:

   F000

The bits that were ANDed with 1, will retain their value. The bits that were ANDed with 0, are forced to 0:

.. bitpattern::
   :emphasize-bits: 12-15
   :inhex:

   1000


Recall that immediates can generally be no more than two consecutive hex chars padded with 0s (like 0xFF or 0xA4000 but not 0xF00F 
where the two non-zero chars are spaced out). Those patterns can be masked directly with an AND. Larger patterns must be built up in a register before 
being used as a mask:

.. armcode::  

   LDR   r5, =0x1BADDEED

   @isolate bits 0-7 (last byte: 0xED)
   @ & means bitwise OR
   AND   r6, r5, #0xFF        @r6 = 0x1BADDEED & 0x000000FF = 0x000000ED


   @isolate bits 8-15 (next to last byte: 0xDE)
   AND   r7, r5, #0xFF00      @r7 = 0x1BADDEED & 0x0000FF00 = 0x0000DE00


   @isolate bits 16-27 (0xBAD from 0x1BADDEED)
   @ want pattern 0x0FFF0000, but that takes too many bits to represent, so build it
   MOV   r8, #0x00FF0000      @Start with 00FF0000
   ORR   r8, r8, #0x0F000000  @r8 = 00FF0000 | 0F000000 = 0FFF0000
   AND   r8, r5, r8           @r8 = 0x1BADDEED & 0x0FFF0000 = 0x0BAD0000


   @isolate bits 2-5 : 0x3C == 0011 1100
   @                   0xED == 1110 1101
   @                 result == 0010 1100 = 0x2C
   AND   r8, r5, #0x3C        @r8 = 0x1BADDEED & 0x0000003C = 0x0000002C

----------------------------------

A mask leaves the bits in their original location. If we want to use the masked value as a number, we would have to shift its 
bits so the leftmost one is aligned with the 0 bit.

If our goal is to end with the desired bits aligned to the right of the register, it may be simpler to just use a pair of shifts 
to clear extra bits and align the ones we want with bit 0. As an example, we will isolate bits 12-15 in the pattern below and align 
them with bit 0:

.. bitpattern::
   :emphasize-bits: 12-15
   :inhex:

   E0821003

First we need to clear out everything past bit 15. We can do this by left shifting by 16 bits:

.. bitpattern::
   :emphasize-bits: 28-31
   :inhex:

   10030-

Then, we shift back to the right. There are 32 total bits, and we want to preserve just 4. So shift right 28 bits:

.. bitpattern::
   :emphasize-bits: 0-3
   :inhex:

   1


.. armcode::  

   LDR   r5, =0xE0821003

   @isolate bits 12-15 using just shifts
   LSL   r9, r5, #16          @r9 = 0x10030000
   LSR   r9, r9, #28          @r9 = 0x00000001

   LDR   r6, =0x1BADDEED
   @isolate bits 16-27 (0xBAD from 0x1BADDEED) using just shifts
   LSL   r10, r6, #4          @r10 = 0xBADDEED0
   LSR   r10, r10, #20        @r10 = 0x00000BAD