// Component StatusBadge – thẻ <mio-status-badge>.
// Thiết kế: docs/design/components/status-badge.md. Chỉ dùng biến từ ui-tokens.css.
(function () {
  const VARIANTS = {
    pending: { label: 'Chờ duyệt', color: 'var(--color-status-warning)' },
    done: { label: 'Đã comment', color: 'var(--color-status-success)' },
    waiting: { label: 'Chờ báo giá', color: 'var(--color-status-info)' },
    failed: { label: 'Thất bại', color: 'var(--color-status-danger)' },
  };

  class MioStatusBadge extends HTMLElement {
    static get observedAttributes() {
      return ['variant'];
    }

    connectedCallback() {
      this.render();
    }

    attributeChangedCallback() {
      this.render();
    }

    render() {
      const variant = VARIANTS[this.getAttribute('variant')] || VARIANTS.pending;
      this.innerHTML = `<span style="display:inline-block;padding:2px var(--space-sm);border-radius:var(--radius-pill);font-size:var(--font-size-xs);font-family:var(--font-family-body);color:var(--color-text-on-primary);background:${variant.color}">${variant.label}</span>`;
    }
  }

  customElements.define('mio-status-badge', MioStatusBadge);
})();
