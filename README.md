# Earthworm
Earthworm is a utility designed to analyze syntactically-valid Python scripts and offer suggestions for improving the program's **functional decomposition**. Earthworm identifies code fragments that serve a separate (algorithmic) purpose from their enclosing function(s), and attempts to create **an entirely new function** from them. The end result is a Python script where each function does exactly one task.

In general, this sort of formatting helps make programs easier to debug and organize, since each task is segmented in its own function. It also reduces the likelihood of unintended side-effects occurring when modifying parts of a program. This makes Earthworm especially useful for software development teams and also as a learning tool for students and professors.

## Authors/Credits
The initial version of Earthworm was a command-line tool proposed, researched, implemented, and presented by Nupur Garg, a graduate student at California Polytechnic State University, San Luis Obispo.

You can find copies of both her Thesis and code repositories below:
```
https://digitalcommons.calpoly.edu/theses/1759/
https://github.com/gargn/thesis
```

This program, written in Python, attempts to rationalize Garg's work into a fully-implemented User Interface, ultimately designed to make Earthworm both easier to use and more understandable.
It was designed by me (Nathan P. Ybanez) as a Senior Project for my undergraduate degree in Computer Science from Cal Poly SLO.

## Features
Earthworm provides the following features:
```
1. Simplistic UI with few menu buttons and plenty of icons - designed to be as user-friendly as possible
2. Syntax highlighting for opened files to make it easier to read text
3. Clear and easy-to-understand highlighting of suggested code fragments
4. Clear and concise descriptions of fixes for suggested code fragments
5. The ability to allow Earthworm to fix a given suggestion, with user direction
```

## How does it work?
Earthworm parses a given Python script and generates an *Abstract Syntax Tree (AST)*, a tree-structured representation of the syntactic structure of the input source code.

![alt_text](https://i.imgur.com/Fc5KU3S.png)

**Figure 2:** AST for (x - 1) + 4

The AST is then used to generate a *Control Flow Graph (CFG)* for each individual function, a graph representation of all paths that might be taken throughout that function's execution. Each individual block of a CFG represents some portion of control flow in the function. For example, a Conditional (IF statement) may have a block for the **guard**, a block for the **then** portion, and a block for the **else** portion.

![alt_text](https://i.imgur.com/gtgSjKk.png)

**Figure 3:** CFG for IF Statement

Within each of the individual branches of the CFG, there may be other nested, intermediate CFGs. Earthworm attempts to analyze these sub-CFGs and determine if the code within can be isolated. Earthworm saves the line numbers corresponding to the newly generated **suggestion**, as well as the variables that need to be passed in and returned in order to maintain the states of the remainder of the CFG (and thereby avoid altering the program's output).

When **Analyzing** a file in the Earthworm GUI, boxes are drawn around the source code corresponding to the line numbers returned by the command-line tool:

![alt_text](https://i.imgur.com/xOdjvNp.png)

**Figure 4:** Highlighted suggestions


If executing the code within a given block would have side effects on the other blocks (for example in the case of a variable which is shared between both blocks), then Earthworm will create an intermediate value and return it back to the calling scope.
