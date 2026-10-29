## Quy ước

Chốt ngày <YYYY-MM-DD>. ADR liên quan: <danh sách mã ADR>.

### Cấu trúc thư mục code

- <monorepo hay không, công cụ quản lý workspace>
- <vị trí backend NestJS, worker trình duyệt, web app, thư viện dùng chung>
- <vị trí test, fixture, migration>

### Đặt tên

- File: <quy tắc>
- Class, interface, type: <quy tắc>
- Biến, hàm: <quy tắc>
- Bảng, cột DB: <quy tắc>
- Endpoint API: <quy tắc>
- Biến môi trường: <quy tắc>

### Nhánh và commit

- Tên nhánh: <mẫu, phải chứa phase-N và mã task>
- Commit message: <chuẩn>
- Merge: <cách merge vào main>

### Lint, format, typecheck

- Công cụ: <danh sách>
- Lệnh: `<lệnh lint>`, `<lệnh format>`, `<lệnh typecheck>`

### Test tự động

- Công cụ: <test runner, thư viện property-based, cách chạy DB thật trong Docker>
- Vị trí và đặt tên file test: <quy tắc>
- Đồng hồ: <cách truyền đồng hồ vào, cấm gọi Date.now() trực tiếp trong logic nghiệp vụ>
- Fixture: <vị trí, cách ẩn thông tin cá nhân>
- Skip: test bị bỏ qua phải in lý do; không được báo pass khi thiếu dữ liệu
- Lệnh: `<lệnh test nhanh>`, `<lệnh integration test>`
