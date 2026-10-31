# Mockup – Đổi mật khẩu (`/account/password`)

- Tính năng: `auth` (giai đoạn 0)
- Thiết kế chi tiết: `docs/phases/phase-0/design/auth.md` mục "Màn hình Đổi mật khẩu"
- Trạng thái: đã duyệt ngày 2026-10-31

## Trạng thái đã vẽ

- `normal.html`: form trống – Mật khẩu hiện tại, Mật khẩu mới (gợi ý "Ít nhất 8 ký tự"), Nhập lại mật khẩu mới, nút "Đổi mật khẩu"; mục "Đổi mật khẩu" ở khối tài khoản đang chọn.
- `confirm-dialog.html`: R-AUT-34 – hộp thoại "Đổi mật khẩu", nút "Đổi và đăng xuất thiết bị khác" (primary, focus sẵn), "Chỉ đổi mật khẩu" (secondary), "Hủy" (ghost).
- `loading.html`: bấm "Đổi và đăng xuất thiết bị khác" – nút đó "Đang lưu…", hai nút còn lại không bấm được.
- `success.html`: R-AUT-23 – form xóa trắng, toast success "Đã đổi mật khẩu. Các thiết bị khác đã được đăng xuất." (chọn "Chỉ đổi mật khẩu": "Đã đổi mật khẩu.").
- `validation-error.html`: cả ba ô trống – R-AUT-19 "Nhập mật khẩu hiện tại", R-AUT-21 "Nhập mật khẩu mới", R-AUT-22 "Nhập lại mật khẩu mới".
- `validation-error-format.html`: R-AUT-19 "Mật khẩu tối đa 128 ký tự", R-AUT-21 "Mật khẩu mới phải từ 8 đến 128 ký tự", R-AUT-22 "Mật khẩu nhập lại không khớp".
- `validation-error-username.html`: R-AUT-21 "Mật khẩu không được trùng tên đăng nhập" – Thợ `ngocanh.nail` nhập `NgocAnh.Nail` (ô đang hiện ký tự).
- `validation-error-current.html`: R-AUT-20 "Mật khẩu hiện tại không đúng" (API trả về, hộp thoại đã đóng, giữ dữ liệu).
- `validation-error-same.html`: R-AUT-21 "Mật khẩu mới phải khác mật khẩu hiện tại" (API trả về).
- `locked.html`: R-AUT-20/R-AUT-06 – banner danger "Nhập sai mật khẩu quá nhiều lần. Thử lại sau 15 phút." (lần sai thứ 5 vừa làm khóa nên còn đủ 15 phút), giữ dữ liệu.
- `system-error.html`: banner danger "Lỗi hệ thống, vui lòng thử lại sau", giữ dữ liệu. Mất mạng: cùng chỗ, "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại."
- Không vẽ:
  - `empty` – lý do: form không có dữ liệu để rỗng; trạng thái ban đầu chính là `normal`.
  - `forbidden` – lý do: cả Quản lý và Thợ đều dùng được (mỗi người đổi mật khẩu của mình).
  - Phiên bị xóa trong lúc gửi (R-AUT-24, R-AUT-31) – lý do: chuyển `/login` với banner, đã vẽ ở `docs/design/ui/login/session-expired.html`.

## Luồng thao tác

1. Bấm "Đổi mật khẩu" ở khối tài khoản → `normal`.
2. Bấm nút "Đổi mật khẩu" → kiểm tra trên web (R-AUT-19, R-AUT-21 ba ý đầu, R-AUT-22): có lỗi → `validation-error*`, không mở hộp thoại; hợp lệ → `confirm-dialog`.
3. Trong hộp thoại: Esc, bấm ra ngoài hoặc "Hủy" → đóng, giữ dữ liệu; bấm một trong hai nút đổi → `loading`.
4. Thành công → `success`. Lỗi → đóng hộp thoại: lỗi theo trường dưới ô (`validation-error-current`, `validation-error-same`), `LOGIN_LOCKED` và lỗi khác thành banner (`locked`, `system-error`).

## Component dùng

- `<mio-app-nav>` (`docs/design/components/app-nav.md`): `active="/account/password"`.
- `<mio-password-field>` (`docs/design/components/password-field.md`): cả ba ô; mỗi ô có nút Hiện/Ẩn riêng.
- Component cơ bản (nút, thẻ, banner, toast, hộp thoại) qua `docs/design/ui/mockup-base.css`.

## Khác với thiết kế chi tiết

- Vùng thông báo (banner) đặt ngay sau ô Nhập lại mật khẩu mới, trước nút "Đổi mật khẩu" (giống màn Đăng nhập); thông báo `LOGIN_LOCKED` đổi thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." → đã cập nhật thiết kế chi tiết, `api/users.md`, `openapi.yaml` ngày 2026-10-31.

## Lịch sử thay đổi

- 2026-10-31: tạo mới
- 2026-10-31: theo góp ý duyệt UI: chuyển banner xuống sau ô Nhập lại mật khẩu mới; đổi câu thông báo khóa
