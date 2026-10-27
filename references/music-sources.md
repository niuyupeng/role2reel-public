# AI 音乐方向：来源与融合决策

核验日期：2026-09-23。下面是方法来源，不是作品效果证明。第三方技能只作只读研究，未执行其脚本或照搬全文；本扩展重新组织为适用于用户分工的规则。外部 main 分支会变化，升级时重新核对，不声称本扩展等于其最新版本。

## 本地能力继承

|来源|保留的能力|适用范围/不带入|
|Role2Reel既有方法|意义忠实、人物与动作因果、五字段分镜、剪辑/生成时钟、属性级引用、源素材绑定|原剧本/人物路径保留；音乐分支不强制重建人生传记|
|本机 imagegen 的 SKILL.md 与 references/prompting.md|用途、构图、具体约束、参考图角色、局部编辑与单变量修订|真正生/改图时读取可用技能；不把CLI参数误当内置工具参数|
|本机 wedding-mv-director 及 directing.md|音乐段落先于平均切镜；素材ID贯穿；区分设计、预览和实片验收|不带入婚礼特有人物、照片与输出流程|
|本机 ffmpeg-video-editor|先探测源文件，区分源时间、成片时间、精确裁剪|仅需要媒体测量或用户授权处理时调用；不因技能融合自动渲染视频|
|本机 skill-creator|按需披露、清晰触发、验证实际边界|不把“全面”变成每个任务都加载全部手册|

这些是本轮实际检查并取用的方法；此前提到但未读到的技能不能声称已吸收。剪映/Remotion仍是可选执行工具，不是选题、画风或提示词判断的依据。

## 公开资料

