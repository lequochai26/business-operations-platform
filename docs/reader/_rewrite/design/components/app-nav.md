<!-- src-section: 0b0fa0b228 f8c53e803e48 -->
# AppNav (`<mio-app-nav>`)

**Tóm tắt.** Component thanh điều hướng trái của khung app. Component đã được duyệt ngày 2026-10-31.

**Chi tiết kỹ thuật**
- File: `components/app-nav.js`.
- Gallery: `components/app-nav.html`.

<!-- src-section: c523695739 4ba2128ad623 -->
## Mục đích

**Tóm tắt.** AppNav là thanh điều hướng trái của khung app, có ở mọi trang sau khi đăng nhập.

**Cách hoạt động**
- Thanh chỉ hiện những mục mà vai trò của người dùng được dùng (R-AUT-29).
- Thanh có khối tài khoản gồm tên hiển thị, vai trò, Đổi mật khẩu và Đăng xuất.

**Vì sao.** Thanh được làm thành component dùng chung để màn hình của các tính năng sau nhúng lại, không phải vẽ lại thanh điều hướng.

<!-- src-section: 9164a82c09 9ca9899fc45b -->
## Cấu tạo

**Tóm tắt.** Thanh gồm logo ở trên, danh sách mục điều hướng ở giữa và khối tài khoản ghim ở cuối.

**Cách hoạt động**
- Trên cùng là logo "Mio" và dòng phụ "Tiệm Nhà Mio · vận hành".
- Danh sách mục nằm ở giữa. Một đường kẻ tách nhóm mục chỉ dành cho Quản lý. Giai đoạn 0 có các mục sau:
  - "Trang chính" (`/`): Quản lý và Thợ đều thấy;
  - đường kẻ: chỉ Quản lý thấy;
  - "Cài đặt" (`/settings`): chỉ Quản lý thấy;
  - "Nhật ký hệ thống" (`/system-log`): chỉ Quản lý thấy.
- Khối tài khoản ghim ở cuối thanh và được tách khỏi danh sách bằng một đường kẻ. Khối gồm:
  - tên hiển thị và badge vai trò (Quản lý hoặc Thợ);
  - "Đổi mật khẩu": liên kết tới `/account/password`, hiển thị như một mục điều hướng;
  - "Đăng xuất": một nút, cũng hiển thị như một mục điều hướng (R-AUT-32).

**Chi tiết kỹ thuật**
- Logo: `font-family-decorative`, `font-size-logo`. Dòng phụ: `color-nav-text-muted`.
- Danh sách mục lấy từ `NAV_ITEMS` trong `app-nav.js`, giống `apps/web/src/app/nav-items.ts`.
- Đường kẻ: `color-nav-divider`.
- Tên hiển thị: `font-weight-semibold`.
- Badge vai trò lấy nhãn từ `ROLE_LABELS`, nền `color-brand-primary-soft`, chữ `color-brand-primary-stronger`.

<!-- src-section: c4594845d8 b11841254b8b -->
## Thuộc tính và biến thể

**Tóm tắt.** Component nhận vai trò, trang đang mở và tên hiển thị của người dùng. Một số thuộc tính chỉ dùng để minh hoạ trong gallery và mockup.

- `role`: `manager` hoặc `technician`, mặc định `manager`. Thuộc tính này quyết định mục nào hiện.
- `active`: đường dẫn trang hiện tại (`/`, `/settings`, `/system-log`, `/account/password`). Mục khớp với đường dẫn hiện ở trạng thái đang chọn. Nếu đường dẫn không khớp mục nào, ví dụ ở trang Không có quyền hay Không tìm thấy, thì không mục nào được chọn.
- `display-name`: tên hiển thị của người dùng, dài từ 1 đến 50 ký tự. Tên dài thì xuống dòng.
- `hover`, `focus`: chỉ để minh hoạ trong gallery hoặc mockup. Giá trị là đường dẫn của mục, hoặc `logout`.

<!-- src-section: 14e51f8ad9 1b9cff695e97 -->
## Trạng thái

**Tóm tắt.** Mục điều hướng có trạng thái thường, hover, đang chọn và focus bàn phím. Mục đang chọn có chữ đậm và được đánh dấu là trang hiện tại.

**Chi tiết kỹ thuật**
- Mục thường: chữ `color-nav-text`.
- Hover: nền `color-nav-item-hover`.
- Đang chọn: nền `color-nav-item-active-background`, chữ `color-nav-item-active-text`, `font-weight-semibold`, `aria-current="page"`.
- Focus bàn phím: viền ngoài `border-width-focus`, màu `color-focus-ring-on-nav`.

<!-- src-section: c84fd6a24b 67937d9e78c7 -->
## Hành vi

**Tóm tắt.** Bấm một mục thì app chuyển trang mà không tải lại. Bấm "Đăng xuất" thì app đăng xuất và về trang đăng nhập.

**Cách hoạt động**
- Bấm một mục: app chuyển trang bằng React Router, không tải lại trang.
- Bấm "Đăng xuất": app gọi API xoá phiên hiện tại, rồi chuyển tới `/login` kèm banner "Bạn đã đăng xuất" (R-AUT-32).
- Thanh cố định khi cuộn và cao bằng khung nhìn. Khối tài khoản luôn nằm ở đáy.
- Bàn phím: phím Tab đi qua các mục theo thứ tự từ trên xuống, rồi tới Đổi mật khẩu và Đăng xuất.

**Chi tiết kỹ thuật**
- Đăng xuất gọi `DELETE /api/v1/sessions/current`.
- Thanh cố định bằng `position: sticky`.

<!-- src-section: cbb25c4ba1 c35336433efb -->
## Nên dùng / không nên dùng

**Tóm tắt.** Dùng AppNav ở mọi trang sau khi đăng nhập. Không dùng ở nơi app chưa biết vai trò của người dùng.

- Nên dùng ở mọi trang sau khi đăng nhập. Thanh đặt ở cột trái của `.app` (`docs/design/ui/mockup-base.css`).
- Không nên dùng ở trang Đăng nhập, màn hình đang nạp phiên hoặc màn hình lỗi nạp phiên. Ở các màn hình này, app chưa biết vai trò.
- Khi tính năng sau thêm mục, cần sửa `ITEMS` trong `app-nav.js` và mục Cấu tạo ở trên. Sau đó chụp lại các màn hình trong `## Màn hình đang dùng`.

<!-- src-section: 4a288e125e a30025dec5d0 -->
## Màn hình đang dùng

Các màn hình sau đang dùng AppNav:

- `docs/design/ui/app-shell/`: khung app và Trang chính (giữ chỗ).
- `docs/design/ui/change-password/`: dùng với `active="/account/password"`.
- `docs/design/ui/forbidden/`: không mục nào được chọn.
- `docs/design/ui/not-found/`: không mục nào được chọn.

<!-- src-section: 80b54c0db6 feb134a25b98 -->
## Lịch sử thay đổi

- 2026-10-31: tạo mới qua lệnh `/ui-design auth`.
