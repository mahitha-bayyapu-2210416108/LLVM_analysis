define i32 @foo(i32 %0, i8** %1) {
        ret i32 7
}
define i32 @main(i32 %0, i8** %1) {
        %res = call i32 @SOURCE ()
        store i32   i32 %abc , i32* %res, align 4
 
        
        call i32 @foo (i32 %abc)
        ret i32 0
}
op: LEAK
 
declare dso_local i32 @SOURCE()
declare dso_local i32 @SINK(i32)