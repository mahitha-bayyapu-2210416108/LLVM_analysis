define i32 @fib(i32 %n) {
  %noArg = icmp slt i32 %n, 2
  br i1 %noArg, label %if_true, label %if_false

if_true:
 ret i32 %n

if_false:
  %n_minus_1 = sub i32 %n, 1
  %n_minus_2 = sub i32 %n, 2
  %call_fib1 = call i32 @fib(i32 %n_minus_1)
  %call_fib2 = call i32 @fib(i32 %n_minus_2)
  %res = add i32 %call_fib1, %call_fib2
  ret i32 %res
}

define i32 @main(i32 %argc) {

  
  %call_fun = call i32 @fib(i32 %argc)
  ret i32 %call_fun
}

