# API – <resource>

Nguồn chính của API. `docs/design/api/openapi.yaml` được sinh từ các file này, không sửa tay.

- Base path: `/api`
- Xác thực: phiên đăng nhập (cookie). Thiếu phiên → 401.
- Lỗi chung: thân `{ "code": "<MÃ_LỖI>", "message": "<thông báo tiếng Việt>", "fields": { "<trường>": "<thông báo>" } }`

### <METHOD> <path>

<mục đích>

- Quyền: <Quản lý | Thợ | cả hai>
- Request:
  - Path: `<tên>`: <kiểu>
  - Query: `<tên>`: <kiểu>, <bắt buộc?>, <mặc định>
  - Body: `<trường>`: <kiểu>, <bắt buộc?>, <ràng buộc> (quy tắc R-<ABC>-nn)
- Response:
  - `<mã HTTP>`: `<cấu trúc JSON>`
- Mã lỗi:
  - `<mã HTTP>` `<MÃ_LỖI>`: <khi nào>

## Lịch sử thay đổi

- <YYYY-MM-DD> | <tính năng> | <thay đổi>
