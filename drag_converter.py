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
from PIL import Image #用來開圖片、轉圖片格式、存成 PDF
import fitz  # PyMuPDF 處理PDF(開啟檔案、讀取檔案)


class DragConverter:
    def __init__(self):
        self.desktop = Path.home() / "Desktop" #桌面路徑
        self.image_exts = {".jpg", ".jpeg", ".png", ".jfif", ".bmp", ".webp"}
        #看副檔名有沒有在set 判斷是不是圖片

    def run(self, file_paths):
        if not file_paths: #如果檔案路徑是空的 print
            print("沒有接收到檔案。")
            print("請把檔案直接拖到這個程式圖示上。")
            return

        success_count = 0
        fail_count = 0

        for file_path in file_paths:
            try:
                result = self.process_file(Path(file_path))
                if result:
                    success_count += 1
                else:
                    fail_count += 1
            except Exception as e:
                fail_count += 1
                print(f"\n處理失敗:{file_path}")
                print(f"錯誤原因：{e}")

        print("\n全部處理完成。")
        print(f"成功：{success_count} 個，失敗：{fail_count} 個")

    def process_file(self, file_path: Path):
        if not file_path.exists():
            print(f"\n找不到檔案:{file_path}")
            return False

        ext = file_path.suffix.lower() # p.suffix 取得副檔名

        if ext in self.image_exts:
            self.image_to_pdf(file_path)
            return True
        elif ext == ".pdf":
            self.pdf_to_images(file_path)
            return True
        else:
            print(f"\n不支援的檔案格式:{file_path.name}")
            return False

    def image_to_pdf(self, image_path: Path): #處理只有一張的圖片
        output_path = self.get_unique_file_path(self.desktop / f"{image_path.stem}.pdf")  #image_path.stem = 取檔名但不含副檔名

        with Image.open(image_path) as img:
            img = img.convert("RGB")
            img.save(output_path, "PDF", resolution=100.0)

        print(f"\n圖片轉 PDF 成功：")
        print(f"{image_path.name} -> {output_path}")

    def pdf_to_images(self, pdf_path: Path):
        output_folder = self.get_unique_folder_path(self.desktop / f"{pdf_path.stem}_images")
        output_folder.mkdir(parents=True, exist_ok=True)

        with fitz.open(pdf_path) as doc:
            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap(dpi=200)
                output_path = output_folder / f"{pdf_path.stem}_page_{page_num + 1}.png"
                pix.save(str(output_path))

        print(f"\nPDF 轉圖片成功：")
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


if __name__ == "__main__":#
    converter = DragConverter()
    converter.run(sys.argv[1:])
