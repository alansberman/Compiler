	.text
	.file	"<string>"
	.section	.rodata.cst4,"aM",@progbits,4
	.align	4
.LCPI0_0:
	.long	1079613850
	.text
	.globl	main
	.align	16, 0x90
	.type	main,@function
main:
	.cfi_startproc
	movl	$1067030938, -4(%rsp)
	movl	$1079613850, -8(%rsp)
	movss	-4(%rsp), %xmm0
	movabsq	$.LCPI0_0, %rax
	mulss	(%rax), %xmm0
	movss	%xmm0, -12(%rsp)
	retq
.Ltmp0:
	.size	main, .Ltmp0-main
	.cfi_endproc


	.section	".note.GNU-stack","",@progbits
