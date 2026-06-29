# Codex 任务收纳

这是“任务收纳”规则与 `$task-box` Skill 的便携安装包，用来让 Codex 在新项目、新支线或会产生多个文件的新任务开始时，先建立独立任务目录，再把素材副本、过程文件、预览和交付物有规律地放好。

## 包含内容

- `AGENTS.md`：全局自动触发规则。
- `skills/task-box/`：任务收纳 Skill。
- `install.ps1`：Windows 一键安装脚本。

## 在另一台 Windows 电脑安装

1. 登录有权访问本私有仓库的 GitHub 账户，下载 ZIP 并解压。
2. 在解压后的目录打开 PowerShell。
3. 执行：

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\install.ps1
```

4. 重新打开 Codex，或新建一个 Codex 会话。

安装脚本会把 Skill 放到当前用户的 `~\.codex\skills\task-box`。如果该位置已经有旧版，脚本会先在同一目录创建带时间戳的备份。

对于全局 `AGENTS.md`：

- 如果文件不存在，直接安装本仓库中的规则。
- 如果文件已存在但没有“任务收纳”章节，只追加这一章节。
- 如果已经存在“任务收纳”章节，不重复添加。

## 手动安装

也可以手动复制：

- `skills/task-box` → `C:\Users\你的用户名\.codex\skills\task-box`
- `AGENTS.md` → `C:\Users\你的用户名\.codex\AGENTS.md`

如果另一台电脑已经有自己的 `AGENTS.md`，不要直接覆盖；把本仓库 `AGENTS.md` 中的“任务收纳”章节合并进去。

## 验证 Skill

```powershell
python "$HOME\.codex\skills\task-box\scripts\test_create_workspace.py"
```

测试全部通过后，可以直接对 Codex 说：

> 新开一个任务，帮我把这次产生的文件单独收纳。

即使不专门点名 `$task-box`，全局规则也会在符合条件的新任务第一次写文件前自动调用它。
