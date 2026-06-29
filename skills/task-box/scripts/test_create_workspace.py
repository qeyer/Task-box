import tempfile
import unittest
from pathlib import Path

from create_workspace import create_workspace


class CreateWorkspaceTests(unittest.TestCase):
    def test_creates_only_planned_folders_and_task_note(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            plan = {
                "project_root": str(root),
                "task_name": "口播字幕包装",
                "task_folder": "口播字幕包装",
                "goal": "完成一套口播字幕视觉包装",
                "folders": [
                    {"path": "原始素材", "purpose": "视频、音频和字幕源文件"},
                    {"path": "工作文件/脚本", "purpose": "处理脚本"},
                    {"path": "最终成品", "purpose": "交付视频"},
                ],
                "deliverables": ["字幕包装成片", "可复用字幕模板"],
            }
            result = create_workspace(plan)
            task_dir = root / "口播字幕包装"
            self.assertEqual(result, task_dir.resolve())
            self.assertTrue((task_dir / "原始素材").is_dir())
            self.assertTrue((task_dir / "工作文件" / "脚本").is_dir())
            self.assertTrue((task_dir / "最终成品").is_dir())
            self.assertFalse((task_dir / "预览").exists())
            note = (task_dir / "任务说明.md").read_text(encoding="utf-8")
            self.assertIn("完成一套口播字幕视觉包装", note)
            self.assertIn("工作文件/脚本", note)

    def test_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = {
                "project_root": tmp,
                "task_name": "越界测试",
                "task_folder": "../escape",
                "goal": "测试",
                "folders": [],
                "deliverables": [],
            }
            with self.assertRaisesRegex(ValueError, "task_folder"):
                create_workspace(plan)

    def test_rejects_absolute_subfolder(self):
        with tempfile.TemporaryDirectory() as tmp:
            plan = {
                "project_root": tmp,
                "task_name": "绝对路径测试",
                "task_folder": "安全目录",
                "goal": "测试",
                "folders": [{"path": "C:/outside", "purpose": "不应创建"}],
                "deliverables": [],
            }
            with self.assertRaisesRegex(ValueError, "folders"):
                create_workspace(plan)

    def test_refuses_to_overwrite_existing_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "重复任务").mkdir()
            plan = {
                "project_root": str(root),
                "task_name": "重复任务",
                "task_folder": "重复任务",
                "goal": "测试",
                "folders": [],
                "deliverables": [],
            }
            with self.assertRaises(FileExistsError):
                create_workspace(plan)


if __name__ == "__main__":
    unittest.main(verbosity=2)
