---
title: LLM 学习路线图 - 完整中文翻译
date: 2026-02-04
categories:
  - [大模型, LLM学习]
tags:
  - LLM
  - AI
  - 深度学习
---

# LLM 学习路线图 - 完整中文翻译

## 1. LLM 架构
深入了解 Transformer 架构并非必须，但了解现代 LLM 的主要步骤非常重要：通过分词将文本转换为数字，通过包括注意力机制在内的各层处理这些词元，最后通过各种采样策略生成新文本。

**架构概述：** 了解从编码器-解码器 Transformer 到像 GPT 这样的纯解码器架构的演变，这些架构构成了现代 LLM 的基础。重点关注这些模型如何在高层次上处理和生成文本。

**分词（Tokenization）：** 学习分词的原理——文本如何转换为 LLM 可以处理的数字表示。探索不同的分词策略及其对模型性能和输出质量的影响。

**注意力机制：** 掌握注意力机制的核心概念，特别是自注意力及其变体。了解这些机制如何使 LLM 能够处理长距离依赖关系并在整个序列中保持上下文。

**采样技术：** 探索各种文本生成方法及其权衡。比较确定性方法（如贪婪搜索和束搜索）与概率方法（如温度采样和核采样）。

📚 **参考资料：**

- **Visual intro to Transformers by 3Blue1Brown：** 为完全初学者提供的 Transformer 可视化介绍。
- **LLM Visualization by Brendan Bycroft：** LLM 内部的交互式 3D 可视化。
- **nanoGPT by Andrej Karpathy：** 一个 2 小时的 YouTube 视频，从头重新实现 GPT（面向程序员）。他还制作了一个关于分词的视频。
- **Attention? Attention! by Lilian Weng：** 历史概述，介绍为何需要注意力机制。
- **Decoding Strategies in LLMs by Maxime Labonne：** 提供代码和可视化介绍不同的解码策略来生成文本。

## 2. 预训练模型
预训练是一个计算密集且昂贵的过程。虽然这不是本课程的重点，但对模型如何预训练有扎实的理解非常重要，特别是在数据和参数方面。预训练也可以由爱好者以小规模进行，使用小于 10 亿参数的模型。

**数据准备：** 预训练需要大量数据集（例如，Llama 3.1 使用 15 万亿个词元进行训练），这些数据集需要仔细策划、清理、去重和分词。现代预训练流程实施复杂的过滤以去除低质量或有问题的内容。

**分布式训练：** 结合不同的并行化策略：数据并行（批次分布）、流水线并行（层分布）和张量并行（操作分割）。这些策略需要跨 GPU 集群的优化网络通信和内存管理。

**训练优化：** 使用带预热的自适应学习率、梯度裁剪和归一化来防止梯度爆炸，使用混合精度训练提高内存效率，并使用现代优化器（AdamW、Lion）和调优的超参数。

**监控：** 使用仪表板跟踪关键指标（损失、梯度、GPU 统计信息），为分布式训练问题实施有针对性的日志记录，并设置性能分析以识别跨设备计算和通信的瓶颈。

📚 **参考资料：**

- **FineWeb by Penedo et al.：** 重建 LLM 预训练大规模数据集（15T）的文章，包括 FineWeb-Edu，一个高质量子集。
- **RedPajama v2 by Weber et al.：** 另一篇关于大规模预训练数据集的文章和论文，包含许多有趣的质量过滤器。
- **nanotron by Hugging Face：** 用于制作 SmolLM2 的简约 LLM 训练代码库。
- **Parallel training by Chenyan Xiong：** 优化和并行化技术概述。
- **Distributed training by Duan et al.：** 关于在分布式架构上高效训练 LLM 的调查。
- **OLMo 2 by AI2：** 开源语言模型，包含模型、数据、训练和评估代码。
- **LLM360 by LLM360：** 开源 LLM 框架，包含训练和数据准备代码、数据、指标和模型。

