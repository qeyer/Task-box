# Task Box 任务收纳

让 Codex 为独立任务建立清晰的工作目录，避免多个任务的素材、过程文件和成品混在一起。

## 什么时候使用

适用于：

- 新项目、新支线或同一项目中的独立任务
- 预计会产生多个文件、需要预览、交付或后续续做的任务
- 用户明确要求整理任务文件

不适用于纯问答、只读分析、状态查看和明确输出位置的单文件小修改。
用户授权执行后，Codex 会自行判断是否需要使用 `$task-box`，不再额外询问。

## 目录规则

只创建实际需要的目录，常用一级目录统一为：

| 目录 | 用途 |
| --- | --- |
| `素材` | 原始资料、图片、音视频、附件和数据 |
| `工作文件` | 草稿、脚本、分析结果、处理数据和测试记录 |
| `预览` | 审核用样张、截图、试看片和试读版本 |
| `成品` | 正式交付文件 |
| `归档` | 需要保留的历史交付版本 |

没有对应内容就不创建目录。一次性简单任务不强制生成任务记录；需要续做、交接或管理待办时，才在 `工作文件/任务记录.md` 建立记录。旧任务已有 `任务说明.md` 时继续复用，不自动移动或重命名。

## 快速安装

把下面这句话发给你的 Codex：

```text
帮我安装这个 Skill：https://github.com/qeyer/codex-task-box
```

Codex 会读取仓库、找到 `task-box`，并完成安装。

## 手动安装

如果 Codex 不支持直接安装：

1. 下载并解压本仓库。
2. 将 `skills/task-box` 复制到 `~/.codex/skills/task-box`。
3. 将本仓库 `AGENTS.md` 中的“任务收纳”章节合并到 `~/.codex/AGENTS.md`。
4. 重新打开 Codex，或新建一个 Codex 会话。

`install.ps1` 仅作为 Windows 的辅助安装脚本，不作为主要安装方式。

## 验证

```powershell
python "$HOME\.codex\skills\task-box\scripts\test_create_workspace.py"
```

macOS：

```bash
python3 "$HOME/.codex/skills/task-box/scripts/test_create_workspace.py"
```

脚本计划示例见 `skills/task-box/references/example-plan.json`，目录判断说明见 `skills/task-box/references/directory-decision-guide.md`。
