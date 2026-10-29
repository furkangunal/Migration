// claude.ai Dashboard çalışma ortamının bağımsız taklidi: index.html'in kullandığı dash.* API'sini
// gömülü verilerle (window.DASH_DATA) karşılar. build_standalone.py bu dosyayı sayfaya gömer.
window.dash = (() => {
  const RAW = window.DASH_DATA || {};
  const DEFAULTS = window.DASH_PARAMS || {};
  const parsed = new Map();   // veri seti id -> {data, columns}
  const calcs = new Map();    // calc id -> {inputs, fn}
  const calcOut = new Map();  // calc id -> sonuç ya da {error}
  const draws = new Map();    // çizim adı -> fn ya da {mount, update, unmount}
  const mounted = new WeakMap();
  const onDataFns = [];
  let params = { ...DEFAULTS };
  let started = false, queued = false;

  function dataset(id) {
    if (parsed.has(id)) return parsed.get(id);
    const r = RAW[id];
    let out;
    if (r.format === 'csv') {
      const data = d3.csvParse(r.text);
      out = { data: Array.from(data), columns: data.columns };
    } else {
      const j = r.data, data = Array.isArray(j) ? j : (j.rows || j.data || j.results || j);
      out = { data, columns: Array.isArray(data) && data.length ? Object.keys(data[0]) : [] };
    }
    parsed.set(id, out);
    return out;
  }

  function calc(id) {
    if (calcOut.has(id)) return calcOut.get(id);
    const c = calcs.get(id);
    let out;
    try {
      const args = c.inputs.map((i) => {
        const d = data(i);
        if (d.status !== 'ok') throw new Error(`${i} yüklenemedi`);
        return d.data;
      });
      out = { value: c.fn(...args) };
    } catch (e) {
      console.error(`dash.calc ${id}:`, e);
      out = { error: String(e.message || e) };
    }
    calcOut.set(id, out);
    return out;
  }

  function data(id) {
    const base = { refreshing: false, meta: [], message: '' };
    if (id in RAW) {
      const d = dataset(id);
      return { ...base, status: 'ok', data: d.data, rows: d.data, columns: d.columns };
    }
    if (calcs.has(id)) {
      const c = calc(id);
      if (c.error) return { ...base, status: 'error', data: [], rows: [], columns: [], message: c.error };
      const v = c.value, cols = Array.isArray(v) && v.length && typeof v[0] === 'object' ? Object.keys(v[0]) : [];
      return { ...base, status: 'ok', data: v, rows: v, value: v, columns: cols };
    }
    return { ...base, status: 'missing', data: [], rows: [], columns: [], message: `${id} bulunamadı` };
  }

  // Gizli (hidden) bir kapsayıcının içindeki çizimler çalıştırılmaz, sekme açılınca çizilir
  const visible = (el) => el.isConnected && !el.closest('[hidden]');

  function runOne(name, el) {
    const d = draws.get(name);
    try {
      if (typeof d === 'function') d(el);
      else {
        if (!mounted.has(el)) { el.replaceChildren(); mounted.set(el, d.mount ? d.mount(el) : undefined); }
        if (d.update) d.update(el, mounted.get(el));
      }
    } catch (e) {
      console.error(`dash.draw ${name}:`, e);
      if (typeof d !== 'function' && d.unmount) { try { d.unmount(el, mounted.get(el)); } catch (_) {} mounted.delete(el); }
    }
  }

  const widths = new WeakMap();
  const ro = new ResizeObserver((entries) => {
    for (const en of entries) {
      const el = en.target, w = Math.round(en.contentRect.width), prev = widths.get(el);
      widths.set(el, w);
      if (prev !== undefined && prev !== w && visible(el)) runOne(el.dataset.draw, el);
    }
  });

  function runDraw(name) {
    document.querySelectorAll(`[data-draw="${CSS.escape(name)}"]`).forEach((el) => {
      if (!visible(el)) return;
      if (!widths.has(el)) { widths.set(el, Math.round(el.clientWidth)); ro.observe(el); }
      runOne(name, el);
    });
  }

  function render() {
    queued = false;
    for (const fn of onDataFns) { try { fn(); } catch (e) { console.error('dash.onData:', e); } }
    for (const name of draws.keys()) runDraw(name);
  }
  function schedule() {
    if (!started || queued) return;
    queued = true;
    requestAnimationFrame(render);
  }

  window.addEventListener('hashchange', () => {
    const h = location.hash.slice(1);
    if (h && h !== params.tab) api.setParams({ tab: h });
  });

  const api = {
    data,
    calc(id, def) { calcs.set(id, def); },
    loader() {},
    onData(fn) { onDataFns.push(fn); if (started) fn(); },
    draw(name, fn) {
      if (fn === undefined) { if (started) runDraw(name); return; }
      draws.set(name, fn);
      schedule();
    },
    params: () => ({ ...params }),
    setParams(p) {
      for (const k in p) { if (p[k] == null) delete params[k]; else params[k] = p[k]; }
      schedule();
    },
    resetParams() { params = { ...DEFAULTS }; schedule(); },
    setLink(name) { if (name) history.replaceState(null, '', '#' + name); },
    refresh() {},
    colors: ['#1f5fbf', '#cf5a33', '#2e8b57', '#8e44ad', '#d4a017', '#17a2b8', '#6c757d', '#e83e8c'],
    __start() { started = true; render(); },
  };
  return api;
})();
