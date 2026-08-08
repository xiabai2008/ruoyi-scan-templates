# Ruoyi-Scan 插件模板仓库

[Ruoyi-Scan](https://github.com/xiabai2008/Ruoyi-Scan) 官方插件分发源（E5/F2）。

## 结构

```
├── manifest.json       # 文件 SHA256 摘要 + Ed25519 签名（更新前强制校验）
├── signing.pub         # 发布者公钥（消费者放置到 ~/.ruoyi-scan/signing.pub 启用验签）
├── plugins_meta.json   # 全部插件元信息（name/cve/cvss/compliance）
└── plugins/
    ├── ruoyi/          # 若依插件
    ├── spring/         # Spring Boot 插件
    └── common/         # 通用插件
```

## 消费者

```bash
# 安装/更新全部插件（下载 → 校验摘要+签名 → 安装到 ~/.ruoyi-scan/plugins/）
python main.py --plugin-update

# 启用签名校验（供应链防护）
cp signing.pub ~/.ruoyi-scan/signing.pub
```

更新后插件自动被扫描器发现（无需 --plugin-path）。

## 贡献者

1. `python main.py --plugin-init <name> --category <category>` 生成插件骨架
2. 实现 `verify()`（三态判定：CONFIRMED/SAFE/UNKNOWN，网络异常绝不判 SAFE）
3. `python main.py --plugin-check <file>` 本地验证
4. 提交 PR（含测试）；合入后由维护者重新生成 manifest 并签名

> ⚠️ 本仓库内容为可执行 Python 代码：安装前请人工审查；只信任本仓库 + 已验证的签名公钥。
