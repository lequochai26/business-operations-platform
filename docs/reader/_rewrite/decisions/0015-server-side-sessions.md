<!-- src-section: 0b0fa0b228 1586eff99029 -->
# 0015 – Phiên đăng nhập lưu phía server trong PostgreSQL, cookie mang token ngẫu nhiên

- Ngày: 2026-10-31
- Trạng thái: chấp nhận
- Liên quan:
  - phase-0 auth (R-AUT-*);
  - mọi endpoint `/api/v1/*`;
  - docs/project/02-features/07-screens-and-settings.md "Yêu cầu chung" (đăng nhập, giữ đăng nhập lâu dài);
  - 04-technical.md mục 7;
  - ADR 0011 (chỉ api truy cập DB).

**Tóm tắt.** Phiên đăng nhập được lưu phía server trong PostgreSQL, còn cookie chỉ mang một token ngẫu nhiên. Cách này cho phép thu hồi phiên tức thì, kiểm thử được hết hạn trượt và vẫn an toàn khi bản sao lưu bị lộ.

<!-- src-section: 0bc81167ac 5b7c24896ea3 -->
## Bối cảnh

- Đây là web app nội bộ, có 2 vai trò (Quản lý, Thợ) và vài tài khoản. Chủ tiệm và thợ muốn giữ đăng nhập lâu dài trên điện thoại.
- Cần đăng xuất được thật, tức là thu hồi được phiên. Khi đổi mật khẩu thì các thiết bị khác phải bị đăng xuất.
- Cơ sở dữ liệu được sao lưu hằng đêm (`backup`). Nếu bản sao lưu bị lộ thì cũng không được dùng lại được phiên đang sống.
- API và web cùng một origin, vì api phục vụ web (R-SKL-14). Không có client bên thứ ba.

<!-- src-section: 1be8f16534 d5428cea36cd -->
## Các phương án

<!-- src-section: 8f9d19d733 d81572967c3e -->
### A. Phiên phía server trong PostgreSQL, cookie HttpOnly mang token ngẫu nhiên

Cookie chứa một token ngẫu nhiên 32 byte. DB chỉ lưu SHA-256 của token, kèm `user_id` và `expires_at`.

**Ưu**

- Thu hồi tức thì khi đăng xuất hoặc đổi mật khẩu.
- Dễ làm hết hạn trượt.
- Lộ bản sao lưu DB không làm lộ token dùng được.
- Không thêm thư viện.
- Dữ liệu phiên nằm cùng chỗ với dữ liệu người dùng, test được bằng DB thật và `FakeClock`.

**Nhược**

- Mỗi request có một truy vấn DB.
- Phải tự viết guard và việc dọn phiên hết hạn.

<!-- src-section: 8d5033982b cafe51cca2df -->
### B. JWT trong cookie (không trạng thái)

**Ưu**

- Không cần truy vấn DB để xác thực.
- Phổ biến.

**Nhược**

- Không thu hồi được trước hạn, trừ khi thêm danh sách chặn. Khi đó hệ thống lại có trạng thái.
- Nếu hạn dài thì rủi ro lớn khi lộ token.
- Phải quản lý khoá ký.
- Muốn hết hạn trượt thì phải cấp lại token.

<!-- src-section: 152921bc8c 20c99a8ec887 -->
### C. Phiên phía server trong Redis (`express-session` và `connect-redis`)

**Ưu**

- Có sẵn thư viện.
- Redis nhanh, TTL tự dọn phiên.

**Nhược**

- Phiên mất khi dữ liệu Redis mất, vì Redis đang dùng làm hàng đợi và không được sao lưu.
- TTL dùng giờ của Redis nên không test được bằng `FakeClock`.
- Thêm hai thư viện.
- `express-session` lưu id phiên dạng thô trong store.

<!-- src-section: 254160d409 1842581f0aca -->
## Quyết định

Chọn phương án A.

**Vì sao.** Với quy mô vài người dùng, chi phí một truy vấn mỗi request là không đáng kể. Trong khi đó, các yêu cầu sau là có thật: thu hồi tức thì, hết hạn trượt kiểm thử được bằng `FakeClock`, và an toàn khi lộ bản sao lưu.

**Quy ước kèm theo** (chi tiết ở thiết kế `auth`)

- Cookie phiên có các thuộc tính cố định. Thuộc tính `Secure` chỉ bật khi địa chỉ công khai của app dùng HTTPS.
- Mọi route API phải khai báo rõ là công khai hay cần vai trò nào. Thiếu khai báo thì api không khởi động, tức là mặc định từ chối.
- Request đổi dữ liệu có header `Origin` khác origin của `PUBLIC_URL` thì bị từ chối. Việc này cùng với `SameSite=Lax` giúp chống CSRF.

**Chi tiết kỹ thuật**

- Cookie `mio_session`: `HttpOnly`, `SameSite=Lax`, `Path=/`, `Secure` khi `PUBLIC_URL` là `https://`.
- Mọi route `/api/v1/*` phải khai báo `@Public()` hoặc `@Roles(...)`.
- Request đổi dữ liệu là các request `POST`, `PUT`, `PATCH`, `DELETE`.

<!-- src-section: 58c5fdb1ed c851c467c1f6 -->
## Hệ quả

**Được**

- Đăng xuất và đổi mật khẩu có hiệu lực ngay trên mọi thiết bị.
- Giữ đăng nhập lâu mà vẫn thu hồi được.
- Không thêm phụ thuộc.
- Mọi tính năng sau chỉ cần gắn `@Roles(...)`.

**Mất và rủi ro**

- Mỗi request gọi API có thêm một truy vấn DB.
- Guard và việc kiểm tra `Origin` là code tự viết, nên phải có test riêng.
- Nếu DB không truy cập được thì mọi request cần đăng nhập đều trả 500. Điều này đã được chấp nhận ở R-SKL-30.
- Nếu mở app bằng địa chỉ khác `PUBLIC_URL`, ví dụ `127.0.0.1` thay vì `localhost`, thì thao tác ghi bị từ chối.
