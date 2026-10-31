# Mockup – Đăng nhập (`/login`)

- Tính năng: `auth` (giai đoạn 0)
- Thiết kế chi tiết: `docs/phases/phase-0/design/auth.md` mục "Màn hình Đăng nhập"
- Trạng thái: đã duyệt ngày 2026-10-31

## Trạng thái đã vẽ

- `normal.html`: form trống – logo "Mio", tiêu đề "Đăng nhập", Tên đăng nhập, Mật khẩu (có nút Hiện/Ẩn), nút "Đăng nhập", dòng "Quên mật khẩu? Nhờ người quản trị app đặt lại."
- `loading.html`: đang gửi, nút "Đang đăng nhập…" có vòng xoay, không bấm được.
- `validation-error.html`: R-AUT-01 "Nhập tên đăng nhập", R-AUT-03 "Nhập mật khẩu".
- `validation-error-length.html`: R-AUT-02 "Tên đăng nhập tối đa 32 ký tự" (33 ký tự), R-AUT-04 "Mật khẩu tối đa 128 ký tự".
- `invalid-credentials.html`: R-AUT-05, banner danger "Tên đăng nhập hoặc mật khẩu không đúng"; giữ tên đăng nhập, xóa ô mật khẩu.
- `locked.html`: R-AUT-06, banner danger "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 12 phút."
- `system-error.html`: `INTERNAL_ERROR`, banner danger "Lỗi hệ thống, vui lòng thử lại sau".
- `network-error.html`: mất mạng, banner danger "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại.", giữ cả hai ô.
- `invalid-origin.html`: R-AUT-17, banner danger "Yêu cầu bị từ chối: hãy mở app bằng địa chỉ http://localhost:3000" (ví dụ `PUBLIC_URL` của máy local).
- `cookie-blocked.html`: banner danger "Trình duyệt đang chặn cookie. Bật cookie cho trang này rồi đăng nhập lại."
- `session-expired.html`: R-AUT-31, banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" (phiên hết hạn, bị đăng xuất từ thiết bị khác, tài khoản bị xóa).
- `signed-out.html`: R-AUT-32, banner info "Bạn đã đăng xuất".
- Không vẽ:
  - `empty` – lý do: form không có dữ liệu để rỗng; trạng thái ban đầu chính là `normal`.
  - `forbidden` – lý do: trang công khai; đã đăng nhập mà mở `/login` thì chuyển `/` (R-AUT-28), không có màn hình riêng.

## Luồng thao tác

1. Mở trang cần đăng nhập khi chưa đăng nhập → chuyển `/login?next=…` (R-AUT-28) → `normal`.
2. Bấm "Đăng nhập" khi thiếu dữ liệu → kiểm tra ngay trên web bằng `loginInputSchema` → `validation-error` / `validation-error-length`, không gửi API.
3. Dữ liệu hợp lệ → `loading` → thành công: chuyển `next` hoặc `/`; lỗi: banner tương ứng trên form (`invalid-credentials`, `locked`, `system-error`, `network-error`, `invalid-origin`, `cookie-blocked`).
4. Bấm "Hiện" ở ô Mật khẩu → hiện ký tự, nút đổi thành "Ẩn".
5. Bị đẩy ra do phiên không còn dùng được → `session-expired`; bấm "Đăng xuất" thành công → `signed-out` (đăng xuất lỗi: `normal`, không banner).

## Component dùng

- `<mio-password-field>` (`docs/design/components/password-field.md`): ô Mật khẩu.
- Component cơ bản (ô nhập, nút, banner, thẻ) qua `docs/design/ui/mockup-base.css`.

## Khác với thiết kế chi tiết

- Vùng thông báo (banner) đặt ngay sau ô Mật khẩu, trước nút "Đăng nhập"; thông báo `LOGIN_LOCKED` đổi thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." → đã cập nhật thiết kế chi tiết, `api/sessions.md`, `openapi.yaml` ngày 2026-10-31.
- Ghi chú vẽ: logo "Mio" và dòng phụ "Tiệm Nhà Mio · vận hành" đặt trên thẻ form, giống thanh điều hướng; ô nhập không đặt `maxlength` để lỗi R-AUT-02, R-AUT-04 hiện được.

## Lịch sử thay đổi

- 2026-10-31: tạo mới
- 2026-10-31: theo góp ý duyệt UI: chuyển banner xuống sau ô Mật khẩu; đổi câu thông báo khóa
- 2026-10-31: `/design-review auth` RV-12: câu banner `session-expired` đổi thành "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại"; RV-10: đăng xuất lỗi không có banner
