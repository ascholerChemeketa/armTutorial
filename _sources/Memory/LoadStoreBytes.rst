.. include:: ../global.rst


Loading & Storing Bytes
================================

.. index:: LDRB

Sometimes, we don't want a whole word of memory - we just want to access a single byte. To do this, we use the ``LDRB`` instruction:

.. armlisting::  LDRB rd, [rn]

   Load Register Byte. Load rd with the byte of memory at the location stored in rn. The upper 3 bytes of the register will be zeroed out.

Say we load 0xFF into a register - we would end up with:

.. bitpattern::
   :emphasize-bits: 0-7
   :inhex:

   FF

That would be the correct value if that 0xFF is just a bit pattern or if it represented an unsigned number (255). However, if that 8-bit pattern 
is being used to represent a signed value, we have a problem. 0xFF is -1. But 0x000000FF is 255. To get the correct 32-bit value, we need to **sign extend** 
the byte as it is loaded. We need to copy the most significant bit from the byte (bit 7) into bits 8-31:

.. bitpattern::
   :emphasize-bits: 7-31
   :inhex:

   F-

Any positive 8-bit signed value will start with a 0. So when it gets sign extended, bits 8-31 get 0's. Here is 100, hex 0x64, getting sign extended:

.. bitpattern::
   :emphasize-bits: 7-31
   :inhex:

   64

.. index:: LDRSB

To handle loading with sign extension, there is an alternative load byte instruction:

.. armlisting::  LDRSB rd, [rn]

   Load Register Signed Byte. Load rd with the byte of memory at the location stored in rn. All the digits in the upper three bytes will be 
   filled with the most significant bit from the byte loaded. (It will be sign extended.)


.. tip::

   We still use LDR to load the byte's address. Then we use LDRB to load an 8-bit value that is either unsigned or not a number, or LDRSB to load 
   an 8-bit signed number.


.. armcode::  

   .data
   b:   .byte   34   @ 0x22
   c:   .byte   -1   @ 0xFF
   d:   .byte   0    @

   .align

   .text
   LDR   r3, =b      @r3 <- address of b
   LDRB  r3, [r3]    @r3 <- b

   LDR   r4, =c      @r4 <- address of c
   @INCORRECT - load negative value as unsigned:
   LDRB  r4, [r4]    @r4 <- 0x000000FF = 255!!!

   LDR   r4, =c      @r4 <- address of c
   @CORRECT - load negative value as signed:
   LDRSB r4, [r4]    @r4 <- 0xFFFFFFFF = -1



Storing Bytes
--------------------------------

.. index:: STRB

To store just a single byte, we yse the ``STRB`` instruction. It writes 8-bits of memory, leaving any neighboring bytes unchanged. 
Because we are going from a 32-bit value (the register), to an 8-bit block of memory, there is no need for a separate signed version - 
bits 8-31 are just chopped off as the value is written. (Which does mean that if the register held a value too large to represent with 
8 bits, the wrong value will be written to memory.)

.. armlisting::  STRB rs, [rn]

   Take the lower byte from rs (bits 0-7) and store it to address rn.

This code sample adds one to the value a in memory by loading it, incrementing the value, then writing it back:

.. armcode::  

   .data
   a:   .byte   6    @ 0x06
   
   .align

   .text
   LDR      r1, =a         @r1 <- address of a
   LDRSB    r2, [r1]       @r2 <- a

   ADD      r2, r2, #1     @r2 <- a + 1
   STRB     r2, [r1]       @a  <- r2
