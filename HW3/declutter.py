import os
import shutil
import hashlib
import argparse
from datetime import datetime

# 定義檔案分類規則 (可依需求自行擴充)
FILE_CATEGORIES = {
    'Images (圖片)': ['.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp', '.bmp'],
    'Documents (文件)': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.xls', '.ppt', '.pptx', '.md', '.csv'],
    'Media (影音)': ['.mp4', '.mp3', '.avi', '.mkv', '.wav', '.mov'],
    'Archives (壓縮檔)': ['.zip', '.tar', '.gz', '.rar', '.7z'],
    'Code (程式碼)': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.json', '.xml']
}

def get_file_hash(filepath, block_size=65536):
    """計算檔案的 SHA-256 雜湊值，用於精準判斷檔案內容是否完全相同"""
    hasher = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for block in iter(lambda: f.read(block_size), b''):
                hasher.update(block)
        return hasher.hexdigest()
    except Exception as e:
        print(f"無法讀取檔案 {filepath}: {e}")
        return None

def get_category(extension):
    """根據副檔名取得分類資料夾名稱"""
    for category, exts in FILE_CATEGORIES.items():
        if extension.lower() in exts:
            return category
    return 'Others (其他)'

def organize_and_deduplicate(target_dir):
    """核心邏輯：掃描、去重與分類"""
    if not os.path.exists(target_dir):
        print(f"❌ 找不到目錄: {target_dir}")
        return

    print(f"🔍 開始掃描目錄: {target_dir}\n")

    # 建立「重複檔案暫存區」，基於安全考量，我們不直接刪除，而是移過去讓使用者確認
    duplicates_dir = os.path.join(target_dir, 'Duplicates_Trash (重複檔案)')
    
    seen_hashes = {}
    stats = {'moved': 0, 'duplicates': 0, 'bytes_saved': 0}

    for filename in os.listdir(target_dir):
        filepath = os.path.join(target_dir, filename)

        # 跳過資料夾，只處理檔案
        if os.path.isdir(filepath):
            continue

        file_hash = get_file_hash(filepath)
        if not file_hash:
            continue

        file_size = os.path.getsize(filepath)

        # 1. 檢查是否為重複檔案
        if file_hash in seen_hashes:
            if not os.path.exists(duplicates_dir):
                os.makedirs(duplicates_dir)
            
            # 處理檔名衝突
            base_name, ext = os.path.splitext(filename)
            new_name = f"{base_name}_duplicate_{datetime.now().strftime('%H%M%S')}{ext}"
            dest_path = os.path.join(duplicates_dir, new_name)
            
            shutil.move(filepath, dest_path)
            stats['duplicates'] += 1
            stats['bytes_saved'] += file_size
            print(f"🗑️ 發現重複檔案: {filename} -> 已移至 {duplicates_dir}")
        
        # 2. 如果不是重複檔案，進行分類整理
        else:
            seen_hashes[file_hash] = filepath
            _, ext = os.path.splitext(filename)
            category_dir_name = get_category(ext)
            category_dir_path = os.path.join(target_dir, category_dir_name)

            if not os.path.exists(category_dir_path):
                os.makedirs(category_dir_path)

            dest_path = os.path.join(category_dir_path, filename)
            
            # 避免覆蓋同名檔案
            if not os.path.exists(dest_path):
                shutil.move(filepath, dest_path)
                stats['moved'] += 1
            else:
                print(f"⚠️ 分類資料夾已存在同名檔案，略過: {filename}")

    # 輸出整理報告
    mb_saved = stats['bytes_saved'] / (1024 * 1024)
    print("\n" + "="*40)
    print("🎉 整理完成！報告如下：")
    print(f"📂 成功分類檔案數: {stats['moved']} 個")
    print(f"👯 揪出重複檔案數: {stats['duplicates']} 個")
    print(f"💾 潛在節省空間: {mb_saved:.2f} MB")
    print("="*40)
    if stats['duplicates'] > 0:
        print(f"💡 提示: 重複的檔案已安全移至 '{duplicates_dir}'，請確認無誤後再手動刪除以釋放空間。")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="智能檔案整理與重複檔案清理工具")
    parser.add_argument("path", nargs="?", default=".", help="要整理的目錄路徑 (預設為當前目錄)")
    args = parser.parse_args()

    # 取得絕對路徑
    target_path = os.path.abspath(args.path)
    organize_and_deduplicate(target_path)
