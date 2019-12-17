.. include:: ../global.rst



Immediate Values
=====================

.. index:: immediate

The **immediate** value is a literal number baked into the bits of an instruction. For example, here is the machine code for ``MOV r1, #5``:

.. bitpattern::
   :emphasize-bits: 0-3, 12-15
   :inhex:

   E3A01005

The bits for r1 (0001) and 5 (0101) can be seen in the resulting instruction. The #5 is literally part of the instruction. 

However, since the immediate is part of the instruction, and the entire instruction needs to be 32 bits, there is a limited space for it. 
If we look at the ARM instruction reference, is shows that MOV instructions look like this: 

.. raw:: html

   <table class="bit-table"><tbody><tr><th>31</th><th>30</th><th>29</th><th>28</th><th>27</th><th>26</th><th>25</th><th>24</th><th>23</th><th>22</th><th>21</th><th>20</th><th>19</th><th>18</th><th>17</th><th>16</th><th>15</th><th>14</th><th>13</th><th>12</th><th>11</th><th>10</th><th>9</th><th>8</th><th>7</th><th>6</th><th>5</th><th>4</th><th>3</th><th>2</th><th>1</th><th>0</th></tr>
   <tr class="bitsrow">
   <td class=" left-border" colspan='4'>cond</td>
   <td class=" left-border" colspan=2'>0 0</td>
   <td class=" left-border"colspan='1'>op</td>
   <td class=" left-border" colspan='4'>op 1</td>
   <td class=" left-border">s</td>
   <td class=" left-border" colspan='4'>0 0 0 0</td>
   <td class=" left-border"  colspan='4'>rd</td>
   <td class=" left-border right-border highlight" colspan='12'>imm12</td>
   </tr>
   </table>

The last 12 bits are the immediate bits. Normally, 12 bits would allow us to store a value up to 4096. However, it is quite possible that we would 
like to have a larger value as an immediate, so the value is not stored as a plain 12-bit number. 
Instead, it is stored as an 8-bit number with a 4-bit shift amount:

.. raw:: html

   <div style="width: 80%; max-width: 500pt;">
   <table class="bit-table" style="width: 38%; margin-left: auto; margin-right: 0px;"><tbody><tr><th>11</th><th>10</th><th>9</th><th>8</th><th>7</th><th>6</th><th>5</th><th>4</th><th>3</th><th>2</th><th>1</th><th>0</th></tr>
   <tr class="bitsrow">
   <td class=" left-border"  colspan='4'>rotate</td>
   <td class=" left-border right-border" colspan='8'>value</td>
   </tr>
   </table>
   </div>


To calculate the actual value an immediate represents, we:

* Take the shift amount as a binary value and double it
* Rotate the value bits to the right the doubled shift, wrapping as needed
* Read the resulting binary value

For example, ``MOV r1, #41728`` looks like this:

.. bitpattern::
   :emphasize-bits: 0-11
   :inhex:

   E3A01CA3

CA3 is not 41,728. Instead, those three hex chars should be interpreted as a rotation of 24 (2 * C) done to 10100011 (A3):

.. raw:: html

   <div style="width: 80%; max-width: 500pt;">
   <table class="bit-table" style="width: 38%; margin-left: auto; margin-right: 0px;"><tbody><tr><th>11</th><th>10</th><th>9</th><th>8</th><th>7</th><th>6</th><th>5</th><th>4</th><th>3</th><th>2</th><th>1</th><th>0</th></tr>
   <tr class="bitsrow">
   <td class=" left-border"  colspan='4'>1100</td>
   <td class=" left-border"  colspan='4'>1010</td>
   <td class=" right-border" colspan='4'>0011</td>
   </tr>
   <tr class="hexrow">
   <td class=""  colspan='4'>C</td>
   <td class=""  colspan='4'>A</td>
   <td class="" colspan='4'>3</td>
   </tr>
   </table>
   </div>

To decode the immediate, we take the pattern A3:

.. bitpattern::
   :emphasize-bits: 0-7
   :inhex:
   :nohex:

   A3

And rotate it 24 bits to the right (which is the same as 8 bits to the left), which produces this pattern which equals 41,728:

.. bitpattern::
   :emphasize-bits: 8-15
   :inhex:
   :nohex:

   A300

---------------------------------

This scheme means not all binary patterns can be represented. We can only represent patterns that require 8-bits of significant digits 
(the first to last 1 must span over no more than 8 bits). And because we double the rotate bits, the final rotation amount must always 
be an even number of bits.

In practical terms, we can use a wide range of values as immediate, including some large values. But there will be values that can't be 
represented and result in an error if we try to use them. To work with values that do not fit as an immediate, we will have to build them 
up in multiple steps or load them into a register from memory.

.. armcode::  

   @Legal - requires a rotate
   MOV   r1, #41728

   @Legal - requires rotating FF
   MOV   r2, #0xFF0000

   @Legal - no rotate required for values < 256
   MOV   r2, #0xA0

   @Illegal - can't be represented - comment out to fix
   MOV   r2, #10000


.. tip:: 

   The error message *Error: invalid constant after fixup* tells you you have an illegal immediate value. 