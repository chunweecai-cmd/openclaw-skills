# pdf-tools

PDF 工具箱 - 合并、拆分、压缩、转换 PDF 文件。

## 功能

- **合并 PDF**：将多个 PDF 文件合并为一个
- **拆分 PDF**：按页码范围拆分 PDF
- **压缩 PDF**：减小 PDF 文件大小
- **PDF 转图片**：将 PDF 页面转换为图片
- **提取文本**：从 PDF 中提取文字内容

## 使用方法

### 合并 PDF

```bash
openclaw skill run pdf-tools --action merge --input "file1.pdf,file2.pdf" --output "merged.pdf"
```

### 拆分 PDF

```bash
# 提取第 1-5 页
openclaw skill run pdf-tools --action split --input "document.pdf" --pages "1-5" --output "extracted.pdf"

# 提取单页
openclaw skill run pdf-tools --action split --input "document.pdf" --pages "3" --output "page3.pdf"
```

### 压缩 PDF

```bash
openclaw skill run pdf-tools --action compress --input "large.pdf" --output "compressed.pdf" --quality medium
```

### PDF 转图片

```bash
openclaw skill run pdf-tools --action pdf2img --input "document.pdf" --output "output_folder" --format png
```

### 提取文本

```bash
openclaw skill run pdf-tools --action extract-text --input "document.pdf" --output "content.txt"
```

## 参数说明

| 参数 | 说明 | 可选值 |
|------|------|--------|
| `--action` | 操作类型 | merge, split, compress, pdf2img, extract-text |
| `--input` | 输入文件路径 | 文件路径，多个文件用逗号分隔 |
| `--output` | 输出文件/文件夹路径 | 路径 |
| `--pages` | 页码范围（拆分用） | "1-5", "3", "1,3,5-10" |
| `--quality` | 压缩质量 | low, medium, high |
| `--format` | 输出图片格式 | png, jpg |

## 示例

```bash
# 合并所有报告
openclaw skill run pdf-tools --action merge --input "report1.pdf,report2.pdf,report3.pdf" --output "annual_report.pdf"

# 压缩扫描件
openclaw skill run pdf-tools --action compress --input "scan.pdf" --output "scan_small.pdf" --quality medium
```

## 依赖

- Python 3.6+
- PyPDF2
- Pillow
- pdf2image (可选，用于 PDF 转图片)

## 安装依赖

```bash
pip install PyPDF2 Pillow pdf2image
```

## 作者

chunweecai-cmd

## 版本

1.0.0

## 许可证

MIT License
