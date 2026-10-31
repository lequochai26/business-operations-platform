# Review thiết kế – Khung ứng dụng (`app-skeleton`)

- Ngày: 2026-10-29
- Đối tượng: thiết kế chi tiết, test case (không có mockup)
- Tổng: 19 điểm (1 chặn, 13 nên sửa, 5 gợi ý)

### RV-01 Job bị stalled vẫn được BullMQ chạy lại một lần
- Mức độ: chặn
- Vị trí: design/app-skeleton.md R-SKL-07, R-SKL-22, R-SKL-29; test P0-SKL-060, P0-SKL-061
- Vấn đề: thiết kế viết job dở dang bị đánh dấu stalled "không tự chạy lại vì `attempts: 1`". Thực tế `attempts` không áp dụng cho stalled: Worker của BullMQ có `maxStalledCount` mặc định 1, nên job stalled lần đầu được đưa lại về `wait` và chạy lại, chỉ lần stalled thứ hai mới `failed`. Với job comment ở giai đoạn 1, đây là đường comment hai lần vào một bài (lằn ranh đỏ "kể cả khi retry"). P0-SKL-060, P0-SKL-061 sẽ không đạt nếu implement theo thiết kế hiện tại.
- Đề xuất:
  - R-SKL-07 thêm: mọi Worker (browser-worker và api) đặt `maxStalledCount: 0`, nên job stalled chuyển thẳng `failed`, không quay về `wait`;
  - nêu `lockDuration` để mặc định (30 giây, tự gia hạn) và yêu cầu processor không chặn event loop (tránh stalled giả khi job vẫn đang chạy);
  - sửa câu trong R-SKL-22, R-SKL-29 cho đúng cơ chế; thêm test tự động (integration) "job stalled → failed, không chạy lần hai".
- Kết quả: đã sửa (R-SKL-07, R-SKL-22, R-SKL-29; P0-SKL-057, Ghi chú chạy: test tự động)

### RV-02 Một job gốc có thể sinh hai tín hiệu kết quả
- Mức độ: nên sửa
- Vị trí: R-SKL-28, R-SKL-29
- Vấn đề: chưa quy định khi một job gốc có cả job kết quả lẫn sự kiện `failed`. Xảy ra khi: processor ném lỗi sau khi đã gửi kết quả; hoặc stalled giả (worker vẫn chạy, mất lock) – api nhận `WorkerCrashedError` rồi sau đó worker vẫn gửi kết quả thật. Nếu tính năng coi `WorkerCrashedError` là "chưa làm" và tự xếp lại việc, thao tác ghi lên Facebook (comment) có thể bị làm hai lần.
- Đề xuất: thêm vào R-SKL-28, R-SKL-29:
  - processor bắt mọi lỗi và luôn gửi job kết quả (lỗi chưa phân loại → `type: 'UnexpectedError'`), sau đó kết thúc job gốc bình thường; job gốc chỉ `failed` khi không gửi được kết quả (worker chết, stalled);
  - api xử lý theo `sourceJobId`, idempotent; kết quả từ hàng đợi kết quả luôn thắng `WorkerCrashedError` dù tới sau;
  - `WorkerCrashedError` nghĩa là "không rõ đã làm tới đâu"; tính năng có thao tác ghi lên Facebook không được coi là chưa làm để tự làm lại.
- Kết quả: đã sửa (R-SKL-28, R-SKL-29; Ghi chú chạy: test tự động)

### RV-03 R-SKL-29 dựa vào sự kiện nên mất tín hiệu khi api tắt
- Mức độ: nên sửa
- Vị trí: R-SKL-29; mục Job và hàng đợi
- Vấn đề: R-SKL-28 bỏ cách dùng sự kiện `completed` vì "api tắt đúng lúc đó sẽ bỏ lỡ sự kiện", nhưng R-SKL-29 lại dựa vào sự kiện `failed` (QueueEvents mặc định chỉ đọc sự kiện mới). Worker chết trong lúc api đang khởi động lại → job gốc `failed` mà không tính năng nào biết; `group-crawl-job` có thể chờ kết quả mãi. Ngoài ra, kiểm tra stalled chỉ do Worker chạy, nên khi không còn browser-worker nào sống, job nằm ở `active` vô thời hạn.
- Đề xuất: thêm vào R-SKL-29: ngoài nghe sự kiện, api đối soát lúc khởi động và mỗi 5 phút: job `failed` của `fb-browser` / `fb-inbox` chưa được xử lý → xử lý như `WorkerCrashedError` (dùng chung đường idempotent của RV-02). Job `active` khi khóa nhịp sống đã hết hạn: ghi rõ do `emergency-stop` phát hiện và báo. Thêm test case: dừng api, giết worker giữa job, chạy lại api → lượt quét ghi thất bại đúng một lần.
- Kết quả: đã sửa (R-SKL-29, mục Tham số; P0-SKL-069)

