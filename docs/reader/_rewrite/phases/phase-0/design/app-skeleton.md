<!-- src-section: 0b0fa0b228 160c2e44ac64 -->
# Thiết kế chi tiết – Khung ứng dụng (`app-skeleton`, `SKL`)

- **Giai đoạn:** 0.
- **Trạng thái:** đã duyệt ngày 2026-10-31.
- **Tài liệu khái quát làm nền:**
  - 04-technical.md mục 1, 2, 3, 7;
  - 05-roadmap.md giai đoạn 0;
  - 03-data-model.md mục 1 "Cài đặt";
  - ADR 0001, 0002, 0006, 0007, 0009, 0010, 0011, 0012, 0013, 0014;
  - `CLAUDE.md` mục Quy ước.

<!-- src-section: 0100e30d6f 4db8f79cefb9 -->
## Tóm tắt

- Tính năng dựng khung chạy được cho mọi tính năng sau. Khung gồm monorepo pnpm, NestJS API, worker trình duyệt tách riêng, PostgreSQL, Redis, BullMQ và web React tối thiểu.
- Docker Compose build được cho linux/amd64 và linux/arm64.
- Khung cung cấp các phần dùng chung: đọc biến môi trường, đồng hồ `Clock`, log, kết nối DB và hàng đợi, bảng cài đặt chung, kiểm tra sức khỏe, và cách đo RAM/CPU từng container.
- Người dùng trực tiếp là người vận hành (Hải). Chủ tiệm và thợ chưa thấy gì từ tính năng này.

<!-- src-section: d14dee88c8 d1162533c1f6 -->
## Module và interface

Hạ tầng dùng chung nằm trong `apps/<app>/src/core/`. Đây không phải module nghiệp vụ, nên không nằm trong `src/modules/`.

<!-- src-section: 122ef9e761 24fe0d6f44e4 -->
### `packages/shared` (`@mio/shared`)

**Tóm tắt.** Package dùng chung chứa đồng hồ, các hằng số, kiểu kết quả của job trình duyệt và cơ chế khai báo cài đặt.

**Chi tiết kỹ thuật**

- Đồng hồ:
  - `interface Clock { now(): Date }`, với token `CLOCK` (`Symbol('CLOCK')`).
  - `class SystemClock implements Clock` nằm trong `src/clock/system-clock.ts`. Đây là file duy nhất được gọi `new Date()`.
  - `class FakeClock implements Clock` nằm trong `src/testing/fake-clock.ts` và được xuất qua `@mio/shared/testing`. Lớp có `constructor(start: Date)`, `set(at: Date)` và `advance(ms: number)`.
- Hằng số:
  - `APP_TIME_ZONE = 'Asia/Ho_Chi_Minh'`;
  - `QUEUE_NAMES` (xem mục Job và hàng đợi);
  - `BROWSER_WORKER_HEARTBEAT_KEY_PREFIX = 'mio:heartbeat:browser-worker:'`. Khóa đầy đủ thêm hostname của container vào sau tiền tố này (R-SKL-18).
- Kết quả job trình duyệt: type `BrowserJobResult<T>` và zod schema tương ứng (R-SKL-28).
- Cài đặt:
  - `defineSetting<T>({ key: string, schema: ZodType<T>, defaultValue: T }) -> SettingDefinition<T>`.
  - `SETTINGS` là object gom mọi `SettingDefinition`. Mỗi tính năng thêm khóa của mình. Ở giai đoạn 0, khung chưa có khóa nào; khóa đầu tiên do `crawl-settings` thêm.
  - Phần cài đặt đặt trong shared để web dùng lại cùng zod schema khi kiểm tra form.

<!-- src-section: 1bf1840368 8dca445de21c -->
### `apps/api` (`@mio/api`)

**Tóm tắt.** API gồm các module hạ tầng trong `core/`, điểm vào chính, script healthcheck và điểm vào CLI.

**Chi tiết kỹ thuật**

- `core/config`: `loadEnv<S>(schema: S, source: NodeJS.ProcessEnv) -> z.infer<S>`. Khi lỗi, hàm ném `EnvValidationError` (R-SKL-01, R-SKL-02). Token là `ENV`.
- `core/clock`: `ClockModule` cung cấp `CLOCK` bằng `SystemClock`, phạm vi global.
- `core/logging`: `LoggingModule` dùng nestjs-pino (ADR 0012) và ghi log JSON ra stdout (R-SKL-17).
- `core/db`:
  - `DbModule` tạo Drizzle client từ `DATABASE_URL`, token `DB`;
  - `runMigrations(db) -> Promise<void>` chạy migration trong `apps/api/migrations/` (R-SKL-03);
  - kết nối được xử lý theo R-SKL-30;
  - schema Drizzle nằm ở `apps/api/src/db/schema/*.ts` (theo `CLAUDE.md`). `core/db` chỉ chứa module kết nối và `runMigrations`.
- `core/queue`: `QueueModule` tạo kết nối BullMQ từ `REDIS_URL`.
  - Module đăng ký hàng đợi của giai đoạn 0: producer `fb-browser` và worker `fb-browser-results`.
  - Module áp tùy chọn mặc định cho job và worker (R-SKL-06, R-SKL-07).
  - Module nghe sự kiện và đối soát job gốc mất kết quả (R-SKL-29).
- `core/settings`: `SettingsService` (R-SKL-08 … R-SKL-12):
  - `get<K extends SettingKey>(key: K) -> Promise<SettingValue<K>>`;
  - `set<K extends SettingKey>(key: K, value: unknown) -> Promise<SettingValue<K>>`;
  - lỗi: `UnknownSettingKeyError`, `SettingValidationError` (có `fields`), `InvalidStoredSettingError`.
- `core/health`: `HealthController` phục vụ `GET /api/v1/health` (R-SKL-13).
- `core/http`: `ApiExceptionFilter` chuẩn hóa mọi lỗi API (R-SKL-15, R-SKL-16). Thân request giới hạn 1 MB. Module này cũng phục vụ file tĩnh của web (R-SKL-14).
- `main.ts`: đọc env, chạy migration, rồi mở HTTP ở cổng 3000 với tiền tố `/api/v1` và bật shutdown hook.
- `healthcheck.ts`: script cho healthcheck của Docker. Script gọi `http://127.0.0.1:3000/api/v1/health` với timeout 4 giây. Script thoát 0 khi nhận 200 và thoát 1 khi nhận kết quả khác. Script này cần thiết vì image `node:*-slim` không có `curl` (R-SKL-31).
- `cli.ts`: điểm vào lệnh CLI. CLI dùng Nest application context và không mở HTTP.
  - Cách chạy: `node dist/cli.js <lệnh> [tham số]`.
  - Khung chỉ có bộ điều phối lệnh và lệnh `help`. Tính năng `auth` thêm lệnh tạo tài khoản.
  - Lệnh không tồn tại thì CLI in "Lệnh không tồn tại: <lệnh>. Chạy help để xem danh sách." và thoát mã 1.

