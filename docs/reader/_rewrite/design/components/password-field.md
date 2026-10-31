<!-- src-section: 0b0fa0b228 773825a3a2d2 -->
# PasswordField (`<mio-password-field>`)

**Tóm tắt.** Component ô nhập mật khẩu. Component đã được duyệt ngày 2026-10-31.

**Chi tiết kỹ thuật**
- File: `components/password-field.js`.
- Gallery: `components/password-field.html`.

<!-- src-section: c523695739 4128c3816d97 -->
## Mục đích

**Tóm tắt.** PasswordField là ô nhập mật khẩu có nút hiện hoặc ẩn ký tự.

**Cách hoạt động**
- Component được dùng ở màn hình Đăng nhập (1 ô) và Đổi mật khẩu (3 ô).
- Sau này component được dùng thêm ở Cài đặt › Người dùng (giai đoạn 2).
- Đây là biến thể của ô nhập cơ bản trong `ui-style.md`, có thêm nút hiện/ẩn.

<!-- src-section: 9164a82c09 b6cefc912f1e -->
## Cấu tạo

**Tóm tắt.** Component gồm nhãn, ô nhập có nút hiện/ẩn ở bên phải và một dòng gợi ý hoặc lỗi bên dưới.

**Cách hoạt động**
- Nhãn nằm phía trên ô.
- Ô nhập mặc định ẩn ký tự. Khi người dùng chọn hiện, ô hiển thị ký tự như ô văn bản thường. Bên phải ô có chừa chỗ cho nút.
- Nút chữ "Hiện" / "Ẩn" nằm trong ô, ở bên phải. Nhãn đọc cho trình đọc màn hình là "Hiện mật khẩu" / "Ẩn mật khẩu".
- Dòng dưới ô hiện gợi ý. Khi có lỗi, thông báo lỗi thay vào chỗ của gợi ý.

**Vì sao.** Nút dùng chữ thay cho biểu tượng con mắt để dễ hiểu hơn.

**Chi tiết kỹ thuật**
- Nhãn: `font-size-sm`, `font-weight-medium`.
- Ô nhập: `type="password"`; khi hiện ký tự là `type="text"`. Chiều cao `size-control-md`, viền `color-control-border`, bo góc `radius-sm`.
- Nút: chữ `color-brand-primary-strong`, nhãn đặt bằng `aria-label`.
- Dòng gợi ý: `color-text-muted`. Dòng lỗi: `color-status-danger`.

<!-- src-section: c4594845d8 8db2c19e94fd -->
## Thuộc tính và biến thể

**Tóm tắt.** Component nhận nhãn, giá trị, gợi ý, lỗi và trạng thái hiển thị. Chỉ có nhãn là bắt buộc.

- `label`: chuỗi, bắt buộc.
- `value`: chuỗi, mặc định trống. Thuộc tính này chỉ dùng để vẽ mockup.
- `hint`: chuỗi, mặc định không có. Ví dụ: "Ít nhất 8 ký tự".
- `error`: chuỗi thông báo lỗi, chép nguyên văn từ thiết kế chi tiết. Khi có lỗi, viền ô và dòng dưới đổi sang `color-status-danger`, và ô có `aria-invalid="true"`.
- `revealed`: có hoặc không, mặc định không. Khi có, ô đang hiện ký tự.
- `state`: `normal`, `hover`, `focus` hoặc `disabled`, mặc định `normal`. Hai giá trị hover và focus chỉ để minh hoạ.
- `autocomplete`: `current-password` (mặc định) hoặc `new-password`.
- `name`: tên trường trong form.

<!-- src-section: 14e51f8ad9 135afa14c907 -->
## Trạng thái

**Tóm tắt.** Ô có các trạng thái bình thường, hover, focus, lỗi và disabled. Việc hiện hay ẩn ký tự là trạng thái riêng, kết hợp được với mọi trạng thái kể trên.

**Cách hoạt động**
- Ở trạng thái disabled, nút hiện/ẩn cũng không bấm được.

**Chi tiết kỹ thuật**
- Hover: viền `color-control-border-hover`.
- Focus: viền ngoài `border-width-focus`, màu `color-focus-ring`.
- Disabled: nền `color-control-background-disabled`, độ mờ `opacity-disabled`.

<!-- src-section: c84fd6a24b c46ef350f740 -->
## Hành vi

**Tóm tắt.** Bấm nút để hiện hoặc ẩn ký tự mà không mất giá trị đã nhập. Ô không chặn số ký tự gõ vào mà báo lỗi khi vượt độ dài.

**Cách hoạt động**
- Bấm "Hiện": ô chuyển sang hiện ký tự và nút đổi thành "Ẩn". Bấm lại thì ô ẩn ký tự. Giá trị và vị trí con trỏ được giữ nguyên.
- Trong thứ tự Tab, nút hiện/ẩn đứng sau ô nhập. Nhấn Enter hoặc Space trên nút chỉ đổi hiện/ẩn, không gửi form.
- Mỗi ô hiện/ẩn độc lập. Ví dụ màn hình Đổi mật khẩu có 3 ô với 3 nút riêng.
- Sau khi gửi form, ô trở về trạng thái ẩn. Điều này áp dụng cả khi gửi thành công và khi lỗi làm xoá ô mật khẩu.
- Ô không giới hạn số ký tự gõ bằng `maxlength`. Khi giá trị vượt độ dài cho phép, component báo lỗi theo quy tắc, ví dụ R-AUT-04.

**Vì sao.** Báo lỗi thay vì chặn gõ giúp người dùng thấy lý do.

<!-- src-section: cbb25c4ba1 b6cfc8a94b75 -->
## Nên dùng / không nên dùng

- Nên dùng cho mọi ô nhập mật khẩu.
- Không nên dùng cho ô nhập thường. Ô nhập thường dùng `.field` / `.input` cơ bản trong `ui-style.md`.

<!-- src-section: 4a288e125e ea7fc558c05b -->
## Màn hình đang dùng

Các màn hình sau đang dùng PasswordField:

- `docs/design/ui/login/`: ô Mật khẩu.
- `docs/design/ui/change-password/`: ô Mật khẩu hiện tại, Mật khẩu mới và Nhập lại mật khẩu mới.

<!-- src-section: 80b54c0db6 feb134a25b98 -->
## Lịch sử thay đổi

- 2026-10-31: tạo mới qua lệnh `/ui-design auth`.
