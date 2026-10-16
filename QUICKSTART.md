# 快速开始：安装、脚本与维护

每个 Skill 是什么、什么时候用、如何用中文调用，见 [README](README.md)。本页只讲技术操作。

## 1. 准备环境

本地 Python 脚本需要 Python 3.11+。以下命令在仓库根目录的 PowerShell 执行：

```powershell
python -m pip install -r requirements.txt
$env:PYTHONPATH = "."
```

检索需要可用网络及对应服务配置；PPT 制作、PDF 报告还需要当前环境具备相应工具。这两条命令不会替你安装所有制作与渲染工具。

## 2. 安装与更新的区别

新环境应将要用的 Skill **完整目录**、`explicit-skill-router` 以及所需 `shared` 依赖放到同一 Skill 根目录下，保持相对结构，例如：

```text
<skills-root>/
  research-problem-formulation/
    SKILL.md
    agents/
    references/
  ...其他需要的 Skill 完整目录...
  explicit-skill-router/
  shared/
```

不要只复制入口文件，也不要以为安装一个搜索 Skill 就不需要它引用的共享搜索代码和配置。首次整套安装时，可携带本仓库的全部 13 个工作 Skill 目录、路由器与 `shared`，再按机器调整路径和配置。

下面三个 PowerShell 脚本是**已有环境的分组同步工具，不是三个各自完整的全仓库安装器**：

| 脚本 | 同步什么 |
| --- | --- |
| `sync_expert_skills.ps1` | 四个协作 Skill、论文搜索及共享研究/搜索依赖 |
| `sync_paper_note_skills.ps1` | 阅读笔记、审稿笔记、论文 PPT、内置 BatchGen 模板及共享材料处理依赖 |
| `sync_explicit_skill_policy.ps1` | 全部工作 Skill 的入口、引用文档、显式调用配置与路由器；不包办所有脚本、配置依赖 |

按修改范围选择，策略同步放在最后：

```powershell
.\shared\scripts\sync_expert_skills.ps1
.\shared\scripts\sync_paper_note_skills.ps1
.\shared\scripts\sync_explicit_skill_policy.ps1
```

默认目标为当前用户的 `.codex/skills`、`.agents/skills`、`.claude/skills`，以及 Obsidian 笔记库中的 `.codex/skills` 和 `.claude/skills`。默认笔记库是 `~/Documents/PHR/obsidian_phr`；可用 `-VaultRoot` 或 `-TargetRoots` 指定实际位置。同步会覆盖这些包的安装副本，**先改仓库源文件，不要把安装目录当作唯一源头**。

这些脚本只处理本地目标。服务器 CLI 需另行部署依赖并检查 Linux 路径；本地成功不代表远程完成。客户端更新后可能要重启或新建会话才能重新加载。

## 3. 直接运行论文检索脚本

Skill 的自然语言调用不要求你手动跑命令。以下用于调试或复用工具：脚本输出候选 JSON，最终筛选、解读和关键原文核查仍由模型完成。

```powershell
# 固定方向的一轮雷达搜索，不会创建定时任务
python weekly-paper-radar\scripts\weekly_radar.py --candidate-pool-total 20 --weekly-target 10 --deep-read-target 4 --download-pdf

# 学习检索：默认近三年和既有研究方向
python topic-paper-finder\scripts\topic_finder.py --mode study --query "hardware aware llm serving" --limit 5 --download-pdf

# 问题边界：默认不限年份、会议和固定方向分类
python topic-paper-finder\scripts\topic_finder.py --mode problem-boundary --query "state reuse tail latency agent inference" --query "context reuse overhead negative results"

# 机制启发：默认不限年份、会议和固定方向分类
python topic-paper-finder\scripts\topic_finder.py --mode mechanism-inspiration --query "reversible resource activation delayed feedback control" --query "adaptive caching pressure tail latency"

# 查已有 Obsidian 笔记，不是上网查论文
python vault-note-finder\scripts\find_notes.py --query "DSPARK"
```

方向和来源配置见 [radar_config.yaml](weekly-paper-radar/radar_config.yaml) 与 [finder_config.yaml](topic-paper-finder/finder_config.yaml)。

下载后应报告实际文件目录与成功/失败状态，不把“找到链接”当作“PDF 已下载”。默认目录与兼容环境变量见 [README](README.md#安装前知道这几件事)。

## 4. 笔记材料清单与 PPT 检查

以下路径为示例，替换后执行。材料清单脚本不负责独立生成最终分析笔记：

```powershell
python reading-note-builder\scripts\build_reading_note.py --paper "C:\papers\paper.pdf"
python review-note-builder\scripts\build_review_note.py --paper "C:\papers\paper.pdf" --pptx "C:\papers\review.pptx" --note "C:\papers\draft.md"
```

两者都接受 `--paper`、可选 `--note` 和 `--pptx`。模型需读取全文并核对相关图表，不能把清单或幻灯片文本抽取结果当作已经理解了论文。

分析与正式评审可分别检查结构，并配对核对结论：

```powershell
python shared\obsidian\note_quality.py --kind review-analysis --path "C:\papers\analysis.md" --expected-title "Paper Title"
python shared\obsidian\note_quality.py --kind review --path "C:\papers\formal-review.md" --companion "C:\papers\analysis.md" --expected-title "Paper Title"
```

PPT 的只读检查示例：

```powershell
# 新模板优先；继续已有稿件则沿用原稿；都没有时使用内置 BatchGen 模板
python paper-presentation-builder\scripts\resolve_template.py
python paper-presentation-builder\scripts\resolve_template.py --template "C:\papers\my-template.pptx"
python paper-presentation-builder\scripts\resolve_template.py --existing-deck "C:\papers\draft.pptx"

python paper-presentation-builder\scripts\audit_deck.py --deck "C:\papers\result.pptx" --source "C:\papers\original.pptx" --preserve 1:1 --preserve 10:14 --expected-count 20 --no-notes --forbid-text OldPaperName --require-text "问题二"
```

`--preserve 10:14` 表示源文件第 10 页对应输出第 14 页，页码按实际显示顺序。只按真实编辑要求传参数；结构检查通过不等于原文解释正确或页面排版合格，仍需渲染查看。

参考文献报告的输入方式和运行命令见 [commands.md](reference-validation-report/references/commands.md)。其中命令按该 Skill 目录写出，运行前先进入对应目录；只传项目实际存在的文献输入。

## 5. 修改后验证

修改 Skill 行为、路由、脚本或依赖后，运行相关检查：

```powershell
python shared\tests\validate_expert_skills.py
python shared\tests\validate_explicit_skill_policy.py
python -m unittest discover -s tests -v
```

再同步对应安装副本并核对哈希。纯 README 修改不改变安装包，无需因此覆盖本地或服务器 Skill。

检查通过应准确说明范围：静态规则通过、夹具测试通过、安装文件一致、模型实际行为通过是不同结论，不能互相代替。行为案例和证据范围见 [协作验证](shared/tests/expert_skill_validation.md) 与 [笔记/PPT 验证](shared/tests/paper_workflow_validation.md)。
