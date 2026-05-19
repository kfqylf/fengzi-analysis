# 美股板块轮动观察 Demo

每个板块由 **10 只美股龙头等权合成指数**（GICS 11 板块 + 主题板块），计算 YTD / 1/5/20/60 日收益与相对标普500（SPY）的相对强度，可下钻查看每只成分股涨跌。

> **免责声明：** 仅供研究与学习，不构成投资建议。行情数据来自 Yahoo Finance，可能存在延迟。

## 快速启动

```powershell
cd "c:\Users\kfqyu\Documents\新建文件夹\sector-rotation-demo"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

浏览器打开终端提示的地址（通常 http://localhost:8501）。

## 可选：DeepSeek AI 解读

1. 复制 `.env.example` 为 `.env`
2. 填入 `DEEPSEEK_API_KEY=你的密钥`
3. 在界面勾选「AI 解读」

未配置时使用内置规则模板，同样可读。

## 后续做成「正式软件」建议

| 阶段 | 内容 |
|------|------|
| Demo（当前） | Streamlit + yfinance，零 API Key |
| v1 | Electron/Tauri 壳 + 本地 Python 服务，或 React 前端 |
| 数据升级 | Polygon / Finnhub 付费源、盘中刷新、更细行业分类 |
| 功能 | 自选板块、历史轮动回放、推送提醒 |

## 项目结构

```
sector-rotation-demo/
  app.py              # Streamlit 入口
  src/
    universe.py       # ETF 列表
    data.py           # 行情拉取
    rotation.py       # 指标与标签
    ai_summary.py     # DeepSeek / 模板摘要
```
