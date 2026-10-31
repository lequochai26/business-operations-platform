# Thiết kế chi tiết – Khung ứng dụng (`app-skeleton`, `SKL`)

- Giai đoạn: 0
- Trạng thái: đã duyệt ngày 2026-10-31
- Tài liệu khái quát: 04-technical.md mục 1, 2, 3, 7; 05-roadmap.md giai đoạn 0; 03-data-model.md mục 1 "Cài đặt"; ADR 0001, 0002, 0006, 0007, 0009, 0010, 0011, 0012, 0013, 0014; `CLAUDE.md` mục Quy ước

## Tóm tắt

Dựng khung chạy được cho mọi tính năng sau: monorepo pnpm, NestJS API, worker trình duyệt tách riêng, PostgreSQL, Redis, BullMQ, web React tối thiểu, Docker Compose build được cho linux/amd64 và linux/arm64. Cung cấp các phần dùng chung: đọc biến môi trường, đồng hồ `Clock`, log, kết nối DB và hàng đợi, bảng cài đặt chung, kiểm tra sức khỏe, cách đo RAM/CPU từng container. Người dùng trực tiếp là người vận hành (Hải); chủ tiệm và thợ chưa thấy gì từ tính năng này.

## Module và interface

Hạ tầng dùng chung nằm trong `apps/<app>/src/core/` (không phải module nghiệp vụ nên không nằm trong `src/modules/`).

### `packages/shared` (`@mio/shared`)

- Đồng hồ:
  - `interface Clock { now(): Date }`; token `CLOCK` (`Symbol('CLOCK')`).
  - `class SystemClock implements Clock` trong `src/clock/system-clock.ts` (file duy nhất được gọi `new Date()`).
  - `class FakeClock implements Clock` trong `src/testing/fake-clock.ts`, xuất qua `@mio/shared/testing`: `constructor(start: Date)`, `set(at: Date)`, `advance(ms: number)`.
- Hằng số: `APP_TIME_ZONE = 'Asia/Ho_Chi_Minh'`; `QUEUE_NAMES` (mục Job và hàng đợi); `BROWSER_WORKER_HEARTBEAT_KEY_PREFIX = 'mio:heartbeat:browser-worker:'` (khóa đầy đủ thêm hostname của container, R-SKL-18).
- Kết quả job trình duyệt: type `BrowserJobResult<T>` và zod schema tương ứng (R-SKL-28).
- Cài đặt:
  - `defineSetting<T>({ key: string, schema: ZodType<T>, defaultValue: T }) -> SettingDefinition<T>`.
  - `SETTINGS`: object gom mọi `SettingDefinition`, mỗi tính năng thêm khóa của mình. Giai đoạn 0 khung chưa có khóa nào; khóa đầu tiên do `crawl-settings` thêm.
  - Đặt trong shared để web dùng lại cùng zod schema khi kiểm tra form.

### `apps/api` (`@mio/api`)

- `core/config`: `loadEnv<S>(schema: S, source: NodeJS.ProcessEnv) -> z.infer<S>`; lỗi ném `EnvValidationError` (R-SKL-01, R-SKL-02). Token `ENV`.
- `core/clock`: `ClockModule` cung cấp `CLOCK` → `SystemClock` (global).
- `core/logging`: `LoggingModule` (nestjs-pino, ADR 0012), log JSON ra stdout (R-SKL-17).
- `core/db`: `DbModule` tạo Drizzle client từ `DATABASE_URL`, token `DB`; `runMigrations(db) -> Promise<void>` chạy migration trong `apps/api/migrations/` (R-SKL-03); xử lý kết nối theo R-SKL-30. Schema Drizzle nằm ở `apps/api/src/db/schema/*.ts` (theo `CLAUDE.md`), `core/db` chỉ chứa module kết nối và `runMigrations`.
- `core/queue`: `QueueModule` tạo kết nối BullMQ từ `REDIS_URL`, đăng ký hàng đợi của giai đoạn 0 (producer `fb-browser`, worker `fb-browser-results`), áp tùy chọn job và worker mặc định (R-SKL-06, R-SKL-07); nghe sự kiện và đối soát job gốc mất kết quả (R-SKL-29).
- `core/settings`: `SettingsService` (R-SKL-08 … R-SKL-12):
  - `get<K extends SettingKey>(key: K) -> Promise<SettingValue<K>>`;
  - `set<K extends SettingKey>(key: K, value: unknown) -> Promise<SettingValue<K>>`;
  - lỗi: `UnknownSettingKeyError`, `SettingValidationError` (có `fields`), `InvalidStoredSettingError`.
- `core/health`: `HealthController` cho `GET /api/v1/health` (R-SKL-13).
- `core/http`: `ApiExceptionFilter` chuẩn hóa mọi lỗi API (R-SKL-15, R-SKL-16); giới hạn thân request 1 MB; phục vụ file tĩnh của web (R-SKL-14).
- `main.ts`: đọc env → chạy migration → mở HTTP cổng 3000, tiền tố `/api/v1`, bật shutdown hook.
- `healthcheck.ts`: script cho healthcheck của Docker, gọi `http://127.0.0.1:3000/api/v1/health` với timeout 4 giây, thoát 0 khi 200, 1 khi khác (image `node:*-slim` không có `curl`; R-SKL-31).
- `cli.ts`: điểm vào lệnh CLI dùng Nest application context, không mở HTTP: `node dist/cli.js <lệnh> [tham số]`. Khung chỉ có bộ điều phối lệnh và lệnh `help`; `auth` thêm lệnh tạo tài khoản. Lệnh không tồn tại → in "Lệnh không tồn tại: <lệnh>. Chạy help để xem danh sách." và thoát mã 1.

