> Bản đọc sinh từ docs/decisions/0003-naming-conventions.md (phiên bản de63f5c, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# 0003 – Quy ước đặt tên bảng DB và endpoint API

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước › Đặt tên; docs/design/db-schema.md, docs/design/api/

**Tóm tắt.** Tên bảng DB dùng snake_case số nhiều. Endpoint API có tiền tố `/api/v1/` và viết kebab-case, còn field JSON và query param viết camelCase.

<a id="s-0bc81167ac"></a>

## Bối cảnh

Tính năng nào cũng thêm bảng và endpoint. Cần một quy tắc duy nhất để thiết kế, code và review đối chiếu được với nhau.

<a id="s-1be8f16534"></a>

## Các phương án

<a id="s-26a0c6e8a9"></a>

### Tên bảng

#### A. snake_case số nhiều (`fb_groups`)

**Ưu**

- Phổ biến với Postgres và Drizzle.
- Đọc tự nhiên khi viết query.

**Nhược**

- Phải nhớ các từ số nhiều bất quy tắc.

#### B. snake_case số ít (`fb_group`)

**Ưu**

- Khớp với tên entity.

**Nhược**

- Dễ trùng từ khoá, ví dụ `user`.

<a id="s-3c27243302"></a>

### Endpoint

#### A. `/api/<danh-từ-số-nhiều>`

**Ưu**

- Đường dẫn ngắn.
- App nội bộ, server và client deploy cùng lúc.

**Nhược**

- Không có sẵn chỗ cho phiên bản API sau này.

#### B. `/api/v1/<danh-từ-số-nhiều>`

**Ưu**

- Có sẵn version nếu sau này có app native cũ vẫn còn chạy.

**Nhược**

- Đường dẫn dài hơn.
- Hiện tại chưa cần.

<a id="s-254160d409"></a>

## Quyết định

- Tên bảng chọn phương án A: snake_case số nhiều.
- Endpoint chọn phương án B: có tiền tố `/api/v1/...` và viết kebab-case.
- Field JSON và query param viết camelCase.

<a id="s-58c5fdb1ed"></a>

## Hệ quả

**Được**

- Quy tắc kiểm tra được trong bước `review-code`.
- Có sẵn đường để nâng version API.

**Mất và rủi ro**

- Mọi đường dẫn dài thêm `/v1`.
- Khoá ngoại dùng dạng số ít, ví dụ `fb_group_id`. Vì vậy phải chuyển qua lại giữa số nhiều và số ít.
