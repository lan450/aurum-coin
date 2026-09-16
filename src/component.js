/* Aurum — zero-dependency SVG coin simulator. */
(() => {
  'use strict';
  if (customElements.get('aurum-coin')) return;
  const COIN_SVG = __COIN_SVG__;
  const names = { front: '正面 · 日曜', back: '反面 · 月相' };
  const ease = t => t * t * t * (t * (t * 6 - 15) + 10);
  const fmt = n => Math.abs(n) < 0.00005 ? '0' : String(Number(n.toFixed(4)));
  let instance = 0;

  class AurumCoin extends HTMLElement {
    constructor() {
      super();
      this._side = 'front';
      this._busy = false;
      this._history = [];
      this._count = 0;
      this.attachShadow({ mode: 'open' });
      // Unique paint IDs also support browsers that resolve fragment URLs globally.
      const prefix = `aurum-${++instance}-`;
      const ids = [...COIN_SVG.matchAll(/\bid="([^"]+)"/g)].map(match => match[1]);
      let svg = COIN_SVG;
      for (const id of ids) {
        svg = svg.replaceAll(`id="${id}"`, `id="${prefix}${id}"`)
          .replaceAll(`#${id}"`, `#${prefix}${id}"`)
          .replaceAll(`#${id})`, `#${prefix}${id})`);
      }
      svg = svg.replace('aria-labelledby="coinTitle coinDesc"', `aria-labelledby="${prefix}coinTitle ${prefix}coinDesc"`);
      this.shadowRoot.innerHTML = `
        <style>
          :host { display:block; color:var(--coin-text,#eee9da); font-family:Inter,-apple-system,BlinkMacSystemFont,"PingFang SC","Microsoft YaHei",sans-serif; }
          * { box-sizing:border-box; } button { font:inherit; -webkit-tap-highlight-color:transparent; }
          .simulator { position:relative; padding:30px 32px 24px; overflow:hidden; background:var(--coin-background,#192322); border-radius:var(--coin-radius,20px); }
          .topline { display:flex; justify-content:space-between; align-items:center; gap:16px; }
          .edition { color:#b3b5a9; font-size:10px; font-weight:500; letter-spacing:2.8px; }
          .ready { display:flex; align-items:center; gap:7px; color:#bbbdaf; font-size:11px; }
          .ready::before { content:""; width:5px; height:5px; background:#d1b976; border-radius:50%; box-shadow:0 0 9px #d1b97645; }
          .stage { position:relative; width:min(100%,400px); margin:8px auto 0; isolation:isolate; }
          .stage::before { content:""; position:absolute; inset:10% 0; z-index:-1; background:radial-gradient(ellipse,#c3ae7420,transparent 65%); }
          .stage svg { display:block; width:100%; height:auto; overflow:visible; filter:drop-shadow(0 18px 16px #0004); }
          .floor { position:absolute; left:24%; bottom:3%; width:52%; height:6%; z-index:-1; background:radial-gradient(ellipse,#0008,transparent 67%); opacity:.8; transform:scale(1); }
          .caption { text-align:center; margin:-1px 0 22px; }
          .eyebrow { color:#b8a576; font-size:10px; letter-spacing:3.2px; margin-bottom:7px; font-family:Georgia,serif; }
          .result { display:block; margin:0; min-height:29px; font-weight:400; font-size:22px; letter-spacing:3px; }
          .hint { margin:9px 0 0; color:#a3aaa0; font-size:12px; letter-spacing:1px; }
          .controls { max-width:300px; margin:auto; }
          .sides { display:flex; justify-content:center; gap:4px; padding:4px; margin-bottom:14px; border:1px solid #eff0da16; border-radius:9px; background:#101b1a60; }
          .side { min-height:38px; flex:1; display:flex; justify-content:center; align-items:center; gap:8px; border:0; border-radius:6px; color:#aeb5a8; background:transparent; cursor:pointer; font-size:12px; transition:background .18s,color .18s; }
          .side[aria-pressed="true"] { color:#e8dab3; background:#a6b29916; box-shadow:0 1px 3px #0002; }
          .side:hover:not(:disabled) { color:#f8e7ba; background:#ffffff0c; }
          .sun,.moon { display:inline-block; width:12px; height:12px; border-radius:50%; border:1px solid #d0b477; }
          .sun { background:#d0b477; box-shadow:inset 0 0 0 2px #192322; }
          .moon { background:linear-gradient(90deg,#d0b477 50%,transparent 50%); }
          .toss { width:100%; min-height:50px; display:flex; justify-content:center; align-items:center; gap:13px; border:1px solid #f4db9a; border-radius:8px; color:#30291a; background:linear-gradient(115deg,#ead6a0,#c8a967); box-shadow:0 3px 10px #0002,inset 0 1px #ffffff45; font-size:14px; font-weight:600; letter-spacing:2px; cursor:pointer; transition:filter .18s,transform .18s; }
          .toss:hover:not(:disabled) { filter:brightness(1.09); transform:translateY(-1px); }
          .toss:active:not(:disabled) { transform:translateY(1px); }
          .toss:disabled { cursor:wait; filter:saturate(.7); }
          button:focus-visible { outline:2px solid #fff1c3; outline-offset:4px; }
          .side:disabled { cursor:default; opacity:.55; }
          .toss svg { width:17px; height:17px; }
          .foot { margin:23px auto 0; max-width:300px; display:flex; justify-content:space-between; align-items:center; min-height:19px; color:#8f9b91; font-size:10px; letter-spacing:.5px; }
          .history { display:flex; gap:6px; align-items:center; min-height:14px; }
          .history i { width:9px; height:9px; display:block; border:1px solid #ceb477; border-radius:50%; }
          .history i[data-side="front"] { background:#ceb477; }
          .history i[data-side="back"] { background:linear-gradient(90deg,#ceb477 50%,transparent 50%); }
          .history i:last-child { box-shadow:0 0 0 2px #cfb57820; }
          @media (max-width:420px) { .simulator{padding:23px 22px 22px} .stage{margin-top:10px} .edition{font-size:9px;letter-spacing:2px} .caption{margin-bottom:20px} .result{font-size:20px} }
          @media (prefers-reduced-motion:reduce) { * { transition:none !important; } }
        </style>
        <section class="simulator" aria-label="日月硬币模拟器">
          <div class="topline"><span class="edition">SOL & LUNA / 01</span><span class="ready">等待抛掷</span></div>
          <div class="stage"><div class="floor"></div>${svg}</div>
          <div class="caption"><div class="eyebrow">A LITTLE CHANCE</div><output class="result" aria-live="polite" aria-atomic="true">${names.front}</output><p class="hint">让偶然，给你一个答案。</p></div>
          <div class="controls">
            <div class="sides" role="group" aria-label="查看硬币两面">
              <button class="side" type="button" data-side="front" aria-pressed="true"><i class="sun" aria-hidden="true"></i>正面</button>
              <button class="side" type="button" data-side="back" aria-pressed="false"><i class="moon" aria-hidden="true"></i>反面</button>
            </div>
            <button class="toss" type="button"><svg viewBox="0 0 20 20" aria-hidden="true"><path d="M5 9a5 5 0 1 1 1.5 7M5 9V4M5 9h5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg><span>抛掷硬币</span></button>
          </div>
          <div class="foot"><span class="count">尚未抛掷</span><div class="history" role="img" aria-label="暂无抛掷记录"></div></div>
        </section>`;
      const $ = selector => this.shadowRoot.querySelector(selector);
      this._nodes = {
        svg: $('.stage svg'), lift: $('[data-lift]'), twist: $('[data-twist]'), scale: $('[data-scale]'),
        edge: $('[data-edge-path]'), clip: $('[data-edge-clip]'), front: $('[data-face="front"]'), back: $('[data-face="back"]'),
        offsets: [...this.shadowRoot.querySelectorAll('[data-offset]')], squashes: [...this.shadowRoot.querySelectorAll('[data-squash]')],
        floor: $('.floor'), result: $('.result'), ready: $('.ready'), toss: $('.toss'), count: $('.count'), history: $('.history'),
        sides: [...this.shadowRoot.querySelectorAll('.side')]
      };
      this._nodes.toss.addEventListener('click', () => this.flip());
      for (const button of this._nodes.sides) button.addEventListener('click', () => this.show(button.dataset.side));
    }

    connectedCallback() {
      if (!this._initialized) {
        this._initialized = true;
        if (this.getAttribute('side') === 'back') this._side = 'back';
        this._render(this._side === 'front' ? 0 : Math.PI);
        this._updateResult();
      }
    }

    disconnectedCallback() { this._cancelAnimation?.(); }
    get side() { return this._side; }
    get isFlipping() { return this._busy; }

    /** Random toss; optional result is useful when an external system chooses a side. */
    async flip({ result, duration } = {}) {
      if (result !== undefined && !['front', 'back'].includes(result)) throw new TypeError('result must be front or back');
      if (this._busy) return null;
      if (result === undefined) result = (crypto.getRandomValues(new Uint32Array(1))[0] & 1) === 0 ? 'front' : 'back';
      return this._animate(result, duration ?? Number(this.getAttribute('duration') || 2200), true);
    }

    /** Show a chosen side without adding a toss to the history. */
    async show(side, { animate = true } = {}) {
      if (!['front', 'back'].includes(side)) throw new TypeError('side must be front or back');
      if (this._busy) return null;
      if (side === this._side) return side;
      return this._animate(side, animate ? 700 : 0, false);
    }

    _render(angle, flight = 0, twist = 0) {
      let c = Math.cos(angle), s = Math.sin(angle), sx = Math.max(Math.abs(c), .0001);
      if (Math.abs(s) < .00001) { s = 0; sx = 1; }
      const dx = 7 * s * (c >= 0 ? 1 : -1), half = 7 * Math.abs(s), rx = 194 * sx;
      const edge = `M ${fmt(-half)} -194 H ${fmt(half)} A ${fmt(rx)} 194 0 0 1 ${fmt(half)} 194 H ${fmt(-half)} A ${fmt(rx)} 194 0 0 1 ${fmt(-half)} -194 Z`;
      const n = this._nodes;
      n.edge.setAttribute('d', edge); n.clip.setAttribute('d', edge);
      n.front.setAttribute('visibility', c >= 0 ? 'visible' : 'hidden');
      n.back.setAttribute('visibility', c >= 0 ? 'hidden' : 'visible');
      for (const el of n.offsets) el.setAttribute('transform', `translate(${fmt(dx)} 0)`);
      for (const el of n.squashes) el.setAttribute('transform', `scale(${fmt(sx)} 1)`);
      n.lift.setAttribute('transform', `translate(0 ${fmt(-34 * flight)})`);
      n.twist.setAttribute('transform', `rotate(${fmt(twist)})`);
      n.scale.setAttribute('transform', `scale(${fmt(1 + .035 * flight)})`);
      n.floor.style.transform = `scale(${1 - .24 * flight})`;
      n.floor.style.opacity = String(.8 - .35 * flight);
    }

    _updateResult() {
      this._nodes.result.textContent = names[this._side];
      this._nodes.svg.querySelector('title').textContent = `Aurum · ${names[this._side]}`;
      for (const button of this._nodes.sides) button.setAttribute('aria-pressed', String(button.dataset.side === this._side));
    }

    _animate(target, duration, toss) {
      const n = this._nodes;
      const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
      duration = Number.isFinite(duration) ? Math.max(0, Math.min(duration, 10000)) : 2200;
      if (reduced) duration = 0;
      this._busy = true;
      n.toss.disabled = true;
      for (const button of n.sides) button.disabled = true;
      n.ready.textContent = toss ? '硬币在空中' : '正在翻面';
      n.toss.querySelector('span').textContent = toss ? '抛掷中…' : '翻面中…';
      const from = this._side === 'front' ? 0 : Math.PI;
      const turns = (toss ? 6 * Math.PI : 0) + (target === this._side ? 0 : Math.PI);
      return new Promise(resolve => {
        const unlock = () => {
          this._busy = false; this._cancelAnimation = null;
          n.toss.disabled = false;
          for (const button of n.sides) button.disabled = false;
          n.toss.querySelector('span').textContent = '抛掷硬币';
        };
        const finish = () => {
          this._side = target;
          // Canonical endpoint: no accumulated angles or rounding drift.
          this._render(target === 'front' ? 0 : Math.PI);
          this._updateResult();
          unlock(); n.ready.textContent = toss ? '已落定' : '等待抛掷';
          if (toss) {
            this._count += 1; this._history.push(target); this._history = this._history.slice(-8);
            n.count.textContent = `已抛掷 ${this._count} 次`;
            n.history.innerHTML = this._history.map(side => `<i data-side="${side}"></i>`).join('');
            n.history.setAttribute('aria-label', `最近结果：${this._history.map(side => names[side]).join('，')}`);
            this.dispatchEvent(new CustomEvent('coin-result', { detail: { side: target, count: this._count }, bubbles: true, composed: true }));
          }
          resolve(target);
        };
        if (!duration) { finish(); return; }
        let start;
        const tick = now => {
          start ??= now;
          const t = Math.min((now - start) / duration, 1);
          if (t === 1) { finish(); return; }
          const flight = Math.sin(Math.PI * t) * (toss ? 1 : .15);
          this._render(from + turns * ease(t), flight, (toss ? 6 : 2) * Math.sin(Math.PI * 2 * t) * flight);
          this._frame = requestAnimationFrame(tick);
        };
        this._cancelAnimation = () => {
          cancelAnimationFrame(this._frame);
          this._render(this._side === 'front' ? 0 : Math.PI);
          unlock(); n.ready.textContent = '等待抛掷'; resolve(null);
        };
        this._frame = requestAnimationFrame(tick);
      });
    }
  }
  customElements.define('aurum-coin', AurumCoin);
})();
