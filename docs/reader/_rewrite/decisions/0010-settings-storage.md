<!-- src-section: 0b0fa0b228 911f358df64f -->
# 0010 – Lưu cài đặt nghiệp vụ dạng mục JSON có schema

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan:
  - phase-0 app-skeleton (bảng `app_settings`), crawl-settings, group-settings, emergency-stop và mọi tính năng có cài đặt;
  - docs/project/03-data-model.md mục 1;
  - 07-screens-and-settings.md mục 2;
  - docs/design/db-schema.md.

**Tóm tắt.** Cài đặt nghiệp vụ được lưu trong một bảng, mỗi khoá là một mục JSON và được kiểm tra bằng zod schema dùng chung. Cách này cho phép đọc và ghi theo nhóm, có thông báo lỗi tiếng Việt, và thêm tham số mà không đụng tới cấu trúc DB.

<!-- src-section: 0bc81167ac 378936911e8f -->
## Bối cảnh

- Tài liệu 07 mục 2 có khoảng 60 tham số, chia theo nhóm: quét, phanh an toàn, lịch, inbox, content, AI và các nhóm khác. Số tham số tăng dần qua từng giai đoạn.
- Cài đặt lưu trong DB. Khi đổi trên web, cài đặt có hiệu lực ngay mà không cần khởi động lại (03 mục 1).
- Cần kiểm tra dữ liệu chặt chẽ về khoảng giá trị, định dạng và thông báo lỗi. Web cũng cần dùng lại đúng các quy tắc này.

<!-- src-section: 1be8f16534 d5428cea36cd -->
## Các phương án

<!-- src-section: 0b7eaf4d6d e65f8be71cc4 -->
### A. Bảng `app_settings` lưu mỗi khoá một mục JSON, kiểm tra bằng zod schema trong `@mio/shared`

**Ưu**

- Thêm tham số không cần migration cấu trúc.
- Mỗi mục (ví dụ `crawl-schedule`) được đọc và ghi trọn vẹn, khớp với một form.
- Zod schema dùng chung cho API và web.
- Giá trị mặc định nằm trong code, cạnh schema.

**Nhược**

- DB không kiểm tra kiểu của từng tham số.
- Đổi schema phải kèm migration dữ liệu. Nếu quên thì giá trị cũ trở thành không hợp lệ; trường hợp này được xử lý bằng R-SKL-12.

<!-- src-section: f249cce0be 1c67a45dc645 -->
### B. Một bảng một dòng, mỗi tham số một cột có kiểu

**Ưu**

- DB kiểm tra kiểu và ràng buộc.
- Truy vấn trực tiếp dễ dàng.

**Nhược**

- Bảng rất rộng.
- Mỗi tham số mới cần một migration.
- Nhiều tính năng cùng sửa một bảng nên dễ xung đột.

<!-- src-section: cf78c4307d 2051ae5c2361 -->
### C. Mỗi tính năng một bảng cài đặt riêng

**Ưu**

- Ràng buộc DB theo từng nhóm.
- Quyền sở hữu được tách rõ.

**Nhược**

- Có nhiều bảng chỉ có một dòng.
- Lặp lại code đọc, ghi và giá trị mặc định.
- Vẫn cần migration cho mỗi tham số mới.

<!-- src-section: 254160d409 37cc7814057b -->
## Quyết định

Chọn phương án A.

**Vì sao**

- Cài đặt được đọc và ghi theo nhóm.
- Việc kiểm tra ở tầng ứng dụng vốn đã bắt buộc, để có thông báo lỗi tiếng Việt.
- Thêm tham số không đụng tới cấu trúc DB.

**Quy ước kèm theo**

- Khoá viết kebab-case. Tính năng sở hữu khoá thì sở hữu luôn schema và giá trị mặc định của khoá đó.
- Khoá chưa có trong DB thì dùng giá trị mặc định.
- Giá trị trong DB không qua được schema thì hệ thống báo lỗi. Lỗi nêu cụ thể từng trường, lý do và giá trị đang lưu. Hệ thống không lặng lẽ dùng giá trị mặc định (R-SKL-12).
- Mỗi khoá có endpoint đọc và ghi riêng, do tính năng sở hữu khai báo. Thao tác ghi thay cả mục.
- Đổi schema của khoá đã có dữ liệu thì phải viết migration dữ liệu trong cùng task.

**Chi tiết kỹ thuật**

- Khai báo khoá: `defineSetting({ key, schema, defaultValue })` trong `SETTINGS` của `@mio/shared`.
- Lỗi khi giá trị đang lưu không hợp lệ: 409 `INVALID_STORED_SETTING`.
- Endpoint: `GET` / `PUT /api/v1/settings/<khóa>`. `PUT` thay cả mục.

<!-- src-section: 58c5fdb1ed 6fb5bdb6614e -->
## Hệ quả

**Được**

- Thêm tham số nhanh.
- Có một nguồn quy tắc kiểm tra cho cả API và web.
- Không có bảng cài đặt rải rác.

**Mất và rủi ro**

- DB không bảo vệ kiểu của từng tham số.
- Nếu quên migration dữ liệu khi đổi schema thì thao tác đọc sẽ báo lỗi. Đây là chủ ý, vì báo lỗi an toàn hơn dùng sai giá trị.
- Truy vấn SQL theo từng tham số không thuận tiện bằng khi có cột riêng.
