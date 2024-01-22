define i32 @main() {
  
  %result = alloca i32

  store i32 10, i32* %result

  %value = load i32, i32* %result

  %cmp = icmp sgt i32 %value, 5
  %res = call i32 @SOURCE ()

  br i1 %cmp, label %if_true, label %if_false

if_true:
  
  call i32 @foo (i32 %res)
  store i32 20, i32* %result

  br label %if_end

if_false:
 
  store i32 30, i32* %result

  br label %if_end

if_end:
  ret i32 0
}
