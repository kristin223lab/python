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
import fitz  # PyMuPDF 處理PDF(開啟檔案、讀取檔案)


class PDFTool:
    def __init__(self):
        self.desktop = Path.home() / "Desktop" #桌面路徑

    def run(self, file_paths):
        if not file_paths: #如果檔案路徑是空的 print
            print("沒有接收到檔案。")
            print("請把 PDF 檔案直接拖到這個程式圖示上。")
            return

        pdf_files = []
        other_files = []

        for file_path in file_paths:
            path = Path(file_path)

            if not path.exists():
                print(f"\n找不到檔案:{path}")
                continue

            if path.suffix.lower() == ".pdf":
                pdf_files.append(path)
            else:
                other_files.append(path)

        for other in other_files:
            print(f"\n不支援的檔案格式:{other.name}")

        if not pdf_files:
            print("\n沒有可處理的 PDF 檔案。")
            return

        try:
            if len(pdf_files) == 1:
                self.split_pdf(pdf_files[0])
            else:
                self.merge_pdfs(pdf_files)

            print("\n全部處理完成。")

        except Exception as e:
            print("\nPDF 處理失敗。")
            print(f"錯誤原因：{e}")

    def merge_pdfs(self, pdf_paths):
        output_path = self.get_unique_file_path(self.desktop / "merged_pdfs.pdf")

        merged_doc = fitz.open()

        for pdf_path in pdf_paths:
            with fitz.open(pdf_path) as doc:
                merged_doc.insert_pdf(doc)

        merged_doc.save(output_path)
        merged_doc.close()

        print(f"\n多個 PDF 合併成功：")
        print(f"輸出檔案 -> {output_path}")

    def split_pdf(self, pdf_path: Path):
        output_folder = self.get_unique_folder_path(self.desktop / f"{pdf_path.stem}_split")
        output_folder.mkdir(parents=True, exist_ok=True)

        with fitz.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                new_doc = fitz.open()
                new_doc.insert_pdf(doc, from_page=page_num, to_page=page_num)

                output_path = output_folder / f"{pdf_path.stem}_page_{page_num + 1}.pdf"
                new_doc.save(output_path)
                new_doc.close()

        print(f"\nPDF 拆頁成功：")
        print(f"{pdf_path.name} -> {output_folder}")

    def get_unique_file_path(self, path: Path):
        if not path.exists():
            return path

        counter = 1
        while True:
            new_path = path.with_name(f"{path.stem}_{counter}{path.suffix}")
            if not new_path.exists():
                return new_path
            counter += 1

    def get_unique_folder_path(self, folder_path: Path):
        if not folder_path.exists():
            return folder_path

        counter = 1
        while True:
            new_folder = folder_path.with_name(f"{folder_path.name}_{counter}")
            if not new_folder.exists():
                return new_folder
            counter += 1


if __name__ == "__main__":
    tool = PDFTool()
    tool.run(sys.argv[1:])