### RV-04 Docker không tự khởi động lại container unhealthy; thiếu tham số healthcheck
- Mức độ: nên sửa
- Vị trí: mục Xử lý lỗi ("browser-worker chết → healthcheck không đạt, Compose khởi động lại"); R-SKL-18; mục Khởi động
- Vấn đề:
  - `restart: unless-stopped` chỉ khởi động lại khi tiến trình thoát; container `unhealthy` nhưng còn chạy (treo) không được Docker Compose khởi động lại. Câu trong thiết kế sai.
  - Chưa có tham số healthcheck (`interval`, `timeout`, `retries`, `start_period`) của 4 dịch vụ, và lệnh healthcheck của api (image `node:*-slim` không có `curl`).
  - Khóa nhịp sống dùng chung một tên: khi chạy 2 browser-worker (P0-SKL-058), worker treo bị worker còn sống che, vẫn báo healthy.
- Đề xuất:
  - sửa câu: tiến trình thoát → restart policy chạy lại; tiến trình treo → `unhealthy`, không tự chạy lại; khóa nhịp sống hết hạn là tín hiệu cho `emergency-stop`;
  - thêm bảng healthcheck: postgres `pg_isready`, redis `redis-cli ping`, api `node dist/healthcheck.js` gọi `/api/v1/health`, browser-worker `node dist/healthcheck.js`; interval 10 giây, timeout 5 giây, retries 3, start_period 30 giây (api 60 giây vì chạy migration);
  - khóa nhịp sống theo tiến trình: `mio:heartbeat:browser-worker:<hostname>`, healthcheck đọc khóa của chính container.
- Kết quả: đã sửa (R-SKL-18, thêm R-SKL-31, mục Tham số; P0-SKL-032, P0-SKL-033, P0-SKL-066, P0-SKL-071)

### RV-05 api và browser-worker có thể chạy bằng user khác nhau trên cùng thư mục dữ liệu
- Mức độ: nên sửa
- Vị trí: R-SKL-20; mục Tham số (base image)
- Vấn đề: hai image khác nhau (`node:26-bookworm-slim` có user `node`, image Playwright có user `pwuser`), uid có thể khác. Cả hai ghi chung `MIO_DATA_DIR`; api cần đọc `debug-dumps/` do worker ghi (ảnh tự dừng ở `emergency-stop`). Trên máy Linux (Oracle) dễ bị lỗi quyền.
- Đề xuất: R-SKL-20 chốt cả hai container chạy cùng `uid:gid` (1000:1000), thư mục và file trong `images/`, `debug-dumps/` cho nhóm đọc được; P0-SKL-011 thêm bước: `id -u`, `id -g` của hai container bằng nhau, api đọc được file worker ghi trong `debug-dumps/`.
- Kết quả: đã sửa (R-SKL-20; P0-SKL-011; 05-roadmap.md mục Triển khai lên máy chủ thêm bước chown)