<!-- src-section: 5562e6486c 41ff4c0bf27f -->
### `apps/browser-worker` (`@mio/browser-worker`)

**Tóm tắt.** browser-worker là ứng dụng NestJS standalone. Nó không mở cổng HTTP và chỉ kết nối Redis (ADR 0011, R-SKL-04).

**Chi tiết kỹ thuật**

- `core/config`, `core/clock`, `core/logging`: giống api.
- `core/queue`:
  - đăng ký worker cho `fb-browser`; processor do các tính năng sau thêm;
  - `fb-inbox` và `render` do tính năng của giai đoạn tương ứng đăng ký (R-SKL-05);
  - producer cho `fb-browser-results`;
  - `publishResult<T>(queue, result: BrowserJobResult<T>) -> Promise<void>` (R-SKL-28).
- `core/heartbeat`: `HeartbeatService` ghi nhịp sống vào Redis (R-SKL-18).
- `healthcheck.ts`: script cho healthcheck của Docker. Script thoát 0 khi khóa nhịp sống **của chính container** (`BROWSER_WORKER_HEARTBEAT_KEY_PREFIX` + hostname) còn tồn tại, và thoát 1 khi không còn.
- `core/data-dir`: lúc khởi động, module tạo thư mục con của `DATA_DIR` và kiểm tra thư mục profile (R-SKL-20).

<!-- src-section: 2a89c6e954 4dffd30360d4 -->
### `apps/web` (`@mio/web`)

**Tóm tắt.** Web ở giai đoạn này chỉ là trang giữ chỗ dựng bằng React + Vite. Màn hình thật do `auth` và các tính năng sau làm.

- Trang giữ chỗ hiển thị "Tiệm Nhà Mio" và nạp `docs/design/ui-tokens.css`.
- Script `predev` / `prebuild` chép file này vào `apps/web/src/styles/ui-tokens.css`. Bản chép là file sinh ra và nằm trong `.gitignore`. Nguồn duy nhất vẫn là `docs/design/ui-tokens.css`.
- Khi dev, Vite proxy chuyển `/api` tới `http://localhost:3000`.
- Web build ra `apps/web/dist`. Thư mục này được chép vào image api để api phục vụ.

<!-- src-section: 9f89aec869 f597aa4adb47 -->
### Công cụ

- `tools/ops/container_stats.py` đo RAM/CPU từng container (mục Trạng thái và thuật toán, R-SKL-24).
- `docker-bake.hcl` build image `api` và `browser-worker` cho `linux/amd64` và `linux/arm64` (R-SKL-21).

<!-- src-section: 51a2c0ad01 4d19ece484e5 -->
## Thay đổi DB

- Tính năng thêm bảng `app_settings`. Chi tiết ở `docs/design/db-schema.md`, mục `app_settings`.
- `created_at` và `updated_at` do app đặt bằng `CLOCK.now()` khi ghi (`db-schema.md` mục Quy ước chung).
- PostgreSQL được cấu hình dùng múi giờ phiên `UTC` (R-SKL-23).

<!-- src-section: c501d518d6 f439464c2ef4 -->
## API

- `GET /api/v1/health` kiểm tra API, DB và Redis còn hoạt động. Chi tiết ở `docs/design/api/system.md`.
- Quy ước chung cho mọi endpoint được mô tả ở đầu `docs/design/api/system.md`, theo R-SKL-11, R-SKL-12, R-SKL-15, R-SKL-16. Quy ước gồm định dạng lỗi và các mã lỗi dùng chung `NOT_FOUND`, `VALIDATION_ERROR`, `INVALID_JSON`, `PAYLOAD_TOO_LARGE`, `INVALID_STORED_SETTING`, `INTERNAL_ERROR`.
- Endpoint cài đặt: mỗi tính năng tự khai báo `GET` / `PUT /api/v1/settings/<khóa>` (ADR 0010). Khung không có endpoint cài đặt.

<!-- src-section: 730c79b0e4 c59494ec55c0 -->
## Màn hình và quy tắc kiểm tra dữ liệu

- Không áp dụng cho màn hình. Tính năng không có màn hình, và trang giữ chỗ của web không có trường nhập.
- Không có trường nhập từ người dùng. Dữ liệu vào là biến môi trường và giá trị cài đặt do tính năng khác gửi xuống `SettingsService`.

<!-- src-section: 960bb4b154 1db0b97ca2b6 -->
### Biến môi trường

**Tóm tắt.** Biến môi trường chỉ chứa khóa bí mật, đường dẫn và địa chỉ kết nối. Mọi cấu hình nghiệp vụ nằm trong `app_settings`.

**Biến của ứng dụng**

| Biến | Dùng ở | Bắt buộc | Yêu cầu (in nguyên văn trong thông báo R-SKL-02) | Ví dụ trong `.env.example` |
|---|---|---|---|---|
| `DATABASE_URL` | api | có | phải là URL postgres:// hoặc postgresql:// | `postgres://mio:<mật khẩu>@postgres:5432/mio` |
| `REDIS_URL` | api, browser-worker | có | phải là URL redis:// | `redis://redis:6379` |
| `DATA_DIR` | api, browser-worker | có | phải là đường dẫn tuyệt đối | `/data` |
| `BROWSER_PROFILE_DIR` | browser-worker | có | phải là đường dẫn tuyệt đối | `/browser-profile` |
| `PUBLIC_URL` | api | có | phải là URL http:// hoặc https://, không có / cuối | `http://localhost:3000` |

**Biến của Docker Compose**

- Các biến này nằm trong file `.env` ở gốc. File này không được commit; repo có `.env.example`.
- `compose.yml` dùng cú pháp `${TÊN:?Thiếu TÊN trong .env}` cho cả ba biến. Vì vậy, thiếu biến hoặc biến rỗng thì `docker compose` dừng ngay với thông báo "Thiếu <TÊN> trong .env". Khi đó không container nào được tạo hay khởi động lại.

| Biến | Bắt buộc | Ý nghĩa |
|---|---|---|
| `POSTGRES_PASSWORD` | có | mật khẩu DB, ghép vào `DATABASE_URL` của api |
| `MIO_DATA_DIR` | có | thư mục trên máy chủ gắn vào `/data` của api và browser-worker (ảnh, debug dump) |
| `MIO_PUBLIC_URL` | có | truyền vào `PUBLIC_URL` của api |

