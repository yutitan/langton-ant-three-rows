# 文献笔记

本文件记录撰写本仓库时查到的两篇相关工作，以及本仓库结果的定位。
所有引文均来自公开 PDF / 网页（2026-11-26 检索）。

## 1. Kossi Roland Etse, MFCS 2026

**Kossi Roland Etse.** *How Long Can The Escaping Ant Be Confined?*
51st International Symposium on Mathematical Foundations of Computer Science
(MFCS 2026), LIPIcs vol. 386, paper 49, Schloss Dagstuhl.
DOI: [10.4230/LIPIcs.MFCS.2026.49](https://doi.org/10.4230/LIPIcs.MFCS.2026.49) ·
全文版: [arXiv:2606.26677](https://arxiv.org/abs/2606.26677) ·
CC BY 4.0.

这篇论文研究朗顿蚂蚁在有限连通区域中的逃逸时间。与本仓库直接相关的三点：

1. **定理 8**（§4.3.2）：对每个整数 $n \ge 2$，三行 $n$ 列矩形满足
   $S_{3,n} \le 10n - 4$。这是本文之前最好的上界。
2. **下界构造**（§4.3.2 末尾，图 12）：原文写道
   > *"Explicit constructions (Figure 12) show that for every n ≥ 3
   > S_{3,n} ≥ 10n − 12 if n is even and S_{3,n} ≥ 10n − 13 if n is odd.
   > Moreover, our simulations for n ≤ 20 yield exact escaping times
   > consistent with these constructions."*
3. **精确值表 1**（§4.1，$1 \le k,n \le 9$）：三行一栏的数值为
   $n = 3,\dots,9$：$17, 28, 37, 48, 57, 68, 77$，与
   $10n-12$（偶）/ $10n-13$（奇）一致。

§5 "Conclusion and Open Questions" 列出的开放方向是：平方区域的多项式上界、
四行猜想 $S_{4,n} \le 34n$、固定高度的线性上界、更大网格的精确值等；
**三行精确值的全宽证明没有被列为已知结果**。因此本仓库补的正是
"下界构造与模拟已知，上界证明缺失"这一步。

## 2. Hao Ke（2026）

**Hao Ke.** *Exact Escape Times of Langton's Ant in Four Rows — A finite
persistent-response classification and an all-width certificate.*
Preprint, 2026-10-26.
Zenodo DOI: [10.5281/zenodo.23675964](https://doi.org/10.5281/zenodo.23675964) ·
作者页面: <https://www.kehao.me/papers/langtons-ant-four-row-escape/>

摘要中的结果：对四行 $n$ 列矩形，$S_{4,n} = 34n - 150$（$n \ge 13$），
并给出所有更小宽度的值；这证明了 Etse 的猜想 $S_{4,n} \le 34n$。
方法是按"重复进入后的响应"对块分类，得到 269 个响应类型和一条精确递推。
这篇论文处理的是四行，不包含三行的全宽上界证明。

四行结果说明这个方向正在被快速推进；本仓库的三行结果是一个更小的、
可以完整写出来的有限证书 + 归纳练习。

## 3. 新颖性核对（仅限检索范围内）

检索过的来源：

* MFCS 2026 论文（LIPIcs 正式版 + arXiv 全文版）的正文、表格和结论；
* Hao Ke 的论文列表与 Zenodo 记录；
* Zenodo、arXiv、普通网页检索（"three-row Langton ant exact escape
  time", "10n-12", "10n-13" 等组合）。

在检索范围内**没有找到**此前发表的三行全宽上界证明或三行精确值定理。
但这只是"没找到"，不是优先权声明：这个论证很短，模型和研究者都可能
独立想到；本仓库按"个人 AI 使用记录 / 小练习"发布，不作任何优先权主张。

## 4. 其它背景

* C. G. Langton, *Studying artificial life with cellular automata*,
  Physica D 22 (1986) 120–149（蚂蚁规则）。
* OEIS A282425：Etse 在 §4.1 指出该序列在 $S_{7,7}$ 处有 1 的误差并在
  表 1 中更正；本仓库的三行数值与表 1 一致（$n=3,\dots,9$）。
