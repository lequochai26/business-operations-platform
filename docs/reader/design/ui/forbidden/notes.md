> Bản đọc sinh từ docs/design/ui/forbidden/notes.md (phiên bản d7b23f1, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# Mockup – Không có quyền

**Tóm tắt.** Mockup màn hình Không có quyền của tính năng `auth` (giai đoạn 0). Mockup đã được duyệt ngày 2026-10-31.

- Thiết kế chi tiết: mục "Màn hình Không có quyền" trong `docs/phases/phase-0/design/auth.md`.

<a id="s-2df8c1fb05"></a>

## Trạng thái đã vẽ

**Tóm tắt.** Mockup chỉ vẽ một trạng thái. Bản thân màn hình đã là trạng thái lỗi phân quyền nên không cần vẽ thêm trạng thái khác.

**Các trạng thái đã vẽ**
- `normal.html`: Thợ mở trực tiếp `/settings`. Màn hình nằm trong khung app, có tiêu đề "Không có quyền truy cập", dòng "Trang này chỉ dành cho Quản lý." và nút "Về Trang chính". Không mục điều hướng nào được chọn, và đường dẫn trên thanh địa chỉ giữ nguyên ([R-AUT-29](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Thanh điều hướng chỉ hiện mục mà vai trò được dùng") *(Thanh điều hướng chỉ hiện mục mà vai trò được dùng)*).

**Không vẽ**
- `empty`, `loading`, `validation-error`, `system-error`, `forbidden`: bản thân màn hình là trạng thái lỗi phân quyền, không nạp dữ liệu và không có trường nhập.
- Trường hợp API trả 403 khi đang thao tác hiện thành toast. Trường hợp này được vẽ ở `docs/design/ui/app-shell/forbidden.html`.

<a id="s-34e57f188d"></a>

## Luồng thao tác

1. Thợ mở `/settings` bằng cách gõ địa chỉ hoặc bấm link cũ. Màn hình này hiện ra.
2. Bấm "Về Trang chính". App chuyển tới `/`.

<a id="s-955f8ca0fb"></a>

## Component dùng

- `<mio-app-nav>` (`docs/design/components/app-nav.md`): dùng với `role="technician"`, không mục nào được chọn.

<a id="s-67d26e4976"></a>

## Khác với thiết kế chi tiết

Mockup không khác thiết kế chi tiết.

<a id="s-80b54c0db6"></a>

## Lịch sử thay đổi

- 2026-10-31: tạo mới.