Profile trình duyệt không nằm trong `MIO_DATA_DIR`. Profile nằm trong named volume `mio-browser-profile`, gắn vào `/browser-profile` của browser-worker (R-SKL-20, ADR 0013).

<!-- src-section: 0f1edd606c 329651041585 -->
### Quy tắc

#### R-SKL-01: Thiếu biến môi trường

Thiếu biến môi trường bắt buộc thì tiến trình ghi log lỗi và thoát mã 1.

- Thông báo là "Thiếu biến môi trường: <TÊN_1>, <TÊN_2>". Thông báo liệt kê hết các biến thiếu trong một dòng.
- Biến có giá trị rỗng hoặc chỉ có khoảng trắng được coi như thiếu.

#### R-SKL-02: Biến sai định dạng

Biến sai định dạng thì tiến trình thoát mã 1 với thông báo "Biến môi trường không hợp lệ: <TÊN> (<yêu cầu>)".

- `<yêu cầu>` lấy nguyên văn cột "Yêu cầu" của bảng Biến môi trường. Ví dụ: "Biến môi trường không hợp lệ: REDIS_URL (phải là URL redis://)".
- Nhiều biến sai thì mỗi biến một dòng log.
- Giá trị của biến không được in ra log.

#### R-SKL-03: Chạy migration

Chỉ api chạy migration. Migration chạy lúc khởi động, trước khi mở cổng HTTP.

- Migration lỗi thì api ghi log lỗi, thoát mã 1 và không mở cổng.
- api chạy một bản duy nhất. Nếu sau này chạy nhiều bản thì phải bọc migration bằng khóa `pg_advisory_lock`.

#### R-SKL-04: browser-worker chỉ kết nối Redis

- browser-worker không kết nối PostgreSQL, không mở cổng HTTP và không gọi API.
- Dữ liệu vào nằm trong dữ liệu job. Dữ liệu ra đi qua hàng đợi kết quả (R-SKL-28, ADR 0011).

#### R-SKL-05: Mỗi lúc chỉ một job trình duyệt

- `fb-browser` có global concurrency bằng 1 (BullMQ `setGlobalConcurrency(1)`). Nhờ vậy, dù chạy nhiều tiến trình browser-worker, cũng chỉ có một job chạy cùng lúc.
- Giai đoạn 0 chỉ đăng ký `fb-browser` và `fb-browser-results`. Các hàng đợi khác chỉ được khai báo tên trong `QUEUE_NAMES`; tính năng của giai đoạn tương ứng tự đăng ký.
- Việc `fb-inbox` tách riêng hay gộp vào `fb-browser` được quyết ở giai đoạn 3, theo 04-technical.md mục 4.3.
  - Trường hợp gộp áp dụng khi inbox dùng chung tài khoản vận hành; khi đó inbox có ưu tiên cao nhất.
  - Nếu tách thì `fb-inbox` cũng có global concurrency 1 và dùng profile riêng.
- Hàng đợi `render` dùng Chromium riêng, không dùng thư mục profile Facebook.

#### R-SKL-06: Tên hàng đợi

Tên hàng đợi chỉ được lấy từ `QUEUE_NAMES`. Code không viết chuỗi tên hàng đợi trực tiếp.

#### R-SKL-07: Job không tự chạy lại

**Tóm tắt.** Mọi hàng đợi có tùy chọn mặc định để job không bao giờ tự chạy lại.

**Vì sao.** Để tránh comment hai lần.

**Cách hoạt động**

- Job có `attempts: 1`, `removeOnComplete: { count: 1000 }`, `removeOnFail: { count: 5000 }`. Tính năng nào cần thử lại phải tự khai báo và chứng minh thao tác an toàn khi chạy lại.
- Mọi Worker (browser-worker và api) đặt `maxStalledCount: 0`.
  - Job bị stalled (worker chết, mất lock) chuyển thẳng sang `failed`, không quay về `wait`.
  - `attempts` không áp dụng cho stalled. Mặc định của BullMQ (`maxStalledCount: 1`) sẽ chạy lại job stalled một lần.
- `lockDuration` để mặc định là 30 giây, và worker tự gia hạn lock. Processor không được chặn event loop quá vài giây, để không bị stalled giả trong lúc vẫn đang chạy.

#### R-SKL-08: Đọc cài đặt không cache

`SettingsService.get` đọc DB ở mỗi lần gọi, không cache. Giá trị mới có hiệu lực từ lần đọc kế tiếp, không cần khởi động lại.

#### R-SKL-09: Khóa chưa có bản ghi

Khóa chưa có bản ghi trong DB thì `get` trả `defaultValue` của khóa và không ghi vào DB.

#### R-SKL-10: Khóa cài đặt không tồn tại

- `get` / `set` với khóa không có trong `SETTINGS` thì ném `UnknownSettingKeyError` với thông báo "Khóa cài đặt không tồn tại: <khóa>".
- Đây là lỗi lập trình. Khóa có kiểu `SettingKey` nên typecheck chặn trước. Nếu lỗi vẫn xảy ra lúc chạy thì API trả 500 `INTERNAL_ERROR` (R-SKL-16).
- Không có mã lỗi riêng cho trường hợp này. Mỗi khóa có route cố định (ADR 0010), nên khóa lạ trên URL rơi vào 404 `NOT_FOUND` (R-SKL-15).

#### R-SKL-11: Giá trị cài đặt không hợp lệ khi ghi

**Tóm tắt.** `set` với giá trị không qua zod schema của khóa thì ném `SettingValidationError` kèm `fields` và không ghi gì vào DB. Endpoint trả 400 `VALIDATION_ERROR` với `message` "Dữ liệu cài đặt không hợp lệ".

**Quy ước chung cho lỗi theo trường của cài đặt** (dùng cả ở R-SKL-12)

- Khóa của `fields` là đường dẫn đầy đủ trong mục. Thuộc tính được nối bằng `.`, chỉ số mảng đặt trong `[]`, ví dụ `goldenHours[1].end`. Lỗi ở gốc (giá trị không phải object) dùng khóa `_root`.
- Giá trị là thông báo tiếng Việt do schema của khóa định nghĩa. Một trường có nhiều lỗi thì lấy lỗi đầu tiên zod trả về.
- Ghi thành công thì lưu **kết quả parse** của schema, không phải giá trị gửi lên. Bản ghi thay cả mục (upsert theo `key`) và cập nhật `updated_at`.
- Trường không có trong schema bị bỏ khi parse, theo mặc định của zod, ở cả `set` và `get`. Vì vậy bỏ một trường khỏi schema không làm giá trị đang lưu thành lỗi.

