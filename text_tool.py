"""
Path():
    p.exists() 判斷檔案或資料夾是否存在
    p.suffix 取得副檔名
    p.name 取得檔名（含副檔名）
    p.stem 取得檔名（不含副檔名）
    p.parent 取得資料夾路徑

"""

import sys #讀程式執行時附帶的參數
from pathlib import Path
import subprocess


class TextTool:
    def __init__(self):
        self.desktop = Path.home() / "Desktop" #桌面路徑
        self.text_exts = {".txt"}

    def run(self, file_paths):
        if not file_paths: #如果檔案路徑是空的 print
            print("沒有接收到檔案。")
            print("請把 txt 檔案直接拖到這個程式圖示上。")
            return

        text_files = []
        other_files = []

        for file_path in file_paths:
            path = Path(file_path)

            if not path.exists():
                print(f"\n找不到檔案:{path}")
                continue

            if path.suffix.lower() in self.text_exts:
                text_files.append(path)
            else:
                other_files.append(path)

        for other in other_files:
            print(f"\n不支援的檔案格式:{other.name}")

        if not text_files:
            print("\n沒有可處理的 txt 檔案。")
            return

        if len(text_files) > 1:
            print("\n文字工具一次只建議拖 1 個 txt 檔。")
            return

        text_file = text_files[0]
        choice = self.choose_action()

        if choice is None:
            print("\n已取消操作。")
            return

        try:
            if choice == "字數統計":
                self.text_statistics(text_file)
            elif choice == "轉大寫":
                self.text_to_upper(text_file)
            elif choice == "轉小寫":
                self.text_to_lower(text_file)

            print("\n全部處理完成。")

        except Exception as e:
            print(f"\n文字檔處理失敗:{text_file}")
            print(f"錯誤原因：{e}")

    def choose_action(self):
        script = '''
        choose from list {"字數統計", "轉大寫", "轉小寫"} with prompt "請選擇文字工具功能：" default items {"字數統計"}
        '''
        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)

        output = result.stdout.strip()

        if output == "false" or output == "":
            return None

        return output

    def text_statistics(self, text_path: Path):
        content = text_path.read_text(encoding="utf-8")

        char_count = len(content)
        char_count_no_space = len(content.replace(" ", "").replace("\n", "").replace("\t", ""))
        line_count = len(content.splitlines())

        words = content.split()
        word_count = len(words)

        output_path = self.get_unique_file_path(self.desktop / f"{text_path.stem}_statistics.txt")

        result_text = (
            f"檔名：{text_path.name}\n"
            f"總字元數（含空白）：{char_count}\n"
            f"總字元數（不含空白）：{char_count_no_space}\n"
            f"總單字數：{word_count}\n"
            f"總行數：{line_count}\n"
        )

        output_path.write_text(result_text, encoding="utf-8")

        print(f"\n文字統計成功：")
        print(f"{text_path.name} -> {output_path}")

    def text_to_upper(self, text_path: Path):
        content = text_path.read_text(encoding="utf-8")
        output_path = self.get_unique_file_path(self.desktop / f"{text_path.stem}_upper.txt")

        output_path.write_text(content.upper(), encoding="utf-8")

        print(f"\n文字轉大寫成功：")
        print(f"{text_path.name} -> {output_path}")

    def text_to_lower(self, text_path: Path):
        content = text_path.read_text(encoding="utf-8")
        output_path = self.get_unique_file_path(self.desktop / f"{text_path.stem}_lower.txt")

        output_path.write_text(content.lower(), encoding="utf-8")

        print(f"\n文字轉小寫成功：")
        print(f"{text_path.name} -> {output_path}")

    def get_unique_file_path(self, path: Path):
        if not path.exists():
            return path

        counter = 1
        while True:
            new_path = path.with_name(f"{path.stem}_{counter}{path.suffix}")
            if not new_path.exists():
                return new_path
            counter += 1


if __name__ == "__main__":
    tool = TextTool()
    tool.run(sys.argv[1:])