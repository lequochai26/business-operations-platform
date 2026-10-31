> Bản đọc sinh từ docs/decisions/0005-eslint-prettier.md (phiên bản 6f6eb8e, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# 0005 – ESLint + Prettier, không dùng git hook

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước › Lint, format, typecheck; skill implement-task, bug-fix, review-code

**Tóm tắt.** Dự án dùng ESLint (typescript-eslint) và Prettier để lint và format code. Tạm thời không dùng git hook; thay vào đó các skill bắt buộc chạy lint, format check và typecheck trước khi commit.

<a id="s-0bc81167ac"></a>

## Bối cảnh

POC chưa có lint và format. Code có nhiều promise (BullMQ, Playwright), nên cần rule dựa trên type. Một số quy ước nên được máy kiểm tra, ví dụ cấm `Date.now()`, cấm skip test và bắt tên file viết kebab-case.

<a id="s-1be8f16534"></a>

## Các phương án

<a id="s-11c313df9d"></a>

### Công cụ

#### A. ESLint (typescript-eslint) và Prettier

**Ưu**

- Có rule dựa trên type, ví dụ `no-floating-promises`.
- Có `no-restricted-syntax`.
- Có plugin cho vitest, unicorn và React.

**Nhược**

- Chạy chậm hơn.
- Phải dùng hai công cụ.

#### B. Biome

**Ưu**

- Chỉ một công cụ.
- Rất nhanh, ít cấu hình.

**Nhược**

- Rule dựa trên type còn hạn chế.
- Ít plugin.

#### C. oxlint và Prettier

**Ưu**

- Lint rất nhanh.

**Nhược**

- Rule type-aware chưa đầy đủ.

<a id="s-0353e60081"></a>

### Kiểm tra trước commit

#### A. Không dùng hook, các skill bắt buộc tự chạy kiểm tra

Các skill bắt buộc chạy lint, format check và typecheck.

**Ưu**

- Không thêm công cụ.
- Commit nhanh.

**Nhược**

- Commit làm ngoài skill không được kiểm tra.

#### B. lefthook pre-commit

Hook chạy format và lint trên các file đã stage.

**Ưu**

- Mọi commit đều sạch.

**Nhược**

- Thêm công cụ.
- Mỗi commit chậm thêm vài giây.

<a id="s-254160d409"></a>

## Quyết định

- Công cụ chọn phương án A.
- Kiểm tra trước commit cũng chọn phương án A, nhưng chỉ là tạm thời.

Nếu thấy commit ngoài skill lọt lỗi thì sẽ thêm lefthook sau.

<a id="s-58c5fdb1ed"></a>

## Hệ quả

**Được**

- Các quy ước quan trọng được lint chặn tự động.
- Lint chạy với `--max-warnings 0`.

**Mất và rủi ro**

- Commit tay ngoài skill có thể lọt lỗi lint.
- Bước `review-code` vẫn chạy lại kiểm tra trước khi merge.