## 3. 后训练数据集
后训练数据集具有精确的结构，包括指令和答案（监督微调）或指令和选择/拒绝答案（偏好对齐）。对话结构比用于预训练的原始文本要少得多，这就是为什么我们经常需要处理种子数据并对其进行细化，以提高样本的准确性、多样性和复杂性。更多信息和示例可在我的仓库 💾 LLM Datasets 中找到。

**存储和聊天模板：** 由于对话结构的特性，后训练数据集以特定格式存储，如 ShareGPT 或 OpenAI/HF。然后，这些格式被映射到聊天模板，如 ChatML 或 Alpaca，以生成模型训练的最终样本。

**合成数据生成：** 使用前沿模型（如 GPT-4o）基于种子数据创建指令-响应对。这种方法允许灵活且可扩展的数据集创建，并提供高质量的答案。关键考虑因素包括设计多样化的种子任务和有效的系统提示。

**数据增强：** 使用技术增强现有样本，如经过验证的输出（使用单元测试或求解器）、使用拒绝采样的多个答案、Auto-Evol、思维链（Chain-of-Thought）、Branch-Solve-Merge、角色扮演等。

**质量过滤：** 传统技术包括基于规则的过滤、删除重复或近似重复（使用 MinHash 或嵌入）以及 n-gram 去污染。奖励模型和评判 LLM 通过细粒度和可定制的质量控制补充此步骤。

📚 **参考资料：**

- **Synthetic Data Generator by Argilla：** 在 Hugging Face space 中使用自然语言构建数据集的入门友好方式。
- **LLM Datasets by Maxime Labonne：** 用于后训练的数据集和工具的精选列表。
- **NeMo-Curator by Nvidia：** 用于预训练和后训练数据的数据集准备和策划框架。
- **Distilabel by Argilla：** 生成合成数据的框架。它还包括有趣的论文复现，如 UltraFeedback。
- **Semhash by MinishLab：** 使用精简嵌入模型进行近似去重和去污染的简约库。
- **Chat Template by Hugging Face：** Hugging Face 关于聊天模板的文档。

## 4. 监督微调（SFT）
SFT 将基础模型转变为有用的助手，能够回答问题和遵循指令。在此过程中，它们学习如何构建答案并重新激活在预训练期间学到的知识子集。灌输新知识是可能的但很肤浅：它不能用于学习完全新的语言。始终优先考虑数据质量而不是参数优化。

**训练技术：** 完全微调更新所有模型参数，但需要大量计算资源。参数高效微调技术（如 LoRA 和 QLoRA）通过训练少量适配器参数同时保持基础权重冻结来减少内存需求。QLoRA 将 4 位量化与 LoRA 结合以减少 VRAM 使用。这些技术都在最流行的微调框架中实现：TRL、Unsloth 和 Axolotl。

**训练参数：** 关键参数包括带调度器的学习率、批次大小、梯度累积、训练轮数、优化器（如 8 位 AdamW）、用于正则化的权重衰减以及用于训练稳定性的预热步骤。LoRA 还增加了三个参数：秩（通常为 16-128）、alpha（秩的 1-2 倍）和目标模块。

**分布式训练：** 使用 DeepSpeed 或 FSDP 跨多个 GPU 扩展训练。DeepSpeed 提供三个 ZeRO 优化阶段，通过状态分区提高内存效率。两种方法都支持梯度检查点以提高内存效率。

**监控：** 跟踪训练指标，包括损失曲线、学习率调度和梯度范数。监控常见问题，如损失尖峰、梯度爆炸或性能下降。

📚 **参考资料：**

- **Fine-tune Llama 3.1 Ultra-Efficiently with Unsloth by Maxime Labonne：** 使用 Unsloth 微调 Llama 3.1 模型的实践教程。
- **Axolotl - Documentation by Wing Lian：** 许多与分布式训练和数据集格式相关的有趣信息。
- **Mastering LLMs by Hamel Husain：** 关于微调的教育资源集合（还包括 RAG、评估、应用和提示工程）。
- **LoRA insights by Sebastian Raschka：** 关于 LoRA 的实用见解以及如何选择最佳参数。