### RV-06 Profile trình duyệt trên ổ Windows: quyền 700 không có tác dụng, rủi ro hỏng phiên
- Mức độ: nên sửa
- Vị trí: R-SKL-20; bảng biến Compose (`MIO_DATA_DIR`); P0-SKL-011 bước 3
- Vấn đề: giai đoạn 0 chạy trên Windows, `MIO_DATA_DIR` nhiều khả năng là thư mục trên ổ NTFS (ví dụ `D:\mio-data`) gắn qua Docker Desktop. Bind mount kiểu này không giữ quyền Unix (`chmod 700` không có tác dụng, P0-SKL-011 bước 3 sẽ không đạt), chậm, và khóa file SQLite của profile Chromium kém tin cậy – ảnh hưởng trực tiếp bài chạy 24 giờ không bị đăng xuất.
- Đề xuất: tách `browser-profile` ra named volume riêng `mio-browser-profile` gắn vào `/data/browser-profile` (nằm trên ext4 trong máy ảo Docker, quyền 700 có hiệu lực); `images/`, `debug-dumps/` giữ trong `MIO_DATA_DIR`. Phù hợp ADR 0009 (khác biệt nằm ở volume) và 04 mục 7 (profile không đưa vào bản sao lưu công khai, không copy khi dời máy). Cập nhật R-SKL-20, P0-SKL-011, P0-SKL-039.
- Kết quả: đã sửa (R-SKL-20, biến BROWSER_PROFILE_DIR, named volume mio-browser-profile; ADR 0013; P0-SKL-008 … P0-SKL-012, P0-SKL-039)

### RV-07 Phiên bản Node của browser-worker chưa chốt, test case giả định Node 26
- Mức độ: nên sửa
- Vị trí: mục Tham số (phiên bản hạ tầng); P0-SKL-038 bước 2
- Vấn đề: image `mcr.microsoft.com/playwright:v1.63.0-noble` mang sẵn Node của Playwright, không chắc là 26. P0-SKL-038 bước 2 mong `v26.x.x` cho cả api và browser-worker. Code dùng chung (`@mio/shared`) phải chạy trên cả hai phiên bản.
- Đề xuất: ghi rõ browser-worker dùng Node đi kèm image Playwright (phiên bản cụ thể ghi vào `plan.md` lúc implement), `@mio/shared` và `apps/browser-worker` chỉ dùng tính năng có trên phiên bản đó; P0-SKL-038 bước 2 đổi thành "api `v26.x.x`, browser-worker đúng phiên bản Node của image Playwright". Phương án khác: build browser-worker từ `node:26-bookworm-slim` + `playwright install --with-deps chromium` để chỉ có một phiên bản Node.
- Kết quả: đã sửa theo phương án A (mục Tham số; ADR 0014; P0-SKL-038)

### RV-08 Mã lỗi API dùng chung chưa đủ và chưa nằm ở chỗ dùng chung
- Mức độ: nên sửa
- Vị trí: R-SKL-10, R-SKL-11, R-SKL-12, R-SKL-15; `docs/design/api/system.md`; `openapi.yaml`; P0-SKL-049
- Vấn đề:
  - `VALIDATION_ERROR` (400) và `INVALID_STORED_SETTING` (409) dùng cho mọi endpoint cài đặt của nhiều tính năng nhưng chưa có trong `api/system.md` và chưa có response dùng chung trong `openapi.yaml`.
  - Chưa quy định thân JSON sai cú pháp và thân quá lớn; NestJS mặc định trả `{ statusCode, message, error }`, trái R-SKL-15.
  - `SETTING_NOT_FOUND` không bao giờ tới được qua HTTP: mỗi khóa có route cố định (ADR 0010), khóa lạ rơi vào 404 `NOT_FOUND`. P0-SKL-049 phải chú thích "câu hỏi mở 3" không tồn tại.
- Đề xuất:
  - R-SKL-15 và `system.md` thêm mã chung: `400 VALIDATION_ERROR` (có `fields`), `400 INVALID_JSON` "Dữ liệu gửi lên không đúng định dạng JSON", `413 PAYLOAD_TOO_LARGE` "Dữ liệu gửi lên quá lớn" (giới hạn thân 1 MB), `409 INVALID_STORED_SETTING`; thêm response dùng chung vào `openapi.yaml` (sinh lại, lint);
  - bỏ `SETTING_NOT_FOUND`: `UnknownSettingKeyError` là lỗi lập trình (khóa có kiểu `SettingKey`, typecheck chặn), nếu xảy ra lúc chạy thì 500 `INTERNAL_ERROR`; P0-SKL-049 bỏ chú thích;
  - thêm test case JSON sai cú pháp và thân quá 1 MB (cần một endpoint nhận thân – chạy khi có `crawl-settings`).