### `apps/browser-worker` (`@mio/browser-worker`)

- NestJS standalone (không mở cổng HTTP), chỉ kết nối Redis (ADR 0011, R-SKL-04).
- `core/config`, `core/clock`, `core/logging`: như api.
- `core/queue`: đăng ký worker cho `fb-browser` (processor do các tính năng sau thêm); `fb-inbox`, `render` do tính năng của giai đoạn tương ứng đăng ký (R-SKL-05); producer cho `fb-browser-results`; `publishResult<T>(queue, result: BrowserJobResult<T>) -> Promise<void>` (R-SKL-28).
- `core/heartbeat`: `HeartbeatService` ghi nhịp sống vào Redis (R-SKL-18).
- `healthcheck.ts`: script cho healthcheck của Docker, thoát 0 khi khóa nhịp sống **của chính container** (`BROWSER_WORKER_HEARTBEAT_KEY_PREFIX` + hostname) còn, 1 khi không.
- `core/data-dir`: tạo thư mục con của `DATA_DIR` và kiểm tra thư mục profile lúc khởi động (R-SKL-20).

### `apps/web` (`@mio/web`)

- React + Vite, trang giữ chỗ hiển thị "Tiệm Nhà Mio" và nạp `docs/design/ui-tokens.css`. Script `predev` / `prebuild` chép file này vào `apps/web/src/styles/ui-tokens.css`; bản chép là file sinh ra, nằm trong `.gitignore`, nguồn duy nhất vẫn là `docs/design/ui-tokens.css`. Màn hình thật do `auth` và các tính năng sau làm.
- Dev: Vite proxy `/api` → `http://localhost:3000`.
- Build ra `apps/web/dist`, được chép vào image api để api phục vụ.

### Công cụ

- `tools/ops/container_stats.py`: đo RAM/CPU từng container (mục Trạng thái và thuật toán, R-SKL-24).
- `docker-bake.hcl`: build image `api`, `browser-worker` cho `linux/amd64` và `linux/arm64` (R-SKL-21).

## Thay đổi DB

- Thêm bảng `app_settings`. Chi tiết: `docs/design/db-schema.md` mục `app_settings`.
- `created_at`, `updated_at` do app đặt bằng `CLOCK.now()` khi ghi (`db-schema.md` mục Quy ước chung).
- Cấu hình PostgreSQL: múi giờ phiên `UTC` (R-SKL-23).

## API

- `GET /api/v1/health` – kiểm tra API, DB, Redis còn hoạt động. Chi tiết: `docs/design/api/system.md`.
- Quy ước chung cho mọi endpoint (định dạng lỗi, mã lỗi dùng chung `NOT_FOUND`, `VALIDATION_ERROR`, `INVALID_JSON`, `PAYLOAD_TOO_LARGE`, `INVALID_STORED_SETTING`, `INTERNAL_ERROR`): R-SKL-11, R-SKL-12, R-SKL-15, R-SKL-16; mô tả ở đầu `docs/design/api/system.md`.
- Endpoint cài đặt: mỗi tính năng tự khai báo `GET` / `PUT /api/v1/settings/<khóa>` (ADR 0010). Khung không có endpoint cài đặt.

## Màn hình và quy tắc kiểm tra dữ liệu

Không áp dụng cho màn hình: tính năng không có màn hình (trang giữ chỗ của web không có trường nhập). Không có trường nhập từ người dùng; dữ liệu vào là biến môi trường và giá trị cài đặt do tính năng khác gửi xuống `SettingsService`.

### Biến môi trường

Chỉ chứa khóa bí mật, đường dẫn và địa chỉ kết nối. Mọi cấu hình nghiệp vụ nằm trong `app_settings`.

| Biến | Dùng ở | Bắt buộc | Yêu cầu (in nguyên văn trong thông báo R-SKL-02) | Ví dụ trong `.env.example` |
|---|---|---|---|---|
| `DATABASE_URL` | api | có | phải là URL postgres:// hoặc postgresql:// | `postgres://mio:<mật khẩu>@postgres:5432/mio` |
| `REDIS_URL` | api, browser-worker | có | phải là URL redis:// | `redis://redis:6379` |
| `DATA_DIR` | api, browser-worker | có | phải là đường dẫn tuyệt đối | `/data` |
| `BROWSER_PROFILE_DIR` | browser-worker | có | phải là đường dẫn tuyệt đối | `/browser-profile` |
| `PUBLIC_URL` | api | có | phải là URL http:// hoặc https://, không có / cuối | `http://localhost:3000` |

Biến của Docker Compose (file `.env` ở gốc, không commit; có `.env.example`). `compose.yml` dùng cú pháp `${TÊN:?Thiếu TÊN trong .env}` cho cả ba biến, nên thiếu hoặc rỗng thì `docker compose` dừng ngay với thông báo "Thiếu <TÊN> trong .env", không tạo hay khởi động lại container nào.

| Biến | Bắt buộc | Ý nghĩa |
|---|---|---|
| `POSTGRES_PASSWORD` | có | mật khẩu DB, ghép vào `DATABASE_URL` của api |
| `MIO_DATA_DIR` | có | thư mục trên máy chủ gắn vào `/data` của api và browser-worker (ảnh, debug dump) |
| `MIO_PUBLIC_URL` | có | truyền vào `PUBLIC_URL` của api |

Profile trình duyệt không nằm trong `MIO_DATA_DIR` mà trong named volume `mio-browser-profile`, gắn vào `/browser-profile` của browser-worker (R-SKL-20, ADR 0013).

