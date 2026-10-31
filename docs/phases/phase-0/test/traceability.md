# Bảng đối chiếu thiết kế ↔ test case – Giai đoạn 0

Mỗi quy tắc trong thiết kế chi tiết phải có ít nhất một case. Thêm dòng khi thiết kế tính năng mới; không xóa dòng của tính năng khác.

| Quy tắc | Mô tả | Case |
|---|---|---|
| R-SKL-01 | Thiếu hoặc rỗng biến môi trường → liệt kê hết, thoát mã 1 | P0-SKL-002, P0-SKL-003, P0-SKL-004, P0-SKL-009 |
| R-SKL-02 | Biến sai định dạng → thoát mã 1, thông báo nguyên văn, không in giá trị | P0-SKL-005, P0-SKL-006, P0-SKL-007, P0-SKL-008, P0-SKL-026 |
| R-SKL-03 | Chỉ api chạy migration trước khi mở cổng; lỗi thì thoát | P0-SKL-001, P0-SKL-013, P0-SKL-014 |
| R-SKL-04 | browser-worker chỉ nối Redis, không cổng HTTP, không gọi API | P0-SKL-009, P0-SKL-015 |
| R-SKL-05 | `fb-browser` global concurrency 1; giai đoạn 0 chỉ đăng ký `fb-browser`, `fb-browser-results` | P0-SKL-037, P0-SKL-058 |
| R-SKL-06 | Tên hàng đợi chỉ lấy từ `QUEUE_NAMES` | P0-SKL-037 |
| R-SKL-07 | Tùy chọn job mặc định, `maxStalledCount: 0`, không tự chạy lại | P0-SKL-057, P0-SKL-060, P0-SKL-061 |
| R-SKL-08 | `get` đọc DB mỗi lần, không cache | P0-SKL-047, P0-SKL-055 |
| R-SKL-09 | Khóa chưa có bản ghi → mặc định, không ghi DB | P0-SKL-045, P0-SKL-055 |
| R-SKL-10 | Khóa không có trong `SETTINGS` → lỗi lập trình (500); khóa lạ trên URL → 404 `NOT_FOUND` | P0-SKL-049 |
| R-SKL-11 | Giá trị sai schema → 400, không ghi; ghi đúng thì upsert kết quả parse, bỏ trường lạ | P0-SKL-046, P0-SKL-048, P0-SKL-053, P0-SKL-065, P0-SKL-068 |
| R-SKL-12 | Giá trị đang lưu không hợp lệ → 409, nêu mọi trường; job thất bại | P0-SKL-050, P0-SKL-051, P0-SKL-052, P0-SKL-063 |
| R-SKL-13 | `/health` công khai, 200/503 theo DB và Redis, kiểm song song, chờ 2 giây | P0-SKL-001, P0-SKL-016, P0-SKL-017, P0-SKL-018, P0-SKL-019, P0-SKL-020 |
| R-SKL-14 | api phục vụ web, SPA fallback, không lộ file ngoài `dist` | P0-SKL-001, P0-SKL-021, P0-SKL-022, P0-SKL-023, P0-SKL-072 |
| R-SKL-15 | Định dạng lỗi chung; mã chung `NOT_FOUND`, `INVALID_JSON`, `PAYLOAD_TOO_LARGE`, `VALIDATION_ERROR` | P0-SKL-021, P0-SKL-048, P0-SKL-049, P0-SKL-065 |
| R-SKL-16 | Lỗi không lường trước → 500, không lộ chi tiết, log đủ | P0-SKL-054 |
| R-SKL-17 | Log JSON một dòng, che khóa nhạy cảm | P0-SKL-006, P0-SKL-025, P0-SKL-026 |
| R-SKL-18 | Nhịp sống theo container, 15 giây, TTL 60 giây, healthcheck đọc khóa của chính container | P0-SKL-009, P0-SKL-018, P0-SKL-032, P0-SKL-033, P0-SKL-066 |
| R-SKL-19 | Chỉ publish cổng api trên 127.0.0.1; dev mở DB, Redis trên 127.0.0.1 | P0-SKL-028, P0-SKL-029 |
| R-SKL-20 | Cùng uid 1000 không root, thư mục con của `DATA_DIR`, profile trong named volume quyền 700, lỗi ghi | P0-SKL-008, P0-SKL-010, P0-SKL-011, P0-SKL-012, P0-SKL-039 |
| R-SKL-21 | Image build được amd64 và arm64, không giá trị phụ thuộc máy | P0-SKL-038, P0-SKL-039 |
| R-SKL-22 | `SIGTERM` → chờ job xong trong ân hạn, thoát mã 0; Node là PID 1 | P0-SKL-034, P0-SKL-059, P0-SKL-060 |
| R-SKL-23 | Múi giờ UTC; lint chặn `Date.now()` / `new Date()` | P0-SKL-030, P0-SKL-031 |
| R-SKL-24 | Đo RAM/CPU từng container của app, CSV và tổng hợp, tham số | P0-SKL-040, P0-SKL-041, P0-SKL-042, P0-SKL-067 |
| R-SKL-25 | `pnpm test:int` fail khi thiếu Docker; cùng image với compose | P0-SKL-043, P0-SKL-044 |
| R-SKL-26 | Giới hạn log Docker 10 MB × 5 | P0-SKL-027 |
| R-SKL-27 | Redis AOF và `noeviction` | P0-SKL-036 |
| R-SKL-28 | Kết quả qua hàng đợi kết quả, `BrowserJobResult`, processor luôn gửi kết quả, kiểm tra zod | P0-SKL-056, P0-SKL-062, P0-SKL-064 |
| R-SKL-29 | Job gốc mất kết quả → `WorkerCrashedError`, không chạy lại, đối soát, idempotent | P0-SKL-060, P0-SKL-061, P0-SKL-069 |
| R-SKL-30 | Kết nối DB/Redis lúc khởi động (thử 30 giây) và khi đang chạy (không sập) | P0-SKL-017, P0-SKL-018, P0-SKL-070 |
| R-SKL-31 | Healthcheck Compose; container unhealthy không tự khởi động lại | P0-SKL-001, P0-SKL-033, P0-SKL-071 |
| SKL mục `cli.ts` | Lệnh CLI: help, lệnh không tồn tại | P0-SKL-035 |
| SKL mục `apps/web` | Trang giữ chỗ, Vite proxy | P0-SKL-022, P0-SKL-024 |
| R-AUT-01 | Tên đăng nhập trống → "Nhập tên đăng nhập" | P0-AUT-005, P0-AUT-006, P0-AUT-010 |
| R-AUT-02 | Tên đăng nhập đã chuẩn hóa > 32 ký tự (đo sau khi đổi chữ thường) | P0-AUT-007 |
| R-AUT-03 | Mật khẩu rỗng → "Nhập mật khẩu"; chỉ khoảng trắng không coi là rỗng | P0-AUT-005, P0-AUT-006, P0-AUT-010 |
| R-AUT-04 | Mật khẩu > 128 ký tự; độ dài theo code point; 400 không đếm vào khóa | P0-AUT-008, P0-AUT-010 |
| R-AUT-05 | Sai tên / sai mật khẩu trả giống hệt, thời gian tương đương | P0-AUT-012, P0-AUT-013, P0-AUT-020 |
| R-AUT-06 | 5 lần sai / 15 phút → khóa 15 phút; khi khóa không đếm, không kéo dài; đồng thời: kiểm lại khóa trong transaction (phần thứ tự: test tự động) | P0-AUT-014, P0-AUT-015, P0-AUT-016, P0-AUT-017, P0-AUT-018, P0-AUT-019, P0-AUT-020, P0-AUT-021, P0-AUT-022, P0-AUT-023, P0-AUT-063 |
| R-AUT-07 | Chuẩn hóa tên đăng nhập, mật khẩu giữ nguyên | P0-AUT-009, P0-AUT-022, P0-AUT-083, P0-AUT-092 |
| R-AUT-08 | Đăng nhập đúng tạo phiên, trả 201; băm lại khi tham số cũ; thay phiên của cookie đang gửi | P0-AUT-001, P0-AUT-002, P0-AUT-077, P0-AUT-096 |
| R-AUT-09 | Token 32 byte, DB chỉ lưu SHA-256; thuộc tính cookie; nhiều phiên | P0-AUT-001, P0-AUT-024, P0-AUT-025, P0-AUT-026 |
| R-AUT-10 | Hết hạn trượt 90 ngày, gia hạn khi cũ hơn 24 giờ; route công khai không gia hạn | P0-AUT-027, P0-AUT-096 |
| R-AUT-11 | Không cookie / token sai / hết hạn → 401, xóa cookie, xóa phiên hết hạn | P0-AUT-028, P0-AUT-029, P0-AUT-031, P0-AUT-045, P0-AUT-073, P0-AUT-074 |
| R-AUT-12 | Đăng xuất công khai, idempotent, luôn 204 và xóa cookie | P0-AUT-026, P0-AUT-031, P0-AUT-034, P0-AUT-035 |
| R-AUT-13 | Dọn phiên hết hạn và bộ đếm cũ khi đăng nhập | P0-AUT-032, P0-AUT-033 |
| R-AUT-14 | Mặc định từ chối; route thiếu khai báo quyền làm api không khởi động (phần khởi động: test tự động) | P0-AUT-040 |
| R-AUT-15 | Sai vai trò → 403 `FORBIDDEN`; thứ tự Origin → đọc thân → phiên → vai trò → dữ liệu | P0-AUT-042, P0-AUT-045 |
| R-AUT-16 | Quyền của từng route; `/api` không có route → 404; file tĩnh công khai | P0-AUT-040, P0-AUT-042, P0-AUT-095 |
| R-AUT-17 | `Origin` khác `PUBLIC_URL` → 403 `INVALID_ORIGIN`, cả route công khai | P0-AUT-045, P0-AUT-046, P0-AUT-047, P0-AUT-048 |
| R-AUT-18 | Header bảo mật; `Cache-Control: no-store` cho sessions, users/me | P0-AUT-035, P0-AUT-049 |
| R-AUT-19 | Mật khẩu hiện tại trống / > 128 ký tự | P0-AUT-045, P0-AUT-055, P0-AUT-057 |
| R-AUT-20 | Mật khẩu hiện tại sai → lỗi theo trường, đếm vào khóa; đang khóa → 429 | P0-AUT-060, P0-AUT-062, P0-AUT-063 |
| R-AUT-21 | Mật khẩu mới: trống, 8–128, không trùng tên, khác hiện tại; sai kiểu; thứ tự kiểm | P0-AUT-055, P0-AUT-056, P0-AUT-058, P0-AUT-061, P0-AUT-062 |
| R-AUT-22 | Nhập lại mật khẩu mới trống / không khớp (chỉ web) | P0-AUT-055, P0-AUT-059 |
| R-AUT-23 | Đổi thành công: phiên mới, xóa bộ đếm; `signOutOtherDevices` true/false/sai kiểu; xếp hàng bằng khóa dòng `users` (phần thứ tự: test tự động) | P0-AUT-050, P0-AUT-051, P0-AUT-064, P0-AUT-065, P0-AUT-066, P0-AUT-067 |
| R-AUT-24 | Đổi mật khẩu đồng thời với đăng xuất ở thiết bị khác (thứ tự: test tự động) | P0-AUT-066 |
| R-AUT-25 | `create-user`: kiểm tên, vai trò, tên hiển thị, mật khẩu; in mọi lỗi; unique; kiểm tham số trước khi hỏi mật khẩu | P0-AUT-081, P0-AUT-082, P0-AUT-083, P0-AUT-084, P0-AUT-085, P0-AUT-086, P0-AUT-087, P0-AUT-088, P0-AUT-090 |
| R-AUT-26 | `reset-password` xóa mọi phiên và bộ đếm, khóa dòng `users`; `list-users` | P0-AUT-081, P0-AUT-082, P0-AUT-091, P0-AUT-092, P0-AUT-093 |
| R-AUT-27 | Nhập mật khẩu CLI qua terminal / stdin; tham số không hợp lệ | P0-AUT-081, P0-AUT-082, P0-AUT-089 |
| R-AUT-28 | Chưa đăng nhập → `/login?next=`; kiểm `next` an toàn (cả ký tự điều khiển); đã đăng nhập mở `/login` → `/` | P0-AUT-001, P0-AUT-028, P0-AUT-030, P0-AUT-037, P0-AUT-038, P0-AUT-039, P0-AUT-078 |
| R-AUT-29 | Điều hướng theo vai trò; màn Không có quyền; 403 khi gửi form → banner, không có form → toast; tải lại vai trò | P0-AUT-002, P0-AUT-041, P0-AUT-043, P0-AUT-044, P0-AUT-074 |
| R-AUT-30 | Log sự kiện auth đủ trường (`failedCount` 5 ở lần làm khóa); log CLI vào log container; không ghi mật khẩu, token, chuỗi băm | P0-AUT-015, P0-AUT-020, P0-AUT-034, P0-AUT-050, P0-AUT-060, P0-AUT-063, P0-AUT-079, P0-AUT-080, P0-AUT-091 |
| R-AUT-31 | Phiên không còn dùng được (khi đang dùng hoặc lúc tải lại app) → về `/login?next=` kèm banner "Phiên đăng nhập đã kết thúc…"; cờ `mio.hadSession`: chưa đăng nhập bao giờ hoặc đã tự đăng xuất thì không có banner | P0-AUT-001, P0-AUT-028, P0-AUT-029, P0-AUT-030, P0-AUT-034, P0-AUT-037, P0-AUT-050, P0-AUT-073, P0-AUT-091 |
| R-AUT-32 | Đăng xuất → `/login` kèm "Bạn đã đăng xuất"; lỗi vẫn chuyển `/login`, không có banner | P0-AUT-034, P0-AUT-036, P0-AUT-048 |
| R-AUT-33 | CLI là đường khôi phục, không cần đăng nhập web, không mở cổng | P0-AUT-094 |
| R-AUT-34 | Đổi mật khẩu qua hộp thoại xác nhận, mặc định đăng xuất thiết bị khác | P0-AUT-050, P0-AUT-051, P0-AUT-052, P0-AUT-053 |
| AUT mục Màn hình (Đăng nhập, Đổi mật khẩu, Khung app, Không có quyền, Không tìm thấy) | Khớp mockup, thuộc tính ô nhập, màn hình chờ và lỗi nạp phiên | P0-AUT-003, P0-AUT-004, P0-AUT-054, P0-AUT-071, P0-AUT-076, P0-AUT-078 |
| AUT mục Xử lý lỗi | DB lỗi → 500, mất mạng, cookie bị chặn, chuỗi băm hỏng (500, không đếm) | P0-AUT-036, P0-AUT-068, P0-AUT-069, P0-AUT-070, P0-AUT-072, P0-AUT-075 |
| AUT mục API (`sessions.md`: `INVALID_JSON`, `PAYLOAD_TOO_LARGE`) | Thân request đăng nhập không phải JSON, quá 1 MB | P0-AUT-011 |
| AUT mục Tham số cài đặt | argon2id `m=19456,t=2,p=1` | P0-AUT-077, P0-AUT-081 |
| AUT mục `apps/web` | Vite proxy đặt lại `Origin` | P0-AUT-048 |
| AUT quy tắc chung (mỗi trường một lỗi) | Trường vi phạm nhiều ý chỉ hiện ý đầu tiên | P0-AUT-087 |

## Lịch sử thay đổi

- 2026-10-31: `/design-review auth`: cập nhật dòng R-AUT-02, 06, 08, 10, 15, 21, 23, 25, 26, 28 … 32, Xử lý lỗi; thêm dòng quy tắc chung; thêm P0-AUT-096