## 5. 偏好对齐
偏好对齐是后训练流程中的第二阶段，专注于将生成的答案与人类偏好对齐。此阶段旨在调整 LLM 的语气并减少毒性和幻觉。然而，它在提升性能和改善实用性方面变得越来越重要。与 SFT 不同，有许多偏好对齐算法。在这里，我们将重点关注三个最重要的算法：DPO、GRPO 和 PPO。

**拒绝采样：** 对于每个提示，使用训练的模型生成多个响应，并对它们进行评分以推断选择/拒绝的答案。这会创建在线策略数据，其中两个响应都来自正在训练的模型，从而提高对齐稳定性。

**直接偏好优化（DPO）：** 直接优化策略以最大化选择响应相对于拒绝响应的可能性。它不需要奖励建模，这使其在计算上比 RL 技术更有效，但在质量方面略差。非常适合创建聊天模型。

**奖励模型：** 使用人类反馈训练奖励模型来预测指标，如人类偏好。它可以利用 TRL、verl 和 OpenRLHF 等框架进行可扩展训练。

**强化学习（RL）：** RL 技术（如 GRPO 和 PPO）迭代更新策略以最大化奖励，同时保持接近初始行为。它们可以使用奖励模型或奖励函数来评分响应。它们往往计算成本高，需要仔细调整超参数，包括学习率、批次大小和裁剪范围。适合创建推理模型。

📚 **参考资料：**

- **Illustrating RLHF by Hugging Face：** RLHF 介绍，包括奖励模型训练和使用强化学习进行微调。
- **LLM Training: RLHF and Its Alternatives by Sebastian Raschka：** RLHF 流程及替代方案（如 RLAIF）的概述。
- **Preference Tuning LLMs by Hugging Face：** 比较 DPO、IPO 和 KTO 算法以执行偏好对齐。
- **Fine-tune with DPO by Maxime Labonne：** 使用 DPO 微调 Mistral-7b 模型并复现 NeuralHermes-2.5 的教程。
- **Fine-tune with GRPO by Maxime Labonne：** 使用 GRPO 微调小型模型的实践练习。
- **DPO Wandb logs by Alexander Vishnevskiy：** 显示要跟踪的主要 DPO 指标以及您应该期望的趋势。

## 6. 评估
可靠地评估 LLM 是一项复杂但必不可少的任务，可指导数据生成和训练。它提供关于改进领域的宝贵反馈，可用于修改数据混合、质量和训练参数。然而，始终要记住古德哈特定律："当一个度量成为目标时，它就不再是一个好的度量。"

**自动化基准测试：** 使用精选数据集和指标（如 MMLU）评估模型在特定任务上的表现。它适用于具体任务，但在抽象和创造性能力方面存在困难。它也容易受到数据污染的影响。

**人工评估：** 涉及人类提示模型并对响应进行评分。方法从氛围检查到具有特定指南的系统注释和大规模社区投票（竞技场）不等。它更适合主观任务，对事实准确性的可靠性较低。

**基于模型的评估：** 使用评判和奖励模型来评估模型输出。它与人类偏好高度相关，但会偏向自己的输出并且评分不一致。

**反馈信号：** 分析错误模式以识别特定弱点，例如遵循复杂指令的限制、缺乏特定知识或容易受到对抗性提示的影响。这可以通过更好的数据生成和训练参数来改善。

📚 **参考资料：**

- **LLM evaluation guidebook by Hugging Face：** 包含实用见解的评估综合指南。
- **Open LLM Leaderboard by Hugging Face：** 以开放和可重现的方式比较 LLM 的主要排行榜（自动化基准测试）。
- **Language Model Evaluation Harness by EleutherAI：** 使用自动化基准测试评估 LLM 的流行框架。
- **Lighteval by Hugging Face：** 替代评估框架，还包括基于模型的评估。
- **Chatbot Arena by LMSYS：** 通用 LLM 的 Elo 评级，基于人类做出的比较（人工评估）。

## 7. 量化
量化是将模型的参数和激活转换为较低精度的过程。例如，使用 16 位存储的权重可以转换为 4 位表示。这项技术对于减少与 LLM 相关的计算和内存成本变得越来越重要。

