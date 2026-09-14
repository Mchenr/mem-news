# mem-news

持续跟踪开源 Agent Memory / Context Engine 的技术路线、工程现状与社区变化。

> 当前基线：2026-09-14 · [最新周报](reports/2026-09-14.md) · 数据来自项目仓库、Release、论文和可复现评测；厂商自报结果会单独标记，不把 GitHub Stars 等同于技术质量。本表 Stars 为 2026-09-07 GitHub 项目页快照。

## 结论先行

Agent Memory 已经从“聊天记录向量检索”分化成五条路线：

1. **Context Database**：将记忆、知识、技能和执行轨迹作为统一上下文管理，例如 OpenViking。
2. **Memory OS / Stateful Runtime**：让 Agent 主动编辑、分页和演化自己的记忆，例如 MemOS、Letta。
3. **Temporal Knowledge Graph**：显式表示事实何时成立、何时失效，例如 Graphiti。
4. **Extract-and-Retrieve Memory Layer**：从交互中抽取持久事实，再以向量、关键词或图检索，例如 Mem0、Memori。
5. **Learning / Graph Pipeline**：从历史交互、反馈和任务结果中归纳模型、策略或结构化知识，例如 Hindsight、Cognee、ReMe。

如果只选择一个项目做技术调研，优先看 **OpenViking、MemOS、Graphiti、Letta**；如果目标是快速接入业务，优先看 **Mem0**；如果要建立评测体系，重点参考 **Hindsight、MemOS/OmniMemEval、ReMe**。

## 技术价值 Top 10

评分权重：记忆模型创新 30%、更新与演化闭环 25%、公开评测与可复现性 20%、工程与集成 15%、开放性与可观测性 10%。排名代表当前调研优先级，不代表所有场景下的产品推荐。

