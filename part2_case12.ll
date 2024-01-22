define i32 @main() {
  
  %sum = alloca i32
  store i32 0, i32* %sum

  %res = alloca i32
  store i32 4, i32* %res

  %counter = alloca i32
  store i32 1, i32* %counter

  br label %loop

loop:
  
  %current_counter = load i32, i32* %counter

  %cmp = icmp sle i32 %current_counter, 10
  br i1 %cmp, label %loop_body, label %after_loop

loop_body:
  
  %current_sum = load i32, i32* %sum
  call i32 @foo (i32 %res)
  %res = call i32 @SOURCE ()
  
  %new_sum = add i32 %current_sum, %current_counter

  
  store i32 %new_sum, i32* %sum

  
  %new_counter = add i32 %current_counter, 1
  store i32 %new_counter, i32* %counter

  
  br label %loop

after_loop:
  
  %final_sum = load i32, i32* %sum

  
  ret i32 %final_sum
}