**基本技术：** 学习不同的精度级别（FP32、FP16、INT8 等）以及如何使用 absmax 和零点技术执行朴素量化。

**GGUF 和 llama.cpp：** 最初设计用于在 CPU 上运行，llama.cpp 和 GGUF 格式已成为在消费级硬件上运行 LLM 的最流行工具。它支持在单个文件中存储特殊词元、词汇表和元数据。

**GPTQ 和 AWQ：** GPTQ/EXL2 和 AWQ 等技术引入了逐层校准，在极低位宽下保持性能。它们使用动态缩放减少灾难性异常值，选择性地跳过或重新定中心最重的参数。

**SmoothQuant 和 ZeroQuant：** 新的量化友好变换（SmoothQuant）和基于编译器的优化（ZeroQuant）有助于在量化之前减轻异常值。它们还通过融合某些操作和优化数据流来减少硬件开销。

📚 **参考资料：**

- **Introduction to quantization by Maxime Labonne：** 量化概述、absmax 和零点量化以及带代码的 LLM.int8()。
- **Quantize Llama models with llama.cpp by Maxime Labonne：** 使用 llama.cpp 和 GGUF 格式量化 Llama 2 模型的教程。
- **4-bit LLM Quantization with GPTQ by Maxime Labonne：** 使用 GPTQ 算法和 AutoGPTQ 量化 LLM 的教程。
- **Understanding Activation-Aware Weight Quantization by FriendliAI：** AWQ 技术及其优势的概述。
- **SmoothQuant on Llama 2 7B by MIT HAN Lab：** 如何在 Llama 2 模型上使用 8 位精度的 SmoothQuant 的教程。
- **DeepSpeed Model Compression by DeepSpeed：** 如何使用 DeepSpeed Compression 使用 ZeroQuant 和极端压缩（XTC）的教程。

## 8. 新趋势
以下是未归入其他类别的值得注意的主题。有些是已建立的技术（模型合并、多模态），但其他技术更具实验性（可解释性、测试时计算扩展）并且是众多研究论文的焦点。

**模型合并：** 合并训练的模型已成为创建高性能模型的流行方式，无需任何微调。流行的 mergekit 库实现了最流行的合并方法，如 SLERP、DARE 和 TIES。

**多模态模型：** 这些模型（如 CLIP、Stable Diffusion 或 LLaVA）通过统一的嵌入空间处理多种类型的输入（文本、图像、音频等），从而解锁强大的应用程序，如文本到图像。

**可解释性：** 机制可解释性技术（如稀疏自编码器（SAE））在提供 LLM 内部工作原理的见解方面取得了显著进展。这也应用于诸如 abliteration 之类的技术，允许您在不训练的情况下修改模型的行为。

**测试时计算：** 使用 RL 技术训练的推理模型可以通过在测试时扩展计算预算来进一步改进。它可以涉及多次调用、MCTS 或专门的模型（如过程奖励模型（PRM））。具有精确评分的迭代步骤显著提高了复杂推理任务的性能。

📚 **参考资料：**

- **Merge LLMs with mergekit by Maxime Labonne：** 使用 mergekit 进行模型合并的教程。
- **Smol Vision by Merve Noyan：** 专门用于小型多模态模型的笔记本和脚本集合。
- **Large Multimodal Models by Chip Huyen：** 多模态系统及该领域近期历史的概述。
- **Unsensor any LLM with abliteration by Maxime Labonne：** 直接应用可解释性技术来修改模型的风格。
- **Intuitive Explanation of SAEs by Adam Karvonen：** 关于 SAE 如何工作以及为什么它们对可解释性有意义的文章。
- **Scaling test-time compute by Beeching et al.：** 教程和实验，使用 3B 模型在 MATH-500 上超越 Llama 3.1 70B。

---

# 👷 LLM 工程师

本课程的这一部分专注于学习如何构建可在生产中使用的 LLM 驱动应用程序，重点是增强模型和部署它们。