### Quy tắc

- R-SKL-01: thiếu biến môi trường bắt buộc → tiến trình ghi log lỗi và thoát mã 1, thông báo "Thiếu biến môi trường: <TÊN_1>, <TÊN_2>" (liệt kê hết biến thiếu trong một dòng). Biến có giá trị rỗng hoặc chỉ có khoảng trắng coi như thiếu.
- R-SKL-02: biến sai định dạng → thoát mã 1, thông báo "Biến môi trường không hợp lệ: <TÊN> (<yêu cầu>)", `<yêu cầu>` lấy nguyên văn cột "Yêu cầu" của bảng Biến môi trường, ví dụ "Biến môi trường không hợp lệ: REDIS_URL (phải là URL redis://)". Nhiều biến sai thì mỗi biến một dòng log. Giá trị của biến không được in ra log.
- R-SKL-03: chỉ api chạy migration, lúc khởi động, trước khi mở cổng HTTP. Migration lỗi → log lỗi và thoát mã 1, không mở cổng. api chạy một bản duy nhất; nếu sau này chạy nhiều bản thì phải bọc migration bằng khóa `pg_advisory_lock`.
- R-SKL-04: browser-worker chỉ kết nối Redis; không kết nối PostgreSQL, không mở cổng HTTP, không gọi API. Dữ liệu vào nằm trong dữ liệu job; dữ liệu ra đi qua hàng đợi kết quả (R-SKL-28, ADR 0011).
- R-SKL-05: `fb-browser` có global concurrency = 1 (BullMQ `setGlobalConcurrency(1)`), nên dù chạy nhiều tiến trình browser-worker cũng chỉ có một job chạy cùng lúc. Giai đoạn 0 chỉ đăng ký `fb-browser` và `fb-browser-results`; các hàng đợi khác chỉ khai báo tên trong `QUEUE_NAMES`, tính năng của giai đoạn tương ứng tự đăng ký. `fb-inbox` tách riêng hay gộp vào `fb-browser` (khi inbox dùng chung tài khoản vận hành, inbox ưu tiên cao nhất) quyết ở giai đoạn 3 theo 04-technical.md mục 4.3; nếu tách thì cũng global concurrency 1 và dùng profile riêng. Hàng đợi `render` dùng Chromium riêng, không dùng thư mục profile Facebook.
- R-SKL-06: tên hàng đợi chỉ lấy từ `QUEUE_NAMES`; không viết chuỗi tên hàng đợi trực tiếp trong code.
- R-SKL-07: tùy chọn mặc định của mọi hàng đợi, để job không bao giờ tự chạy lại (tránh comment hai lần):
  - job: `attempts: 1`, `removeOnComplete: { count: 1000 }`, `removeOnFail: { count: 5000 }`; tính năng nào cần thử lại phải tự khai báo và chứng minh thao tác an toàn khi chạy lại;
  - mọi Worker (browser-worker và api): `maxStalledCount: 0`, nên job bị stalled (worker chết, mất lock) chuyển thẳng `failed`, không quay về `wait`. `attempts` không áp dụng cho stalled; mặc định của BullMQ (`maxStalledCount: 1`) sẽ chạy lại job stalled một lần;
  - `lockDuration` để mặc định (30 giây, worker tự gia hạn); processor không được chặn event loop quá vài giây, để không bị stalled giả trong lúc vẫn đang chạy.
- R-SKL-08: `SettingsService.get` đọc DB ở mỗi lần gọi, không cache. Giá trị mới có hiệu lực từ lần đọc kế tiếp, không cần khởi động lại.
- R-SKL-09: khóa chưa có bản ghi trong DB → trả `defaultValue` của khóa, không ghi vào DB.
- R-SKL-10: `get` / `set` với khóa không có trong `SETTINGS` → ném `UnknownSettingKeyError`, thông báo "Khóa cài đặt không tồn tại: <khóa>". Đây là lỗi lập trình: khóa có kiểu `SettingKey` nên typecheck chặn trước; nếu vẫn xảy ra lúc chạy thì API trả 500 `INTERNAL_ERROR` (R-SKL-16). Không có mã lỗi riêng: mỗi khóa có route cố định (ADR 0010), khóa lạ trên URL rơi vào 404 `NOT_FOUND` (R-SKL-15).
- R-SKL-11: `set` với giá trị không qua zod schema của khóa → ném `SettingValidationError` kèm `fields`, không ghi gì vào DB; endpoint trả 400 `VALIDATION_ERROR`, `message` "Dữ liệu cài đặt không hợp lệ". Quy ước chung cho lỗi theo trường của cài đặt (dùng cả ở R-SKL-12):
  - khóa của `fields` là đường dẫn đầy đủ trong mục: thuộc tính nối bằng `.`, chỉ số mảng trong `[]`, ví dụ `goldenHours[1].end`; lỗi ở gốc (giá trị không phải object) dùng khóa `_root`;
  - giá trị là thông báo tiếng Việt do schema của khóa định nghĩa; một trường có nhiều lỗi thì lấy lỗi đầu tiên zod trả về;
  - ghi thành công thì lưu **kết quả parse** của schema (không phải giá trị gửi lên), thay cả mục (upsert theo `key`), cập nhật `updated_at`;
  - trường không có trong schema bị bỏ khi parse (mặc định của zod), ở cả `set` và `get`; bỏ một trường khỏi schema không làm giá trị đang lưu thành lỗi.
