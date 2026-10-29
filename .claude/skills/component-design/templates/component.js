// Component <TênComponent> – thẻ <mio-ten-component>.
// Thiết kế: docs/design/components/<ten-component>.md. Chỉ dùng biến từ ui-tokens.css.
// Nạp bằng <script src="…/components/<ten-component>.js"></script> (không dùng type="module": bị chặn khi mở file://).
(function () {
  const VARIANTS = { pending: { label: 'Chờ duyệt', color: 'var(--color-status-warning)' } };

  class MioTenComponent extends HTMLElement {
    static get observedAttributes() {
      return ['variant', 'state'];
    }

    connectedCallback() {
      this.render();
    }

    attributeChangedCallback() {
      this.render();
    }

    render() {
      const variant = VARIANTS[this.getAttribute('variant')] || VARIANTS.pending;
      const disabled = this.getAttribute('state') === 'disabled';
      this.innerHTML = `<span style="display:inline-block;padding:2px var(--space-sm);border-radius:var(--radius-pill);font-size:var(--font-size-xs);color:var(--color-text-on-primary);background:${variant.color};opacity:${disabled ? 0.5 : 1}">${this.textContent.trim() || variant.label}</span>`;
    }
  }

  customElements.define('mio-ten-component', MioTenComponent);
})();
