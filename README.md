# Ruoyi-Scan 插件模板仓库

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/xiabai2008/ruoyi-scan-templates.svg?style=social&label=Star)](https://github.com/xiabai2008/ruoyi-scan-templates)
[![GitHub forks](https://img.shields.io/github/forks/xiabai2008/ruoyi-scan-templates.svg?style=social&label=Fork)](https://github.com/xiabai2008/ruoyi-scan-templates)

[Ruoyi-Scan](https://github.com/xiabai2008/Ruoyi-Scan) 官方插件分发源（E5/F2）：开源插件经 Ed25519 签名分发，构建防供应链投毒的插件生态。

## 结构

```
├── manifest.json       # 文件 SHA256 摘要 + Ed25519 签名（更新前强制校验）
├── signing.pub         # 发布者公钥（消费者放置到 ~/.ruoyi-scan/signing.pub）
├── plugins_meta.json   # 全部插件元信息（name/cve/cvss/compliance）
├── scripts/
│   └── sign_manifest.py # 签名 manifest 脚本（CI 与本地通用）
├── .github/workflows/
│   └── sign-manifest.yml # 自动签名发布（push main / 手动触发）
└── plugins/
    ├── ruoyi/          # 若依插件
    ├── spring/         # Spring Boot 插件
    └── common/         # 通用插件
```

## 消费者（强制验签）

```bash
# 1. 放置并核对发布者公钥（首次使用必做）
cp signing.pub ~/.ruoyi-scan/signing.pub

# 2. 安装/更新全部插件（下载 → SHA256 + Ed25519 强制验签 → 安装）
python main.py --plugin-update
```

> ⚠️ **供应链安全（fail-closed）**：远程安装强制验签。无签名 / 公钥缺失 / 验签失败一律**拒绝安装**。
> 公钥指纹（SHA256）：`6784756b032928f8e19c16356f5f876496363b122ef710873c63c4e8502db760`
> 请通过独立渠道（本文档 / 主仓库）核对指纹后再信任。

更新后插件自动被扫描器发现（无需 --plugin-path）。

## 发布（CI 自动签名）

`manifest.json` 由 `.github/workflows/sign-manifest.yml` 自动重新生成并签名：

- **触发**：push 到 `main` 分支，或手动 `workflow_dispatch`
- **密钥**：Ed25519 私钥保存在 GitHub Secrets（`SIGNING_KEY`），**永不进入仓库**；公钥以 `signing.pub` 提交
- **幂等**：插件内容无变化时跳过提交，不产生噪音 commit
- **本地生成**（可选）：

  ```bash
  python scripts/sign_manifest.py --out-dir . --key-path ~/.ruoyi-scan/signing.key
  ```

## 贡献者

1. `python main.py --plugin-init <name> --category <category>` 生成插件骨架
2. 实现 `verify()`（三态判定：CONFIRMED/SAFE/UNKNOWN，网络异常绝不判 SAFE）
3. `python main.py --plugin-check <file>` 本地验证
4. 提交 PR（含测试）；合入 `main` 后由 CI 自动重新生成签名 manifest

> ⚠️ 本仓库内容为可执行 Python 代码：安装前请人工审查；只信任本仓库 + 已验证的签名公钥（见上方指纹）。

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=xiabai2008/ruoyi-scan-templates&type=Date)](https://star-history.com/#xiabai2008/ruoyi-scan-templates&Date)