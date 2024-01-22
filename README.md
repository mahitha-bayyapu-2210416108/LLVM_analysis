# LLVM_analysis
This project is to analyze the LLVM bit code and identify. There are two parts for this project. The first part constructs a control flow graph. The second part identifies if there are any leaks or no leaks.

To enhance the clarity and conciseness of your description, you can consider the following revision:

## Table of Contents

- [Control-Flow Graph Construction](#Control-Flow Graph Construction)
- [Static Dataflow Analysis](#Static Dataflow Analysis)

## Control-Flow Graph Construction

The program's core function involves generating control-flow graphs in the graphviz dot format for each function declared in the provided input file. Each function's control-flow graph consists of nodes with a record shape and an empty label. Edges are directed and labeled based on their position in the branch.

### Example:
Input:
```
define i32 @main(i32 %argc) {
        %noArgs = icmp eq i32 %argc, 1
        br i1 %noArgs, label %lbl_t, label %lbl_f
lbl_t:
        %varT = add i32 1, 0
        br label %end
lbl_f:
        %varF = add i32 2, 0
        br label %end
end:
        %var = phi i32 [%varT, %lbl_t], [%varF, %lbl_f]
        ret i32 %var
}
```

Commands to run:
./analysis -i input.ll -g mydir

Output:
```
digraph {
        Node0 [shape=record,label=""]
        Node0 -> Node1 [label=1];
        Node0 -> Node2 [label=2];
        Node1 [shape=record,label=""]
        Node1 -> Node3 [label=1];
        Node2 [shape=record,label=""]
        Node2 -> Node3 [label=1];
        Node3 [shape=record,label=""]
}
```
Graphviz: 
To view the graph use graphviz

## Static Dataflow Analysis

The primary objective is to perform flow-sensitive static dataflow analysis over the control-flow graphs. The goal is to identify any flow from the result of invoking a function SOURCE to the (single) argument of a function SINK within any function in the input. If such a flow is detected, the program will exit with code 0. 

###Example:

Input:
```
define i32 @main(i32 %0, i8** %1) {
        %res = call i32 @SOURCE ()
        call i32 @SINK (i32 %res)
        ret i32 0
}
declare dso_local i32 @SOURCE()
declare dso_local i32 @SINK(i32)
```

Commad to run:
./analysis -i input.ll -i <infile>

Output:
```
LEAK
```
