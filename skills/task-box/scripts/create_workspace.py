#!/usr/bin/env python3
import argparse
import json
import re
from datetime import datetime
from pathlib import Path


WINDOWS_ABSOLUTE_RE = re.compile(r"^[A-Za-z]:[\\/]")
INVALID_CHARS_RE = re.compile(r'[<>:"|?*]')


def validate_segment(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} 必须是非空字符串")
    value = value.strip()
    if "/" in value or "\\" in value or value in {".", ".."}:
        raise ValueError(f"{field} 必须是单层相对目录名：{value!r}")
    if INVALID_CHARS_RE.search(value):
        raise ValueError(f"{field} 含有非法字符：{value!r}")
    return value


def validate_relative_path(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} 必须是非空相对路径")
    value = value.strip().replace("\\", "/")
    if value.startswith("/") or WINDOWS_ABSOLUTE_RE.match(value):
        raise ValueError(f"{field} 不能是绝对路径：{value!r}")
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        raise ValueError(f"{field} 不能包含空段、. 或 ..：{value!r}")
    if any(INVALID_CHARS_RE.search(part) for part in parts):
        raise ValueError(f"{field} 含有非法字符：{value!r}")
    return Path(*parts)


def validate_plan(plan):
    if not isinstance(plan, dict):
        raise ValueError("计划必须是 JSON 对象")
    root_value = plan.get("project_root")
    if not isinstance(root_value, str) or not root_value.strip():
        raise ValueError("project_root 必须是项目根目录")
    root = Path(root_value).expanduser().resolve()
    if not root.is_dir():
        raise ValueError(f"project_root 不存在或不是目录：{root}")
    task_name = str(plan.get("task_name", "")).strip()
    if not task_name:
        raise ValueError("task_name 不能为空")
    task_folder = validate_segment(plan.get("task_folder"), "task_folder")
    goal = str(plan.get("goal", "")).strip()
    if not goal:
        raise ValueError("goal 不能为空")
    folders = plan.get("folders", [])
    if not isinstance(folders, list):
        raise ValueError("folders 必须是数组")
    normalized_folders = []
    seen = set()
    for index, item in enumerate(folders, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"folders[{index}] 必须是对象")
        relative = validate_relative_path(item.get("path"), f"folders[{index}].path")
        key = relative.as_posix().casefold()
        if key in seen:
            raise ValueError(f"folders 出现重复路径：{relative.as_posix()}")
        seen.add(key)
        normalized_folders.append(
            {
                "path": relative,
                "purpose": str(item.get("purpose", "")).strip() or "按任务需要存放相关文件",
            }
        )
    deliverables = plan.get("deliverables", [])
    if not isinstance(deliverables, list):
        raise ValueError("deliverables 必须是数组")
    deliverables = [str(item).strip() for item in deliverables if str(item).strip()]
    return root, task_name, task_folder, goal, normalized_folders, deliverables


def render_task_note(task_name, goal, project_root, folders, deliverables):
    created = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %z")
    folder_rows = (
        "\n".join(
            f"| `{item['path'].as_posix()}` | {item['purpose']} |" for item in folders
        )
        or "| （暂无子目录） | 需要时再创建，不预建空目录 |"
    )
    deliverable_rows = "\n".join(f"- [ ] {item}" for item in deliverables) or "- [ ] 根据任务推进补充"
    return f"""# {task_name}

## 目标

{goal}

## 基本信息

- 项目根目录：`{project_root}`
- 创建时间：{created}
- 当前状态：进行中

## 目录

| 路径 | 用途 |
|---|---|
{folder_rows}

## 计划交付

{deliverable_rows}

## 工作约束

- 本任务过程文件放在当前任务目录中；仓库源码遵循原有结构，用户指定位置优先。
- 只创建实际需要的子目录，不为套模板预建空目录。
- 不为整理擅自移动、覆盖或删除既有文件；已授权修改无需重复确认。

## 当前成品

尚未生成。交付时更新为实际成品的相对链接。

## 素材与续做

- 素材位置：待记录
- 下一步：按任务目标执行
- 关键决定：暂无
"""


def create_workspace(plan):
    root, task_name, folder_name, goal, folders, deliverables = validate_plan(plan)
    create_note = plan.get("create_note", False)
    if not isinstance(create_note, bool):
        raise ValueError("create_note 必须是布尔值")
    if create_note and not any(item["path"] == Path("工作文件") for item in folders):
        folders.append({"path": Path("工作文件"), "purpose": "过程文件和任务记录"})
    task_dir = (root / folder_name).resolve()
    if task_dir.parent != root:
        raise ValueError("task_folder 必须直接位于 project_root 下")
    if task_dir.exists():
        raise FileExistsError(f"任务目录已存在：{task_dir}")
    for item in folders:
        candidate = (task_dir / item["path"]).resolve()
        if task_dir not in candidate.parents:
            raise ValueError(f"folders 路径越界：{item['path']}")
    task_dir.mkdir()
    for item in folders:
        (task_dir / item["path"]).mkdir(parents=True, exist_ok=True)
    if create_note:
        note = render_task_note(task_name, goal, root, folders, deliverables)
        (task_dir / "工作文件" / "任务记录.md").write_text(note, encoding="utf-8")
    return task_dir


def main():
    parser = argparse.ArgumentParser(description="按 JSON 计划建立独立任务工作区")
    parser.add_argument("plan", type=Path, help="UTF-8 JSON 计划文件")
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text(encoding="utf-8"))
    task_dir = create_workspace(plan)
    print(json.dumps({"task_directory": str(task_dir)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