- Kết quả: đã sửa (R-SKL-10, R-SKL-15; api/system.md; openapi.yaml sinh lại, lint sạch; P0-SKL-049, P0-SKL-065)

### RV-09 Thông báo lỗi biến môi trường chưa nguyên văn; "biến rỗng coi như thiếu" chưa có trong thiết kế
- Mức độ: nên sửa
- Vị trí: bảng Biến môi trường; R-SKL-01, R-SKL-02; P0-SKL-004, P0-SKL-006
- Vấn đề: R-SKL-02 chỉ có ví dụ cho `REDIS_URL`; phần `<yêu cầu>` của `DATABASE_URL`, `DATA_DIR`, `PUBLIC_URL` chỉ xuất hiện trong test case. P0-SKL-004 dựa vào quy tắc "biến rỗng coi như thiếu" mà thiết kế không có. Test case dẫn "câu hỏi mở 1, 2" không tồn tại ở cả hai file.
- Đề xuất: thêm cột "Yêu cầu (in trong thông báo)" vào bảng: `DATABASE_URL` "phải là URL postgres:// hoặc postgresql://", `REDIS_URL` "phải là URL redis://", `DATA_DIR` "phải là đường dẫn tuyệt đối", `PUBLIC_URL` "phải là URL http:// hoặc https://, không có / cuối"; R-SKL-01 thêm "giá trị rỗng hoặc chỉ có khoảng trắng coi như thiếu"; xóa chú thích "câu hỏi mở" trong P0-SKL-004, P0-SKL-006.
- Kết quả: đã sửa (bảng Biến môi trường, R-SKL-01, R-SKL-02; P0-SKL-004, P0-SKL-006)

### RV-10 `SettingsService` còn chỗ hiểu hai cách
- Mức độ: nên sửa
- Vị trí: R-SKL-11, R-SKL-12; mục Đọc / ghi cài đặt; P0-SKL-051
- Vấn đề:
  - chưa nói lưu giá trị gửi lên hay giá trị sau parse; trường lạ (không có trong schema) bị bỏ hay báo lỗi, ở cả `set` lẫn `get`;
  - định dạng đường dẫn trong `fields` chỉ nêu ở R-SKL-12; chưa có cách ghi lỗi ở gốc (thân không phải object) và trường có nhiều lỗi;
  - "đang lưu: <giá trị>" chưa nói in thế nào (chuỗi có ngoặc kép không) và cắt 100 ký tự tính trên gì.
- Đề xuất:
  - lưu kết quả parse; trường lạ bị bỏ (mặc định của zod) ở cả `set` và `get`, nên bỏ một trường khỏi schema không làm giá trị cũ thành lỗi;
  - một định dạng đường dẫn cho R-SKL-11 và R-SKL-12 (`goldenHours[1].end`); lỗi ở gốc dùng khóa `_root`; một trường nhiều lỗi lấy lỗi đầu tiên;
  - giá trị in bằng `JSON.stringify` (chuỗi có ngoặc kép, ví dụ `"abc"`), cắt khi chuỗi JSON dài hơn 100 ký tự; P0-SKL-051 đổi biên: chuỗi 98 ký tự (JSON 100) không cắt, 99 ký tự (JSON 101) bị cắt.
- Kết quả: đã sửa (R-SKL-11, R-SKL-12; P0-SKL-048, P0-SKL-051, P0-SKL-068)

### RV-11 `created_at` lấy giờ DB, `updated_at` lấy `CLOCK`
- Mức độ: nên sửa
- Vị trí: `docs/design/db-schema.md` mục `app_settings` và Quy ước chung; mục Đọc / ghi cài đặt
- Vấn đề: lần ghi đầu, `created_at` lấy `now()` của DB còn `updated_at` lấy `CLOCK.now()` (hoặc cũng `now()` – thiết kế không nói nhánh INSERT). Trong test dùng `FakeClock`, `updated_at` có thể nhỏ hơn `created_at`; các bảng sau sẽ lặp lại cùng vấn đề.
- Đề xuất: db-schema Quy ước chung thêm: app đặt `created_at`, `updated_at` bằng `CLOCK.now()` khi ghi; mặc định `now()` của DB chỉ là dự phòng cho SQL viết tay. Mục Đọc / ghi cài đặt ghi rõ nhánh INSERT đặt cả hai cột.
- Kết quả: đã sửa (db-schema.md Quy ước chung; mục Đọc / ghi cài đặt; P0-SKL-046)

