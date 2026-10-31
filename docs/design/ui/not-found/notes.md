# Mockup – Không tìm thấy trang

- Tính năng: `auth` (giai đoạn 0)
- Thiết kế chi tiết: `docs/phases/phase-0/design/auth.md` mục "Màn hình Không tìm thấy trang"
- Trạng thái: đã duyệt ngày 2026-10-31

## Trạng thái đã vẽ

- `normal.html`: Quản lý mở `/khong-co` – trong khung app, tiêu đề "Không tìm thấy trang", nút "Về Trang chính"; không mục điều hướng nào được chọn.
- Không vẽ:
  - `empty`, `loading`, `validation-error`, `system-error` – lý do: không nạp dữ liệu, không có trường nhập.
  - `forbidden` – lý do: chưa đăng nhập thì R-AUT-28 chuyển `/login` trước; đã đăng nhập thì vai trò nào cũng thấy màn hình này.

## Luồng thao tác

1. Mở đường dẫn không khớp trang nào sau khi đã đăng nhập → màn hình này.
2. Bấm "Về Trang chính" → `/`.

## Component dùng

- `<mio-app-nav>` (`docs/design/components/app-nav.md`): không mục nào được chọn.

## Khác với thiết kế chi tiết

- Không có.

## Lịch sử thay đổi

- 2026-10-31: tạo mới
