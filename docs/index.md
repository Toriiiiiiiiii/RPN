## RPN - IPL Written in Python
*RPN is an Interpreted Programming Language (IPL) written entirely in Python.*

### What is RPN?
RPN Stands for *Reverse Polish Notation*, which is a way of writing mathematical or computational expressions in a way easier for a computer to interpret.
For example, in RPN, `(3+2) * 5` would be expressed as `3 2 + 5 *`.

In RPN, instructions are carried out left-to-right. In the example above, $3 2 + 5 *$ would be interpreted as:
1. Push `3` onto the stack.
2. Push `2` onto the stack.
3. Remove the top two numbers from the stack, and push the sum of them onto the stack.
4. Push `5` onto the stack.
5. Remove the top two numbers from the stack, and push the product of them onto the stack.

