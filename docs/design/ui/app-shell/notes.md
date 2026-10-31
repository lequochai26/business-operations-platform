# Mockup – Khung app, Trang chính giữ chỗ (`/`)

- Tính năng: `auth` (giai đoạn 0)
- Thiết kế chi tiết: `docs/phases/phase-0/design/auth.md` mục "Khung app"
- Trạng thái: đã duyệt ngày 2026-10-31

## Trạng thái đã vẽ

- `normal.html`: Quản lý ở Trang chính – thanh điều hướng có Trang chính (đang chọn), đường kẻ, Cài đặt, Nhật ký hệ thống; khối tài khoản "Huỳnh Mio · Quản lý", Đổi mật khẩu, Đăng xuất; nội dung chỉ có tiêu đề "Hôm nay" (giữ chỗ, `emergency-stop` thêm khối "Trạng thái tự động hóa").
- `normal-technician.html`: Thợ ở Trang chính – chỉ có mục Trang chính (R-AUT-29).
- `loading.html`: mở app, đang nạp `GET /api/v1/sessions/current` – logo, vòng xoay, "Đang tải…"; chưa vẽ thanh điều hướng.
- `system-error.html`: nạp phiên lỗi 500 – "Lỗi hệ thống, vui lòng thử lại sau" và nút "Thử lại". Mất mạng: cùng bố cục, thông báo "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại."
- `forbidden.html`: R-AUT-29 – API trả 403 khi thao tác không có form (nút trong danh sách, công tắc) → toast danger "Bạn không có quyền thực hiện thao tác này" (không tự ẩn, có nút "Đóng"). 403 khi gửi form: banner danger ở vùng thông báo của form đó (`ui-style.md` mục "Vị trí thông báo"), vẽ ở màn hình của tính năng có form. Thợ mở trang chỉ dành cho Quản lý: xem `docs/design/ui/forbidden/`.
- Không vẽ:
  - `empty` – lý do: Trang chính giai đoạn 0 chỉ là trang giữ chỗ, không có dữ liệu.
  - `validation-error` – lý do: không có trường nhập.

## Luồng thao tác

1. Mở app → `loading` → phiên hợp lệ: `normal` / `normal-technician`; 401: chuyển `/login?next=…` (R-AUT-28); 500 hoặc mất mạng: `system-error`.
2. `system-error` → bấm "Thử lại" → `loading` lại.
3. Bấm mục trên thanh điều hướng → chuyển trang, mục đó đổi sang đang chọn.
4. Bấm "Đổi mật khẩu" → `/account/password`. Bấm "Đăng xuất" → `/login` kèm banner "Bạn đã đăng xuất" (R-AUT-32).

## Component dùng

- `<mio-app-nav>` (`docs/design/components/app-nav.md`): thanh điều hướng trái và khối tài khoản.
- Component cơ bản (nút, thẻ, toast) qua `docs/design/ui/mockup-base.css`.

## Khác với thiết kế chi tiết

- Thêm màn hình chờ (`loading`) và màn hình lỗi nạp phiên có nút "Thử lại" (`system-error`) → đã cập nhật thiết kế chi tiết mục "Khung app" ngày 2026-10-31.
- Ghi chú vẽ: badge vai trò dùng nền `color-brand-primary-soft`, chữ `color-brand-primary-stronger` (badge status-soft không hợp nền xanh đậm); "Đổi mật khẩu" và "Đăng xuất" hiển thị như mục điều hướng.

## Lịch sử thay đổi

- 2026-10-31: tạo mới
- 2026-10-31: `/design-review auth` RV-11: `forbidden.html` chỉ cho thao tác không có form
