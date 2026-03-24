#!/usr/bin/env python3
"""
PDF Tools - PDF 工具箱
支持合并、拆分、压缩、转换 PDF
"""

import sys
import os
from pathlib import Path

def merge_pdfs(input_files, output_file):
    """合并多个 PDF 文件"""
    try:
        from PyPDF2 import PdfMerger
        
        merger = PdfMerger()
        
        for pdf_file in input_files:
            if os.path.exists(pdf_file):
                merger.append(pdf_file)
                print(f"✓ 添加: {pdf_file}")
            else:
                print(f"⚠ 文件不存在: {pdf_file}")
        
        merger.write(output_file)
        merger.close()
        print(f"✅ 合并完成: {output_file}")
        return True
    except ImportError:
        print("❌ 请先安装依赖: pip install PyPDF2")
        return False
    except Exception as e:
        print(f"❌ 合并失败: {e}")
        return False

def split_pdf(input_file, pages, output_file):
    """按页码拆分 PDF"""
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        reader = PdfReader(input_file)
        writer = PdfWriter()
        
        total_pages = len(reader.pages)
        page_numbers = parse_page_range(pages, total_pages)
        
        for page_num in page_numbers:
            writer.add_page(reader.pages[page_num - 1])
        
        with open(output_file, 'wb') as output_pdf:
            writer.write(output_pdf)
        
        print(f"✅ 拆分完成: {output_file} (共 {len(page_numbers)} 页)")
        return True
    except ImportError:
        print("❌ 请先安装依赖: pip install PyPDF2")
        return False
    except Exception as e:
        print(f"❌ 拆分失败: {e}")
        return False

def parse_page_range(pages_str, total_pages):
    """解析页码范围字符串"""
    page_numbers = []
    
    for part in pages_str.split(','):
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            page_numbers.extend(range(int(start), int(end) + 1))
        else:
            page_numbers.append(int(part))
    
    # 过滤有效页码
    return [p for p in page_numbers if 1 <= p <= total_pages]

def compress_pdf(input_file, output_file, quality='medium'):
    """压缩 PDF 文件"""
    try:
        from PyPDF2 import PdfReader, PdfWriter
        
        reader = PdfReader(input_file)
        writer = PdfWriter()
        
        quality_settings = {
            'low': {'compress': True},
            'medium': {'compress': True},
            'high': {'compress': False}
        }
        
        for page in reader.pages:
            writer.add_page(page)
        
        with open(output_file, 'wb') as output_pdf:
            writer.write(output_pdf)
        
        original_size = os.path.getsize(input_file) / 1024
        compressed_size = os.path.getsize(output_file) / 1024
        
        print(f"✅ 压缩完成: {output_file}")
        print(f"   原大小: {original_size:.1f} KB")
        print(f"   新大小: {compressed_size:.1f} KB")
        print(f"   节省: {(1 - compressed_size/original_size)*100:.1f}%")
        return True
    except ImportError:
        print("❌ 请先安装依赖: pip install PyPDF2")
        return False
    except Exception as e:
        print(f"❌ 压缩失败: {e}")
        return False

def pdf_to_images(input_file, output_folder, format='png'):
    """将 PDF 转换为图片"""
    try:
        from pdf2image import convert_from_path
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        images = convert_from_path(input_file)
        
        for i, image in enumerate(images):
            output_path = os.path.join(output_folder, f"page_{i+1}.{format}")
            image.save(output_path, format.upper())
            print(f"✓ 生成: {output_path}")
        
        print(f"✅ 共转换 {len(images)} 页")
        return True
    except ImportError:
        print("❌ 请先安装依赖: pip install pdf2image Pillow")
        print("   注意: pdf2image 需要安装 poppler")
        return False
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        return False

def extract_text(input_file, output_file):
    """从 PDF 提取文本"""
    try:
        from PyPDF2 import PdfReader
        
        reader = PdfReader(input_file)
        text_content = []
        
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                text_content.append(f"=== 第 {i+1} 页 ===\n{text}\n")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(text_content))
        
        print(f"✅ 提取完成: {output_file}")
        print(f"   共 {len(reader.pages)} 页")
        return True
    except ImportError:
        print("❌ 请先安装依赖: pip install PyPDF2")
        return False
    except Exception as e:
        print(f"❌ 提取失败: {e}")
        return False

def show_help():
    """显示帮助信息"""
    print("""
PDF Tools - PDF 工具箱

用法: python main.py --action <操作> [参数]

操作类型:
  merge         合并多个 PDF
  split         按页码拆分 PDF
  compress      压缩 PDF
  pdf2img       PDF 转图片
  extract-text  提取文本

示例:
  python main.py --action merge --input "a.pdf,b.pdf" --output "out.pdf"
  python main.py --action split --input "doc.pdf" --pages "1-5" --output "part.pdf"
  python main.py --action compress --input "large.pdf" --output "small.pdf"
  python main.py --action pdf2img --input "doc.pdf" --output "images" --format png
  python main.py --action extract-text --input "doc.pdf" --output "text.txt"
""")

def main():
    """主函数"""
    args = sys.argv[1:]
    
    if not args or '--help' in args or '-h' in args:
        show_help()
        return
    
    # 解析参数
    action = None
    input_file = None
    output_file = None
    pages = None
    quality = 'medium'
    format_type = 'png'
    
    i = 0
    while i < len(args):
        if args[i] == '--action' or args[i] == '-a':
            action = args[i + 1] if i + 1 < len(args) else None
            i += 2
        elif args[i] == '--input' or args[i] == '-i':
            input_file = args[i + 1] if i + 1 < len(args) else None
            i += 2
        elif args[i] == '--output' or args[i] == '-o':
            output_file = args[i + 1] if i + 1 < len(args) else None
            i += 2
        elif args[i] == '--pages' or args[i] == '-p':
            pages = args[i + 1] if i + 1 < len(args) else None
            i += 2
        elif args[i] == '--quality' or args[i] == '-q':
            quality = args[i + 1] if i + 1 < len(args) else 'medium'
            i += 2
        elif args[i] == '--format' or args[i] == '-f':
            format_type = args[i + 1] if i + 1 < len(args) else 'png'
            i += 2
        else:
            i += 1
    
    # 检查必需参数
    if not action:
        print("❌ 请指定操作类型: --action merge|split|compress|pdf2img|extract-text")
        return
    
    if not input_file:
        print("❌ 请指定输入文件: --input <文件路径>")
        return
    
    if not output_file:
        print("❌ 请指定输出文件: --output <文件路径>")
        return
    
    # 执行操作
    success = False
    
    if action == 'merge':
        input_files = input_file.split(',')
        success = merge_pdfs(input_files, output_file)
    elif action == 'split':
        if not pages:
            print("❌ 拆分操作需要 --pages 参数")
            return
        success = split_pdf(input_file, pages, output_file)
    elif action == 'compress':
        success = compress_pdf(input_file, output_file, quality)
    elif action == 'pdf2img':
        success = pdf_to_images(input_file, output_file, format_type)
    elif action == 'extract-text':
        success = extract_text(input_file, output_file)
    else:
        print(f"❌ 未知操作: {action}")
        show_help()
        return
    
    if success:
        print("\n✨ 操作完成!")
    else:
        print("\n❌ 操作失败")
        sys.exit(1)

if __name__ == '__main__':
    main()
