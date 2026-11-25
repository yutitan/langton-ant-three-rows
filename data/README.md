# 数值结果

## exact_search_1_14.txt

由 `verify/exact_search.py 14` 生成（分支精确搜索，宽度 1–14）。
宽度 1–7 与 `brute.c` 的穷举一致；宽度 8–14 用于与本记录公式对照。

    width  S(3,n)  formula  match  seconds
        1       2        2   True     0.0
        2      12       12   True     0.0
        3      17       17   True     0.0
        4      28       28   True     0.0
        5      37       37   True     0.0
        6      48       48   True     0.0
        7      57       57   True     0.1
        8      68       68   True     0.1
        9      77       77   True     0.3
       10      88       88   True     0.8
       11      97       97   True     2.0
       12     108      108   True     8.0
       13     117      117   True    22.5
       14     128      128   True    56.8
    EXIT:0

## brute_force_1_7.txt

由 `verify/brute.c` 生成（C 穷举全部 2^(3n) 种染色 × 12n 个起点位姿，
宽度 1–7）：

    n=1 S3_1=2
    n=2 S3_2=12
    n=3 S3_3=17
    n=4 S3_4=28
    n=5 S3_5=37
    n=6 S3_6=48
    n=7 S3_7=57
    real 0m7.334s (machine dependent)

编译与运行：

    gcc -O2 -o brute brute.c
    ./brute 7

## s_values.csv

宽度 1–14 的精确值与所用方法。n=3..9 与 Etse 论文表 1 的
17, 28, 37, 48, 57, 68, 77 一致。

## 与 Etse 论文的对照

* 表 1（§4.1）给出三行、n=3..9 的精确值：17,28,37,48,57,68,77。
* §4.3.2 给出下界 10n−12（n 偶）/ 10n−13（n 奇），n≥3，并报告
  n≤20 的模拟与构造一致。
* 本文的上界证明对任意 n 成立；数值表只是健全性检查。
