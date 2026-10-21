# 电影化风格方向 v001

日期：2026-10-21。画幅统一为9:16。工具为Codex内置ImageGen；模型与服务端采样参数未返回，标记为未知。三张图均以官网授权素材按固定顺序作为参考：

1. `assets/source/website/010-1790553932266631.jpg`：设备外观、蓝色和大体比例。
2. `assets/source/website/025-1790490274674288.jpg`：厂房尺度与环境。
3. `assets/source/website/016-1790481828389271.jpg`：成品料包形状和材质。

## 候选

| 编号 | 文件 | SHA256 | 定位 | 适用镜头 | 已知问题 |
|---|---|---|---|---|---|
| A | `assets/generated/style-direction-v001/A-documentary-cg-v001.png` | `BEEAA3D9F5944D162055A3AE8A57AB887A221142B579E0AB9FFBE1B8F380FF37` | 工业纪实与精密CG混合 | 厂房建立、操作员尺度、生产链 | 设备和控制台细节为生成改写，不可作实机证明 |
| B | `assets/generated/style-direction-v001/B-premium-hero-v001.png` | `09BE918133A7A13BC455C0169719D267F65748E3712083A577D3B93727AC9171` | 高端工业广告 | 开场、英雄镜头、高潮出包 | 低机位和强逆光会弱化完整生产链信息 |
| C | `assets/generated/style-direction-v001/C-engineering-cutaway-v001.png` | `CE151AC320BD9D55525D3522701E2F636B884262964CC2235BBCCE599A8BC93A` | 电影化工程可视化 | 压缩原理、内部运动、流程解释 | 内部结构是概念推演，必须标注并等待工程确认 |

建议组合：A作为叙事基底，B负责开场与成品英雄镜头，C只用于短暂的概念剖切。这样既有现场可信度，也能呈现传统实拍难以拍清的压缩动作。

## 共同约束

- 不在生成图中制作品牌字、参数、认证、型号或可读控制界面；后期确定性合成。
- 不把生成出的管线、油缸、护栏、控制台或内部结构当作产品事实。
- 后续图生视频必须继承Blender v002的运动合同，不让模型改变“进料→压缩→开门→出包”的因果顺序。
- 所有人物保持安全距离并佩戴PPE；正式发布前由品牌方复核安全表现。

## 准确提示词

### A：纪实电影 + 精密CG

```text
Use case: ads-marketing
Asset type: 9:16 cinematic industrial film style-direction keyframe
Primary request: Create a photorealistic vertical film frame for a Chinese industrial baler manufacturer. Show a blue automatic horizontal baler operating inside a real, spacious recycling factory, with one PPE-equipped operator at a safe distance for human scale. Loose cardboard and plastic enter on a conveyor; the machine is the visual hero. This is a restrained documentary-and-precision-CG hybrid, grounded in the supplied product and factory references.
Input images: Image 1 is the product silhouette, blue paint and machinery proportion reference; Image 2 is the factory scale and environment reference; Image 3 is the finished compressed-bale material reference.
Scene/backdrop: large working factory, steel structure, soft atmospheric depth, believable floor wear, clean but active production line
Style/medium: premium industrial documentary cinematography with subtle CG polish, physically plausible, natural texture
Composition/framing: portrait 9:16, three-quarter low-wide view, full machine readable, operator small in midground, strong depth layers, safe negative space near upper third for later titles
Lighting/mood: cool early-morning factory light mixed with warm practical lamps, controlled haze, confident and purposeful
Color palette: deep industrial blue, graphite steel, muted kraft brown, restrained amber accents
Materials/textures: painted steel, hydraulic metal, rubber conveyor, cardboard fibers, concrete dust
Constraints: preserve the recognizable horizontal baler type and blue industrial color from the references; believable safety distance; cinematic frame rather than brochure layout; no legible brand text; no invented control-screen text; no logos; no watermark
Avoid: PPT composition, infographic panels, floating UI, exploded parts, impossible machinery, excessive sparks, sci-fi factory, glossy toy appearance
```

### B：高端工业广告

```text
Use case: ads-marketing
Asset type: 9:16 industrial hero-shot style-direction keyframe
Primary request: Create a high-end cinematic hero shot of a blue automatic horizontal baler at the decisive compression moment. The image should feel like a premium international machinery campaign: heavy scale, kinetic energy, precision, and reliability. Base the machine family and colors on the supplied product reference, while treating the result as concept visualization rather than an engineering diagram.
Input images: Image 1 is the machine appearance and color reference; Image 2 is the authentic factory reference; Image 3 is the compressed-bale texture reference.
Scene/backdrop: dark working factory aisle with distant structure and dust in the air, hints of conveyor material entering
Style/medium: photorealistic industrial advertising, anamorphic cinematic character, practical realism
Composition/framing: portrait 9:16, dramatic low three-quarter angle, machine fills lower two thirds, compression chamber and hydraulic mass emphasized, diagonal conveyor leading line, clean upper area
Lighting/mood: strong rim light through haze, small warm practical highlights, deep blue shadows, tense but controlled
Color palette: saturated machinery blue, near-black graphite, amber edge light, natural cardboard brown
Materials/textures: scuffed painted steel, brushed cylinder metal, dust motes, fibrous waste, concrete
Constraints: retain plausible industrial proportions; one coherent factory scene; no readable text, no logos, no statistics, no interface overlays, no watermark
Avoid: presentation slide, product catalog cutout, fantasy robot, neon cyberpunk, flying debris toward people, unsafe operator placement, excessive sparks
```

### C：工程可视化

```text
Use case: stylized-concept
Asset type: 9:16 engineering-visualization style-direction keyframe for an industrial film
Primary request: Create a sophisticated cinematic cutaway visualization of a blue horizontal baler compressing loose recyclable material into a dense rectangular bale. The exterior shell is partially opened only where needed so the compression plate, hydraulic rod, chamber, material flow and output direction are immediately understandable. Use the supplied product as appearance reference and the bale image as material reference. This is an explanatory concept frame, not a certified engineering cross-section.
Input images: Image 1 is the exterior product family and blue color reference; Image 2 is environmental scale reference; Image 3 is finished-bale shape and texture reference.
Scene/backdrop: minimal dark factory volume with subtle floor reflections and faint structural context
Style/medium: premium 3D industrial visualization blended with cinematic photography, clean physically based materials
Composition/framing: portrait 9:16, side three-quarter cutaway, clear left-to-right material path, compression plate and dense bale visually separated, full machine kept inside safe margins
Lighting/mood: precise cool key light, restrained amber accents along moving interfaces, calm and analytical
Color palette: industrial blue shell, graphite interior, steel cylinder, kraft and muted recycled-material colors
Materials/textures: powder-coated metal, machined steel, fibrous compressed waste, matte concrete
Constraints: show one continuous machine and one clear compression action; no labels or arrows because those will be composited later; no legible brand text; no logo; no dimensions; no watermark
Avoid: classroom infographic, multiple panels, exploded-view separation, transparent toy plastic, impossible internal mechanisms, sci-fi holograms
```