## 1. 运行 LLM
由于硬件要求高，运行 LLM 可能很困难。根据您的用例，您可能希望简单地通过 API（如 GPT-4）使用模型或在本地运行它。无论哪种情况，额外的提示和引导技术都可以改善和约束应用程序的输出。

**LLM API：** API 是部署 LLM 的便捷方式。这个领域分为私有 LLM（OpenAI、Google、Anthropic 等）和开源 LLM（OpenRouter、Hugging Face、Together AI 等）。

**开源 LLM：** Hugging Face Hub 是查找 LLM 的好地方。您可以直接在 Hugging Face Spaces 中运行其中一些，或在 LM Studio 等应用程序中下载并在本地运行它们，或通过 CLI 使用 llama.cpp 或 ollama。

**提示工程：** 常见技术包括零样本提示、少样本提示、思维链和 ReAct。它们在更大的模型上效果更好，但可以适应较小的模型。

**结构化输出：** 许多任务需要结构化输出，如严格的模板或 JSON 格式。可以使用 Outlines 等库来指导生成并遵守给定的结构。一些 API 还使用 JSON 模式原生支持结构化输出生成。

📚 **参考资料：**

- **Run an LLM locally with LM Studio by Nisha Arya：** 关于如何使用 LM Studio 的简短指南。
- **Prompt engineering guide by DAIR.AI：** 带有示例的提示技术详尽列表。
- **Outlines - Quickstart：** Outlines 启用的引导生成技术列表。
- **LMQL - Overview：** LMQL 语言介绍。

## 2. 构建向量存储
创建向量存储是构建检索增强生成（RAG）流程的第一步。加载文档，进行分割，并使用相关块生成向量表示（嵌入），这些表示存储供推理期间将来使用。

**摄取文档：** 文档加载器是方便的包装器，可以处理多种格式：PDF、JSON、HTML、Markdown 等。它们还可以直接从某些数据库和 API（GitHub、Reddit、Google Drive 等）检索数据。

**分割文档：** 文本分割器将文档分解为更小的、语义上有意义的块。与其在 n 个字符后分割文本，通常更好的做法是按标题或递归分割，并带有一些额外的元数据。

**嵌入模型：** 嵌入模型将文本转换为向量表示。选择特定于任务的模型可显著提高语义搜索和 RAG 的性能。

**向量数据库：** 向量数据库（如 Chroma、Pinecone、Milvus、FAISS、Annoy 等）旨在存储嵌入向量。它们能够根据向量相似性高效检索与查询"最相似"的数据。

📚 **参考资料：**

- **LangChain - Text splitters：** LangChain 中实现的不同文本分割器列表。
- **Sentence Transformers library：** 流行的嵌入模型库。
- **MTEB Leaderboard：** 嵌入模型排行榜。
- **The Top 7 Vector Databases by Moez Ali：** 最佳和最流行向量数据库的比较。

## 3. 检索增强生成（RAG）
通过 RAG，LLM 从数据库中检索上下文文档以提高其答案的准确性。RAG 是一种无需任何微调即可增强模型知识的流行方式。

**编排器：** LangChain 和 LlamaIndex 等编排器是将 LLM 与工具和数据库连接的流行框架。模型上下文协议（MCP）引入了一个新标准，用于跨提供商向模型传递数据和上下文。

**检索器：** 查询重写器和生成式检索器（如 CoRAG 和 HyDE）通过转换用户查询来增强搜索。多向量和混合检索方法将嵌入与关键词信号结合以提高召回率和精确度。

**记忆：** 为了记住以前的指令和答案，ChatGPT 等 LLM 和聊天机器人将此历史记录添加到其上下文窗口中。可以通过摘要（例如，使用较小的 LLM）、向量存储 + RAG 等来改进此缓冲区。

**评估：** 我们需要评估文档检索（上下文精确度和召回率）和生成阶段（忠实度和答案相关性）。可以使用 Ragas 和 DeepEval（评估质量）等工具进行简化。

📚 **参考资料：**

