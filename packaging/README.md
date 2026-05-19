# 峰子分析 · 打包发布说明

## 方式一：便携启动（推荐，最简单）

1. 将整个 `sector-rotation-demo` 文件夹复制到 U 盘或任意目录  
2. 双击 **`峰子分析.bat`**  
3. 首次会自动创建虚拟环境并安装依赖  

适合：自己用、发给朋友试用、发表 Demo 视频

## 方式二：制作 ZIP 发布包

在 PowerShell 中于项目根目录执行：

```powershell
.\packaging\create_release_zip.ps1
```

会生成 `dist/峰子分析-v1.0.zip`，内含程序与启动脚本。

## 方式三：桌面快捷方式（Windows）

```powershell
.\packaging\create_shortcut.ps1
```

会在桌面创建「峰子分析」快捷方式。

## 发表软件时建议附带

- `assets/logo.png` — 产品图标  
- `docs/SCREENSHOTS.md` — 宣传截图清单  
- 免责声明：仅供研究，不构成投资建议  

## 系统要求

- Windows 10/11  
- Python 3.10+（若未安装，`峰子分析.bat` 会尝试使用本机 Python）  
- 联网（拉取 Yahoo Finance 行情）  
