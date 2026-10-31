// Component AppNav – thẻ <mio-app-nav>.
// Thiết kế: docs/design/components/app-nav.md. Chỉ dùng biến từ ui-tokens.css.
// Nạp bằng <script src="…/components/app-nav.js"></script> (không dùng type="module": bị chặn khi mở file://).
(function () {
  // Mục điều hướng theo vai trò (NAV_ITEMS). Mỗi tính năng có màn hình tự thêm mục của mình.
  const ITEMS = [
    { label: 'Trang chính', path: '/', roles: ['manager', 'technician'] },
    { divider: true, roles: ['manager'] },
    { label: 'Cài đặt', path: '/settings', roles: ['manager'] },
    { label: 'Nhật ký hệ thống', path: '/system-log', roles: ['manager'] },
  ];
  const ROLE_LABELS = { manager: 'Quản lý', technician: 'Thợ' };
  const CHANGE_PASSWORD_PATH = '/account/password';

  const STYLE = `
    :host { display: block; position: sticky; top: 0; height: 100vh; }
    nav { box-sizing: border-box; height: 100%; display: flex; flex-direction: column; background: var(--color-nav-background); color: var(--color-nav-text); padding: var(--space-xl) var(--space-lg); font-family: var(--font-family-body); font-size: var(--font-size-md); line-height: var(--line-height-normal); }
    .logo { font-family: var(--font-family-decorative); font-size: var(--font-size-logo); line-height: 1; }
    .logo-sub { font-size: var(--font-size-xs); color: var(--color-nav-text-muted); margin-top: var(--space-xs); }
    ul { list-style: none; margin: var(--space-xl) 0 0; padding: 0; display: flex; flex-direction: column; gap: var(--space-xxs); }
    a, button { box-sizing: border-box; display: flex; align-items: center; width: 100%; min-height: var(--size-control-md); padding: 0 var(--space-md); border: 0; border-radius: var(--radius-sm); background: transparent; color: inherit; font: inherit; text-align: left; text-decoration: none; cursor: pointer; transition: background var(--duration-fast); }
    a:hover, button:hover, .is-hover { background: var(--color-nav-item-hover); }
    a:focus-visible, button:focus-visible, .is-focus { outline: var(--border-width-focus) solid var(--color-focus-ring-on-nav); outline-offset: var(--space-xxs); }
    a[aria-current='page'] { background: var(--color-nav-item-active-background); color: var(--color-nav-item-active-text); font-weight: var(--font-weight-semibold); }
    li.divider { margin: var(--space-md) 0; border-top: var(--border-width-default) solid var(--color-nav-divider); }
    .account { margin-top: auto; padding-top: var(--space-lg); border-top: var(--border-width-default) solid var(--color-nav-divider); }
    .who { display: flex; flex-wrap: wrap; align-items: center; gap: var(--space-sm); padding: 0 var(--space-md) var(--space-sm); }
    .name { font-weight: var(--font-weight-semibold); overflow-wrap: anywhere; }
    .role { padding: var(--space-xxs) var(--space-sm); border-radius: var(--radius-pill); background: var(--color-brand-primary-soft); color: var(--color-brand-primary-stronger); font-size: var(--font-size-xs); font-weight: var(--font-weight-semibold); white-space: nowrap; }
    .account ul { margin-top: 0; }
    .account a, .account button { font-size: var(--font-size-sm); }
  `;

  function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  }

  class MioAppNav extends HTMLElement {
    static get observedAttributes() {
      return ['role', 'active', 'display-name', 'hover', 'focus'];
    }

    constructor() {
      super();
      this.attachShadow({ mode: 'open' });
    }

    connectedCallback() {
      this.render();
    }

    attributeChangedCallback() {
      this.render();
    }

    // Lớp trạng thái minh họa (hover/focus) cho gallery và mockup; app thật dùng :hover, :focus-visible.
    demoClass(key) {
      const classes = [];
      if (this.getAttribute('hover') === key) classes.push('is-hover');
      if (this.getAttribute('focus') === key) classes.push('is-focus');
      return classes.length ? ` class="${classes.join(' ')}"` : '';
    }

    render() {
      const role = ROLE_LABELS[this.getAttribute('role')] ? this.getAttribute('role') : 'manager';
      const active = this.getAttribute('active') || '/';
      const displayName = escapeHtml(this.getAttribute('display-name') || '');
      const items = ITEMS.filter((item) => item.roles.includes(role))
        .map((item) => {
          if (item.divider) return '<li class="divider" role="separator"></li>';
          const current = item.path === active ? ' aria-current="page"' : '';
          return `<li><a href="#${item.path}"${current}${this.demoClass(item.path)}>${item.label}</a></li>`;
        })
        .join('');
      const passwordCurrent = active === CHANGE_PASSWORD_PATH ? ' aria-current="page"' : '';
      this.shadowRoot.innerHTML = `
        <style>${STYLE}</style>
        <nav aria-label="Điều hướng chính">
          <div class="logo">Mio</div>
          <div class="logo-sub">Tiệm Nhà Mio · vận hành</div>
          <ul>${items}</ul>
          <div class="account">
            <div class="who"><span class="name">${displayName}</span><span class="role">${ROLE_LABELS[role]}</span></div>
            <ul>
              <li><a href="#${CHANGE_PASSWORD_PATH}"${passwordCurrent}${this.demoClass(CHANGE_PASSWORD_PATH)}>Đổi mật khẩu</a></li>
              <li><button type="button"${this.demoClass('logout')}>Đăng xuất</button></li>
            </ul>
          </div>
        </nav>`;
    }
  }

  customElements.define('mio-app-nav', MioAppNav);
})();
