# 0015 – Phiên đăng nhập lưu phía server trong PostgreSQL, cookie mang token ngẫu nhiên

- Ngày: 2026-10-31
- Trạng thái: chấp nhận
- Liên quan: phase-0 auth (R-AUT-*); mọi endpoint `/api/v1/*`; docs/project/02-features/07-screens-and-settings.md "Yêu cầu chung" (đăng nhập, giữ đăng nhập lâu dài); 04-technical.md mục 7; ADR 0011 (chỉ api truy cập DB)

## Bối cảnh

- Web app nội bộ, 2 vai trò (Quản lý, Thợ), vài tài khoản. Chủ tiệm và thợ muốn giữ đăng nhập lâu dài trên điện thoại.
- Cần đăng xuất được thật (thu hồi phiên), và đổi mật khẩu thì các thiết bị khác phải đăng xuất.
- Cơ sở dữ liệu được sao lưu hằng đêm (`backup`); lộ bản sao lưu không được cho phép dùng lại phiên đang sống.
- API và web cùng một origin (api phục vụ web, R-SKL-14), không có client bên thứ ba.

## Các phương án

### A. Phiên phía server trong PostgreSQL, cookie HttpOnly mang token ngẫu nhiên
- Token 32 byte ngẫu nhiên trong cookie; DB chỉ lưu SHA-256 của token, kèm `user_id`, `expires_at`.
- Ưu: thu hồi tức thì (đăng xuất, đổi mật khẩu); hết hạn trượt dễ làm; lộ bản sao lưu DB không lộ token dùng được; không thêm thư viện; dữ liệu phiên sống cùng chỗ với người dùng, test bằng DB thật + `FakeClock`.
- Nhược: mỗi request có một truy vấn DB; phải tự viết guard, dọn phiên hết hạn.

### B. JWT trong cookie (không trạng thái)
- Ưu: không truy vấn DB để xác thực; phổ biến.
- Nhược: không thu hồi được trước hạn nếu không thêm danh sách chặn (lúc đó lại có trạng thái); hạn dài thì rủi ro lớn khi lộ token; phải quản lý khóa ký; hết hạn trượt phải cấp lại token.

### C. Phiên phía server trong Redis (`express-session` + `connect-redis`)
- Ưu: thư viện có sẵn; Redis nhanh, TTL tự dọn.
- Nhược: phiên mất khi dữ liệu Redis mất (Redis đang là hàng đợi, không được sao lưu); TTL dùng giờ của Redis nên không test được bằng `FakeClock`; thêm hai thư viện; `express-session` lưu id phiên dạng thô trong store.

## Quyết định

Chọn A vì quy mô vài người dùng làm chi phí một truy vấn mỗi request không đáng kể, trong khi thu hồi tức thì, hết hạn trượt kiểm thử được bằng `FakeClock` và an toàn khi lộ bản sao lưu là yêu cầu thật.

Quy ước kèm theo (chi tiết ở thiết kế `auth`):
- Cookie `mio_session`: `HttpOnly`, `SameSite=Lax`, `Path=/`, `Secure` khi `PUBLIC_URL` là `https://`.
- Mọi route `/api/v1/*` phải khai báo `@Public()` hoặc `@Roles(...)`; thiếu thì api không khởi động (mặc định từ chối).
- Request đổi dữ liệu (`POST`, `PUT`, `PATCH`, `DELETE`) có header `Origin` khác origin của `PUBLIC_URL` bị từ chối (chống CSRF cùng với `SameSite=Lax`).

## Hệ quả

- Được: đăng xuất và đổi mật khẩu có hiệu lực ngay trên mọi thiết bị; giữ đăng nhập lâu mà vẫn thu hồi được; không thêm phụ thuộc; mọi tính năng sau chỉ cần gắn `@Roles(...)`.
- Mất / rủi ro: mỗi request gọi API thêm một truy vấn DB; tự viết guard và kiểm tra `Origin` nên phải có test riêng; DB không truy cập được thì mọi request cần đăng nhập trả 500 (đã chấp nhận ở R-SKL-30); mở app bằng địa chỉ khác `PUBLIC_URL` (ví dụ `127.0.0.1` thay vì `localhost`) thì thao tác ghi bị từ chối.