- R-SKL-12: giá trị trong DB không qua schema hiện tại (ví dụ schema đổi mà thiếu migration dữ liệu) → `get` ném `InvalidStoredSettingError`, không lặng lẽ dùng mặc định. Lỗi phải nêu cụ thể nguyên nhân, liệt kê **mọi** trường lỗi:
  - thông báo: "Cài đặt <khóa> đang lưu không hợp lệ: <trường 1>: <lý do 1> (đang lưu: <giá trị 1>); <trường 2>: …", ví dụ "Cài đặt crawl-schedule đang lưu không hợp lệ: maxScrolls: phải từ 1 đến 20 (đang lưu: 25)";
  - `<trường>`, `<lý do>` theo quy ước của R-SKL-11; trường bị thiếu ghi "(đang lưu: không có)";
  - `<giá trị>` in bằng `JSON.stringify` (chuỗi có ngoặc kép, ví dụ `"abc"`; số, `true`, `null` in như JSON); chuỗi JSON dài hơn 100 ký tự thì lấy 100 ký tự đầu và thêm "…";
  - log: mức `error`, gồm thông báo trên, `key`, danh sách `{ path, reason, storedValue }`;
  - endpoint `GET` / `PUT /api/v1/settings/<khóa>` của tính năng trả 409 `INVALID_STORED_SETTING` với `message` là thông báo trên và `fields` là `{ <trường>: <lý do> }`; `PUT` một giá trị hợp lệ thì ghi đè và hết lỗi;
  - job đọc cài đặt bị lỗi thì thất bại với đúng thông báo trên làm lý do (tính năng sở hữu job quyết định có tự dừng và báo khẩn hay không).
- R-SKL-13: `GET /api/v1/health` không cần đăng nhập. Kiểm DB (`select 1`) và Redis (`PING`) **song song**, dùng kết nối riêng cho health (không dùng chung kết nối của BullMQ), mỗi kiểm tra timeout 2 giây. Cả hai trả lời trong 2 giây → 200 `status: ok`; một trong hai lỗi hoặc quá 2 giây → 503 `status: error`, trường tương ứng `down`. Response không chứa thông báo lỗi chi tiết, phiên bản hay đường dẫn.
- R-SKL-14: api phục vụ web: `GET` đường dẫn không bắt đầu bằng `/api/` mà có file trong `apps/web/dist` → trả file; không có file → trả `index.html` (định tuyến phía SPA). Không bao giờ trả file nằm ngoài `apps/web/dist` (đường dẫn có `..` hay dạng mã hóa `%2e%2e`).
- R-SKL-15: mọi lỗi API trả thân `{ "code": "<MÃ_LỖI>", "message": "<tiếng Việt>", "fields"?: { "<trường>": "<thông báo>" } }`. Mã lỗi dùng chung:
  - 404 `NOT_FOUND`: đường dẫn `/api/...` không có route, "Không tìm thấy địa chỉ yêu cầu";
  - 400 `INVALID_JSON`: thân request không phải JSON hợp lệ, "Dữ liệu gửi lên không đúng định dạng JSON";
  - 413 `PAYLOAD_TOO_LARGE`: thân request lớn hơn 1 MB, "Dữ liệu gửi lên quá lớn";
  - 400 `VALIDATION_ERROR`: dữ liệu sai quy tắc, có `fields` (quy ước đường dẫn trường theo R-SKL-11);
  - 409 `INVALID_STORED_SETTING`: R-SKL-12;
  - 500 `INTERNAL_ERROR`: R-SKL-16.
- R-SKL-16: lỗi không lường trước → 500 `INTERNAL_ERROR`, thông báo "Lỗi hệ thống, vui lòng thử lại sau"; không trả stack trace hay nội dung lỗi gốc; ghi log lỗi đầy đủ kèm `requestId`.
- R-SKL-17: log là JSON một dòng ra stdout, gồm `time`, `level`, `app`, `msg`, và `requestId` / `jobId` khi có. Che (`[REDACTED]`) bằng `redact` của pino theo danh sách đường dẫn cố định (pino không có wildcard đệ quy):
  - header: `req.headers.authorization`, `req.headers.cookie`, `res.headers["set-cookie"]`;
  - khóa `password`, `token`, `secret`, `cookie`, `authorization` ở độ sâu 1 đến 3 (`x`, `*.x`, `*.*.x`, `*.*.*.x`);
  - loại bí mật mới thì bổ sung danh sách (ADR 0012). Không ghi nội dung bài, tin nhắn, tên người hay giá trị biến môi trường.
- R-SKL-18: mỗi tiến trình browser-worker ghi khóa riêng `mio:heartbeat:browser-worker:<hostname>` (`<hostname>` là hostname của container; giá trị: thời điểm ISO lấy từ `CLOCK`) mỗi 15 giây, TTL 60 giây. Healthcheck Docker của browser-worker chỉ đạt khi khóa của chính container còn tồn tại, nên một worker treo không bị worker khác che. Phát hiện "không còn worker nào sống" (không còn khóa nào) và báo cho chủ tiệm thuộc `emergency-stop`.
- R-SKL-19: `compose.yml` chỉ publish cổng api, gắn vào `127.0.0.1:3000`. PostgreSQL và Redis không publish cổng; khi dev, `compose.dev.yml` publish chúng lên `127.0.0.1` (5432, 6379).
- R-SKL-20: thư mục dữ liệu và quyền:
  - api và browser-worker chạy bằng cùng `uid:gid` `1000:1000` (không phải root), nên file một bên tạo thì bên kia đọc, ghi, xóa được;
  - lúc khởi động, app tạo các thư mục con của `DATA_DIR` nếu chưa có: `images/`, `debug-dumps/` (cả api và browser-worker);
  - profile trình duyệt nằm ở `BROWSER_PROFILE_DIR`, là named volume `mio-browser-profile` (không phải thư mục của máy chủ), quyền `700`. Dockerfile của browser-worker tạo sẵn `/browser-profile` thuộc `1000:1000` quyền `700` để volume mới nhận đúng chủ; lúc khởi động worker đặt lại quyền `700` (ADR 0013);
  - không ghi được vào `DATA_DIR` hoặc `BROWSER_PROFILE_DIR` → thoát mã 1, thông báo "Không ghi được vào thư mục dữ liệu: <đường dẫn>";
  - trên máy chủ Linux, thư mục `MIO_DATA_DIR` phải thuộc `1000:1000` (`chown -R 1000:1000 <MIO_DATA_DIR>` trước lần chạy đầu và sau khi khôi phục từ bản sao lưu; ghi trong mục "Triển khai lên máy chủ" của roadmap).
