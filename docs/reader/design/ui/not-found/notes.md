> Bản đọc sinh từ docs/design/ui/not-found/notes.md (phiên bản d1ffa15, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# Mockup – Không tìm thấy trang

**Tóm tắt.** Mockup màn hình Không tìm thấy trang của tính năng `auth` (giai đoạn 0). Mockup đã được duyệt ngày 2026-10-31.

- Thiết kế chi tiết: mục "Màn hình Không tìm thấy trang" trong `docs/phases/phase-0/design/auth.md`.

<a id="s-2df8c1fb05"></a>

## Trạng thái đã vẽ

**Tóm tắt.** Mockup chỉ vẽ một trạng thái. Các trạng thái khác không áp dụng vì màn hình không nạp dữ liệu và không có trường nhập.

**Các trạng thái đã vẽ**
- `normal.html`: Quản lý mở `/khong-co`. Màn hình nằm trong khung app, có tiêu đề "Không tìm thấy trang" và nút "Về Trang chính". Không mục điều hướng nào được chọn.

**Không vẽ**
- `empty`, `loading`, `validation-error`, `system-error`: màn hình không nạp dữ liệu và không có trường nhập.
- `forbidden`: người chưa đăng nhập được chuyển tới `/login` trước theo [R-AUT-28](../../../phases/phase-0/design/auth.md#s-0f1edd606c "Chưa đăng nhập mà mở trang cần đăng nhập") *(Chưa đăng nhập mà mở trang cần đăng nhập)*. Người đã đăng nhập thì vai trò nào cũng thấy màn hình này.

<a id="s-34e57f188d"></a>

## Luồng thao tác

1. Sau khi đăng nhập, mở một đường dẫn không khớp trang nào. Màn hình này hiện ra.
2. Bấm "Về Trang chính". App chuyển tới `/`.

<a id="s-955f8ca0fb"></a>

## Component dùng

- `<mio-app-nav>` (`docs/design/components/app-nav.md`): không mục nào được chọn.

<a id="s-67d26e4976"></a>

## Khác với thiết kế chi tiết

Mockup không khác thiết kế chi tiết.

<a id="s-80b54c0db6"></a>

## Lịch sử thay đổi

- 2026-10-31: tạo mới.
