# 0005 – ESLint + Prettier, không dùng git hook

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước › Lint, format, typecheck; skill implement-task, bug-fix, review-code

## Bối cảnh

POC chưa có lint/format. Code nhiều promise (BullMQ, Playwright) nên cần rule dựa trên type; một số quy ước (cấm `Date.now()`, cấm skip test, tên file kebab-case) nên được máy kiểm tra.

## Các phương án

### Công cụ

#### A. ESLint (typescript-eslint) + Prettier
- Ưu: rule dựa trên type (`no-floating-promises`), `no-restricted-syntax`, plugin vitest, unicorn, React.
- Nhược: chậm hơn, hai công cụ.

#### B. Biome
- Ưu: một công cụ, rất nhanh, ít cấu hình.
- Nhược: rule dựa trên type còn hạn chế, ít plugin.

#### C. oxlint + Prettier
- Ưu: lint rất nhanh.
- Nhược: rule type-aware chưa đầy đủ.

### Kiểm tra trước commit

#### A. Không hook, các skill bắt buộc chạy lint/format check/typecheck
- Ưu: không thêm công cụ; commit nhanh.
- Nhược: commit ngoài skill không được kiểm tra.

#### B. lefthook pre-commit (format + lint file đã stage)
- Ưu: mọi commit đều sạch.
- Nhược: thêm công cụ, commit chậm thêm vài giây.

## Quyết định

Công cụ chọn A. Kiểm tra trước commit chọn A, tạm thời; thêm lefthook sau nếu thấy commit ngoài skill lọt lỗi.

## Hệ quả

- Được: các quy ước quan trọng được lint chặn tự động; `--max-warnings 0`.
- Mất / rủi ro: commit tay ngoài skill có thể lọt lỗi lint; `review-code` vẫn chạy lại trước merge.
