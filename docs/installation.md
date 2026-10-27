# 安装与维护 · Installation

[返回首页](../README.md) · [English overview](../README.en.md)

## 推荐：让 Codex 安装

```text
$skill-installer 从 https://github.com/niuyupeng/role2reel-public 安装仓库根目录的 Skill，名称设为 role2reel-public。
```

The skill lives at the repository root. With the built-in installer, select path `.` and explicitly set the destination name to `role2reel-public`. Installation should keep the full directory together, not only copy SKILL.md.

下一轮可以调用 `$role2reel-public`。若未发现，检查安装位置、是否多嵌套一层目录，并重新打开会话。

## 手动安装

以下使用默认 `~/.codex/skills`。若你设置了 `CODEX_HOME`，请使用其 `skills` 子目录；已有其他受支持的技能安装位置可继续使用，但只安装一份公开版。

macOS / Linux:

```bash
mkdir -p "$HOME/.codex/skills"
git clone https://github.com/niuyupeng/role2reel-public.git "$HOME/.codex/skills/role2reel-public"
```

Windows PowerShell:

```powershell
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.codex\skills" | Out-Null
git clone https://github.com/niuyupeng/role2reel-public.git "$env:USERPROFILE\.codex\skills\role2reel-public"
```

或者下载 [最新 Release](https://github.com/niuyupeng/role2reel-public/releases/latest) 的命名 ZIP，解压后应为：

```text
skills/
  role2reel-public/
    SKILL.md
    VERSION
    agents/
    references/
    assets/
    scripts/
```

保留整个文件夹。不要把源码下载包再嵌套成 `role2reel-public/role2reel-public/`，也不要覆盖内部 `role2reel/`。

## 验证下载

每个命名 ZIP 随附 `.sha256` 校验文件。比较 ZIP 的 SHA-256 与该文件第一列；文件名可能随版本变化。

macOS / Linux（两个文件在同一目录）：

```bash
shasum -a 256 -c Role2Reel_Public_20261027_Quality.sha256
```

Windows PowerShell:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath .\Role2Reel_Public_20261027_Quality.zip
Get-Content -LiteralPath .\Role2Reel_Public_20261027_Quality.sha256
```

This checks downloaded bytes against the release's declared checksum; it is not a software or creative-quality review.

## 更新与卸载

Git安装：先保存本地修改，再在**公开版目录**执行 `git pull --ff-only`。ZIP安装：先备份本地修改，再用新包更新公开版目录。保持内部版独立，不合并内部私有案例。

卸载只移除 `role2reel-public` 技能目录。**项目必须放在技能目录之外**，不能把自己的剧本当作安装文件一起删除。用户自己的模型、编辑器和项目资料不属于这个包。

旧 `public-2026-10-27` 首包曾使用 `role2reel/` 根目录。已有此目录时先保留原内容，改装最新独立的 `role2reel-public/`；不要把已有内部版当成旧包直接删除。

## 常见问题

- **需要API Key吗？** 普通 Skill 文字使用由当前 Codex 会话执行；包内没有独立模型账号。外部图片/视频/协作服务是否需要凭据，由你选择的服务决定。不要把凭据写入仓库。
- **需要先跑Python吗？** 普通文字任务不需要手动运行脚本。初始化、结构审计和打包是可选开发工具；见[开发工具](development.md)。
- **其他助手能用吗？** 指令和方法可以阅读；这里的安装和自动检查以Codex Skill及所列Python环境为范围，未宣称其他宿主的自动发现兼容。
- **会直接出视频吗？** 本包交付创作方法、文本和本地工具。实际图像、文档和视频操作需要当前环境的相应工具及已授权任务。没有这些工具时应交付方案并说明缺项。
- **为何不让我先审所有分镜？** 选择资产优先模式时，内部分镜完成后直接交付整段提示词；明确要求分镜表时仍可查看和修改。
