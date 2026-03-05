# TRAE Friends 社区运营维护指南

本文档旨在帮助运营团队快速上手维护本仓库内容，包括定期更新活动时间轴和修改文案。

## 1. 定期更新活动时间轴

我们采用“数据驱动”的方式来维护活动列表，您只需要维护一个 CSV 表格，运行脚本即可自动生成精美的 Markdown 时间轴并同步到中英文 README。

### 步骤一：更新数据文件

找到并编辑仓库中的数据文件：`data/events.csv`。

文件内容示例：
```csv
Date,Type,City_EN,City_ZH
2026-02-09,Talk,Hefei,合肥
2026-02-08,Workshop,Zhongshan,中山
```

**字段说明**：
- **Date**: 活动日期，格式必须为 `YYYY-MM-DD`。
- **Type**: 活动类型（如 `Talk`, `Workshop`, `Meetup`, `Demoday`, `Hackathon`, `Family Day` 等，会自动匹配对应颜色的标签）。
- **City_EN**: 城市英文名（用于英文版 README）。
- **City_ZH**: 城市中文名（用于中文版 README）。

**操作**：直接在文件末尾添加新的活动行即可。

### 步骤二：运行更新脚本

在 Trae 的终端（Terminal）中运行以下命令：

```bash
python scripts/update_readme.py
```

脚本运行成功后，`README.md` 和 `README.zh-CN.md` 中的时间轴部分会自动更新。请提交（Commit）并推送（Push）更改。

---

## 2. 使用 Trae 修改文档文案

如果您需要修改 README 中的介绍文案、数据统计或链接（参考之前的文案修改需求），可以直接通过对话让 Trae 帮您完成。

### 提示词（Prompt）示例

您可以直接将修改要求发送给 Trae，建议带上文件路径以提高准确性。

**示例 1：修改介绍文案**
> 请帮我修改 `README.zh-CN.md` 的介绍文案。
> 原文：...
> 改为：TRAE Friends 是由 TRAE Fellow 发起的城市社区活动...

**示例 2：更新统计数据**
> 把 `README.md` 和 `README.zh-CN.md` 里的数据更新一下：
> 覆盖城市：70+
> 累计场次：100+
> 参与开发者：10000+

**示例 3：替换链接**
> 把底部的“成为讲师”链接换成这个新链接：https://...

### 最佳实践 Tips
1.  **明确文件**：在对话中指明要修改的文件（如 `README.zh-CN.md`），或者将文件打开/添加到上下文中。
2.  **提供原文和新文案**：明确告诉 Trae “把什么” 改成 “什么”，避免歧义。
3.  **检查变更**：Trae 修改后会展示 Diff（差异对比），请务必确认修改内容是否符合预期。

---

## 目录结构说明

- `data/events.csv`: 活动数据源文件，用于生成时间轴。
- `scripts/update_readme.py`: 自动更新 README 时间轴的 Python 脚本。
- `README.md`: 英文版主页，包含项目介绍、统计数据和活动时间轴。
- `README.zh-CN.md`: 中文版主页，内容与英文版同步。
