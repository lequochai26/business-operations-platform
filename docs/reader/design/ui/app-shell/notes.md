> Bản đọc sinh từ docs/design/ui/app-shell/notes.md (phiên bản 48208c5, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# Mockup – Khung app, Trang chính giữ chỗ (`/`)

**Tóm tắt.** Mockup khung app và Trang chính giữ chỗ của tính năng `auth` (giai đoạn 0). Mockup đã được duyệt ngày 2026-10-31.

- Thiết kế chi tiết: mục "Khung app" trong `docs/phases/phase-0/design/auth.md`.

<a id="s-2df8c1fb05"></a>

## Trạng thái đã vẽ

**Tóm tắt.** Mockup vẽ Trang chính của Quản lý và của Thợ, màn hình đang nạp phiên, màn hình lỗi nạp phiên và thông báo khi không có quyền thao tác.

**Các trạng thái đã vẽ**
- `normal.html`: Quản lý ở Trang chính.
  - Thanh điều hướng có Trang chính (đang chọn), đường kẻ, Cài đặt và Nhật ký hệ thống.
  - Khối tài khoản có "Huỳnh Mio · Quản lý", Đổi mật khẩu và Đăng xuất.
  - Nội dung chỉ có tiêu đề "Hôm nay". Đây là phần giữ chỗ. Tính năng `emergency-stop` sẽ thêm khối "Trạng thái tự động hóa".
- `normal-technician.html`: Thợ ở Trang chính. Thanh điều hướng chỉ có mục Trang chính ([R-AUT-29](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Thanh điều hướng chỉ hiện mục mà vai trò được dùng") *(Thanh điều hướng chỉ hiện mục mà vai trò được dùng)*).
- `loading.html`: app vừa mở và đang nạp `GET /api/v1/sessions/current`. Màn hình có logo, vòng xoay và chữ "Đang tải…". Thanh điều hướng chưa được vẽ.
- `system-error.html`: nạp phiên bị lỗi 500. Màn hình hiện "Lỗi hệ thống, vui lòng thử lại sau" và nút "Thử lại". Khi mất mạng, bố cục giữ nguyên với thông báo "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại."
- `forbidden.html` ([R-AUT-29](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Thanh điều hướng chỉ hiện mục mà vai trò được dùng") *(Thanh điều hướng chỉ hiện mục mà vai trò được dùng)*): API trả 403 khi người dùng thao tác không qua form, ví dụ bấm nút trong danh sách hoặc bật công tắc. Màn hình hiện toast danger "Bạn không có quyền thực hiện thao tác này". Toast không tự ẩn và có nút "Đóng".
  - Khi gửi form mà nhận 403, banner danger hiện ở vùng thông báo của form đó (`ui-style.md` mục "Vị trí thông báo"). Trạng thái này được vẽ ở màn hình của tính năng có form.
  - Khi Thợ mở trang chỉ dành cho Quản lý, xem `docs/design/ui/forbidden/`.

**Không vẽ**
- `empty`: Trang chính ở giai đoạn 0 chỉ là trang giữ chỗ, không có dữ liệu.
- `validation-error`: màn hình không có trường nhập.

<a id="s-34e57f188d"></a>

## Luồng thao tác

**Tóm tắt.** Khi mở app, app nạp phiên trước rồi mới hiện khung app. Nếu chưa đăng nhập, app chuyển tới trang đăng nhập.

1. Mở app. Màn hình hiện `loading`, sau đó:
   - phiên hợp lệ: hiện `normal` hoặc `normal-technician`;
   - lỗi 401: chuyển tới `/login?next=…` ([R-AUT-28](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Chưa đăng nhập mà mở trang cần đăng nhập") *(Chưa đăng nhập mà mở trang cần đăng nhập)*);
   - lỗi 500 hoặc mất mạng: hiện `system-error`.
2. Ở `system-error`, bấm "Thử lại". Màn hình quay lại `loading`.
3. Bấm một mục trên thanh điều hướng. App chuyển trang và mục đó đổi sang trạng thái đang chọn.
4. Bấm "Đổi mật khẩu" để tới `/account/password`. Bấm "Đăng xuất" để về `/login` kèm banner "Bạn đã đăng xuất" ([R-AUT-32](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Bấm 'Đăng xuất'") *(Bấm "Đăng xuất")*).

<a id="s-955f8ca0fb"></a>

## Component dùng

- `<mio-app-nav>` (`docs/design/components/app-nav.md`): thanh điều hướng trái và khối tài khoản.
- Các component cơ bản (nút, thẻ, toast) được dùng qua `docs/design/ui/mockup-base.css`.

<a id="s-67d26e4976"></a>

## Khác với thiết kế chi tiết

**Tóm tắt.** Mockup thêm màn hình chờ và màn hình lỗi nạp phiên. Thiết kế chi tiết đã được cập nhật theo.

**Thay đổi**
- Thêm màn hình chờ (`loading`) và màn hình lỗi nạp phiên có nút "Thử lại" (`system-error`). Thiết kế chi tiết mục "Khung app" đã được cập nhật ngày 2026-10-31.

**Ghi chú vẽ**
- Badge vai trò dùng nền `color-brand-primary-soft` và chữ `color-brand-primary-stronger`. Lý do là badge status-soft không hợp với nền xanh đậm.
- "Đổi mật khẩu" và "Đăng xuất" hiển thị như mục điều hướng.

<a id="s-80b54c0db6"></a>

## Lịch sử thay đổi

- 2026-10-31: tạo mới.
- 2026-10-31: qua `/design-review auth`, điểm RV-11 giới hạn `forbidden.html` chỉ cho thao tác không có form.
