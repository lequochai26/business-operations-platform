# Test case – Cài đặt danh sách group (`group-settings`, `GRP`)

- Thiết kế: `docs/phases/phase-0/design/group-settings.md`
- Mockup: `docs/design/ui/settings-groups/`
- Cập nhật: 2026-11-05

## Khía cạnh không áp dụng

- 10. Thời gian: tính năng không có hành vi phụ thuộc thời gian.

## P0-GRP-011 Giới hạn comment/ngày = 50 (biên trên)
- Thiết kế: R-GRP-04
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: không
- Người thực hiện: Claude
- Tiền điều kiện: đăng nhập vai trò Quản lý; đã có group "Nail Q11"
- Các bước:
  1. Mở Cài đặt › Group, bấm Sửa group "Nail Q11" → form sửa hiện ra
  2. Nhập 50 vào "Giới hạn comment/ngày", bấm Lưu → thông báo "Đã lưu cài đặt" [evidence]
  3. Kiểm tra DB: `select comment_limit from fb_group where name = 'Nail Q11'` → 50 [evidence]

## P0-GRP-012 Giới hạn comment/ngày = 51 (trên biên)
- Thiết kế: R-GRP-04
- Khía cạnh: Kiểm tra dữ liệu nhập
- Kỹ thuật: giá trị biên
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: như P0-GRP-011
- Các bước:
  1. Nhập 51 vào "Giới hạn comment/ngày", bấm Lưu → lỗi "Giới hạn từ 0 đến 50" dưới ô, không lưu [evidence]
  2. Tải lại trang → giá trị vẫn là giá trị cũ [evidence]

## P0-GRP-020 Vai trò Thợ mở thẳng URL cài đặt group
- Thiết kế: R-GRP-05
- Khía cạnh: Phân quyền
- Kỹ thuật: đoán lỗi
- Ưu tiên: cao
- Regression: có
- Người thực hiện: Claude
- Tiền điều kiện: đăng nhập vai trò Thợ
- Các bước:
  1. Gõ thẳng URL `/settings/groups` → màn hình "Bạn không có quyền xem trang này" [evidence]
  2. Gọi `GET /api/groups` bằng cookie của Thợ → 403 [evidence]