### RV-12 Mất kết nối DB/Redis: "thư viện tự kết nối lại" còn mơ hồ
- Mức độ: nên sửa
- Vị trí: mục Xử lý lỗi; mục Khởi động; R-SKL-13
- Vấn đề:
  - chưa quy định khi khởi động không kết nối được PostgreSQL/Redis (api khởi động lại lúc DB đang dừng);
  - khi đang chạy, pool `pg` phát sự kiện `error` mà không ai bắt sẽ làm sập tiến trình (P0-SKL-017 kiểm `RestartCount` không đổi);
  - `/health` kiểm tuần tự thì tổng có thể tới 4 giây, trái P0-SKL-020 (2–3 giây); nếu dùng chung kết nối BullMQ (thử lại vô hạn) thì lệnh ping xếp hàng sau.
- Đề xuất: thêm quy tắc:
  - khởi động: thử kết nối mỗi 2 giây tối đa 30 giây, không được thì thoát mã 1, thông báo "Không kết nối được PostgreSQL" / "Không kết nối được Redis";
  - đang chạy: bắt sự kiện lỗi của pool `pg` và ioredis, ghi log `warn`, không thoát; ioredis thử lại không giới hạn (`maxRetriesPerRequest: null` theo yêu cầu BullMQ); request cần DB trong lúc mất kết nối → 500 `INTERNAL_ERROR`;
  - `/health` kiểm DB và Redis song song, dùng kết nối riêng, mỗi kiểm tra timeout 2 giây.
  - Thêm test case: chạy lại api khi PostgreSQL đang dừng.
- Kết quả: đã sửa (R-SKL-13, thêm R-SKL-30; P0-SKL-020, P0-SKL-070)

### RV-13 `container_stats.py` thiếu khoảng tham số và phạm vi container
- Mức độ: nên sửa
- Vị trí: R-SKL-24; mục Đo RAM/CPU từng container; P0-SKL-040 … P0-SKL-042
- Vấn đề: `docker stats` liệt kê mọi container trên máy (cả Testcontainers, container khác), làm lẫn số liệu nghiệm thu. `--interval` chưa có khoảng hợp lệ, `--out` chưa rõ bắt buộc hay mặc định, `cpu_percent` trên 100% chưa giải thích, `summary` với file không tồn tại chưa quy định.
- Đề xuất:
  - chỉ lấy container có nhãn `com.docker.compose.project` của project app;
  - `--interval`: số nguyên 5–3600, mặc định 60; sai → thoát mã 2, "--interval phải là số nguyên từ 5 đến 3600";
  - `--out`: mặc định `.local/metrics/<YYYY-MM-DD-HHmm>.csv` theo giờ `Asia/Ho_Chi_Minh`;
  - `cpu_percent` theo `docker stats`, 100% = 1 lõi;
  - `summary` file không có → thoát mã 1, "Không tìm thấy file: <đường dẫn>";
  - thêm test case biên `--interval` (4, 5, 3600, 3601, `abc`) và container ngoài project bị bỏ qua.
- Kết quả: đã sửa (R-SKL-24, mục Đo RAM/CPU; P0-SKL-040, P0-SKL-067)

### RV-14 Case về "không tự chạy lại job" chưa gắn regression
- Mức độ: nên sửa
- Vị trí: test/cases/app-skeleton.md P0-SKL-057
- Vấn đề: P0-SKL-057 kiểm `attempts: 1`, gắn với lằn ranh đỏ "không comment hai lần (kể cả khi retry)", nhưng `Regression: không`. Checklist test case yêu cầu case của lằn ranh đỏ có `Regression: có`.
- Đề xuất: đổi `Regression: có`; nếu nhận RV-01 thì thêm bước kiểm `maxStalledCount` của worker (qua log khởi động hoặc cấu hình).
- Kết quả: đã sửa (P0-SKL-057 Regression: có)