#### R-SKL-12: Giá trị đang lưu không hợp lệ

**Tóm tắt.** Giá trị trong DB không qua schema hiện tại thì `get` ném `InvalidStoredSettingError`, không lặng lẽ dùng mặc định. Ví dụ: schema đổi mà thiếu migration dữ liệu. Lỗi phải nêu cụ thể nguyên nhân và liệt kê **mọi** trường lỗi.

**Cách hoạt động**

- Thông báo có dạng "Cài đặt <khóa> đang lưu không hợp lệ: <trường 1>: <lý do 1> (đang lưu: <giá trị 1>); <trường 2>: …". Ví dụ: "Cài đặt crawl-schedule đang lưu không hợp lệ: maxScrolls: phải từ 1 đến 20 (đang lưu: 25)".
- `<trường>` và `<lý do>` theo quy ước của R-SKL-11. Trường bị thiếu ghi "(đang lưu: không có)".
- `<giá trị>` được in bằng `JSON.stringify`. Chuỗi có ngoặc kép, ví dụ `"abc"`; số, `true`, `null` in như JSON. Chuỗi JSON dài hơn 100 ký tự thì lấy 100 ký tự đầu và thêm "…".
- Log ở mức `error`, gồm thông báo trên, `key` và danh sách `{ path, reason, storedValue }`.
- Endpoint `GET` / `PUT /api/v1/settings/<khóa>` của tính năng trả 409 `INVALID_STORED_SETTING`. `message` là thông báo trên, còn `fields` là `{ <trường>: <lý do> }`. `PUT` một giá trị hợp lệ thì ghi đè và hết lỗi.
- Job đọc phải cài đặt lỗi thì thất bại, lấy đúng thông báo trên làm lý do. Tính năng sở hữu job quyết định có tự dừng và báo khẩn hay không.

#### R-SKL-13: Kiểm tra sức khỏe

`GET /api/v1/health` không cần đăng nhập.

- Endpoint kiểm DB (`select 1`) và Redis (`PING`) **song song**. Mỗi kiểm tra dùng kết nối riêng cho health, không dùng chung kết nối của BullMQ, và có timeout 2 giây.
- Cả hai trả lời trong 2 giây thì endpoint trả 200 `status: ok`.
- Một trong hai lỗi hoặc quá 2 giây thì endpoint trả 503 `status: error`, và trường tương ứng có giá trị `down`.
- Response không chứa thông báo lỗi chi tiết, phiên bản hay đường dẫn.

#### R-SKL-14: api phục vụ web

- Với request `GET` tới đường dẫn không bắt đầu bằng `/api/`: nếu có file trong `apps/web/dist` thì api trả file đó. Nếu không có file thì api trả `index.html` để SPA tự định tuyến.
- api không bao giờ trả file nằm ngoài `apps/web/dist`, kể cả với đường dẫn có `..` hay dạng mã hóa `%2e%2e`.

#### R-SKL-15: Định dạng lỗi API

Mọi lỗi API trả thân `{ "code": "<MÃ_LỖI>", "message": "<tiếng Việt>", "fields"?: { "<trường>": "<thông báo>" } }`. Các mã lỗi dùng chung:

- 404 `NOT_FOUND`: đường dẫn `/api/...` không có route; thông báo "Không tìm thấy địa chỉ yêu cầu".
- 400 `INVALID_JSON`: thân request không phải JSON hợp lệ; thông báo "Dữ liệu gửi lên không đúng định dạng JSON".
- 413 `PAYLOAD_TOO_LARGE`: thân request lớn hơn 1 MB; thông báo "Dữ liệu gửi lên quá lớn".
- 400 `VALIDATION_ERROR`: dữ liệu sai quy tắc, có `fields` (quy ước đường dẫn trường theo R-SKL-11).
- 409 `INVALID_STORED_SETTING`: theo R-SKL-12.
- 500 `INTERNAL_ERROR`: theo R-SKL-16.

#### R-SKL-16: Lỗi không lường trước

- Lỗi không lường trước trả 500 `INTERNAL_ERROR` với thông báo "Lỗi hệ thống, vui lòng thử lại sau".
- Response không chứa stack trace hay nội dung lỗi gốc.
- Log ghi lỗi đầy đủ kèm `requestId`.

#### R-SKL-17: Log

Log là JSON một dòng ghi ra stdout, gồm `time`, `level`, `app`, `msg`, và `requestId` / `jobId` khi có. Thông tin nhạy cảm được che thành `[REDACTED]` bằng `redact` của pino, theo một danh sách đường dẫn cố định. Danh sách phải cố định vì pino không có wildcard đệ quy.

- Header bị che: `req.headers.authorization`, `req.headers.cookie`, `res.headers["set-cookie"]`.
- Các khóa `password`, `token`, `secret`, `cookie`, `authorization` bị che ở độ sâu 1 đến 3 (`x`, `*.x`, `*.*.x`, `*.*.*.x`).
- Có loại bí mật mới thì bổ sung danh sách (ADR 0012).
- Log không ghi nội dung bài, tin nhắn, tên người hay giá trị biến môi trường.

#### R-SKL-18: Nhịp sống browser-worker

- Mỗi tiến trình browser-worker ghi khóa riêng `mio:heartbeat:browser-worker:<hostname>` mỗi 15 giây, với TTL 60 giây.
  - `<hostname>` là hostname của container.
  - Giá trị của khóa là thời điểm ISO lấy từ `CLOCK`.
- Healthcheck Docker của browser-worker chỉ đạt khi khóa của chính container còn tồn tại. Nhờ vậy một worker treo không bị worker khác che.
- Việc phát hiện "không còn worker nào sống" (không còn khóa nào) và báo cho chủ tiệm thuộc tính năng `emergency-stop`.

#### R-SKL-19: Cổng mạng

- `compose.yml` chỉ publish cổng api, gắn vào `127.0.0.1:3000`.
- PostgreSQL và Redis không publish cổng. Khi dev, `compose.dev.yml` publish hai dịch vụ này lên `127.0.0.1` (5432, 6379).

#### R-SKL-20: Thư mục dữ liệu và quyền

- api và browser-worker chạy bằng cùng `uid:gid` `1000:1000`, không phải root. Vì vậy file một bên tạo thì bên kia đọc, ghi, xóa được.
- Lúc khởi động, app tạo các thư mục con của `DATA_DIR` nếu chưa có: `images/`, `debug-dumps/`. Việc này áp dụng cho cả api và browser-worker.
- Profile trình duyệt nằm ở `BROWSER_PROFILE_DIR`. Đây là named volume `mio-browser-profile`, không phải thư mục của máy chủ, và có quyền `700`.
  - Dockerfile của browser-worker tạo sẵn `/browser-profile` thuộc `1000:1000` với quyền `700`, để volume mới nhận đúng chủ.
  - Lúc khởi động, worker đặt lại quyền `700` (ADR 0013).
