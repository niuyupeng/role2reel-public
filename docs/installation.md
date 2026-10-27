# 安装、更新与卸载

[返回首页](../README.md) · [English installation guide](installation.en.md) · [开发工具](development.md) · [English usage](usage.en.md)

公开版是仓库根目录的**整个 Skill 包**，安装目录与调用名均为 `role2reel-public`。不要覆盖内部 `role2reel`。普通文字使用不需要先运行 Python、初始化工程或配置独立 API Key。

## 选择安装方式

| 方式 | 适用情况 | 注意事项 |
|---|---|---|
| Codex 内置 skill-installer | 在对话中从仓库安装 | 仓库路径选 `.`，名称明确设为 `role2reel-public`；已有目录时不是自动更新 |
| 手动解压命名 Release ZIP | 固定发布版本，不装 Git/Python | 核对同版本校验值，在临时目录解压后安装完整目录 |
| 可选发布安装器 | 校验包、保守更新与回滚 | 需 Python 3.11+；只接收新路径或其自身管理且未修改的安装 |
| Git 检出 | 开发或维护本地修改 | 明确所用分支/标签，更新前保存修改 |

在有内置安装器的 Codex 中发送：

```text
$skill-installer 从 https://github.com/niuyupeng/role2reel-public 安装仓库根目录的 Skill，名称设为 role2reel-public。
```

需要固定版本时，另外指定 Release 中的实际标签。不能只复制 `SKILL.md`，否则引用、模板和工具会缺失。下一轮调用 `$role2reel-public`；若未发现，按下文核对目录并新开会话。文件落盘成功和某个具体客户端确实发现技能是不同的检查结果。

## CODEX_HOME 与手动 Git 安装

Codex 内置安装器使用 `$CODEX_HOME/skills`；未设置 `CODEX_HOME` 时使用 `~/.codex/skills`。请采用**正在运行的宿主**使用的值，不要只在临时终端设另一个值，也不必为套示例改变既有环境。Windows 默认是用户目录下的 `.codex\skills`；macOS/Linux 默认是 `$HOME/.codex/skills`。

Windows PowerShell，新安装：

```powershell
$skillHome = if ([string]::IsNullOrWhiteSpace($env:CODEX_HOME)) {
    Join-Path $env:USERPROFILE '.codex'
} else { $env:CODEX_HOME }
$skillDir = Join-Path (Join-Path $skillHome 'skills') 'role2reel-public'
if (Test-Path -LiteralPath $skillDir) { throw '目录已存在，请按更新说明操作。' }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $skillDir) | Out-Null
git clone https://github.com/niuyupeng/role2reel-public.git "$skillDir"
```

macOS / Linux，新安装：

```bash
skill_home="${CODEX_HOME:-$HOME/.codex}"
skill_dir="$skill_home/skills/role2reel-public"
mkdir -p "$skill_home/skills"
git clone https://github.com/niuyupeng/role2reel-public.git "$skill_dir"
```

新安装须使用尚不存在的目标路径；已有公开版请走更新。命令为带空格路径保留引号。以上说明的是文件操作，不表示已在所有系统的所有 Codex 客户端验证自动发现。

正确结构为：

```text
<Codex home>/skills/
  role2reel-public/
    SKILL.md
    VERSION
    agents/
    references/
    assets/
    scripts/
    docs/
```

不要嵌成 `role2reel-public/role2reel-public/SKILL.md`。GitHub 自动生成的 “Source code” 压缩包有仓库/标签外层目录，与下面的命名发布包及校验值不同。

## Release 下载、校验与手动安装

