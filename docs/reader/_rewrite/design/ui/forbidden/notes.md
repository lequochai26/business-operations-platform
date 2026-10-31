<!-- src-section: 0b0fa0b228 484342be2665 -->
# Mockup – Không có quyền

**Tóm tắt.** Mockup màn hình Không có quyền của tính năng `auth` (giai đoạn 0). Mockup đã được duyệt ngày 2026-10-31.

- Thiết kế chi tiết: mục "Màn hình Không có quyền" trong `docs/phases/phase-0/design/auth.md`.

<!-- src-section: 2df8c1fb05 d4b0858e767b -->
## Trạng thái đã vẽ

**Tóm tắt.** Mockup chỉ vẽ một trạng thái. Bản thân màn hình đã là trạng thái lỗi phân quyền nên không cần vẽ thêm trạng thái khác.

**Các trạng thái đã vẽ**
- `normal.html`: Thợ mở trực tiếp `/settings`. Màn hình nằm trong khung app, có tiêu đề "Không có quyền truy cập", dòng "Trang này chỉ dành cho Quản lý." và nút "Về Trang chính". Không mục điều hướng nào được chọn, và đường dẫn trên thanh địa chỉ giữ nguyên (R-AUT-29).

**Không vẽ**
- `empty`, `loading`, `validation-error`, `system-error`, `forbidden`: bản thân màn hình là trạng thái lỗi phân quyền, không nạp dữ liệu và không có trường nhập.
- Trường hợp API trả 403 khi đang thao tác hiện thành toast. Trường hợp này được vẽ ở `docs/design/ui/app-shell/forbidden.html`.

<!-- src-section: 34e57f188d c2ecdf55b2a3 -->
## Luồng thao tác

1. Thợ mở `/settings` bằng cách gõ địa chỉ hoặc bấm link cũ. Màn hình này hiện ra.
2. Bấm "Về Trang chính". App chuyển tới `/`.

<!-- src-section: 955f8ca0fb 9692f41d99d7 -->
## Component dùng

- `<mio-app-nav>` (`docs/design/components/app-nav.md`): dùng với `role="technician"`, không mục nào được chọn.

<!-- src-section: 67d26e4976 19e0c8d82a2a -->
## Khác với thiết kế chi tiết

Mockup không khác thiết kế chi tiết.

<!-- src-section: 80b54c0db6 8204c5b8d50f -->
## Lịch sử thay đổi

- 2026-10-31: tạo mới.