- Không ghi được vào `DATA_DIR` hoặc `BROWSER_PROFILE_DIR` thì tiến trình thoát mã 1 với thông báo "Không ghi được vào thư mục dữ liệu: <đường dẫn>".
- Trên máy chủ Linux, thư mục `MIO_DATA_DIR` phải thuộc `1000:1000`. Cần chạy `chown -R 1000:1000 <MIO_DATA_DIR>` trước lần chạy đầu và sau khi khôi phục từ bản sao lưu. Bước này được ghi trong mục "Triển khai lên máy chủ" của roadmap.

#### R-SKL-21: Build đa kiến trúc

- Image `api` và `browser-worker` build được cho `linux/amd64` và `linux/arm64` bằng `docker buildx bake`.
- Chỉ dùng base image đa kiến trúc.
- Code, Dockerfile và `compose.yml` không chứa giá trị phụ thuộc máy (ADR 0009).

#### R-SKL-22: Dừng gọn khi nhận `SIGTERM`

- Khi nhận `SIGTERM`, tiến trình ngừng nhận job mới và chờ job đang chạy xong trong thời gian ân hạn (mục Tham số cài đặt). Sau đó tiến trình đóng kết nối và thoát mã 0.
- Dockerfile chạy Node trực tiếp dạng exec (`CMD ["node", "dist/main.js"]`), không qua `pnpm` hay `sh`. Nhờ vậy Node là PID 1 và nhận được tín hiệu.
- Hết thời gian ân hạn thì Docker dừng cứng. Job dở dang bị BullMQ đánh dấu stalled và chuyển sang `failed`. Job **không** chạy lại nhờ `maxStalledCount: 0` (R-SKL-07), rồi được xử lý theo R-SKL-29.

#### R-SKL-23: Múi giờ

- Container đặt `TZ=UTC`. Phiên PostgreSQL dùng múi giờ `UTC`.
- Logic nghiệp vụ lấy giờ từ `CLOCK` và đổi múi giờ bằng `APP_TIME_ZONE` (ADR 0007).
- Lint chặn `Date.now()` / `new Date()` không tham số ngoài `system-clock.ts`.

#### R-SKL-24: Đo RAM/CPU từng container

`tools/ops/container_stats.py` đo CPU % và RAM của từng container theo chu kỳ. Script ghi CSV và in bảng tổng hợp trung bình / lớn nhất cho mỗi container.

- Script chỉ đo container **thuộc project Compose của app**, nhận biết qua nhãn `com.docker.compose.project`. Testcontainers và container khác bị bỏ qua.
- Tham số và thông báo lỗi nằm ở mục Đo RAM/CPU từng container.
- Docker không chạy thì script thoát mã 1 với thông báo "Không kết nối được Docker. Bật Docker Desktop rồi chạy lại."

#### R-SKL-25: Test integration cần Docker

- `pnpm test:int` khi không kết nối được Docker thì fail, không skip, với thông báo "Không kết nối được Docker. Bật Docker Desktop rồi chạy lại."
- Testcontainers dùng đúng image PostgreSQL và Redis như `compose.yml`. Tag được lấy từ một hằng chung, không lặp chuỗi.

#### R-SKL-26: Giới hạn log Docker

Docker giới hạn log của mỗi container: driver `json-file`, `max-size: 10m`, `max-file: 5`.

#### R-SKL-27: Redis giữ job

Redis bật AOF (`appendonly yes`) và `maxmemory-policy noeviction`; BullMQ yêu cầu cấu hình này. Mục đích là để job không mất khi khởi động lại.

#### R-SKL-28: browser-worker trả kết quả qua hàng đợi

**Tóm tắt.** browser-worker trả kết quả bằng cách thêm job vào hàng đợi kết quả. Nó không dùng giá trị trả về của job hay sự kiện `completed`.

**Cách hoạt động**

- Cặp hàng đợi: `fb-browser` gửi kết quả sang `fb-browser-results`. `fb-inbox` gửi sang `fb-inbox-results`, khi giai đoạn 3 thêm hàng đợi này.
- Dữ liệu job kết quả theo `BrowserJobResult<T>`:
  - `sourceJobId` là id job gốc; `sourceJobName` là tên job gốc;
  - `outcome` là `ok` hoặc `failed`;
  - `data` là kết quả, kiểu `T` do tính năng định nghĩa, chỉ có khi `ok`;
  - `error` là `{ type, message, dumpPath? }`, chỉ có khi `failed`. `type` là tên lớp lỗi đã phân loại (`SessionExpiredError`, `CheckpointError`, `GroupInaccessibleError`…); lỗi chưa phân loại dùng `UnexpectedError`. `dumpPath` là đường dẫn tương đối trong `DATA_DIR` tới ảnh màn hình và HTML lúc lỗi.
- Processor bắt mọi lỗi và luôn gửi job kết quả, kể cả khi `failed`. Sau đó processor kết thúc job gốc bình thường (`completed`).
- Job gốc chỉ `failed` khi không gửi được kết quả: worker chết, stalled, hoặc không ghi được vào Redis.
- Job kết quả dùng `jobId` là `<sourceJobId>-result`. Nhờ vậy gửi lại cùng một kết quả không tạo job trùng.
- api kiểm tra dữ liệu job kết quả bằng zod. Sai cấu trúc thì job kết quả thất bại, và api ghi log lỗi kèm `sourceJobId`, không log dữ liệu job.

#### R-SKL-29: Job gốc mất kết quả

**Tóm tắt.** Job gốc `failed` mà không có job kết quả (R-SKL-28) thì api chuyển cho tính năng sở hữu job. Tính năng xử lý nó như một kết quả `failed` với `error.type = 'WorkerCrashedError'`. Job gốc không tự chạy lại (R-SKL-07).

**Cách hoạt động**

