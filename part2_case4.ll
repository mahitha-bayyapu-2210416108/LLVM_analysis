define i32 @foo(i32 %0, i8** %1) {
        ret i32 7
}
define i32 @main(i32 %0, i8** %1) {
        %res = call i32 @SOURCE ()
        store i32 1 , i32* %res, align 4
        %reg = load i32, i32* %res, align 4
        %a_i = mul i32 %argc, 0
        call i32 @foo (i32 %reg)
        ret i32 0
}


declare dso_local i32 @SOURCE()
declare dso_local i32 @SINK(i32)