|ID与来源|本轮读取范围|用于什么|边界|
|S01 [YouTube Shorts discovery](https://support.google.com/youtube/answer/11914225?hl=en)|官方正文|观看选择、停留、满意度与观众匹配；没有单一偏好格式|不外推成抖音算法|
|S02 [Shorts analytics](https://support.google.com/youtube/answer/12942217?hl=en)|官方正文|区分观看与划走等指标、流量入口|后台字段以实际账户为准|
|S03 [YouTube Trends](https://support.google.com/youtube/answer/11962757?hl=en)|官方正文|搜索需求、相似作者作品、内容缺口作为选题线索|页面提示地区/语言/设备及版本差异|
|S04 [Thumbnail & title tips](https://support.google.com/youtube/answer/12340300?hl=en)|官方正文|标题/封面共同兑现内容承诺，按入口检查效果|不将常规视频封面策略直接等同Shorts流|
|S05 [抖音优质创作指南](https://www.douyin.com/video/7369165937590783284)|搜索摘要；正文无法展开|人设、内容方向与呈现是可研究维度|2024历史入口；未观看教程、不推导时长阈值|
|S06 [B站创作中心封面模板](https://www.bilibili.com/opus/604733602895505877)|公开文字页|封面为独立制作环节|历史功能介绍，不证明当前规格或画风偏好|
|S07 [Runway I2V guide](https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide)|官方正文|图定义起点，文字重点描述运动；起点图瑕疵会影响视频|当前文档说明面向Gen-4.5；临用核验|
|S08 [Runway Gen-4 guide](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide)|官方正文|简洁、正向动作描述的模型适配|旧型号时长不迁移到Seedance|
|S09 [Seedance 2.5官方发布](https://seed.bytedance.com/en/blog/one-take-creation-flexible-referencing-introducing-seedance-2-5)|2026-07-31官方正文|当前支持多模态与多镜头，提示按媒体属性分别引用|厂商能力说明不是本项目实测；不能保证逐毫秒执行|
|S10 [musical-mv-storyboard](https://github.com/huangserva/musical-mv-storyboard/blob/main/SKILL.md)|公开SKILL主体，显示v2.11|采用音乐先行、完整乐句、服装状态、设定图与镜头图区别|不继承外部API、固定付费流程、固定镜头秒数、强制自动生成|
|S11 [storyboard-video-previs](https://github.com/gainubi/storyboard-video-skill/blob/main/SKILL.md)|公开SKILL文本|镜头目的、画面节奏、情绪递进|分镜网格是规划，非所有I2V的主图|
|S12 [storyboard-prompt-assistant](https://github.com/seaartpublic/skills/blob/main/storyboard-prompt-assistant/SKILL.md)|公开SKILL文本|镜头表、用途与交接说明|不替换用户既定Role2Reel字段|
|S13 [Seedance 2.0](https://seed.bytedance.com/en/seedance2_0)|官方产品页|确认多模态概念的来源|历史型号能力不覆盖2.5界面|

## 排除与待研究

未将第三方Seedance品牌网站视为字节官方；未将搜索聚合页当实时热榜；未将“2026抖音创作者大会”的媒体转述当本项目流量提升依据；未将2018年B站专栏封面比例当视频投稿规格。公开作品搜索可发现候选，但尚未完成跨平台足量视听样本研究，因此本扩展没有发布“当前最热门画风榜”。

## 冲突优先级

用户当前目标与授权→项目已定素材/角色→本次工具真实能力→本技能相关分支→外部示例。参考素材全部属性默认可借用、固定一键视频生成、强制重写歌曲、所有任务必须多轮审批等外部要求不进入此分支。真正对接模型任务时继续遵守Role2Reel原有媒体合同；简短策划回答不伪造合同完成状态。

## 表演与水墨修订的新增来源（2026-09-23）

- [Emily2040 seedance-audio](https://github.com/Emily2040/seedance-2.0/blob/main/skills/seedance-audio/SKILL.md)：本次读主体，取说话者与音频角色绑定，不宣称执行全部依赖或保证同步。
- [kissdstudio Seedance prompting](https://github.com/kissdstudio/Seedance-2.0-Skill/blob/main/SKILL.md)：取属性级引用；拒绝全局慢动作和过时参数迁移。下游prompt-patterns未取得。
- [YouTube官方Shorts访谈](https://blog.youtube/creator-and-artist-stories/youtube-shorts-deep-dive/)：开场兴趣与情节回报；创作者经验不当跨平台算法阈值。

新增方法见[音乐表演与画风](music-performance-style.md)。热门作品原提示词不可见时，不声称已逆推出原提示词；候选静帧不可替代动态表演验收。社区技能没有验证热度排名，不能因搜索排序就称最热门。

## 角色两图资产补充调研 · 2026-09-23

本次阅读以下仓库主文件，不执行其中CLI或外部生成服务；方法用本项目文字重新表述，没有复制安装整套技能。

- [fal-ai-community character-design](https://github.com/fal-ai-community/skills/blob/main/skills/character-design/SKILL.md)：采用稳定身份与场景变量分开、一张已确认脸派生表情、脸型/体型漂移需退回检查的原则；不照搬其模型路由或付费服务。
- [inference-sh character-design-sheet](https://github.com/inference-sh/skills/blob/main/guides/design/character-design-sheet/SKILL.md)：采用体态、表情与服装分层及记录比例/配色的思路；不强制四视角默认、固定描述字数或必须训练LoRA的说法，也不宣称seed保证身份。
- [alew3 character-sheet-template](https://github.com/alew3/skills/blob/main/plugins/higgsfield-seedance-video-suite/templates/character-sheet-template.md)：采用先确认身份母版、局部漂移局部修复的思路；拒绝其三视图/表情/服装/文字整合成单张大板的布局，独立图片便于按用途引用。

体态、表情、剧情造型分层；版式、基础服装与画幅按项目需求配置。模板只是可选起点，结构可检查，身份与角度仍需实际生成验收。


## 分支经验与证据的边界
整合分支时覆盖所有模块；仅提炼可复用方法，原始任务记录、分享口令、失败日志和项目事实留在本地。来源核验方法见 music-research-platforms.md；合并分支不代表原始记录获准公开。
