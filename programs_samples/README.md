# Примеры программ

В данной папке вы можете найти некоторое количество программ, на которых вы можете проверить
работу вашей реализации процессора:

## [`arith.dat`](./arith.dat)

Проверка работы reg-reg и reg-imm арифметических операций.

```
addi $s0, $0, 7
addi $s1, $0, 8
add $s2, $s1, $s0
sub $s3, $s1, $s0
and $s4, $s1, $s0
or $s5, $s1, $s0
slt $s6, $s1, $s0
```

## [`memory.dat`](./memory.dat)

Проверка работы с памятью.

```
addi $t0, $0, 32767
sw $t0, 0($0)
lw $t1, 0($0)
lw $t2, 4($0)
```

## [`branch.dat`](./branch.dat)

Проверка работы условного перехода.

```
addi $s0, $0, 8
addi $s1, $0, 8
beq $s0, $s1, eq
add $t0, $s0, $s1
eq:
sub $t0, $s0, $s1
```

## [`hello_world.dat`](./hello_world.dat)

Загружает ASCII строчку "Hello world!" в память.

За пример спасибо Тимофею Белоусову.

```
addi $t0, $zero, 72 # H
beq $zero, $zero, mult2x8
fi:
addi $t0, $t0, 101 # e

addi $t1, $zero, 8
loop1:
beq $t1, $zero, fi1
add $t0, $t0, $t0
sub $t1, $t1, $t2
beq $zero, $zero, loop1
fi1:

addi $t0, $t0, 108 # l

addi $t1, $zero, 8
loop2:
beq $t1, $zero, fi2
add $t0, $t0, $t0
sub $t1, $t1, $t2
beq $zero, $zero, loop2
fi2:

addi $t0, $t0, 108 # l
sw $t0, 0($zero)

addi $t0, $zero, 111 # o

addi $t1, $zero, 8
loop3:
beq $t1, $zero, fi3
add $t0, $t0, $t0
sub $t1, $t1, $t2
beq $zero, $zero, loop3
fi3:

addi $t0, $t0, 32 # space

addi $t1, $zero, 8
loop4:
beq $t1, $zero, fi4
add $t0, $t0, $t0
sub $t1, $t1, $t2
beq $zero, $zero, loop4
fi4:

addi $t0, $t0, 119 # w

addi $t1, $zero, 8
loop5:
beq $t1, $zero, fi5
add $t0, $t0, $t0
sub $t1, $t1, $t2
beq $zero, $zero, loop5
fi5:

addi $t0, $t0, 111 # o
sw $t0, 4($zero)

addi $t0, $zero, 114 # r

addi $t1, $zero, 8
loop6:
beq $t1, $zero, fi6
add $t0, $t0, $t0
sub $t1, $t1, $t2
beq $zero, $zero, loop6
fi6:

addi $t0, $t0, 108 # l

addi $t1, $zero, 8
loop7:
beq $t1, $zero, fi7
add $t0, $t0, $t0
sub $t1, $t1, $t2
beq $zero, $zero, loop7
fi7:

addi $t0, $t0, 100 # d

addi $t1, $zero, 8
loop8:
beq $t1, $zero, fi8
add $t0, $t0, $t0
sub $t1, $t1, $t2
beq $zero, $zero, loop8
fi8:

addi $t0, $t0, 33 # !
sw $t0, 8($zero)



beq $zero, $zero, halt
mult2x8:
addi $t1, $zero, 8
addi $t2, $zero, 1

loop:
beq $t1, $zero, fi

add $t0, $t0, $t0

sub $t1, $t1, $t2
beq $zero, $zero, loop
halt:
beq $zero, $zero, halt
```