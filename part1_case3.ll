define i32 @main(i32 %argc){
lbl_case1:
	%noArgs = icmp eq i32 %argc, 1
	br i1 %noArgs, label %lbl_t, label %lbl_f
lbl_t:
	ret i32 1
lbl_f:
	%a_i = mul i32 %argc, 0
	%b_i = add i32 %a_i,1
	%r_i = add i32 %a_i , %b_i
	%i_i = add i32 %argc, 2
	%cond1 = icmp sle i32 %i_i, %argc
	br i1 %cond1, label %lbl_ret, label %lbl_cont

lbl_ret:
	%r = phi i32 [%r_i, %lbl_f],[%r_u,%lbl_check]
	ret i32 %r
lbl_cont:
	%r_c = phi i32 [%r_i, %lbl_f], [%r_u, %lbl_check] 
	%b = phi i32 [%b_i, %lbl_f], [%b_u, %lbl_check] 
        %i = phi i32 [%i_i, %lbl_f], [%i_u, %lbl_check]
	%a_u = add i32 %b, 0
	%b_u = add i32 %r_c, 0
	%i_u = add i32 %i, 1
	br label %lbl_check
lbl_check:
	%r_u = add i32 %a_u, %b_u
	%cond2 = icmp sle i32 %i_u, %argc
        br i1 %cond1, label %lbl_ret, label %lbl_cont



}