- Cách phát hiện: api nghe sự kiện `failed` của hàng đợi gốc, **và** đối soát lúc api khởi động cùng mỗi 5 phút. Job `failed` của hàng đợi gốc chưa được xử lý thì được xử lý như trên. Đối soát bù cho các sự kiện bị lỡ khi api tắt.
- Việc xử lý theo `sourceJobId` và idempotent: một job gốc chỉ được ghi nhận một lần cho mỗi loại tín hiệu.
- Kết quả từ hàng đợi kết quả luôn thắng `WorkerCrashedError`, kể cả khi tới sau. Trường hợp này xảy ra khi stalled giả: worker vẫn chạy xong và gửi kết quả.
- `WorkerCrashedError` nghĩa là "không rõ đã làm tới đâu", không phải "chưa làm". Tính năng có thao tác ghi lên Facebook (comment, đăng bài, trả lời inbox) không được coi là chưa làm để tự làm lại.
- Job gốc nằm ở `active` khi không còn browser-worker nào sống thì khung không tự xử lý, vì việc kiểm tra stalled chỉ do Worker chạy. `emergency-stop` phát hiện tình huống này qua khóa nhịp sống (R-SKL-18).

#### R-SKL-30: Kết nối PostgreSQL và Redis

- **Lúc khởi động:** không kết nối được thì thử lại mỗi 2 giây, tối đa 30 giây. Vẫn không được thì tiến trình thoát mã 1 với thông báo "Không kết nối được PostgreSQL" hoặc "Không kết nối được Redis".
- **Khi đang chạy:** mất kết nối không làm sập tiến trình.
  - Sự kiện lỗi của pool `pg` và ioredis được bắt và ghi log `warn`.
  - ioredis thử lại không giới hạn (`maxRetriesPerRequest: null`, BullMQ yêu cầu).
  - Request cần DB trong lúc mất kết nối nhận 500 `INTERNAL_ERROR` (R-SKL-16). `/health` trả 503 (R-SKL-13).
  - Có kết nối lại thì tiến trình chạy tiếp, không khởi động lại.

#### R-SKL-31: Healthcheck và khởi động lại trong Compose

- Lệnh healthcheck: `postgres` dùng `pg_isready -U mio -d mio`; `redis` dùng `redis-cli ping`; `api` dùng `node dist/healthcheck.js`; `browser-worker` dùng `node dist/healthcheck.js`. Tham số nằm ở mục Tham số cài đặt.
- Mọi dịch vụ có `restart: unless-stopped`.
- Docker chỉ khởi động lại container khi tiến trình **thoát**. Container `unhealthy` mà tiến trình còn chạy (treo) không được khởi động lại.
- Tình trạng treo của browser-worker do `emergency-stop` phát hiện qua khóa nhịp sống (R-SKL-18).

<!-- src-section: 9ce7add77d 56d100a0ca6c -->
## Job và hàng đợi

**Tóm tắt.** Khung chỉ tạo hàng đợi và worker rỗng của giai đoạn 0. Processor và job cụ thể do các tính năng sau thêm.

**Các hàng đợi trong `QUEUE_NAMES` và nơi chạy.** Chỉ hai hàng đợi đầu được đăng ký ở giai đoạn 0 (R-SKL-05).

- `fb-browser`: chạy ở browser-worker, global concurrency 1. Hàng đợi này dùng để quét group, comment và đăng group.
- `fb-browser-results`: chạy ở api, concurrency 1. Hàng đợi này nhận kết quả của `fb-browser` (R-SKL-28).
- `fb-inbox`: chạy ở browser-worker, từ giai đoạn 3. Việc tách riêng hay gộp vào `fb-browser` được quyết ở giai đoạn 3.
- `fb-inbox-results`: chạy ở api, từ giai đoạn 3, nếu `fb-inbox` tách riêng.
- `render`: chạy ở browser-worker, concurrency 1, từ giai đoạn 4.
- `ai-text`, `ai-image`, `messenger`, `page-publish`: chạy ở api, từ giai đoạn 1 trở đi.

**Chiều dữ liệu**

1. api thêm job vào `fb-browser`, kèm mọi cài đặt worker cần.
2. browser-worker xử lý job.
3. browser-worker thêm job vào hàng đợi kết quả.
4. api ghi kết quả vào DB.

Kết quả nằm trong Redis tới khi api xử lý, nên api khởi động lại không làm mất kết quả. Trường hợp job gốc mất kết quả được xử lý theo R-SKL-29.

**Tùy chọn khác**

- Tùy chọn mặc định theo R-SKL-07. Ưu tiên, retry và timeout riêng do tính năng khai báo khi thêm job.
- Nhịp sống browser-worker không phải job BullMQ. Đó là `setInterval` ghi Redis (R-SKL-18).

<!-- src-section: 44dde0ce1e 2f6bde79fe3a -->
## Trạng thái và thuật toán

Mục này mô tả trình tự khởi động, cách đọc và ghi cài đặt, cách đo RAM/CPU và cách build đa kiến trúc.

<!-- src-section: 7cdff4df0a 191af8d3266c -->
### Khởi động

**Tóm tắt.** api và browser-worker khởi động theo các bước cố định. Compose khởi động các dịch vụ theo thứ tự phụ thuộc.

**api**

1. Đọc và kiểm tra env (R-SKL-01, 02).
2. Kiểm tra hoặc tạo thư mục dữ liệu (R-SKL-20).
3. Kết nối DB (R-SKL-30).
4. Chạy migration (R-SKL-03).
5. Kết nối Redis, đăng ký hàng đợi và đối soát job gốc mất kết quả (R-SKL-29).
6. Mở cổng 3000.

**browser-worker**

1. Đọc env.
2. Tạo thư mục dữ liệu và kiểm tra thư mục profile.
3. Kết nối Redis (R-SKL-30).
4. Đăng ký worker.
5. Bắt đầu ghi nhịp sống.

**Thứ tự trong Compose.** `postgres` và `redis` healthy trước. Sau đó `api` healthy (kiểm qua `/api/v1/health`). Cuối cùng là `browser-worker`. Healthcheck và khởi động lại theo R-SKL-31.

<!-- src-section: 66e9251b2f 4ca6a38f366e -->
### Đọc / ghi cài đặt

**Tóm tắt.** Đọc cài đặt trả giá trị đã parse hoặc giá trị mặc định. Ghi cài đặt kiểm giá trị bằng schema rồi upsert.

**Đọc: `get(key)`**

1. Tìm định nghĩa trong `SETTINGS`. Không có thì ném `UnknownSettingKeyError` (R-SKL-10).
2. Chạy `SELECT value FROM app_settings WHERE key = $1`.
3. Không có dòng thì trả mặc định (R-SKL-09).
4. Có dòng thì chạy `schema.safeParse(value)`. Lỗi thì xử lý theo R-SKL-12. Đạt thì trả giá trị đã parse.

**Ghi: `set(key, value)`**

1. Tìm định nghĩa.
2. Chạy `schema.safeParse(value)`. Lỗi thì xử lý theo R-SKL-11.
3. Ghi bằng `INSERT (key, value, created_at, updated_at) VALUES ($key, <giá trị đã parse>, <CLOCK.now()>, <CLOCK.now()>) ON CONFLICT (key) DO UPDATE SET value = …, updated_at = <CLOCK.now()>`.
4. Trả giá trị đã lưu.