- **Llamaindex - High-level concepts：** 构建 RAG 流程时需要了解的主要概念。
- **Model Context Protocol：** MCP 介绍，包括动机、架构和快速入门。
- **Pinecone - Retrieval Augmentation：** 检索增强过程概述。
- **LangChain - Q&A with RAG：** 构建典型 RAG 流程的分步教程。
- **LangChain - Memory types：** 具有相关用法的不同类型记忆列表。
- **RAG pipeline - Metrics：** 用于评估 RAG 流程的主要指标概述。

## 4. 高级 RAG
实际应用程序可能需要复杂的流程，包括 SQL 或图数据库，以及自动选择相关工具和 API。这些高级技术可以改进基线解决方案并提供附加功能。

**查询构造：** 存储在传统数据库中的结构化数据需要特定的查询语言，如 SQL、Cypher、元数据等。我们可以通过查询构造直接将用户指令转换为查询以访问数据。

**工具：** 代理通过自动选择最相关的工具来提供答案来增强 LLM。这些工具可以像使用 Google 或 Wikipedia 一样简单，也可以更复杂，如 Python 解释器或 Jira。

**后处理：** 最终步骤，处理输入到 LLM 的输入。它通过重新排序、RAG 融合和分类来增强检索文档的相关性和多样性。

**程序化 LLM：** DSPy 等框架允许您以程序化方式基于自动化评估优化提示和权重。

📚 **参考资料：**

- **LangChain - Query Construction：** 关于不同类型查询构造的博客文章。
- **LangChain - SQL：** 关于如何使用 LLM 与 SQL 数据库交互的教程，涉及文本到 SQL 和可选的 SQL 代理。
- **Pinecone - LLM agents：** 介绍代理和工具及不同类型。
- **LLM Powered Autonomous Agents by Lilian Weng：** 关于 LLM 代理的更理论性文章。
- **LangChain - OpenAI's RAG：** OpenAI 采用的 RAG 策略概述，包括后处理。
- **DSPy in 8 Steps：** DSPy 通用指南，介绍模块、签名和优化器。

## 5. 代理
LLM 代理可以通过基于对其环境的推理采取行动来自主执行任务，通常通过使用工具或函数与外部系统交互。

**代理基础：** 代理使用思考（内部推理以决定下一步做什么）、行动（执行任务，通常通过与外部工具交互）和观察（分析反馈或结果以改进下一步）来运作。

**代理协议：** 模型上下文协议（MCP）是将代理连接到外部工具和数据源（通过 MCP 服务器和客户端）的行业标准。最近，Agent2Agent（A2A）试图标准化代理互操作性的通用语言。

**供应商框架：** 如果您特别依赖某个供应商，每个主要云模型提供商都有自己的代理框架，包括 OpenAI SDK、Google ADK 和 Claude Agent SDK。

**其他框架：** 可以使用不同的框架简化代理开发，如 LangGraph（工作流的设计和可视化）、LlamaIndex（使用 RAG 的数据增强代理）或自定义解决方案。更实验性的框架包括不同代理之间的协作，例如 CrewAI（基于角色的团队工作流）和 AutoGen（对话驱动的多代理系统）。

📚 **参考资料：**

- **Agents Course：** Hugging Face 制作的关于 AI 代理的流行课程。
- **LangGraph：** 如何使用 LangGraph 构建 AI 代理的概述。
- **LlamaIndex Agents：** 使用 LlamaIndex 构建代理的用例和资源。

## 6. 推理优化
文本生成是一个昂贵的过程，需要昂贵的硬件。除了量化之外，还提出了各种技术来最大化吞吐量并降低推理成本。

**Flash Attention：** 优化注意力机制，将其复杂性从二次转换为线性，从而加快训练和推理速度。

**键值缓存：** 了解键值缓存以及多查询注意力（MQA）和分组查询注意力（GQA）中引入的改进。

**推测解码：** 使用小型模型生成草稿，然后由较大的模型审查，以加快文本生成速度。EAGLE-3 是一个特别流行的解决方案。

📚 **参考资料：**