| 排名 | 项目 | 当前快照 | 核心技术价值 | 主要限制 |
|---:|---|---|---|---|
| 1 | [OpenViking](https://github.com/volcengine/OpenViking) | 35,852 ★ · v0.4.19 · AGPL-3.0 | 文件系统式 Context DB，统一 Memory、Knowledge、Skills；分层加载、递归检索和可观测轨迹 | 较新；服务端 AGPL 对商业集成有约束 |
| 2 | [MemOS](https://github.com/MemTensor/MemOS) | 11,214 ★ · v2.0.33 / local plugin v2.0.19 · Apache-2.0 | 同时抽象文本、激活和参数记忆；MemCube、调度、版本、技能复用 | 架构范围大，部署和概念复杂度较高 |
| 3 | [Graphiti](https://github.com/getzep/graphiti) | 30,651 ★ · core v0.30.2 / MCP v1.1.0 · Apache-2.0 | 双时态知识图谱，适合动态事实、冲突更新和历史状态查询 | 不是完整 Memory OS；通常依赖图数据库和 LLM 抽取 |
| 4 | [Letta](https://github.com/letta-ai/letta) | 24,638 ★ · 0.16.8 · Apache-2.0 | MemGPT 的工程化延续，Agent 自主管理核心、召回与归档记忆 | 是完整 Agent Runtime，只接记忆时偏重 |
| 5 | [Hindsight](https://github.com/vectorize-io/hindsight) | 23,019 ★ · v0.9.2 · MIT | 多策略召回与 mental model；公开多套长期记忆 benchmark | 项目和结论主要来自同一团队，需独立复验成本/效果 |
| 6 | [Mem0](https://github.com/mem0ai/mem0) | 64,815 ★ · Apache-2.0 | 事实抽取、多作用域、多信号检索，生态与接入成熟度领先 | 托管平台和 OSS 能力并非完全同一条边界 |
| 7 | [Cognee](https://github.com/topoteretes/cognee) | 30,543 ★ · v1.5.4 · Apache-2.0 | Graph + Vector ECL 管线；remember/recall/improve/forget 生命周期完整 | 灵活但复杂；独立同口径评测仍不足 |
| 8 | [ReMe](https://github.com/agentscope-ai/ReMe) | 3,421 ★ · v0.4.1.11 · Apache-2.0 | 文件与向量双形态；Personal、Procedural、Tool Memory；评测代码较完整 | 生态较小且接口快速演进 |
| 9 | [Supermemory](https://github.com/supermemoryai/supermemory) | 29,248 ★ · server-v0.0.8 · MIT | 通用 Context Engine，MCP、TypeScript 和 Coding Agent 体验突出 | 云端、OSS、自托管能力边界需要逐项确认 |
| 10 | [Memori](https://github.com/MemoriLabs/Memori) | 16,467 ★ · v3.3.6 | 从对话和 Agent 执行中形成实体、事件、事实、关系、规则与技能 | 服务/平台导向明显，独立评测证据较少 |

## 横向能力比较

“强/中/弱”是基于公开架构和代码能力的定性判断，不是 benchmark 分数。

| 项目 | 时间/冲突建模 | 用户长期记忆 | 程序/经验记忆 | Agent 主动管理 | 可观测/可编辑 | 默认基础设施 |
|---|---|---|---|---|---|---|
| OpenViking | 中 | 强 | 强 | 强 | 强 | 自有 Context DB、Embedding/LLM |
| MemOS | 中 | 强 | 强 | 强 | 强 | 可插拔向量/图存储、LLM |
| Graphiti | **强** | 强 | 中 | 弱 | 中 | Neo4j/FalkorDB、Embedding/LLM |
| Letta | 中 | 强 | 强 | **强** | 强 | Letta Server、数据库/向量检索 |
| Hindsight | 强 | 强 | 强 | 中 | 中 | 单体服务/PostgreSQL 路线 |
| Mem0 | 中 | **强** | 中 | 弱 | 中 | 内嵌或外部向量库，可选图存储 |
| Cognee | 中 | 强 | 强 | 中 | 强 | SQLite/LanceDB/Kuzu 或外部后端 |
| ReMe | 中 | 强 | **强** | 中 | **强** | Markdown/BM25 或向量存储 |
| Supermemory | 中 | 强 | 中 | 中 | 中 | 本地服务或托管 API |
| Memori | 中 | 强 | 强 | 中 | 中 | BYODB、托管/VPC/本地部署路线 |

## 十个项目现状与优缺点

### 1. OpenViking

**定位。** OpenViking 把记忆看成 Agent 全部上下文的一部分，而不是独立的向量表。资源、记忆和技能映射为 `viking://` URI，并按 L0 摘要、L1 概览、L2 详情分层加载。检索先定位目录，再递归进入内容，同时保留检索轨迹。[项目说明](https://github.com/volcengine/OpenViking/blob/main/README.md)

**技术亮点。** Session commit 后异步抽取用户偏好和 Agent 经验；文件系统结构提供显式信息边界；检索路径可用于解释误召回；同一套系统还能承载知识库和技能。官方同时报告了 LoCoMo 用户记忆、tau2-bench 经验记忆和 HotpotQA 知识问答结果，覆盖面比只测对话问答的项目更完整。

**优点。** 上下文统一、分层按需加载、可观测、对 Coding Agent/长任务友好；同时覆盖“记住用户”和“复用做事经验”。

**缺点。** 体系比普通 Memory API 更重；写入阶段需要解析、摘要和索引；服务端 AGPL 需要在商业部署前确认合规边界；官方评测仍应在统一模型和统一预算下复验。

**适合。** 长任务 Agent、Coding Agent、需要知识/记忆/技能统一治理，以及需要诊断召回路径的系统。

### 2. MemOS

**定位。** MemOS 将记忆抽象为操作系统资源。`MemCube` 可以封装一个用户、Session 或 Agent 的多类记忆，`MOS` 负责路由、调度和生命周期管理。[架构说明](https://github.com/MemTensor/MemOS/blob/main/docs/en/open_source/home/memos_intro.md)

**技术亮点。** 除文本记忆外，还把 KV Cache 视为激活记忆、LoRA 等适配参数视为参数记忆；支持树形/偏好记忆、混合检索、版本管理和跨任务技能复用。配套的 [OmniMemEval](https://github.com/MemTensor/OmniMemEval) 将用户记忆和 Agent 任务记忆分为两条评测轨道。

**优点。** 概念覆盖最完整；不仅解决“把什么文本塞回提示词”，还尝试统一缓存、模型适配和技能；研究与评测资产丰富。

**缺点。** 抽象层多、组件多，学习和运维成本高；不是每类记忆都达到同样的工程成熟度；需要避免被宏大的 Memory OS 叙事掩盖具体场景成本。

**适合。** Memory OS 研究、异构记忆调度、Agent 自演化和跨任务技能沉淀。

### 3. Graphiti

**定位。** Graphiti 是 Zep 的开源 temporal context graph 引擎。数据被组织成 Episode、Entity Node 和 Fact Edge，每条信息同时记录摄取时间和事件实际发生时间。[项目说明](https://github.com/getzep/graphiti)

**技术亮点。** 双时态模型允许系统区分“现在知道这件事”和“这件事在何时成立”，并保留被新事实取代的历史关系；实体和边可按 `group_id` 隔离。

**优点。** 时间推理、事实冲突、审计轨迹和变化中的企业数据是明显强项；模型结构比扁平向量记忆更可解释。

**缺点。** 图构建需要实体抽取、去重和关系维护，成本高于事实列表；通常需要外部图数据库；它提供的是记忆核心而非完整 Agent 生命周期。

**适合。** 客户状态演化、合规时间线、动态组织知识、需要回答“某个时间点什么是真的”的应用。

### 4. Letta

**定位。** Letta 是 MemGPT 路线的持续工程化：Agent 拥有始终在上下文中的 Memory Blocks、可检索的外部记忆和消息历史，并通过工具主动修改记忆。[Memory schema](https://github.com/letta-ai/letta/blob/main/letta/schemas/memory.py)

**技术亮点。** 新的 MemFS 把长期记忆投影为 Git-backed Markdown 文件系统；系统目录进入提示词，其他文件按需发现；Git 提供版本、差异和冲突处理，后台 memory subagent 可并行整理记忆。[MemFS 说明](https://github.com/letta-ai/letta-docs-md/blob/main/concepts/memfs/index.md)

**优点。** Agent-native、自编辑和状态持久化模型成熟；研究影响力大；记忆、Agent loop、工具和身份统一。

**缺点。** 如果已有自己的 Agent Harness，只想接入 `add/search`，采用完整 Letta Runtime 的迁移成本较高；主动写记忆依赖模型行为，仍需治理错误写入和膨胀。

**适合。** 从零构建长期存活、有身份、会主动维护记忆的 Agent。

### 5. Hindsight

**定位。** Hindsight 强调 Agent 不仅能 recall，还能从历史形成可复用 mental model，并以多种检索策略支持事实、时间和多跳问题。[项目说明](https://github.com/vectorize-io/hindsight)

**技术亮点。** 团队公开了 Agent Memory Benchmark，覆盖 LoCoMo、LongMemEval、LifeBench、PersonaMem、BEAM，并区分 single-query 与 agentic retrieval，记录准确率、延迟和 token 成本。[评测说明](https://github.com/vectorize-io/hindsight/blob/main/hindsight-docs/blog/2026-03-23-agent-memory-benchmark.mdx)

**优点。** 对评测尺度、超长历史、多跳召回和成本权衡关注充分；自托管路径相对集中；更新速度快。

**缺点。** 项目方同时是方案提供者和主要评测发布者；高准确率配置可能使用更大的召回上下文，不能只看最终准确率。

**适合。** 把检索质量作为首要目标，并愿意对准确率、延迟和 token 做完整复验的团队。

### 6. Mem0

**定位。** Mem0 是最典型的通用 Memory Layer：从交互中提取持久事实，按 `user_id`、`agent_id`、`run_id` 隔离，再进行语义、关键词、实体和可选图检索。[项目说明](https://github.com/mem0ai/mem0)

**技术亮点。** API 和集成生态完整，支持从 SDK 逐步迁移到服务；当前路线增加了多信号融合、实体链接和时间相关召回。

**优点。** 上手快、社区最大、框架和存储适配丰富，适合用户画像和跨会话偏好记忆。

**缺点。** 抽取的原子事实可能损失叙事和来源上下文；冲突治理不如双时态图明确；仓库明确说明最新高分使用包含私有优化的托管平台栈，OSS 用户不能假定相同结果。

**适合。** 需要尽快给现有 Chatbot 或 Agent 加上用户长期记忆的业务。

### 7. Cognee

**定位。** Cognee 通过 Extract/Cognify/Load 管线把文本、结构化数据和交互加工为图与向量索引，并暴露 `remember`、`recall`、`improve`、`forget` 生命周期。[示例索引](https://github.com/topoteretes/cognee/blob/main/examples/README.md)

**技术亮点。** 支持自定义 ontology、DataPoint、图模型、Pipeline 和后端；Session 反馈可以调整召回，再通过 `memify` 把有用模式固化为长期图知识。

**优点。** 可扩展性强，适合组织知识、实体关系、多租户和定制图模式；本地可从 SQLite/LanceDB/Kuzu 起步。

**缺点。** Pipeline 和配置面较大；图的实体规范化、去重和演化质量仍高度依赖模型与 schema；缺少足够的独立同口径评测。

**适合。** 企业知识图谱、事件/实体密集数据，以及需要定制记忆加工管线的系统。

### 8. ReMe

**定位。** ReMe 同时提供人类可读的文件记忆 ReMeLight 和向量式记忆。向量模式明确区分 Personal、Procedural、Tool Memory。[项目说明](https://github.com/agentscope-ai/ReMe)

**技术亮点。** 文件模式维护 `MEMORY.md`、daily journal、原始 JSONL 对话和工具结果缓存，并使用 Vector + BM25 混合检索；项目包含 LoCoMo、HaluMem、BEAM 以及 Procedural Memory 任务评测。

**优点。** 文件可编辑、可迁移、证据链清晰；对任务成功/失败模式和工具经验的建模比单纯用户偏好更进一步；与 AgentScope/QwenPaw/OpenClaw 方向衔接自然。

**缺点。** 不同版本和包仍在重组；部分实验环境与公开基准并非完全一致；社区和生产案例小于头部项目。

**适合。** 中文 Agent 生态、Coding/Tool Agent、需要程序记忆以及希望文件为事实源的系统。

### 9. Supermemory

**定位。** Supermemory 是面向应用和 Agent 的 Memory/Context Engine，强调快速接入、MCP、Web/文档数据和本地部署。[项目说明](https://github.com/supermemoryai/supermemory)

**技术亮点。** 具有较完整的 TypeScript 产品栈和 Coding Agent 入口，公开材料报告了 LongMemEval 的多 Session、偏好和时间推理结果。

**优点。** 开发体验和跨工具连接较好，适合把多个数据源统一为 Agent Context；社区增长快。

**缺点。** 仓库同时包含应用、服务和商业产品相关代码，需要确认具体能力在 OSS 本地版是否完整；内部记忆演化机制不如 Memory OS 路线透明。

**适合。** TypeScript/MCP 团队、Coding Agent、希望统一网页和应用上下文的场景。

### 10. Memori

**定位。** Memori 将对话和 Agent execution 转换为结构化、持久状态，关注 entity/process/session 三层归属和现有数据库集成。[项目说明](https://github.com/MemoriLabs/Memori)

**技术亮点。** 除用户偏好外，还抽取事件、事实、人物、关系、规则与技能；主张后台增强，不阻塞主推理链；提供 Python、TypeScript、MCP、OpenClaw 和 Hermes 接入。

**优点。** 更贴近企业已有数据基础设施；执行信息比只存用户话语更完整；部署形态覆盖托管、单租户、VPC 和本地/BYODB。

**缺点。** 高级能力和平台服务边界需要验证；公开、独立、同模型 benchmark 较少；底层记忆表示和检索细节不如研究型项目透明。

**适合。** 需要把 Agent 运行过程纳入结构化审计和长期状态、且不希望替换现有数据库的企业系统。

## 怎么选

| 你的核心问题 | 优先候选 | 选择理由 |
|---|---|---|
| 记忆、知识、技能散落且召回不可诊断 | OpenViking | 统一目录、分层加载、检索轨迹 |
| 研究异构记忆和自演化 | MemOS | 文本/激活/参数记忆统一调度 |
| 事实会变化，需要历史和审计 | Graphiti | 双时态图和事实失效语义 |
| 从零构建长期有状态 Agent | Letta | Agent Runtime 与自编辑记忆一体化 |
| 优先追求长期问答准确率 | Hindsight | 多策略召回和完整 benchmark 关注 |
| 快速给现有应用加用户记忆 | Mem0 | API 简洁、生态成熟 |
| 从复杂数据建立组织记忆 | Cognee | 可定制 Graph + Vector Pipeline |
| 沉淀任务、工具和失败经验 | ReMe | Procedural/Tool Memory 与文件事实源 |
| TypeScript/MCP、多来源 Context | Supermemory | 集成和产品体验 |
| 复用现有企业数据库和结构化状态 | Memori | BYODB 与执行状态抽取 |

## 评测时必须统一的边界

不同项目公布的数字通常不可直接横比。至少固定以下条件：

- 同一数据集版本、样本范围、Answer LLM、Judge LLM 和 Prompt；
- 区分 memory construction 与 recall/answer 阶段的 token、延迟和费用；
- 区分单次检索与允许模型多次调用工具的 agentic retrieval；
- 同时报告 P50/P95/P99、召回上下文 token、写入吞吐与最终准确率；
- 测试事实更新、删除、冲突、时间推理、拒答和租户隔离，不只测“能否找回一句话”；
- 明确评测对象是 OSS、本地自托管、托管服务还是包含私有优化的平台版本。

## 周报机制

- 固定项目清单：[data/projects.json](data/projects.json)
- 原始采集脚本：[scripts/collect.py](scripts/collect.py)
- 周报目录：[reports/](reports/)
- 每周检查：Release、默认分支提交、关键 PR、README/文档、benchmark、License/部署边界；同时扫描最近 120 天创建且快速增长的新项目。
- 只有合并、发布或官方文档已经出现的内容才记为“确认新增”；PR、Issue 和路线图分别标为“开发中”或“计划”。

本地采集示例：

```bash
# 完整七日快照；推荐设置 GITHUB_TOKEN，避免匿名共享出口限流
python3 scripts/collect.py \
  --since 2026-08-21 \
  --date 2026-08-28 \
  --output /tmp/mem-news-2026-08-28.md \
  --json-output /tmp/mem-news-2026-08-28.json

# 低请求量 smoke test
python3 scripts/collect.py --project OpenViking --skip-emerging
```

## 免责声明

本项目是技术情报与研究索引，不是厂商排名。项目方 benchmark、Star 增长和营销描述仅作为线索；关键架构选型应在统一模型、数据、预算和部署边界下自行复现。