- R-SKL-21: image `api` và `browser-worker` build được cho `linux/amd64` và `linux/arm64` bằng `docker buildx bake`; chỉ dùng base image đa kiến trúc; không có giá trị phụ thuộc máy trong code, Dockerfile hay `compose.yml` (ADR 0009).
- R-SKL-22: nhận `SIGTERM` → ngừng nhận job mới, chờ job đang chạy xong trong thời gian ân hạn (mục Tham số), đóng kết nối rồi thoát mã 0. Dockerfile chạy Node trực tiếp dạng exec (`CMD ["node", "dist/main.js"]`, không qua `pnpm` hay `sh`) để Node là PID 1 và nhận được tín hiệu. Hết thời gian ân hạn thì Docker dừng cứng; job dở dang bị BullMQ đánh dấu stalled, chuyển `failed` và **không** chạy lại nhờ `maxStalledCount: 0` (R-SKL-07), rồi xử lý theo R-SKL-29.
- R-SKL-23: container đặt `TZ=UTC`; phiên PostgreSQL dùng múi giờ `UTC`. Logic nghiệp vụ lấy giờ từ `CLOCK` và đổi múi giờ bằng `APP_TIME_ZONE` (ADR 0007); lint chặn `Date.now()` / `new Date()` không tham số ngoài `system-clock.ts`.
- R-SKL-24: `tools/ops/container_stats.py` đo CPU % và RAM của từng container **thuộc project Compose của app** (nhãn `com.docker.compose.project`; bỏ qua Testcontainers và container khác) theo chu kỳ, ghi CSV và in bảng tổng hợp trung bình / lớn nhất cho mỗi container. Tham số và thông báo lỗi ở mục Đo RAM/CPU từng container. Docker không chạy → thoát mã 1, thông báo "Không kết nối được Docker. Bật Docker Desktop rồi chạy lại."
- R-SKL-25: `pnpm test:int` khi không kết nối được Docker → fail (không skip), thông báo "Không kết nối được Docker. Bật Docker Desktop rồi chạy lại."; Testcontainers dùng đúng image PostgreSQL và Redis như `compose.yml` (lấy tag từ một hằng chung, không lặp chuỗi).
- R-SKL-26: Docker giới hạn log mỗi container: driver `json-file`, `max-size: 10m`, `max-file: 5`.
- R-SKL-27: Redis bật AOF (`appendonly yes`) và `maxmemory-policy noeviction` (BullMQ yêu cầu), để job không mất khi khởi động lại.
- R-SKL-28: browser-worker trả kết quả bằng cách thêm job vào hàng đợi kết quả (`fb-browser` → `fb-browser-results`; `fb-inbox` → `fb-inbox-results` khi giai đoạn 3 thêm), không dùng giá trị trả về của job hay sự kiện `completed`. Dữ liệu job kết quả theo `BrowserJobResult<T>`:
  - `sourceJobId`: id job gốc; `sourceJobName`: tên job gốc;
  - `outcome`: `ok` hoặc `failed`;
  - `data`: kết quả (kiểu `T` do tính năng định nghĩa), chỉ có khi `ok`;
  - `error`: `{ type, message, dumpPath? }`, chỉ có khi `failed`; `type` là tên lớp lỗi đã phân loại (`SessionExpiredError`, `CheckpointError`, `GroupInaccessibleError`…), lỗi chưa phân loại dùng `UnexpectedError`; `dumpPath` là đường dẫn tương đối trong `DATA_DIR` của ảnh màn hình và HTML lúc lỗi.
  - Processor bắt mọi lỗi và luôn gửi job kết quả (kể cả `failed`), sau đó kết thúc job gốc bình thường (`completed`). Job gốc chỉ `failed` khi không gửi được kết quả (worker chết, stalled, không ghi được vào Redis).
  - Job kết quả dùng `jobId` = `<sourceJobId>-result`, nên gửi lại cùng một kết quả không tạo job trùng.
  - api kiểm tra dữ liệu job kết quả bằng zod; sai cấu trúc → job kết quả thất bại, log lỗi kèm `sourceJobId` (không log dữ liệu job).