**Ghi đồng thời.** Lần ghi sau thắng và cả mục bị thay. Điều này chấp nhận được vì chỉ Quản lý sửa cài đặt.

<!-- src-section: d53e3622c8 b5d7ec5b89fa -->
### Đo RAM/CPU từng container

**Tóm tắt.** Script có hai lệnh: `record` ghi số đo CPU và RAM vào file CSV, `summary` in bảng tổng hợp từ file đó. Kết quả dùng cho báo cáo nghiệm thu giai đoạn 0.

**Lệnh**

- `py tools/ops/container_stats.py record [--interval <giây>] [--out <file.csv>]`
- `py tools/ops/container_stats.py summary <file.csv>`

**Tham số của `record`**

- `--interval`: số nguyên từ 5 đến 3600, mặc định 60. Giá trị sai (ngoài khoảng, hoặc không phải số nguyên) thì lệnh thoát mã 2 với thông báo "--interval phải là số nguyên từ 5 đến 3600".
- `--out`: mặc định là `.local/metrics/<YYYY-MM-DD-HHmm>.csv`, theo giờ `Asia/Ho_Chi_Minh` lúc bắt đầu. Thư mục cha chưa có thì được tạo.

**Cách `record` hoạt động**

- Lệnh lấy mẫu ngay khi bắt đầu, sau đó cứ mỗi `--interval` giây lấy một lần.
- Mỗi lần lấy mẫu, lệnh gọi `docker stats --no-stream --format "{{json .}}"` và chỉ giữ container thuộc project Compose của app (R-SKL-24).
- Mỗi container được ghi một dòng CSV gồm các cột:
  - `time` (ISO UTC);
  - `container` (tên container, ví dụ `mio-api-1`);
  - `cpu_percent` (theo `docker stats`; 100% tương ứng 1 lõi CPU, nên giá trị có thể vượt 100);
  - `mem_bytes`;
  - `mem_limit_bytes`.
- Lệnh chạy tới khi bấm Ctrl+C và thoát gọn với mã 0.
- Nếu file đã có thì lệnh ghi nối tiếp. Nhờ vậy có thể gộp nhiều lần chạy thành tổng 24 giờ.

**Cách `summary` hoạt động**

- Lệnh in cho mỗi container: số mẫu, CPU trung bình, CPU lớn nhất, RAM trung bình, RAM lớn nhất (MiB).
- File không tồn tại thì lệnh thoát mã 1 với thông báo "Không tìm thấy file: <đường dẫn>".

File CSV nằm trong `.local/` và không được commit.

<!-- src-section: c00df10db9 f45edca115a0 -->
### Build đa kiến trúc

**Tóm tắt.** Image `api` và `browser-worker` được build cho hai kiến trúc bằng `docker buildx bake`.

- `docker buildx bake` dùng `docker-bake.hcl` với target `api`, `browser-worker` và `platforms = ["linux/amd64", "linux/arm64"]`.
- Lệnh build:
  - `pnpm docker:build` build cho amd64 và nạp vào Docker local;
  - `pnpm docker:build:multiarch` build cả hai kiến trúc để kiểm tra build được; arm64 chạy qua QEMU.
- Kiểm tra arm64: build thành công, và chạy được `node --version` trong image arm64 qua QEMU. api phải ra Node 26. browser-worker ra phiên bản Node của image Playwright.
- Việc chạy Chromium trên arm64 thật được kiểm chứng khi triển khai lên máy chủ (04 mục 2).

<!-- src-section: 2b1fe40749 f6dcdbe261a6 -->
## Tích hợp bên ngoài

Không áp dụng. Khung không gọi Facebook, Gemini hay Messenger. Khung chỉ tích hợp với hạ tầng nội bộ: PostgreSQL, Redis, Docker.

<!-- src-section: a2cb20bfc7 ff7a86ce5831 -->
## Xử lý lỗi, log, bảo mật, phân quyền

**Lỗi**

- Một số lỗi lúc khởi động làm tiến trình thoát mã 1 (R-SKL-01, 02, 03, 20, 30): thiếu hoặc sai env, không ghi được thư mục dữ liệu, migration lỗi, không kết nối được DB hoặc Redis. Compose khởi động lại container theo `restart: unless-stopped`, và log ghi rõ nguyên nhân.
- Mất kết nối Redis hoặc DB khi đang chạy được xử lý theo R-SKL-30. Trong lúc mất kết nối, health trả 503 (R-SKL-13).
- Tiến trình browser-worker thoát thì Compose khởi động lại. Tiến trình treo thì chuyển sang `unhealthy`, và Docker **không** tự khởi động lại (R-SKL-31). Việc phát hiện và báo cho chủ tiệm thuộc `emergency-stop`.
- Job gốc mất kết quả được xử lý theo R-SKL-29.

**Log:** R-SKL-17, R-SKL-26.

**Bảo mật**

- Khóa bí mật chỉ nằm ở `.env` (không commit, có `.env.example`) và trong biến môi trường của container.
- Cổng chỉ mở trên `127.0.0.1` (R-SKL-19). HTTPS được thêm khi triển khai lên máy chủ (ADR 0009).
- Tiến trình chạy bằng user không phải root (`1000:1000`). Profile trình duyệt nằm trong named volume riêng với quyền `700` (R-SKL-20, ADR 0013).
- File tĩnh không thoát ra ngoài `apps/web/dist` (R-SKL-14).
- `.gitignore` có `.env`, `.local/`, `node_modules/`, `dist/`, `apps/web/src/styles/ui-tokens.css`.

**Phân quyền.** Không áp dụng ở khung. Endpoint duy nhất (`/health`) là công khai (R-SKL-13). Phân quyền theo vai trò thuộc tính năng `auth`.

<!-- src-section: d0d46a0edb 2f9eece6de75 -->
## Tham số cài đặt

**Tóm tắt.** Khung không thêm khóa cài đặt nghiệp vụ. Các hằng kỹ thuật dưới đây đặt trong code, không chỉnh trên web.

