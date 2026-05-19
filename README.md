<p align="center">
  <img src="assets/logo.png" alt="峰子分析" width="120">
</p>

<h1 align="center">峰子分析 · Fengzi Analysis</h1>

<p align="center">
  <strong>美股板块轮动实时分析工具 | US Sector Rotation Dashboard</strong>
</p>

<p align="center">
  <a href="https://fengzistockanalysis.streamlit.app/">🌐 在线体验 Live Demo</a> ·
  <a href="https://github.com/kfqylf/fengzi-analysis/releases">📦 下载桌面版</a> ·
  <a href="#功能特性">✨ 功能特性</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.32+-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License">
  <img src="https://img.shields.io/github/stars/kfqylf/fengzi-analysis?style=social" alt="Stars">
</p>

---

## 功能特性

**17 个板块** — GICS 11 大行业 + 6 大主题板块（半导体、商业航天、航空国防、软件、生物科技、核电）

**龙头等权合成** — 每个板块精选 10 只美股龙头，等权合成板块指数，比单只 ETF 更准确

**多维度分析** — YTD / 1日 / 5日 / 20日 / 60日 收益率 + 相对 SPY 强度

**高级可视化**
- 多周期热力图 — 一眼看清各板块各时段强弱
- 轮动散点图 — 动量 vs 趋势，识别板块轮动阶段
- 矩阵树图 — 市场全景俯瞰
- 雷达图 — 单板块多维画像
- 棒棒糖图 — 成分股涨跌排名

**中英双语** — 一键切换中文 / English 界面

**AI 解读** — 可选接入 DeepSeek AI，智能生成板块轮动分析报告

---

## 在线使用

直接访问，无需安装：

**https://fengzistockanalysis.streamlit.app/**

---

## 本地安装

### 方式一：一键启动（Windows）

1. [下载 ZIP](https://github.com/kfqylf/fengzi-analysis/releases)
2. 解压到任意文件夹
3. 双击 `峰子分析.bat`
4. 首次会自动安装依赖，浏览器自动打开

### 方式二：手动安装

```bash
git clone https://github.com/kfqylf/fengzi-analysis.git
cd fengzi-analysis
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

浏览器打开 http://localhost:8501

---

## AI 解读（可选）

1. 复制 `.env.example` 为 `.env`
2. 填入 `DEEPSEEK_API_KEY=你的密钥`
3. 在界面勾选「AI 解读」

未配置时使用内置规则模板，同样可读。

---

## 板块列表

| 类型 | 板块 |
|------|------|
| GICS | 科技、金融、医疗保健、通信服务、可选消费、必需消费、工业、能源、原材料、公用事业、房地产 |
| 主题 | 半导体、商业航天/太空、航空航天国防、软件、生物科技、核电 |

每个板块由 10 只精选龙头股等权合成，代表该板块整体走势。

---

## 项目结构

```
fengzi-analysis/
├── app.py                  # Streamlit 主入口
├── src/
│   ├── sectors.py          # 板块定义 & 龙头池
│   ├── data.py             # yfinance 行情拉取
│   ├── basket.py           # 等权合成指数
│   ├── rotation.py         # 轮动指标 & 标签
│   ├── market_date.py      # 交易日判定
│   ├── ai_summary.py       # DeepSeek / 模板摘要
│   ├── i18n.py             # 中英双语文案
│   └── ui/
│       ├── theme.py        # 暗色主题 & KPI 卡片
│       └── charts.py       # Plotly 高级图表
├── assets/logo.png         # 品牌 Logo
├── requirements.txt
└── .streamlit/config.toml  # 主题配置
```

---

## 技术栈

| 模块 | 技术 |
|------|------|
| 前端 | Streamlit + Plotly |
| 数据 | yfinance (Yahoo Finance) |
| AI | DeepSeek API (可选) |
| 语言 | Python 3.10+ |

---

## 免责声明

本工具仅供研究与学习，不构成任何投资建议。行情数据来自 Yahoo Finance，可能存在延迟。投资有风险，决策需谨慎。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/kfqylf">kfqylf</a>
</p>
