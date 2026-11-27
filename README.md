# 大模型的小练习（二）：三行朗顿蚂蚁的精确逃逸时间

**LLM Exercises II — the exact escape time of Langton's ant on three-row boards**

**Author:** [@yutitan](https://github.com/yutitan) · **Date:** 2026-11-26
· **Derived with:** GPT 6.2 Astra (OpenAI Codex, model `gpt-6.2-astra`),
independently verified with DeepSeek Harness — see [Provenance](#provenance)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24540968.svg)](https://doi.org/10.5281/zenodo.24540968) · **Archived release:** v1.0.0 (2026-11-26)

> 本仓库是"大模型的小练习"系列的第二篇，是一份个人 AI 使用记录，不是论文，
> 不作优先权主张。系列第一篇：
> [Counterexamples to *Written on the Wall II* conjecture #138](https://github.com/yutitan/wowii-conjecture-138)
> — [DOI 10.5281/zenodo.24540807](https://doi.org/10.5281/zenodo.24540807)。
> 系列第三篇：
> [Langton's ant on n×n boards — an explicit escape-time bound](https://github.com/yutitan/langton-ant-square-bound)
> — [DOI 10.5281/zenodo.24541703](https://doi.org/10.5281/zenodo.24541703)。
> 系列第四篇：
> [Reverse-play thresholds for Langton's ant](https://github.com/yutitan/langton-reverse-thresholds)
> — release v1.0.0（Zenodo DOI 待回填）。

## 结果

朗顿蚂蚁：白格右转、黑格左转，翻转脚下格子，向前走一格。设 S(n) 为在
3 × n 棋盘上，对所有初始染色、起点和朝向取最大值时，蚂蚁第一次走出棋盘
所需的最多步数（计入走出那一步）。则

    S(1) = 2,   S(2) = 12,
    S(n) = 10n - 12   (n >= 3, n 偶),
    S(n) = 10n - 13   (n >= 3, n 奇).

**下界**由 Kossi Roland Etse 在 MFCS 2026 的论文中给出（显式构造，见
[文献笔记](literature/notes.md)）；论文还报告了 n ≤ 20 的精确模拟与构造
一致。**本记录补的是任意宽度的上界证明。**

| n | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| S(n) | 2 | 12 | 17 | 28 | 37 | 48 | 57 | 68 | 77 | 88 | 97 | 108 | 117 | 128 |

宽度 1–7 由穷举得到，8–14 由精确搜索得到（`data/`）。

## 证明思路

1. **端块记录。** 取棋盘最右的 w 列。蚂蚁每次进入块都记下进入行和回应
   （从同一侧返回的行，或"出界"）；每次访问后块内颜色被保留。对宽 2 和
   宽 4 的端块穷举全部染色（2^6 = 64 与 2^12 = 4096），得到**同样的
   34 条记录**。
2. **有限证书。** 对每条记录 r，令 P_w(r) 为宽 w 的块实现 r 时块内最多
   步数。穷举给出 P4(r) − P2(r) ≤ 20（差值分布 0:3, 8:20, 15:1, 16:2,
   20:8）。完整证书与见证染色在
   [`verify/certificate.json`](verify/certificate.json)。
3. **替换归纳。** 对 n ≥ 8 和任意起点，取起点另一侧的 4 列端块，把它换成
   能实现同一记录且块内步数为 P2(r) 的 2 列块。块外运动完全相同，块内至多
   少 20 步，所以 S(n) ≤ S(n−2) + 20。基例 2,12,17,28,37,48,57 给出
   S(n) ≤ 10n−12（偶）与 S(n) ≤ 10n−13（奇）。与 Etse 的下界合起来即得
   等式。

完整证明（含奇偶性引理、镜像对称、替换引理的严格陈述）见
[`note/note.md`](note/note.md)。

## 验证

所有数值与有限证书都由仓库里的程序独立核验（不依赖语言模型的输出）：

    bash verify/run_all.sh

| 文件 | 作用 |
| --- | --- |
| [verify/verify_three_row_ant.py](verify/verify_three_row_ant.py) | 推导时的主程序（34 条记录、差值、基例） |
| [verify/ant_transcript_crosscheck.py](verify/ant_transcript_crosscheck.py) | 按坐标重演，左右两端各验一遍 |
| [verify/make_certificate.py](verify/make_certificate.py) | 生成含见证染色的证书 |
| [verify/check_certificate.py](verify/check_certificate.py) | 重放证书见证，核对记录与步数 |
| [verify/independent_enumeration.py](verify/independent_enumeration.py) | 独立重写的枚举（不导入主程序），与证书逐项一致 |
| [verify/replacement_test.py](verify/replacement_test.py) | 400 个随机棋盘上替换构造的端到端测试 |
| [verify/brute.c](verify/brute.c) | C 穷举宽度 1–7（全部染色 × 位姿） |
| [verify/exact_search.py](verify/exact_search.py) | 分支搜索宽度 1–14 |

记录下来的运行输出在 [verify/results.txt](verify/results.txt)；
`data/` 里是穷举与精确搜索的原始输出。

## Provenance

* 结果与证明由 **GPT 6.2 Astra**（OpenAI Codex）在 2026-11-25 17:55:34 UTC
  的一次会话中给出（该会话同时用于系列第一篇）；原始回答保存在
  [provenance/gpt-6.2-astra-answer.md](provenance/gpt-6.2-astra-answer.md)。
* **DeepSeek Harness** 在同一人类指令下做了独立复核：独立枚举、C 穷举、
  宽度到 14 的精确搜索、400 次替换构造测试，并整理发布本仓库。
* 人类作者（[@yutitan](https://github.com/yutitan)）发起并指导两个会话，
  审阅结果，发布仓库，对内容负责。AI 不是法律作者。

时间线、哈希与原始脚本见 [PROVENANCE.md](PROVENANCE.md)。

## 定位

* 结论在 Etse 的论文中已由下界构造 + n ≤ 20 模拟"锁定"；本文只补上界。
* 证明是计算机辅助的：一个 34 项有限证书 + 初等替换归纳。
* 没有重新证明 Etse 的下界；四行的类似问题已由 Hao Ke 解决
  （34n−150，n ≥ 13）。
* 这是个人 AI 使用记录，**不声明新颖性/优先权**；文献检索范围见
  [literature/notes.md](literature/notes.md)。

## Citation

If you use this material, please cite it (see [`CITATION.cff`](CITATION.cff)):

Archived releases are on Zenodo: **v1.0.0** has DOI [10.5281/zenodo.24540968](https://doi.org/10.5281/zenodo.24540968) (concept DOI [10.5281/zenodo.24540967](https://doi.org/10.5281/zenodo.24540967)). The DOI always refers to the archived snapshot; later commits are not part of it.

```bibtex
@misc{yutitan2026langton,
  author       = {yutitan},
  title        = {大模型的小练习（二）：三行朗顿蚂蚁的精确逃逸时间},
  year         = {2026},
  howpublished = {\url{https://github.com/yutitan/langton-ant-three-rows}},
  publisher    = {Zenodo},
  doi          = {10.5281/zenodo.24540968},
  note         = {Langton's ant on 3-row boards; series entry (一) is DOI 10.5281/zenodo.24540807}
}
```

## License

代码 MIT（[LICENSE](LICENSE)）；文字、数据与图片 CC BY 4.0
（[LICENSE-CONTENT.md](LICENSE-CONTENT.md)）。
