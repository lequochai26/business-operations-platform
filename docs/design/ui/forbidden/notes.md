# Mockup – Không có quyền

- Tính năng: `auth` (giai đoạn 0)
- Thiết kế chi tiết: `docs/phases/phase-0/design/auth.md` mục "Màn hình Không có quyền"
- Trạng thái: đã duyệt ngày 2026-10-31

## Trạng thái đã vẽ

- `normal.html`: Thợ mở trực tiếp `/settings` – trong khung app, tiêu đề "Không có quyền truy cập", dòng "Trang này chỉ dành cho Quản lý.", nút "Về Trang chính"; không mục điều hướng nào được chọn, đường dẫn giữ nguyên (R-AUT-29).
- Không vẽ:
  - `empty`, `loading`, `validation-error`, `system-error`, `forbidden` – lý do: bản thân màn hình là trạng thái lỗi phân quyền, không nạp dữ liệu, không có trường nhập.
  - API trả 403 khi đang thao tác (toast) – vẽ ở `docs/design/ui/app-shell/forbidden.html`.

## Luồng thao tác

1. Thợ mở `/settings` (gõ địa chỉ, link cũ) → màn hình này.
2. Bấm "Về Trang chính" → `/`.

## Component dùng

- `<mio-app-nav>` (`docs/design/components/app-nav.md`): `role="technician"`, không mục nào được chọn.

## Khác với thiết kế chi tiết

- Không có.

## Lịch sử thay đổi

- 2026-10-31: tạo mới
