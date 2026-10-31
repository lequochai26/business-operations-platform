# 0010 – Lưu cài đặt nghiệp vụ dạng mục JSON có schema

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: phase-0 app-skeleton (bảng `app_settings`), crawl-settings, group-settings, emergency-stop và mọi tính năng có cài đặt; docs/project/03-data-model.md mục 1; 07-screens-and-settings.md mục 2; docs/design/db-schema.md

## Bối cảnh

- 07 mục 2 có khoảng 60 tham số chia theo nhóm (quét, phanh an toàn, lịch, inbox, content, AI…), tăng dần qua từng giai đoạn.
- Cài đặt lưu trong DB, đổi trên web có hiệu lực ngay, không khởi động lại (03 mục 1).
- Cần kiểm tra dữ liệu chặt (khoảng, định dạng, thông báo lỗi) và dùng lại cùng quy tắc ở web.

## Các phương án

### A. Bảng `app_settings` khóa → JSON, mỗi khóa là một mục, kiểm tra bằng zod schema trong `@mio/shared`
- Ưu: thêm tham số không cần migration cấu trúc; một mục (ví dụ `crawl-schedule`) đọc/ghi trọn vẹn, khớp với một form; zod dùng chung cho API và web; mặc định nằm trong code cạnh schema.
- Nhược: DB không kiểm tra kiểu từng tham số; đổi schema phải kèm migration dữ liệu, nếu quên thì giá trị cũ không hợp lệ (xử lý bằng R-SKL-12).

### B. Một bảng một dòng, mỗi tham số một cột có kiểu
- Ưu: DB kiểm tra kiểu và ràng buộc; truy vấn trực tiếp dễ.
- Nhược: bảng rất rộng; mỗi tham số mới cần migration; nhiều tính năng cùng sửa một bảng, dễ xung đột.

### C. Mỗi tính năng một bảng cài đặt riêng
- Ưu: ràng buộc DB theo từng nhóm, tách sở hữu rõ.
- Nhược: nhiều bảng một dòng; lặp lại code đọc/ghi/mặc định; vẫn cần migration cho mỗi tham số mới.

## Quyết định

Chọn A vì cài đặt được đọc/ghi theo nhóm, kiểm tra ở tầng ứng dụng đã bắt buộc (để có thông báo lỗi tiếng Việt), và thêm tham số không đụng tới cấu trúc DB.

Quy ước kèm theo:
- Khóa kebab-case, khai báo bằng `defineSetting({ key, schema, defaultValue })` trong `SETTINGS` của `@mio/shared`; tính năng sở hữu khóa sở hữu schema và mặc định.
- Khóa chưa có trong DB → dùng mặc định; giá trị trong DB không qua schema → báo lỗi nêu cụ thể từng trường, lý do và giá trị đang lưu (409 `INVALID_STORED_SETTING`), không lặng lẽ dùng mặc định (R-SKL-12).
- Endpoint: mỗi khóa có `GET` / `PUT /api/v1/settings/<khóa>` do tính năng sở hữu khai báo; `PUT` thay cả mục.
- Đổi schema của khóa đã có dữ liệu → viết migration dữ liệu trong cùng task.

## Hệ quả

- Được: thêm tham số nhanh; một nguồn quy tắc kiểm tra cho API và web; không có bảng cài đặt rải rác.
- Mất / rủi ro: DB không bảo vệ kiểu từng tham số; quên migration dữ liệu khi đổi schema sẽ làm thao tác đọc báo lỗi (cố ý, an toàn hơn dùng sai giá trị); không truy vấn SQL theo từng tham số thuận tiện như cột riêng.