### RV-15 Đăng ký hàng đợi của giai đoạn sau ngay trong khung
- Mức độ: gợi ý
- Vị trí: mục Job và hàng đợi; R-SKL-05; P0-SKL-037
- Vấn đề: khung đăng ký worker cho `fb-inbox`, `render`, `ai-*`… dù giai đoạn 0 không dùng. 04 mục 4.3: nếu inbox dùng chung tài khoản vận hành thì `fb-inbox` gộp vào `fb-browser` (inbox ưu tiên cao nhất) – chủ tiệm chưa chọn. Hai hàng đợi riêng cùng mở một `browser-profile/` sẽ xung đột.
- Đề xuất: giai đoạn 0 chỉ khai báo tên trong `QUEUE_NAMES`, chỉ đăng ký `fb-browser`, `fb-browser-results`; tính năng của giai đoạn sau tự đăng ký. R-SKL-05 ghi chú: gộp hay tách `fb-inbox` quyết ở giai đoạn 3 theo 04 mục 4.3. P0-SKL-037 bỏ phần `fb-inbox`.
- Kết quả: đã sửa (R-SKL-05, mục Job và hàng đợi; P0-SKL-037)

### RV-16 pino không che được khóa "ở mọi độ sâu"
- Mức độ: gợi ý
- Vị trí: R-SKL-17; ADR 0012
- Vấn đề: `redact` của pino nhận đường dẫn cụ thể và wildcard một cấp, không có wildcard đệ quy. Yêu cầu "ở mọi độ sâu" buộc phải viết serializer duyệt cả object cho mỗi dòng log.
- Đề xuất: chốt danh sách đường dẫn: header request/response (`authorization`, `cookie`, `set-cookie`) và `password`, `token`, `secret`, `cookie` tới độ sâu 3 (`*.x`, `*.*.x`, `*.*.*.x`); giữ yêu cầu "không lộ" bằng test tự động cho từng đường dẫn.
- Kết quả: đã sửa (R-SKL-17)

### RV-17 Compose nên báo thiếu biến ngay thay vì truyền chuỗi rỗng
- Mức độ: gợi ý
- Vị trí: bảng biến Compose; P0-SKL-004
- Vấn đề: thiếu `MIO_PUBLIC_URL` trong `.env` thì Compose chỉ cảnh báo, truyền chuỗi rỗng, api rơi vào vòng khởi động lại.
- Đề xuất: dùng `${MIO_PUBLIC_URL:?Thiếu MIO_PUBLIC_URL trong .env}` (tương tự `POSTGRES_PASSWORD`, `MIO_DATA_DIR`) để `docker compose up` dừng ngay với thông báo rõ; P0-SKL-004 đổi kết quả mong đợi. R-SKL-01 vẫn giữ cho trường hợp chạy image trực tiếp.
- Kết quả: đã sửa (bảng biến Compose; P0-SKL-004)

### RV-18 Vài chi tiết implement nên ghi rõ
- Mức độ: gợi ý
- Vị trí: R-SKL-22; mục `apps/web`; mục `apps/api` (`core/db`)
- Vấn đề / đề xuất:
  - R-SKL-22: Dockerfile dùng `CMD ["node", "dist/main.js"]` dạng exec (không qua `pnpm` hay `sh`), nếu không `SIGTERM` không tới Node;
  - `ui-tokens.css` "chép lúc build": ghi rõ bản chép là file sinh ra (gitignore) để không có hai nguồn;
  - `core/db` (DbModule) và `src/db/schema/` (theo `CLAUDE.md`) là hai thư mục DB; ghi rõ schema và `runMigrations` nằm đâu;
  - api chạy một bản; nếu sau này chạy nhiều bản thì migration cần khóa (`pg_advisory_lock`).
- Kết quả: đã sửa (R-SKL-03, R-SKL-22, mục apps/web, core/db; P0-SKL-034)

### RV-19 Bổ sung vài test case
- Mức độ: gợi ý
- Vị trí: test/cases/app-skeleton.md
- Vấn đề: chưa có case truy cập file ngoài `apps/web/dist` qua đường dẫn tĩnh (`../`).
- Đề xuất: thêm case `curl --path-as-is http://127.0.0.1:3000/../package.json` và `/%2e%2e/package.json` → trả `index.html` hoặc 404, không trả nội dung file ngoài `dist`.
- Kết quả: đã sửa (R-SKL-14; P0-SKL-072)
