# Thiết kế chi tiết – Cài đặt danh sách group (`group-settings`, `GRP`)

- Giai đoạn: 0
- Trạng thái: đã duyệt ngày 2026-11-04
- Tài liệu khái quát: 07-screens-and-settings.md mục 2 "Group"; 01-group-auto-comment.md mục 2; 03-data-model.md mục 2

## Tóm tắt

Quản lý khai báo danh sách group Facebook mà app quét. Quản lý thêm, sửa, xóa group và bật/tắt từng công tắc.

## Module và interface

- `GroupsModule` (API): CRUD group; interface `GroupsService.create(input: CreateGroupInput) -> Group`.
- `GroupRefParser` (shared): `parseGroupRef(raw: string) -> { kind: 'id' | 'slug', value: string }`.

## Thay đổi DB

- Thêm bảng `fb_group`. Chi tiết: `docs/design/db-schema.md` mục `fb_group`.

## API

- `GET /api/groups`, `POST /api/groups`, `PATCH /api/groups/{id}`, `DELETE /api/groups/{id}`. Chi tiết: `docs/design/api/groups.md`.

## Màn hình và quy tắc kiểm tra dữ liệu

### Màn hình Cài đặt › Group
- Vai trò được dùng: Quản lý
- Trường:
  - Link hoặc ID: chuỗi, bắt buộc, link `facebook.com/groups/<slug|id>` hoặc chuỗi số
  - Giới hạn comment/ngày: số nguyên, không bắt buộc, 0–50, mặc định trống (dùng giới hạn chung)
  - Ghi chú luật group: chuỗi, không bắt buộc, tối đa 1000 ký tự
### Quy tắc
- R-GRP-01: Link hoặc ID bắt buộc → lỗi "Nhập link hoặc ID group"
- R-GRP-02: sai định dạng → lỗi "Link hoặc ID group không hợp lệ"
- R-GRP-03: group đã có → lỗi "Group này đã có trong danh sách"
- R-GRP-04: giới hạn ngoài 0–50 → lỗi "Giới hạn từ 0 đến 50"
- R-GRP-05: chỉ vai trò Quản lý được xem và sửa (Thợ nhận 403)

## Job và hàng đợi

Không áp dụng: tính năng chỉ lưu cấu hình; job quét thuộc `group-crawl-job`.

## Trạng thái và thuật toán

Không áp dụng: group không có vòng đời trạng thái, chỉ có công tắc bật/tắt.

## Tích hợp bên ngoài

Không áp dụng: không gọi Facebook khi lưu (kiểm tra truy cập group thuộc `group-crawl-job`).

## Xử lý lỗi, log, bảo mật, phân quyền

- Lỗi: sửa group đã bị xóa → 404, thông báo "Group không còn tồn tại".
- Log: ghi ai thêm/xóa group, không ghi nội dung ghi chú.
- Phân quyền: R-GRP-05.

## Tham số cài đặt

- Giới hạn comment/group/ngày mặc định: 3, khoảng 0–50, nguồn 06-open-issues mục 3.

## Câu hỏi mở

- [x] Link có `?ref=share` chấp nhận hay báo lỗi? — đã chốt: chấp nhận, bỏ phần query.

## Lịch sử thay đổi

- 2026-11-03: tạo mới
- 2026-11-04: chốt câu hỏi `?ref=share`
