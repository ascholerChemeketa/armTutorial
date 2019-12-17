.. include:: ../global.rst


Clearing
=====================

.. index:: BIC, clear

Clearing bits is the opposite of masking. Instead of wanting to keep certain bits, we want to 0 out specific 
bits while keeping other ones. For instance, we might want to clear out bits 25-29 from this pattern:

.. bitpattern::
   :emphasize-bits: 25-29
   :inhex:

   1BADDEED

To do so, we could mask by ANDing with this pattern:

.. bitpattern::
   :emphasize-bits: 0-24, 30-31
   :inhex:

   C1FFFFFF

Bits 25-29 would become 0 and everything else would remain as is. 
However, that pattern is too complex to represent as an immediate. Any time we are trying to clear a small number of bits, 
we will have a similar problem of needing a large mask to AND with.

Instead, we can use the bitwise clear instruction - it uses a pattern to specify which bits to clear (ANDing with a pattern specifies 
which bits to keep).


.. armlisting::  BIC rd, rn, rm / #

   BIt Clear. Take the pattern from rn, clear out the bits that are 1 in either register rm or immediate #, place the results in rd.


.. armcode::  

   LDR   r5, =0x1BADDEED
   
   @Clear bits 25-29
   BIC   r6, r5, #0b111         @or #0x7

   @Clear bits 16-31 (first two bytes)
   BIC   r7, r5,  #0xFF000000   @clear first byte
   BIC   r7, r7,  #0x00FF0000   @now clear second