- R-SKL-29: job gốc `failed` (không có job kết quả, R-SKL-28) → api chuyển cho tính năng sở hữu job xử lý như một kết quả `failed` với `error.type = 'WorkerCrashedError'`. Job gốc không tự chạy lại (R-SKL-07).
  - Cách phát hiện: nghe sự kiện `failed` của hàng đợi gốc, **và** đối soát lúc api khởi động và mỗi 5 phút: job `failed` của hàng đợi gốc chưa được xử lý → xử lý như trên. Đối soát bù cho sự kiện bị lỡ khi api tắt.
  - Xử lý theo `sourceJobId`, idempotent: một job gốc chỉ được ghi nhận một lần cho mỗi loại tín hiệu. Kết quả từ hàng đợi kết quả luôn thắng `WorkerCrashedError`, kể cả khi tới sau (stalled giả: worker vẫn chạy xong và gửi kết quả).
  - `WorkerCrashedError` nghĩa là "không rõ đã làm tới đâu", không phải "chưa làm". Tính năng có thao tác ghi lên Facebook (comment, đăng bài, trả lời inbox) không được coi là chưa làm để tự làm lại.
  - Job gốc nằm ở `active` khi không còn browser-worker nào sống (kiểm tra stalled chỉ do Worker chạy): không tự xử lý ở khung; `emergency-stop` phát hiện qua khóa nhịp sống (R-SKL-18).
- R-SKL-30: kết nối PostgreSQL và Redis:
  - lúc khởi động: không kết nối được thì thử lại mỗi 2 giây, tối đa 30 giây; vẫn không được thì thoát mã 1, thông báo "Không kết nối được PostgreSQL" hoặc "Không kết nối được Redis";
  - đang chạy: mất kết nối không làm sập tiến trình; bắt sự kiện lỗi của pool `pg` và ioredis, ghi log `warn`; ioredis thử lại không giới hạn (`maxRetriesPerRequest: null`, BullMQ yêu cầu); request cần DB trong lúc mất kết nối → 500 `INTERNAL_ERROR` (R-SKL-16); `/health` trả 503 (R-SKL-13); có kết nối lại thì chạy tiếp, không khởi động lại.
- R-SKL-31: healthcheck và khởi động lại trong Compose:
  - healthcheck: `postgres` `pg_isready -U mio -d mio`; `redis` `redis-cli ping`; `api` `node dist/healthcheck.js`; `browser-worker` `node dist/healthcheck.js`. Tham số ở mục Tham số cài đặt;
  - mọi dịch vụ `restart: unless-stopped`. Docker chỉ khởi động lại container khi tiến trình **thoát**; container `unhealthy` mà tiến trình còn chạy (treo) không được khởi động lại. Tình trạng treo của browser-worker do `emergency-stop` phát hiện qua khóa nhịp sống (R-SKL-18).

## Job và hàng đợi

Khung chỉ tạo hàng đợi và worker rỗng của giai đoạn 0; processor và job cụ thể do các tính năng sau thêm.

- `QUEUE_NAMES` và nơi chạy (chỉ hai hàng đợi đầu được đăng ký ở giai đoạn 0, R-SKL-05):
  - `fb-browser`: browser-worker, global concurrency 1 (quét group, comment, đăng group).
  - `fb-browser-results`: api, concurrency 1 (nhận kết quả của `fb-browser`, R-SKL-28).
  - `fb-inbox`: browser-worker (giai đoạn 3; tách hay gộp vào `fb-browser` quyết ở giai đoạn 3).
  - `fb-inbox-results`: api (giai đoạn 3, nếu `fb-inbox` tách riêng).
  - `render`: browser-worker, concurrency 1 (giai đoạn 4).
  - `ai-text`, `ai-image`, `messenger`, `page-publish`: api (giai đoạn 1 trở đi).
- Chiều dữ liệu: api thêm job vào `fb-browser`, kèm mọi cài đặt worker cần → browser-worker xử lý → browser-worker thêm job vào hàng đợi kết quả → api ghi DB. Kết quả nằm trong Redis tới khi api xử lý, nên api khởi động lại không làm mất kết quả. Job gốc mất kết quả: R-SKL-29.
- Tùy chọn mặc định: R-SKL-07. Ưu tiên, retry, timeout riêng: tính năng khai báo khi thêm job.
- Nhịp sống browser-worker: không phải job BullMQ, là `setInterval` ghi Redis (R-SKL-18).

## Trạng thái và thuật toán

### Khởi động

- api: đọc và kiểm tra env (R-SKL-01, 02) → kiểm tra/tạo thư mục dữ liệu (R-SKL-20) → kết nối DB (R-SKL-30) → chạy migration (R-SKL-03) → kết nối Redis, đăng ký hàng đợi, đối soát job gốc mất kết quả (R-SKL-29) → mở cổng 3000.
- browser-worker: đọc env → tạo thư mục dữ liệu, kiểm tra thư mục profile → kết nối Redis (R-SKL-30) → đăng ký worker → bắt đầu ghi nhịp sống.
- Thứ tự trong Compose: `postgres`, `redis` healthy → `api` healthy (qua `/api/v1/health`) → `browser-worker`. Healthcheck và khởi động lại: R-SKL-31.

### Đọc / ghi cài đặt

- `get(key)`: tìm định nghĩa trong `SETTINGS` (không có → `UnknownSettingKeyError`, R-SKL-10) → `SELECT value FROM app_settings WHERE key = $1` → không có dòng: trả mặc định (R-SKL-09) → có: `schema.safeParse(value)`, lỗi thì R-SKL-12, đạt thì trả giá trị đã parse.
- `set(key, value)`: tìm định nghĩa → `schema.safeParse(value)` (lỗi → R-SKL-11) → `INSERT (key, value, created_at, updated_at) VALUES ($key, <giá trị đã parse>, <CLOCK.now()>, <CLOCK.now()>) ON CONFLICT (key) DO UPDATE SET value = …, updated_at = <CLOCK.now()>` → trả giá trị đã lưu.
- Ghi đồng thời: ghi sau thắng (cả mục bị thay). Chấp nhận được vì chỉ Quản lý sửa cài đặt.

### Đo RAM/CPU từng container

