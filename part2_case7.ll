define i32 @foo(i32 %0, i8** %1) {
        ret i32 7
}
define i32 @main(i32 %0, i8** %1) {
        %res = call i32 @SOURCE ()
        %a_i = sub i32 %res, 0
        call i32 @foo (i32 %a_i)
        ret i32 0
}


declare dso_local i32 @SOURCE()
declare dso_local i32 @SINK(i32)