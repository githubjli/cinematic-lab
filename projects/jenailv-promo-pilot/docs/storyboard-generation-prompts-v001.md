# 连续分镜生成提示词 v001

日期：2026-10-22。工具：Codex内置ImageGen。模型版本、种子和服务端采样参数未返回，标记为未知。

## S01输入顺序

1. `assets/generated/style-direction-v001/A-documentary-cg-v001.png`：光线与风格参考。
2. `assets/source/website/010-1790553932266631.jpg`：设备类别与蓝色参考。
3. `assets/source/website/025-1790490274674288.jpg`：厂房参考。
4. `assets/source/website/016-1790481828389271.jpg`：物料配色参考。

```text
Use case: illustration-story
Asset type: one 9:16 cinematic storyboard keyframe for a continuous industrial brand film
Shot S01, 0–5 seconds — CHAOS HAS VOLUME.
Input images: Image 1 sets the approved documentary-CG lighting and palette; Image 2 anchors the blue horizontal baler family; Image 3 anchors the Chinese factory; Image 4 anchors recycled material colors for later continuity.
Scene: camera at waste height moving through loose kraft cardboard and white plastic in the same factory. One recognizable blue plastic fragment is sharp near center-lower foreground and becomes the continuity hero. The blue baler is only a distant soft silhouette through layered material.
Style: photoreal industrial documentary with restrained premium CG polish.
Composition: portrait 9:16, extreme foreground occlusion, deep factory layers, organic disorder.
Lighting: cool daylight with restrained warm practical lamps, real dust and fiber texture.
Constraints: no captions, no logos, no readable text, no watermark, no UI, no panels, no PPT layout.
Avoid: garbage disaster, unsafe piles, horror mood, brochure composition, completed bale.
```

## S02输入顺序

1. `assets/generated/storyboard-v001/S01-chaos-v001.png`：上一镜头与连续性参考。
2. `assets/source/website/010-1790553932266631.jpg`：设备结构参考。
3. `assets/source/website/025-1790490274674288.jpg`：厂房参考。

```text
Use case: illustration-story
Asset type: 9:16 cinematic storyboard keyframe, Shot S02 of the same continuous industrial film
Primary request: Continue directly from Image 1. The exact recognizable blue plastic fragment from S01 now rides upward with the same kraft cardboard and white plastic on the inclined conveyor toward the same blue horizontal baler's hopper. Camera tracks very close beside the belt; the factory and full machine become clearer ahead.
Input images: Image 1 is the prior shot and continuity source; Image 2 anchors machine structure; Image 3 anchors factory environment.
Style: same photoreal industrial documentary and restrained premium CG polish as Image 1.
Composition: portrait 9:16, conveyor makes a strong lower-left to upper-right diagonal, blue fragment near lower-middle, believable belt rails and rollers, layered depth.
Lighting: identical cool daylight and warm practical lamps.
Constraints: one continuous conveyor path to the hopper; no finished bale; no people in unsafe area; no captions, logos, readable text, UI, panels, watermark or PPT layout.
Avoid: floating waste, impossible conveyor, catalog product shot, changing the blue fragment color or material batch.
```

## 中止记录

四镜并行批次长时间无返回，主动终止；其结果未知。随后S03单张生成也长时间无返回并终止，未形成可归档输出。S03–S08在v001分镜板中使用明确标注的风格、机械或官网素材代理，等待后续逐镜生成或本地ComfyUI验证。
