# PasswordField (`<mio-password-field>`)

- File: `components/password-field.js`, gallery `components/password-field.html`
- Trạng thái: đã duyệt ngày 2026-10-31

## Mục đích

Ô nhập mật khẩu có nút hiện/ẩn ký tự. Dùng ở màn hình Đăng nhập (1 ô) và Đổi mật khẩu (3 ô), sau này ở Cài đặt › Người dùng (giai đoạn 2). Là biến thể của ô nhập cơ bản trong `ui-style.md`, thêm nút hiện/ẩn.

## Cấu tạo

- Nhãn phía trên ô (`font-size-sm`, `font-weight-medium`).
- Ô nhập `type="password"` (hiện: `type="text"`), cao `size-control-md`, viền `color-control-border`, bo `radius-sm`; chừa chỗ bên phải cho nút.
- Nút chữ "Hiện" / "Ẩn" nằm trong ô, bên phải, chữ `color-brand-primary-strong`; `aria-label` "Hiện mật khẩu" / "Ẩn mật khẩu". Dùng chữ thay biểu tượng con mắt cho dễ hiểu.
- Dòng dưới ô: gợi ý (`color-text-muted`) hoặc thông báo lỗi (`color-status-danger`) thay chỗ gợi ý.

## Thuộc tính và biến thể

- `label`: chuỗi, bắt buộc.
- `value`: chuỗi, mặc định trống (chỉ để vẽ mockup).
- `hint`: chuỗi, mặc định không có (ví dụ "Ít nhất 8 ký tự").
- `error`: chuỗi thông báo lỗi nguyên văn từ thiết kế chi tiết; có thì viền ô và dòng dưới đổi sang `color-status-danger`, `aria-invalid="true"`.
- `revealed`: có/không, mặc định không – đang hiện ký tự.
- `state`: `normal` | `hover` | `focus` | `disabled`, mặc định `normal` (hover/focus chỉ để minh họa).
- `autocomplete`: `current-password` (mặc định) | `new-password`.
- `name`: tên trường trong form.

## Trạng thái

- Bình thường, hover (viền `color-control-border-hover`), focus (viền ngoài `border-width-focus` màu `color-focus-ring`), lỗi, disabled (nền `color-control-background-disabled`, độ mờ `opacity-disabled`, nút hiện/ẩn cũng không bấm được).
- Hiện / ẩn ký tự là trạng thái riêng, kết hợp được với mọi trạng thái trên.

## Hành vi

- Bấm "Hiện": đổi ô sang hiện ký tự, nút đổi thành "Ẩn"; bấm lại thì ẩn. Giữ nguyên giá trị và vị trí con trỏ.
- Nút hiện/ẩn nằm sau ô trong thứ tự Tab; Enter/Space trên nút chỉ đổi hiện/ẩn, không gửi form.
- Mỗi ô hiện/ẩn độc lập (Đổi mật khẩu có 3 ô, 3 nút riêng).
- Gửi form xong (thành công hoặc lỗi xóa ô mật khẩu): ô trở về trạng thái ẩn.
- Không giới hạn số ký tự gõ bằng `maxlength`: vượt độ dài thì báo lỗi theo quy tắc (ví dụ R-AUT-04), để người dùng thấy lý do.

## Nên dùng / không nên dùng

- Nên: mọi ô nhập mật khẩu.
- Không nên: ô nhập thường (dùng `.field` / `.input` cơ bản trong `ui-style.md`).

## Màn hình đang dùng

- `docs/design/ui/login/` – ô Mật khẩu
- `docs/design/ui/change-password/` – Mật khẩu hiện tại, Mật khẩu mới, Nhập lại mật khẩu mới

## Lịch sử thay đổi

- 2026-10-31: tạo mới (`/ui-design auth`)
