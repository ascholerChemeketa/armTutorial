.. include:: ../global.rst


Branch
================================

.. index:: B, branch

The unconditional branch instruction allows us to skip to a new location to continue executing code from. When the branch executes, the 
program counter is not increased by 4 bytes as normal, but instead its value is replaced with the address of a new instruction.


.. armlisting::  B label

   Branch. Change the program counter to the address of the line identified by label.

In this code sample, line number 3 has a branch that will cause execution to skip over the code on lines 4 and 5 and execute the next line 
after the label ``target``, which is line 7.

.. armcode::  
   :linenos:
   :emphasize-lines: 3

      MOV   r1, #1    @random work
      MOV   r2, #2 
      B     target    @branch to target
      MOV   r3, #3    @skipped
      MOV   r4, #4    @skipped
   target:
      MOV   r5, #5

----------------------------------------------

The assembler calculates the destination address and stores it in the instruction as +/- value to add to the ``PC`` register when the branch executes. 
This offset is stored as 24-bits in the instruction:

.. raw:: html

   <table class="bit-table"><tbody><tr><th>31</th><th>30</th><th>29</th><th>28</th><th>27</th><th>26</th><th>25</th><th>24</th><th>23</th><th>22</th><th>21</th><th>20</th><th>19</th><th>18</th><th>17</th><th>16</th><th>15</th><th>14</th><th>13</th><th>12</th><th>11</th><th>10</th><th>9</th><th>8</th><th>7</th><th>6</th><th>5</th><th>4</th><th>3</th><th>2</th><th>1</th><th>0</th></tr>
   <tr class="bitsrow">
   <td class=" left-border" colspan='4'>cond</td>
   <td class=" left-border" colspan='3'>101</td>
   <td class=" left-border" colspan='1'>L</td>
   <td class=" left-border right-border" colspan='24'>24-bit offset</td>
   </tr>
   </table>

Since instruction addresses in ARM are always multiples of 4, the last two bits of any instruction address are always 00. This fact is used to compress 
the stored offsets - the value stored in the instruction has been right shifted 2 bits to remove those 0s. To use the stored address, the hardware first 
shifts it to the left 2 bits and then sign extends it. For example, in the code sample above, the instruction looks like:

.. bitpattern::
   :emphasize-bits: 0-24
   :inhex:

   EA000001

If we mask the last 24 bits and then shift them left 2 and sign extend, we get:

.. raw:: html

   <table class="bit-table"><tbody><tr><th>31</th><th>30</th><th>29</th><th>28</th><th>27</th><th>26</th><th>25</th><th>24</th><th>23</th><th>22</th><th>21</th><th>20</th><th>19</th><th>18</th><th>17</th><th>16</th><th>15</th><th>14</th><th>13</th><th>12</th><th>11</th><th>10</th><th>9</th><th>8</th><th>7</th><th>6</th><th>5</th><th>4</th><th>3</th><th>2</th><th>1</th><th>0</th></tr>
   <tr class="bitsrow">
   <td class=" left-border" colspan='1'>0</td>
   <td class=" left-border" colspan='1'>0</td>
   <td class=" left-border" colspan='1'>0</td>
   <td class=" left-border" colspan='1'>0</td>
   <td class=" left-border" colspan='1'>0</td>
   <td class=" left-border" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>0</td>
   <td class=" left-border highlight" colspan='1'>1</td>
   <td class=" left-border" colspan='1'>0</td>
   <td class=" left-border right-border">0</td>
   </tr>
   </table>

The final offset value is 4. To that value, we have to add 8. (This add 8 is due to the historical design of the ARM architecture where the 
``PC`` will already have advanced 2 instructions or 8 bytes before the branch address is actually used). So the final amount for the branch is 12 bytes, or 
at 4 bytes per instructions, 3 instructions ahead. Sure enough, the shown branch skips over 2 instructions and runs the third one after the ``B``.
