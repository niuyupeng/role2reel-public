# 可选本地工具 · Optional tooling

普通文字任务直接调用 Skill；以下工具用于维护可追溯项目或验证软件，不是创作前置门槛。命令从技能/仓库根目录执行；Windows可使用已选定的Python 3.11+解释器，不替换用户的虚拟环境。

## 项目放在独立目录

macOS / Linux:

```bash
python3 scripts/init_project.py "$HOME/Documents/role2reel-projects/my-film" --characters "A,B" --scene scene-001
```

Windows PowerShell:

```powershell
python scripts/init_project.py "$env:USERPROFILE\Documents\role2reel-projects\my-film" --characters "角色甲,角色乙" --scene scene-001
```

首次初始化建立人物、场景和制作模板；再次以相同参数执行会保留已有文件。初始化生成的是待填写模板，不是已批准剧本或合格资产。

**不要为了新增角色使用 `--force`。** 它会重建已有的受管理模板，包括 `main.fountain` 等稿件，适用于已备份且明确要求重置的工程，不是增量更新。要单独建立一个未接入场景的角色，可用 `--profiles-only --characters "NewCharacter"`；将角色真正接入既有场景和关系仍需针对原文件修改，不要用重置代替更新。

## 依赖与检查

```bash
python3 -m pip install -r requirements-dev.txt
python3 scripts/validate_repo.py
python3 scripts/audit_public_export.py --tracked
python3 -m unittest discover -s tests -v
python3 scripts/package_skill.py
```

Windows将 `python3` 换成选定的 `python`。PyYAML用于YAML模板及对应审计；初始化、打包、对白检查和CSV/JSON时间检查使用标准库。缺依赖时先安装依赖，不把它误判成素材或技能损坏。

`--tracked` 隐私检查要求Git检出；安装自ZIP时使用 `python3 scripts/audit_public_export.py` 按打包白名单检查。另可通过 `--private-rules` 指向**仓库外**的本地敏感词JSON数组。扫描只是审查的一部分，不证明语义隐私已完全验证。

打包默认写入 `dist/role2reel-public.zip`。根目录固定为 `role2reel-public/`，仅包含显式白名单文件；`VERSION` 标明包版本。发布时将ZIP及对应SHA-256一同上传到匹配的GitHub tag，Release指向准确提交。

## 按任务选择工具

| 需要检查 | 工具 | 证据范围 |
|---|---|---|
| 对白审阅线索 | `scripts/audit_dialogue.py` | 警告信号，不是审美判分 |
| 分镜时间与持久源绑定 | `scripts/audit_storyboard.py` | CSV旧式结构检查，或实际源文件支撑的正式YAML检查 |
| 一镜一条的复制格式 | `scripts/audit_clipboard_prompts.py` | 固定单镜导出合同，不用于替换多镜完整段落正文 |
| 正式角色运行、人物来路与资产状态 | `scripts/audit_character_runtime.py` / `audit_life_paths.py` / `audit_continuity.py` | 对应结构、来源和绑定，不能证明表演或因果的艺术质量 |
| 视频任务结构 | `scripts/audit_video_task.py` | 已选模式与引用合同，不等于实际视频通过 |

逐项参数用 `python3 scripts/<script>.py --help` 查看。不要让用户为了普通简易表伪造一整套哈希和审批；正式机器审计需要真实上游文件。更多工具限制见[生产合同](../references/production-contracts.md#use-the-included-resources)。

## 修改与发布

新增文件必须进入 `scripts/package_skill.py` 的白名单，确认引用可达，再检查源码和最终包。保留MIT与第三方声明。禁止从内部项目批量复制文件或Git历史到公开仓库。

回归应覆盖变化的真实约束；模型文本、静态图像、音频、动态视频和人类采用分别记录。现有脚本通过不增加媒体效果证据。公开报告状态见[EVALS](../EVALS.md)。
