# Aurum · 日月硬币

同一枚金色硬币的正面、反面与翻转动画，以及可直接嵌入网页的原生 Web Component。所有硬币图案均由 SVG 矢量构成，无图片、字体下载或第三方运行时依赖。

## 打开与资源

在线演示：<https://lan450.github.io/aurum-coin/>（GitHub Pages）。也可直接打开 `index.html` 离线体验完整模拟器——页面已内嵌组件与预览资源，无需启动服务器，单文件即可任意分发。

| 文件 | 用途 |
| --- | --- |
| `assets/coin-front.svg` | 日曜正面，透明背景 |
| `assets/coin-back.svg` | 月相反面，透明背景 |
| `assets/coin-flip.svg` | 自动翻转并依次停留在两面，6.4 秒无限循环 |
| `coin-simulator.js` | 完整交互组件，包含图案、样式与动画 |

三张 SVG 均使用 `viewBox="0 0 512 512"`，可等比例缩放。静态图、独立动画与组件共享面纹和投影几何；落定时恢复规范正面或反面姿态，位移、旋转及缩放归位。独立动画的首尾姿态相同，可无缝循环。已验证导出与运行时在两端及代表性中间角度的几何一致。

## 嵌入组件

将 `coin-simulator.js` 放入网站，然后加入：

```html
<script src="./coin-simulator.js"></script>
<aurum-coin id="coin" side="front" duration="2200"></aurum-coin>
```

`side` 设置首次连接时的显示面，可选 `front` 或 `back`，默认为 `front`；之后通过 `show()` 切换。`duration` 设置抛掷时长，单位毫秒，默认 `2200`，有效范围为 `0` 至 `10000`。组件跟随容器宽度，可通过 `--coin-background`、`--coin-text`、`--coin-radius` 三个 CSS 自定义属性调整外观。

## 控制与结果

```js
const coin = document.querySelector('#coin');

coin.addEventListener('coin-result', event => {
  const { side, count } = event.detail;
  console.log(side, count); // front / back，以及累计抛掷次数
});

await coin.flip();                             // 随机抛掷
await coin.flip({ result: 'back', duration: 1800 }); // 指定结果
await coin.show('front');                      // 翻面查看，不计入抛掷
await coin.show('back', { animate: false });    // 直接显示

console.log(coin.side, coin.isFlipping);        // 只读当前面与动画状态
```

`flip()` 未指定 `result` 时使用 `crypto.getRandomValues()` 选择正反面。指定 `result` 时按外部选择展示结果；动画是视觉表现，不是物理抛掷计算。

完成的 `flip()` 返回结果面，更新累计次数与最近 8 次记录，并发出会冒泡、可穿过 Shadow DOM 的 `coin-result` 事件。`show()` 返回显示面，不更新记录或发出结果事件。动画进行中的新调用返回 `null`；组件被移出文档时取消进行中的动画、还原上一落定面，并将该次调用解析为 `null`。非法面名称会使调用以 `TypeError` 拒绝。

## 动画与无障碍

组件提供原生按钮、键盘焦点、选中状态和结果播报。系统启用 `prefers-reduced-motion: reduce` 时，组件直接显示结果；演示页的动画预览同步暂停并显示静态替代图。

独立的 `coin-flip.svg` 使用 SVG SMIL 自动循环。作为 `<img>` 使用时没有交互暂停按钮，宿主页面也不能通过该图片元素直接控制内部时间轴。需要暂停、定位时间或响应减少动态效果偏好时，可内联 SVG，并由宿主调用 `pauseAnimations()`、`unpauseAnimations()` 和 `setCurrentTime()`；也可改用交互组件或静态图。

## 重新生成

在项目目录执行：

```sh
python3 src/build.py
```

生成脚本仅使用 Python 标准库，会更新三张 SVG、`coin-simulator.js` 与离线 `index.html`。修改图案请编辑 `src/motifs.py`，修改共享几何请编辑 `src/build.py`，组件与演示页源码分别位于 `src/component.js` 和 `src/demo.html`。
