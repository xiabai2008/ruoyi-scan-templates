# 贡献指南（ruoyi-scan-templates）

感谢贡献 POC！本仓库是 [Ruoyi-Scan](https://github.com/xiabai2008/Ruoyi-Scan) 的官方插件分发源。

## 流程

1. **生成骨架**（在主仓库中开发）

   ```bash
   python main.py --plugin-init <name> --category <ruoyi|spring|common>
   ```

2. **实现 `verify()`**，遵守三态判定：
   - `CONFIRMED`：确认存在（多条件联合，防误报）
   - `SAFE`：确认不存在
   - `UNKNOWN`：网络异常等无法判定——**绝不判 SAFE**

3. **本地验证**

   ```bash
   python main.py --plugin-check plugins/<category>/<name>.py
   python -m pytest tests/ -q          # 全量零回归
   ```

4. **提交 PR** 到 [Ruoyi-Scan](https://github.com/xiabai2008/Ruoyi-Scan)（使用 POC 模板）
5. 合入后维护者重新生成 `manifest.json` 并签名，本仓库自动更新

## POC 规范

| 要求 | 说明 |
|------|------|
| 必需字段 | `name`（中文）/ `cve` / `severity` / `category` / `description` / `fix` |
| 建议字段 | `fix_detail` / `reproduce` / `cvss_vector` / `compliance` / `affected_versions` |
| 安全 | 仅存在性验证；禁止破坏性 payload（写 webshell / 删数据 / 真实命令执行） |
| 降误报 | 状态码 + 正向关键字 + 负向排除（WAF 页/错误页）联合判定 |
| 注释 | 简体中文 |

## 常见拒绝原因

- 缺少测试、全量回归失败
- 判定条件过宽（单关键字即判 CONFIRMED）
- 网络异常判 SAFE
- 破坏性 payload
- 漏洞未经自建靶场/授权目标复现

## 奖励

合入的 POC 贡献者进入 README 贡献者署名墙 🎉