- **Nhịp sống browser-worker:** ghi mỗi 15 giây, TTL 60 giây. Nguồn: quyết định mới; người dùng chỉnh TTL ngày 2026-10-29.
- **Thời gian chờ mỗi kiểm tra trong `/health`:** 2 giây; hai kiểm tra chạy song song. Nguồn: quyết định mới.
- **Healthcheck Compose (R-SKL-31):** `interval` 10 giây, `timeout` 5 giây, `retries` 3. `start_period` là 60 giây cho api (vì chạy migration) và 30 giây cho các dịch vụ khác. Nguồn: quyết định mới (review RV-04).
- **Kết nối lúc khởi động:** thử lại mỗi 2 giây, tối đa 30 giây (R-SKL-30). Nguồn: quyết định mới (review RV-12).
- **Đối soát job gốc mất kết quả:** lúc api khởi động và mỗi 5 phút (R-SKL-29). Nguồn: quyết định mới (review RV-03).
- **Giới hạn thân request API:** 1 MB (R-SKL-15). Nguồn: quyết định mới (review RV-08).
- **Thời gian ân hạn khi dừng (`stop_grace_period`):** api 30 giây, browser-worker 120 giây. Nguồn: quyết định mới; `group-crawl-job` xem lại khi chốt độ dài một job.
- **Giữ job:** giữ 1000 job hoàn thành và 5000 job lỗi; `maxStalledCount` là 0 (R-SKL-07). Nguồn: quyết định mới.
- **Log Docker:** 10 MB × 5 file mỗi container (R-SKL-26). Nguồn: quyết định mới.
- **Chu kỳ đo RAM/CPU:** mặc định 60 giây, trong khoảng 5–3600 giây, đổi bằng `--interval`. Nguồn: quyết định mới.
- **Phiên bản hạ tầng** (chốt 2026-10-29, câu hỏi mở 2). Mọi image đều đa kiến trúc.
  - Node.js 26 cho api (image `node:26-bookworm-slim`).
  - PostgreSQL 18 (`postgres:18-alpine`).
  - Redis 8 (`redis:8-alpine`).
  - browser-worker dùng `mcr.microsoft.com/playwright:v1.63.0-noble`, khớp phiên bản `playwright` trong `package.json`, và dùng Node đi kèm image (ADR 0014). Phiên bản Node cụ thể được ghi vào `plan.md` lúc implement. `@mio/shared` và `apps/browser-worker` chỉ dùng tính năng có trên phiên bản đó.
  - Tag không tồn tại lúc implement thì lấy bản vá mới nhất cùng dòng và ghi lại trong `plan.md` của task. Tag PostgreSQL và Redis được khai báo một chỗ, dùng chung cho `compose.yml` và Testcontainers (R-SKL-25).

<!-- src-section: 505f20bb78 c893bc8288ce -->
## Câu hỏi mở

Cả 3 câu hỏi đều đã được chốt.

- [x] **1. browser-worker chỉ kết nối Redis, không kết nối PostgreSQL?** Đã chốt 2026-10-29: chỉ kết nối Redis (ADR 0011). Kết quả được trả qua hàng đợi kết quả `fb-browser-results` / `fb-inbox-results` (R-SKL-28, R-SKL-29).
- [x] **2. Phiên bản hạ tầng?** Đã chốt 2026-10-29: Node.js 26, PostgreSQL 18, Redis 8, Playwright 1.63 (mục Tham số cài đặt). Bổ sung 2026-10-31: browser-worker dùng Node đi kèm image Playwright (ADR 0014).
- [x] **3. Giá trị cài đặt trong DB không còn hợp lệ thì làm gì?** Đã chốt 2026-10-29: báo lỗi và không dùng mặc định. Thông báo nêu cụ thể từng trường lỗi, lý do và giá trị đang lưu (R-SKL-12). Đổi schema cài đặt phải kèm migration dữ liệu.

<!-- src-section: 80b54c0db6 64923f645c0e -->
## Lịch sử thay đổi

- 2026-10-29: tạo mới.
- 2026-10-29: chốt câu hỏi 3. R-SKL-12 ghi rõ nội dung lỗi và mã `INVALID_STORED_SETTING` (409).
- 2026-10-29: chốt câu hỏi 1, 2. Thêm hàng đợi kết quả `fb-browser-results`, `fb-inbox-results` (R-SKL-28, R-SKL-29). Chốt phiên bản hạ tầng.
- 2026-10-29: đổi TTL nhịp sống browser-worker từ 45 lên 60 giây (R-SKL-18); duyệt thiết kế.
- 2026-10-31: sửa theo `reviews/app-skeleton-review.md`:
  - R-SKL-07, R-SKL-22: `maxStalledCount: 0`, job stalled không chạy lại (RV-01);
  - R-SKL-28, R-SKL-29: processor luôn gửi kết quả, thêm `UnexpectedError`, xử lý idempotent, kết quả thật thắng `WorkerCrashedError`, đối soát lúc khởi động và mỗi 5 phút (RV-02, RV-03);
  - R-SKL-18 và thêm R-SKL-31: khóa nhịp sống theo container, healthcheck Compose, container treo không tự khởi động lại (RV-04);
  - R-SKL-20 và thêm biến `BROWSER_PROFILE_DIR`: cùng uid `1000:1000`, profile trong named volume `mio-browser-profile` (RV-05, RV-06; ADR 0013);
  - Tham số: browser-worker dùng Node của image Playwright (RV-07; ADR 0014);
  - R-SKL-10, R-SKL-15: bỏ `SETTING_NOT_FOUND`, thêm mã chung `INVALID_JSON`, `PAYLOAD_TOO_LARGE`, giới hạn thân request 1 MB (RV-08);
  - R-SKL-01, R-SKL-02 và bảng biến: thông báo nguyên văn cho từng biến, biến rỗng coi như thiếu (RV-09);
  - R-SKL-11, R-SKL-12: lưu kết quả parse, bỏ trường lạ, quy ước đường dẫn trường, khóa `_root`, in giá trị bằng `JSON.stringify` (RV-10);
  - Thay đổi DB, Đọc / ghi cài đặt: `created_at`, `updated_at` lấy từ `CLOCK` (RV-11);
  - R-SKL-13 và thêm R-SKL-30: kết nối lúc khởi động và khi đang chạy, health kiểm song song (RV-12);
  - R-SKL-24 và mục Đo RAM/CPU: lọc theo project Compose, khoảng của `--interval`, mặc định của `--out`, lỗi của `summary` (RV-13);
  - R-SKL-05 và mục Job và hàng đợi: giai đoạn 0 chỉ đăng ký `fb-browser`, `fb-browser-results` (RV-15);
  - R-SKL-17: danh sách đường dẫn che cố định (RV-16);
  - bảng biến Compose: cú pháp `${TÊN:?…}` (RV-17);
  - R-SKL-03, R-SKL-22, mục `apps/web`, `core/db`: thêm chi tiết implement (RV-18);
  - R-SKL-14: không trả file ngoài `apps/web/dist` (RV-19).
- 2026-10-31: duyệt thiết kế sau review.
