<!-- src-section: 0b0fa0b228 247e61182436 -->
# Mockup – Không tìm thấy trang

**Tóm tắt.** Mockup màn hình Không tìm thấy trang của tính năng `auth` (giai đoạn 0). Mockup đã được duyệt ngày 2026-10-31.

- Thiết kế chi tiết: mục "Màn hình Không tìm thấy trang" trong `docs/phases/phase-0/design/auth.md`.

<!-- src-section: 2df8c1fb05 d47409bb1819 -->
## Trạng thái đã vẽ

**Tóm tắt.** Mockup chỉ vẽ một trạng thái. Các trạng thái khác không áp dụng vì màn hình không nạp dữ liệu và không có trường nhập.

**Các trạng thái đã vẽ**
- `normal.html`: Quản lý mở `/khong-co`. Màn hình nằm trong khung app, có tiêu đề "Không tìm thấy trang" và nút "Về Trang chính". Không mục điều hướng nào được chọn.

**Không vẽ**
- `empty`, `loading`, `validation-error`, `system-error`: màn hình không nạp dữ liệu và không có trường nhập.
- `forbidden`: người chưa đăng nhập được chuyển tới `/login` trước theo R-AUT-28. Người đã đăng nhập thì vai trò nào cũng thấy màn hình này.

<!-- src-section: 34e57f188d d66c721cdd5c -->
## Luồng thao tác

1. Sau khi đăng nhập, mở một đường dẫn không khớp trang nào. Màn hình này hiện ra.
2. Bấm "Về Trang chính". App chuyển tới `/`.

<!-- src-section: 955f8ca0fb 0792b858c023 -->
## Component dùng

- `<mio-app-nav>` (`docs/design/components/app-nav.md`): không mục nào được chọn.

<!-- src-section: 67d26e4976 19e0c8d82a2a -->
## Khác với thiết kế chi tiết

Mockup không khác thiết kế chi tiết.

<!-- src-section: 80b54c0db6 8204c5b8d50f -->
## Lịch sử thay đổi

- 2026-10-31: tạo mới.
