# Thiết kế chi tiết – <tên tính năng> (`<slug>`, `<ABC>`)

- Giai đoạn: <N>
- Trạng thái: <đang thiết kế | đã duyệt ngày YYYY-MM-DD>
- Tài liệu khái quát: <file + mục>

## Tóm tắt

<2–4 câu: tính năng làm gì, cho ai>

## Module và interface

- <module>: <trách nhiệm>; interface: `<tên hàm/lớp>(<tham số>) -> <kết quả>`

## Thay đổi DB

- <thêm/sửa bảng>. Chi tiết: `docs/design/db-schema.md` mục <bảng>.

## API

- `<METHOD> <path>` – <mục đích>. Chi tiết: `docs/design/api/<resource>.md`.

## Màn hình và quy tắc kiểm tra dữ liệu

### Màn hình <tên>
- Vai trò được dùng: <Quản lý | Thợ>
- Trường:
  - <tên trường>: kiểu <…>, bắt buộc <có/không>, <khoảng/định dạng>, mặc định <…>
### Quy tắc
- R-<ABC>-01: <quy tắc> → lỗi "<thông báo nguyên văn>"

## Job và hàng đợi

- <tên job>: lịch chạy <…>, hàng đợi <…>, ưu tiên <…>, retry <…>, timeout <…>

## Trạng thái và thuật toán

- Trạng thái: <danh sách>; chuyển hợp lệ: <A → B khi …>; chuyển không hợp lệ: <…>
- Thuật toán: <mô tả từng bước>

## Tích hợp bên ngoài

- <Facebook/Messenger/Gemini>: <selector, payload, prompt, schema>

## Xử lý lỗi, log, bảo mật, phân quyền

- Lỗi: <tình huống> → <hành vi, thông báo>
- Log: <ghi gì, không ghi dữ liệu cá nhân nào>
- Phân quyền: R-<ABC>-nn …

## Tham số cài đặt

- <tên>: mặc định <…>, khoảng <…>, nguồn <tài liệu khái quát | quyết định mới>

## Câu hỏi mở

- [ ] <câu hỏi> — đề xuất: <…>

## Lịch sử thay đổi

- <YYYY-MM-DD>: tạo mới