到 [Releases](https://github.com/niuyupeng/role2reel-public/releases) 选择同一个版本，下载三个附件到技能目录和项目目录以外的空临时目录：

- `role2reel-public-v<VERSION>.zip`
- `role2reel-public-v<VERSION>.manifest.json`
- `SHA256SUMS.txt`

`<VERSION>` 是该发布的实际版本，不是要求把尖括号写进文件名。历史包可能使用旧命名，请按具体 Release 的附件核对，不混用两个版本。

Linux，在附件所在目录：

```bash
sha256sum -c SHA256SUMS.txt
```

macOS：

```bash
shasum -a 256 -c SHA256SUMS.txt
```

Windows PowerShell，逐项将实际哈希与 `SHA256SUMS.txt` 中对应文件比较：

```powershell
Get-ChildItem -File -Filter 'role2reel-public-v*' | Get-FileHash -Algorithm SHA256
Get-Content -LiteralPath .\SHA256SUMS.txt
```

不一致时停止安装，重新取得匹配文件。校验值说明下载字节与可信发布声明一致，不是数字签名、安全审计或创作质量证明。manifest 记录版本、标签、源提交及文件哈希；也要确认发布来源，不只看文件名。

手动安装时先在临时目录解压，再将里面完整的 `role2reel-public` 目录复制到选定的 `skills` 目录。已有安装不直接叠加覆盖，按下文保存旧目录再替换。剧本、媒体、用户词库与项目记录应放在技能目录之外。

## 可选：带完整性检查的发布安装器

仅需 Python 3.11+ 标准库，普通文字任务不用运行。先验证 ZIP，再从可信检出或已验证的临时解压目录运行脚本。先创建父级 `skills` 目录；首次安装的 `role2reel-public` 路径应不存在。安装器仅接收 `build_release.py` 生成、含 `.release.json` 的版本发布 ZIP，不能用于基本 `package_skill.py` ZIP 或 GitHub 自动源码包。

下列是参数模板，请替换路径和哈希；macOS/Linux 可把 `python` 换成所选的 `python3`：

```text
python scripts/install_release.py install --archive "<ZIP绝对路径>" --sha256 <可信记录中的ZIP的64位十六进制哈希> --destination "<Codex home>/skills/role2reel-public"
python scripts/install_release.py verify --destination "<Codex home>/skills/role2reel-public"
```

`--sha256` 使用 ZIP 的哈希，不是 manifest 的哈希。目标末级目录必须正好叫 `role2reel-public`。已有目录必须是安装器自身管理且内容未被更改的版本；手动/Git 安装、局部修改、删文件或加入新文件都会被拒绝。只有与包内 Python 源文件对应的有限字节码缓存例外；不自动接管或合并本地工作。

同一条 `install` 命令可更新未改动的受管理安装。旧版会保存到技能目录之外的 `<Codex home>/role2reel-backups/role2reel-public-<id>`，脚本打印确切路径。不要把备份放回任何技能发现目录，否则其中的 `SKILL.md` 可能形成重复技能。技术约束与中断恢复见[发布维护说明](releasing.md)。

## 更新：先保护自己的文件

先记录已装 `VERSION` 和源标签/提交，将**整个公开版目录**备份到所有技能发现目录之外。项目另存；若以前把剧本或素材放进安装目录，先搬出并检查，再执行替换。

- **安装器管理的版本：**先 `verify`，再安装已校验的新包。检测到修改就先保存、审阅；没有强制覆盖选项。确需替换时，把旧目录整体归档到技能目录外，在原公开版路径重新安装，然后有选择地合入需要保留的改动。
- **手动 ZIP / Codex 内置安装器：**保留整个旧目录到技能目录外，再将新版安装到空出的 `role2reel-public` 路径。逐项合入自定义改动，不把整个旧目录盖回新版，以免恢复旧规则和已经删除的文件。
- **Git：**在公开版检出中先看 `git status --short`，保存或提交本地改动。干净分支可 `git pull --ff-only`；停在发行标签上的分离 HEAD 应先获取标签，再切到明确选定的新标签。不要用 `reset --hard` 或 `clean` 代替保留工作。有本地提交且历史分叉时，明确选择合并/变基或另行安装，不能强行替换。

内部 `role2reel` 保持独立。升级 Skill 不等于改写用户项目，也不自动重做已有输出。完成后检查 `SKILL.md` 与 `VERSION`，必要时重开会话，先做一个小型文字任务确认使用路径。

### 回滚

受安装器管理的安装，使用之前打印的确切备份路径：

```text
python scripts/install_release.py rollback --destination "<Codex home>/skills/role2reel-public" --backup "<之前打印的备份路径>"
```

仅接受其备份目录内符合生成命名的备份，并检查两端内容；当前版本会另存为新备份，打印路径。不要绕过本地改动拒绝。手动回滚同理：先将当前公开版归档到技能目录外，再把保存的旧目录恢复为 `role2reel-public`。Git 可在保存改动后回到记录的旧标签/提交。回滚只恢复技能文件，不撤销其间修改过的项目或生成结果。

### 卸载与旧版迁移

确认准确的 `role2reel-public` 安装目录及其内容。可先移到所有技能目录之外，可逆地停用；确认没有需要保留的项目文件后，也可仅删除该目录。不要删除父级 `skills`、内部 `role2reel`、用户项目、模型权重或应用配置。备份另外决定保留还是删除。

历史 `public-2026-10-27` 首包使用过 `role2reel/` 根目录；同名目录也可能是真正内部版。先识别并保留内容，再将当前公开版独立安装为 `role2reel-public`，不能一概把旧 `role2reel` 删掉。

## 故障与兼容性边界

| 情况 | 检查方法 |
|---|---|
| 调用名未出现 | 宿主实际 `CODEX_HOME`、末级目录名、是否多嵌套一层、`SKILL.md` 是否完整；再新开会话 |
| 重复技能或规则冲突 | 检查所用各技能目录，把旧副本和备份移出发现范围 |
| 引用缺失 | 安装整个包，保留子目录，不只复制入口文件 |
| 校验值不一致 | ZIP、manifest、校验文件必须来自同一发布；不要用命名ZIP的哈希检验自动源码包 |
| 更新被拒绝 | 按报错保存并查看本地增删改或非受管理目录；不要删标记文件绕过保护 |
| Git更新失败 | 检查本地修改、分离HEAD或分叉历史，先保留工作再选维护方式 |
| 缺少PyYAML | 按[工具说明](development.md)用所选解释器装开发依赖；不影响不运行脚本的文字任务 |
| 无Word/生图/视频工具 | 如实交文字方案或使用当前可用工具；安装Skill不等于新增这些服务 |

已支持的使用入口是能读取本地 Skill 的 Codex。软件测试范围以 [EVALS](../EVALS.md) 与具体 CI 记录为准：Windows/Ubuntu 的 Python 检查不证明所有客户端、macOS 自动发现或其他助手的兼容性。其他助手可以阅读这些方法，但自动安装、调用和工具衔接需要单独验证。外部服务是否需要凭据由所选服务决定，不把凭据写入公开包。