- **GPU Inference by Hugging Face：** 解释如何在 GPU 上优化推理。
- **LLM Inference by Databricks：** 在生产中优化 LLM 推理的最佳实践。
- **Optimizing LLMs for Speed and Memory by Hugging Face：** 解释优化速度和内存的三种主要技术，即量化、Flash Attention 和架构创新。
- **Assisted Generation by Hugging Face：** HF 版本的推测解码。这是一篇关于它如何工作的有趣博客文章，包含实现它的代码。
- **EAGLE-3 paper：** 介绍 EAGLE-3 并报告高达 6.5 倍的加速。
- **Speculators：** vLLM 制作的库，用于构建、评估和存储用于 LLM 推理的推测解码算法（例如 EAGLE-3）。

## 7. 部署 LLM
大规模部署 LLM 是一项工程壮举，可能需要多个 GPU 集群。在其他情况下，演示和本地应用程序可以以低得多的复杂性实现。

**本地部署：** 隐私是开源 LLM 相对于私有 LLM 的重要优势。本地 LLM 服务器（LM Studio、Ollama、oobabooga、kobold.cpp 等）利用此优势为本地应用程序提供动力。

**演示部署：** Gradio 和 Streamlit 等框架有助于原型应用程序和共享演示。您还可以轻松在线托管它们，例如使用 Hugging Face Spaces。

**服务器部署：** 大规模部署 LLM 需要云（另请参阅 SkyPilot）或本地基础设施，并且通常利用优化的文本生成框架，如 TGI、vLLM 等。

**边缘部署：** 在受限环境中，MLC LLM 和 mnn-llm 等高性能框架可以在 Web 浏览器、Android 和 iOS 中部署 LLM。

📚 **参考资料：**

- **Streamlit - Build a basic LLM app：** 使用 Streamlit 制作基本的类似 ChatGPT 的应用程序的教程。
- **HF LLM Inference Container：** 使用 Hugging Face 的推理容器在 Amazon SageMaker 上部署 LLM。
- **Philschmid blog by Philipp Schmid：** 关于使用 Amazon SageMaker 部署 LLM 的高质量文章集合。
- **Optimizing latence by Hamel Husain：** 在吞吐量和延迟方面比较 TGI、vLLM、CTranslate2 和 mlc。

## 8. 保护 LLM
除了与软件相关的传统安全问题之外，LLM 由于训练和提示方式而具有独特的弱点。

**提示攻击：** 与提示工程相关的不同技术，包括提示注入（额外指令以劫持模型的答案）、数据/提示泄露（检索其原始数据/提示）和越狱（制作提示以绕过安全功能）。

**后门：** 攻击向量可以针对训练数据本身，通过毒化训练数据（例如，使用虚假信息）或创建后门（秘密触发器以在推理期间改变模型的行为）。

**防御措施：** 保护 LLM 应用程序的最佳方法是针对这些漏洞进行测试（例如，使用红队和像 garak 这样的检查）并在生产中观察它们（使用 langfuse 等框架）。

📚 **参考资料：**

- **OWASP LLM Top 10 by HEGO Wiki：** LLM 应用程序中看到的 10 个最关键漏洞列表。
- **Prompt Injection Primer by Joseph Thacker：** 为工程师提供的关于提示注入的简短指南。
- **LLM Security by @llm_sec：** 与 LLM 安全相关的资源广泛列表。
- **Red teaming LLMs by Microsoft：** 关于如何使用 LLM 执行红队的指南。

---

## 致谢
此路线图受到 Milan Milanović 和 Romano Roth 的优秀 DevOps 路线图的启发。

特别感谢：

- **Thomas Thelen** 激励我创建路线图
- **André Frade** 对第一稿的输入和审查
- **Dino Dunn** 提供有关 LLM 安全的资源
- **Magdalena Kuhn** 改进"人工评估"部分
- **Odoverdose** 建议 3Blue1Brown 关于 Transformers 的视频
- **所有为本课程中的教育参考资料做出贡献的人 :)**

**免责声明：** 我与此处列出的任何来源均无关联。
