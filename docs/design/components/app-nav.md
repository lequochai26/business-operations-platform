# AppNav (`<mio-app-nav>`)

- File: `components/app-nav.js`, gallery `components/app-nav.html`
- Trạng thái: đã duyệt ngày 2026-10-31

## Mục đích

Thanh điều hướng trái của khung app, có ở mọi trang sau khi đăng nhập. Chỉ hiện mục mà vai trò được dùng (R-AUT-29) và khối tài khoản (tên hiển thị, vai trò, Đổi mật khẩu, Đăng xuất). Dùng chung để mọi màn hình của các tính năng sau nhúng lại, không vẽ lại thanh điều hướng.

## Cấu tạo

- Logo "Mio" (`font-family-decorative`, `font-size-logo`) và dòng phụ "Tiệm Nhà Mio · vận hành" (`color-nav-text-muted`).
- Danh sách mục (`NAV_ITEMS` trong `app-nav.js`, giống `apps/web/src/app/nav-items.ts`), đường kẻ `color-nav-divider` tách nhóm chỉ dành cho Quản lý. Giai đoạn 0:
  - "Trang chính" (`/`): Quản lý, Thợ;
  - đường kẻ: Quản lý;
  - "Cài đặt" (`/settings`): Quản lý;
  - "Nhật ký hệ thống" (`/system-log`): Quản lý.
- Khối tài khoản ghim cuối thanh, tách bằng đường kẻ:
  - tên hiển thị (`font-weight-semibold`) + badge vai trò (`ROLE_LABELS`: Quản lý, Thợ), nền `color-brand-primary-soft`, chữ `color-brand-primary-stronger`;
  - "Đổi mật khẩu": liên kết tới `/account/password`, hiển thị như một mục điều hướng;
  - "Đăng xuất": nút, hiển thị như một mục điều hướng (R-AUT-32).

## Thuộc tính và biến thể

- `role`: `manager` | `technician`, mặc định `manager` – quyết định mục nào hiện.
- `active`: đường dẫn trang hiện tại (`/`, `/settings`, `/system-log`, `/account/password`); mục khớp hiện trạng thái đang chọn. Đường dẫn không khớp mục nào (trang Không có quyền, Không tìm thấy) thì không mục nào được chọn.
- `display-name`: tên hiển thị của người dùng (1–50 ký tự, xuống dòng khi dài).
- `hover`, `focus`: chỉ để minh họa trong gallery/mockup; giá trị là đường dẫn mục hoặc `logout`.

## Trạng thái

- Mục thường: chữ `color-nav-text`.
- Hover: nền `color-nav-item-hover`.
- Đang chọn: nền `color-nav-item-active-background`, chữ `color-nav-item-active-text`, `font-weight-semibold`, `aria-current="page"`.
- Focus bàn phím: viền ngoài `border-width-focus` màu `color-focus-ring-on-nav`.

## Hành vi

- Bấm mục: chuyển trang (React Router), không tải lại trang.
- Bấm "Đăng xuất": gọi `DELETE /api/v1/sessions/current` rồi chuyển `/login` kèm banner "Bạn đã đăng xuất" (R-AUT-32).
- Thanh cố định khi cuộn (`position: sticky`), cao bằng khung nhìn; khối tài khoản luôn ở đáy.
- Bàn phím: Tab đi qua các mục theo thứ tự trên xuống, rồi Đổi mật khẩu, Đăng xuất.

## Nên dùng / không nên dùng

- Nên: mọi trang sau khi đăng nhập, đặt ở cột trái của `.app` (`docs/design/ui/mockup-base.css`).
- Không nên: trang Đăng nhập, màn hình đang nạp phiên hoặc lỗi nạp phiên (chưa biết vai trò).
- Tính năng sau thêm mục: sửa `ITEMS` trong `app-nav.js` và mục Cấu tạo ở trên, chụp lại các màn hình trong `## Màn hình đang dùng`.

## Màn hình đang dùng

- `docs/design/ui/app-shell/` – khung app, Trang chính (giữ chỗ)
- `docs/design/ui/change-password/` – `active="/account/password"`
- `docs/design/ui/forbidden/` – không mục nào được chọn
- `docs/design/ui/not-found/` – không mục nào được chọn

## Lịch sử thay đổi

- 2026-10-31: tạo mới (`/ui-design auth`)
