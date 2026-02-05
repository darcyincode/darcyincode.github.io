# Attention Is All You Need - 第一章及之前内容中文翻译

---

在适当标注来源的情况下，Google 特此授予许可，允许在新闻或学术作品中单独复制本文中的表格和图表。

## Attention Is All You Need（注意力机制就是你所需要的一切）

**作者：**

- Ashish Vaswani* - Google Brain (avaswani@google.com)
- Noam Shazeer* - Google Brain (noam@google.com)
- Niki Parmar* - Google Research (nikip@google.com)
- Jakob Uszkoreit* - Google Research (usz@google.com)
- Llion Jones* - Google Research (llion@google.com)
- Aidan N. Gomez*† - University of Toronto (aidan@cs.toronto.edu)
- Łukasz Kaiser* - Google Brain (lukaszkaiser@google.com)
- Illia Polosukhin*‡ (illia.polosukhin@gmail.com)

---

## 摘要

主流的序列转换模型基于复杂的循环或卷积神经网络，包含编码器和解码器。性能最佳的模型还通过注意力机制连接编码器和解码器。我们提出了一种新的简单网络架构——Transformer，它完全基于注意力机制，完全摒弃了循环和卷积。在两个机器翻译任务上的实验表明，这些模型在质量上更优越，同时具有更好的并行性，并且所需的训练时间显著减少。我们的模型在 WMT 2014 英译德翻译任务上达到了 28.4 BLEU 分数，比现有最佳结果（包括集成模型）提高了超过 2 个 BLEU 分数。在 WMT 2014 英译法翻译任务上，我们的模型在 8 个 GPU 上训练 3.5 天后，建立了新的单模型最佳 BLEU 分数 41.8，这只是文献中最佳模型训练成本的一小部分。我们通过将 Transformer 成功应用于英语成分句法分析（无论是在大规模还是有限的训练数据下），展示了 Transformer 能够很好地泛化到其他任务。

---

***同等贡献。列出顺序是随机的。** Jakob 提出用自注意力替换 RNN，并开始了评估这个想法的工作。Ashish 与 Illia 一起设计并实现了第一个 Transformer 模型，并在这项工作的每个方面都发挥了关键作用。Noam 提出了缩放点积注意力、多头注意力和无参数位置表示，并成为几乎参与每个细节的另一个人。Niki 在我们原始代码库和 tensor2tensor 中设计、实现、调优和评估了无数的模型变体。Llion 也尝试了新颖的模型变体，负责我们最初的代码库，以及高效的推理和可视化。Lukasz 和 Aidan 花费了无数个漫长的日子设计 tensor2tensor 的各个部分并实现它，替换了我们早期的代码库，极大地改善了结果并大幅加速了我们的研究。

†工作在 Google Brain 完成。

‡工作在 Google Research 完成。

第 31 届神经信息处理系统会议（NIPS 2017），加利福尼亚州长滩，美国。

arXiv:1706.03762v7 [cs.CL] 2 Aug 2023

---

## 1. 引言

循环神经网络，特别是长短期记忆网络（LSTM）[13] 和门控循环神经网络（GRU）[7]，已被牢固确立为序列建模和转换问题（如语言建模和机器翻译）的最先进方法 [35, 2, 5]。此后，许多努力继续推动循环语言模型和编码器-解码器架构的边界 [38, 24, 15]。

循环模型通常沿着输入和输出序列的符号位置进行因子计算。将位置对齐到计算时间步长，它们生成一系列隐藏状态 $h_t$，作为前一个隐藏状态 $h_{t-1}$ 和位置 $t$ 的输入的函数。这种固有的序列性质排除了训练样本内的并行化，这在较长的序列长度下变得至关重要，因为内存约束限制了跨样本的批处理。最近的工作通过因子分解技巧 [21] 和条件计算 [32] 在计算效率方面取得了显著改进，同时在后者的情况下也提高了模型性能。然而，顺序计算的基本约束仍然存在。

注意力机制已成为各种任务中引人注目的序列建模和转换模型的组成部分，允许对依赖关系进行建模，而无需考虑它们在输入或输出序列中的距离 [2, 19]。然而，除了少数情况 [27] 外，这种注意力机制都是与循环网络结合使用的。

在这项工作中，我们提出了 Transformer，这是一种避开循环的模型架构，而是完全依赖注意力机制来绘制输入和输出之间的全局依赖关系。Transformer 允许显著更多的并行化，并且在 8 个 P100 GPU 上仅训练 12 小时后就能达到翻译质量的新的最先进水平。
