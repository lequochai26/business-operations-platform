# Schema cơ sở dữ liệu

Nguồn chính về schema của toàn app. Migration trong code phải khớp file này (`/code-review` kiểm tra).

## Quy ước chung

- PostgreSQL. Tên bảng, cột theo `CLAUDE.md` mục `## Quy ước`.
- Mọi thời điểm lưu UTC (`timestamptz`); hiển thị theo `Asia/Ho_Chi_Minh`.
- Mọi bảng có `id`, `created_at`, `updated_at`.
- Không xóa cứng bản ghi đã được tham chiếu bởi lịch sử; dùng cờ lưu trữ.

## <tên_bảng>

<mục đích, tính năng sở hữu>

| Cột | Kiểu | Null | Mặc định | Ràng buộc | Ghi chú |
|---|---|---|---|---|---|
| id | uuid | không | gen_random_uuid() | PK | |
| created_at | timestamptz | không | now() | | |
| updated_at | timestamptz | không | now() | | |

### Index
- <tên index>: <cột>, <unique?>

### Quan hệ
- <cột> → <bảng>.<cột>, <on delete …>

## Lịch sử thay đổi

- <YYYY-MM-DD> | <tính năng> | <thay đổi>