- Lệnh: `py tools/ops/container_stats.py record [--interval <giây>] [--out <file.csv>]` và `py tools/ops/container_stats.py summary <file.csv>`.
- Tham số của `record`:
  - `--interval`: số nguyên từ 5 đến 3600, mặc định 60; sai (ngoài khoảng, không phải số nguyên) → thoát mã 2, "--interval phải là số nguyên từ 5 đến 3600";
  - `--out`: mặc định `.local/metrics/<YYYY-MM-DD-HHmm>.csv` theo giờ `Asia/Ho_Chi_Minh` lúc bắt đầu; thư mục cha chưa có thì tạo.
- `record`: lấy mẫu ngay khi bắt đầu, sau đó mỗi `--interval` giây; mỗi lần gọi `docker stats --no-stream --format "{{json .}}"`, chỉ giữ container thuộc project Compose của app (R-SKL-24), ghi một dòng CSV cho mỗi container: `time` (ISO UTC), `container` (tên container, ví dụ `mio-api-1`), `cpu_percent` (theo `docker stats`, 100% = 1 lõi CPU nên có thể vượt 100), `mem_bytes`, `mem_limit_bytes`. Chạy tới khi bấm Ctrl+C (thoát gọn, mã 0); ghi nối tiếp nếu file đã có, để gộp nhiều lần chạy thành tổng 24 giờ.
- `summary`: in cho mỗi container: số mẫu, CPU trung bình, CPU lớn nhất, RAM trung bình, RAM lớn nhất (MiB). File không tồn tại → thoát mã 1, "Không tìm thấy file: <đường dẫn>". Kết quả dùng cho báo cáo nghiệm thu giai đoạn 0.
- CSV nằm trong `.local/` (không commit).

### Build đa kiến trúc

- `docker buildx bake` với `docker-bake.hcl`: target `api`, `browser-worker`, `platforms = ["linux/amd64", "linux/arm64"]`.
- Lệnh `pnpm docker:build` (amd64, nạp vào Docker local) và `pnpm docker:build:multiarch` (cả hai kiến trúc, kiểm tra build được; arm64 qua QEMU).
- Kiểm tra arm64: build thành công, và chạy được `node --version` trong image arm64 qua QEMU (api ra Node 26, browser-worker ra phiên bản Node của image Playwright). Chạy Chromium trên arm64 thật kiểm chứng khi triển khai lên máy chủ (04 mục 2).

## Tích hợp bên ngoài

Không áp dụng: khung không gọi Facebook, Gemini hay Messenger. Chỉ tích hợp với hạ tầng nội bộ (PostgreSQL, Redis, Docker).

## Xử lý lỗi, log, bảo mật, phân quyền

- Lỗi:
  - thiếu/sai env, không ghi được thư mục dữ liệu, migration lỗi, không kết nối được DB/Redis lúc khởi động → thoát mã 1 (R-SKL-01, 02, 03, 20, 30); Compose khởi động lại theo `restart: unless-stopped`, log ghi rõ nguyên nhân;
  - mất kết nối Redis/DB khi đang chạy → R-SKL-30; health trả 503 trong lúc mất (R-SKL-13);
  - tiến trình browser-worker thoát → Compose khởi động lại; tiến trình treo → `unhealthy`, Docker **không** tự khởi động lại (R-SKL-31); việc phát hiện và báo cho chủ tiệm thuộc `emergency-stop`;
  - job gốc mất kết quả → R-SKL-29.
- Log: R-SKL-17, R-SKL-26.
- Bảo mật:
  - khóa bí mật chỉ ở `.env` (không commit, có `.env.example`) và biến môi trường container;
  - cổng chỉ mở trên `127.0.0.1` (R-SKL-19); HTTPS thêm khi triển khai lên máy chủ (ADR 0009);
  - user không phải root (`1000:1000`); profile trình duyệt trong named volume riêng, quyền `700` (R-SKL-20, ADR 0013);
  - file tĩnh không thoát ra ngoài `apps/web/dist` (R-SKL-14);
  - `.gitignore` có `.env`, `.local/`, `node_modules/`, `dist/`, `apps/web/src/styles/ui-tokens.css`.
- Phân quyền: không áp dụng ở khung; endpoint duy nhất (`/health`) công khai (R-SKL-13). Phân quyền theo vai trò thuộc `auth`.

## Tham số cài đặt

Khung không thêm khóa cài đặt nghiệp vụ. Các hằng kỹ thuật (đặt trong code, không chỉnh trên web):

