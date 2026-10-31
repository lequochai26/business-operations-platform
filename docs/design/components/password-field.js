// Component PasswordField – thẻ <mio-password-field>.
// Thiết kế: docs/design/components/password-field.md. Chỉ dùng biến từ ui-tokens.css.
// Nạp bằng <script src="…/components/password-field.js"></script> (không dùng type="module": bị chặn khi mở file://).
(function () {
  const STYLE = `
    :host { display: block; font-family: var(--font-family-body); }
    label { display: flex; flex-direction: column; gap: var(--space-xs); font-size: var(--font-size-sm); font-weight: var(--font-weight-medium); color: var(--color-text-default); }
    .box { position: relative; display: flex; }
    input { box-sizing: border-box; width: 100%; height: var(--size-control-md); padding: 0 calc(var(--space-xxxl) + var(--space-md)) 0 var(--space-md); font: inherit; font-size: var(--font-size-md); font-weight: var(--font-weight-regular); color: var(--color-text-default); background: var(--color-surface-card); border: var(--border-width-default) solid var(--color-control-border); border-radius: var(--radius-sm); }
    input:hover, input.is-hover { border-color: var(--color-control-border-hover); }
    input:focus, input.is-focus { outline: var(--border-width-focus) solid var(--color-focus-ring); outline-offset: var(--space-xxs); border-color: var(--color-control-border-hover); }
    input:disabled { background: var(--color-control-background-disabled); opacity: var(--opacity-disabled); cursor: not-allowed; }
    .toggle { position: absolute; top: var(--space-xxs); right: var(--space-xxs); bottom: var(--space-xxs); min-width: var(--size-control-sm); padding: 0 var(--space-sm); border: 0; border-radius: var(--radius-sm); background: transparent; color: var(--color-brand-primary-strong); font: inherit; font-size: var(--font-size-sm); font-weight: var(--font-weight-semibold); cursor: pointer; transition: background var(--duration-fast); }
    .toggle:hover { background: var(--color-brand-primary-soft); }
    .toggle:focus-visible { outline: var(--border-width-focus) solid var(--color-focus-ring); outline-offset: 0; }
    .toggle:disabled { opacity: var(--opacity-disabled); cursor: not-allowed; }
    .hint { font-size: var(--font-size-sm); font-weight: var(--font-weight-regular); color: var(--color-text-muted); }
    :host([error]) input { border-color: var(--color-status-danger); }
    :host([error]) .hint { color: var(--color-status-danger); }
  `;

  function escapeHtml(text) {
    return String(text).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);
  }

  class MioPasswordField extends HTMLElement {
    static get observedAttributes() {
      return ['label', 'value', 'hint', 'error', 'revealed', 'state', 'autocomplete', 'name'];
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

    render() {
      const isRevealed = this.hasAttribute('revealed');
      const state = this.getAttribute('state') || 'normal';
      const isDisabled = state === 'disabled';
      const error = this.getAttribute('error');
      const message = error || this.getAttribute('hint') || '';
      const inputClass = state === 'hover' || state === 'focus' ? ` class="is-${state}"` : '';
      this.shadowRoot.innerHTML = `
        <style>${STYLE}</style>
        <label>
          <span>${escapeHtml(this.getAttribute('label') || '')}</span>
          <span class="box">
            <input type="${isRevealed ? 'text' : 'password'}" name="${escapeHtml(this.getAttribute('name') || '')}"
              autocomplete="${escapeHtml(this.getAttribute('autocomplete') || 'current-password')}"
              aria-invalid="${error ? 'true' : 'false'}"${inputClass}${isDisabled ? ' disabled' : ''}>
            <button type="button" class="toggle" aria-label="${isRevealed ? 'Ẩn mật khẩu' : 'Hiện mật khẩu'}"${isDisabled ? ' disabled' : ''}>${isRevealed ? 'Ẩn' : 'Hiện'}</button>
          </span>
          ${message ? `<span class="hint">${escapeHtml(message)}</span>` : ''}
        </label>`;
      // Gán value bằng thuộc tính DOM để ô mật khẩu hiện dấu chấm thay vì lộ trong HTML.
      this.shadowRoot.querySelector('input').value = this.getAttribute('value') || '';
      this.shadowRoot.querySelector('.toggle').addEventListener('click', () => {
        const input = this.shadowRoot.querySelector('input');
        this.setAttribute('value', input.value);
        this.toggleAttribute('revealed');
      });
    }
  }

  customElements.define('mio-password-field', MioPasswordField);
})();