- Chu kỳ ghi nhịp sống browser-worker: 15 giây; TTL 60 giây. Nguồn: quyết định mới, người dùng chỉnh TTL ngày 2026-10-29.
- Thời gian chờ mỗi kiểm tra trong `/health`: 2 giây, hai kiểm tra chạy song song. Nguồn: quyết định mới.
- Healthcheck Compose (R-SKL-31): `interval` 10 giây, `timeout` 5 giây, `retries` 3; `start_period` 60 giây cho api (chạy migration), 30 giây cho các dịch vụ khác. Nguồn: quyết định mới (review RV-04).
- Kết nối lúc khởi động: thử lại mỗi 2 giây, tối đa 30 giây (R-SKL-30). Nguồn: quyết định mới (review RV-12).
- Đối soát job gốc mất kết quả: lúc api khởi động và mỗi 5 phút (R-SKL-29). Nguồn: quyết định mới (review RV-03).
- Giới hạn thân request API: 1 MB (R-SKL-15). Nguồn: quyết định mới (review RV-08).
- Thời gian ân hạn khi dừng (`stop_grace_period`): api 30 giây, browser-worker 120 giây. Nguồn: quyết định mới; `group-crawl-job` xem lại khi chốt độ dài một job.
- Giữ job: hoàn thành 1000, lỗi 5000; `maxStalledCount` 0 (R-SKL-07). Nguồn: quyết định mới.
- Log Docker: 10 MB × 5 file mỗi container (R-SKL-26). Nguồn: quyết định mới.
- Chu kỳ đo RAM/CPU: mặc định 60 giây, khoảng 5–3600 giây, đổi bằng `--interval`. Nguồn: quyết định mới.
- Phiên bản hạ tầng (chốt 2026-10-29, câu hỏi mở 2), mọi image đa kiến trúc:
  - Node.js 26 cho api (image `node:26-bookworm-slim`);
  - PostgreSQL 18 (`postgres:18-alpine`);
  - Redis 8 (`redis:8-alpine`);
  - browser-worker: `mcr.microsoft.com/playwright:v1.63.0-noble`, khớp phiên bản `playwright` trong `package.json`; dùng Node đi kèm image (ADR 0014). Phiên bản Node cụ thể ghi vào `plan.md` lúc implement; `@mio/shared` và `apps/browser-worker` chỉ dùng tính năng có trên phiên bản đó;
  - tag không tồn tại lúc implement → lấy bản vá mới nhất cùng dòng, ghi lại trong `plan.md` của task. Tag PostgreSQL và Redis khai báo một chỗ, dùng chung cho `compose.yml` và Testcontainers (R-SKL-25).

## Câu hỏi mở

- [x] 1. browser-worker chỉ kết nối Redis, không kết nối PostgreSQL? — đã chốt 2026-10-29: chỉ Redis (ADR 0011); kết quả trả qua hàng đợi kết quả `fb-browser-results` / `fb-inbox-results` (R-SKL-28, R-SKL-29).
- [x] 2. Phiên bản hạ tầng? — đã chốt 2026-10-29: Node.js 26, PostgreSQL 18, Redis 8, Playwright 1.63 (mục Tham số cài đặt). Bổ sung 2026-10-31: browser-worker dùng Node đi kèm image Playwright (ADR 0014).
- [x] 3. Giá trị cài đặt trong DB không còn hợp lệ thì làm gì? — đã chốt 2026-10-29: báo lỗi, không dùng mặc định, thông báo nêu cụ thể từng trường lỗi, lý do và giá trị đang lưu (R-SKL-12). Đổi schema cài đặt phải kèm migration dữ liệu.

## Lịch sử thay đổi

- 2026-10-29: tạo mới
- 2026-10-29: chốt câu hỏi 3; R-SKL-12 ghi rõ nội dung lỗi, mã `INVALID_STORED_SETTING` (409)
- 2026-10-29: chốt câu hỏi 1, 2; thêm hàng đợi kết quả `fb-browser-results`, `fb-inbox-results` (R-SKL-28, R-SKL-29); chốt phiên bản hạ tầng
- 2026-10-29: đổi TTL nhịp sống browser-worker 45 → 60 giây (R-SKL-18); duyệt thiết kế
- 2026-10-31: sửa theo `reviews/app-skeleton-review.md`:
  - R-SKL-07, R-SKL-22: `maxStalledCount: 0`, job stalled không chạy lại (RV-01);
  - R-SKL-28, R-SKL-29: processor luôn gửi kết quả, `UnexpectedError`, xử lý idempotent, kết quả thật thắng `WorkerCrashedError`, đối soát lúc khởi động và mỗi 5 phút (RV-02, RV-03);
  - R-SKL-18, thêm R-SKL-31: khóa nhịp sống theo container, healthcheck Compose, container treo không tự khởi động lại (RV-04);
  - R-SKL-20, thêm biến `BROWSER_PROFILE_DIR`: cùng uid `1000:1000`, profile trong named volume `mio-browser-profile` (RV-05, RV-06; ADR 0013);
  - Tham số: browser-worker dùng Node của image Playwright (RV-07; ADR 0014);
  - R-SKL-10, R-SKL-15: bỏ `SETTING_NOT_FOUND`, thêm mã chung `INVALID_JSON`, `PAYLOAD_TOO_LARGE`, giới hạn thân 1 MB (RV-08);
  - R-SKL-01, R-SKL-02, bảng biến: thông báo nguyên văn từng biến, biến rỗng coi như thiếu (RV-09);
  - R-SKL-11, R-SKL-12: lưu kết quả parse, bỏ trường lạ, quy ước đường dẫn trường, `_root`, in giá trị bằng `JSON.stringify` (RV-10);
  - Thay đổi DB, Đọc / ghi cài đặt: `created_at`, `updated_at` lấy từ `CLOCK` (RV-11);
  - R-SKL-13, thêm R-SKL-30: kết nối lúc khởi động và khi đang chạy, health kiểm song song (RV-12);
  - R-SKL-24, mục Đo RAM/CPU: lọc theo project Compose, khoảng `--interval`, mặc định `--out`, lỗi `summary` (RV-13);
  - R-SKL-05, mục Job và hàng đợi: giai đoạn 0 chỉ đăng ký `fb-browser`, `fb-browser-results` (RV-15);
  - R-SKL-17: danh sách đường dẫn che cố định (RV-16);
  - bảng biến Compose: cú pháp `${TÊN:?…}` (RV-17);
  - R-SKL-03, R-SKL-22, mục `apps/web`, `core/db`: chi tiết implement (RV-18);
  - R-SKL-14: không trả file ngoài `apps/web/dist` (RV-19).
- 2026-10-31: duyệt thiết kế sau review
