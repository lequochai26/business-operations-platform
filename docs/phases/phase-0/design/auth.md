# Thiết kế chi tiết – Đăng nhập và phân quyền (`auth`, `AUT`)

- Giai đoạn: 0
- Trạng thái: đã duyệt ngày 2026-10-31 (duyệt thiết kế sau `/design-review`)
- Tài liệu khái quát: 07-screens-and-settings.md "Yêu cầu chung" (Đăng nhập, HTTPS), mục 1 "Quyền của vai trò Thợ", mục 1.9, 1.10, mục 2 "Người dùng"; 03-data-model.md mục 1 "Người dùng"; 04-technical.md mục 7; 05-roadmap.md giai đoạn 0 (đăng nhập hai vai trò); 01-overview.md mục 6; ADR 0011, 0012, 0015; thiết kế `app-skeleton` (R-SKL-14 … R-SKL-17, `cli.ts`)

## Tóm tắt

Cho chủ tiệm (vai trò Quản lý) và thợ (vai trò Thợ) đăng nhập web app bằng tên đăng nhập và mật khẩu, giữ đăng nhập lâu dài trên thiết bị, đăng xuất và tự đổi mật khẩu. Chặn đoán mật khẩu bằng giới hạn số lần đăng nhập sai. Cung cấp cơ chế phân quyền theo vai trò cho mọi endpoint và màn hình của các tính năng sau, cùng khung app (thanh điều hướng theo vai trò). Giai đoạn 0 tạo và đặt lại tài khoản bằng lệnh CLI; màn hình quản lý tài khoản thợ làm ở giai đoạn 2.

## Module và interface

### `packages/shared` (`@mio/shared`), thư mục `src/auth/`

- Vai trò: `ROLES = ['manager', 'technician'] as const`; `type Role`; `ROLE_LABELS = { manager: 'Quản lý', technician: 'Thợ' }`.
- zod schema dùng chung cho API, web và CLI (thông báo lỗi nguyên văn theo mục Quy tắc):
  - `loginInputSchema`: `{ username, password }` (R-AUT-01 … R-AUT-04, R-AUT-07);
  - `changePasswordInputSchema`: `{ currentPassword, newPassword, signOutOtherDevices }` (R-AUT-20, R-AUT-21, R-AUT-23);
  - `changePasswordFormSchema`: thêm `confirmPassword`, chỉ web dùng (R-AUT-22);
  - `usernameSchema`, `displayNameSchema`, `passwordSchema` cho CLI (R-AUT-25);
  - `sessionUserSchema`: `{ id, username, displayName, role }`.
- `normalizeUsername(raw: string) -> string`: bỏ khoảng trắng hai đầu, đổi chữ thường (R-AUT-07).

### `apps/api` (`@mio/api`), module `src/modules/auth/`

- `PasswordHasher` (`password-hasher.ts`), argon2id qua `@node-rs/argon2` (mục Tham số):
  - `hash(plain: string) -> Promise<string>` (chuỗi PHC);
  - `verify(hash: string, plain: string) -> Promise<boolean>`;
  - `needsRehash(hash: string) -> boolean` (tham số trong chuỗi PHC khác tham số hiện tại).
- `UsersRepository`: `findByUsername(username) -> User | null`, `findById(id) -> User | null`, `lockById(tx, id) -> User | null`, `lockByUsername(tx, username) -> User | null` (`SELECT … FOR UPDATE` trong transaction của bên gọi, R-AUT-23, R-AUT-26), `create(input) -> User`, `updatePasswordHash(id, hash) -> void`, `list() -> User[]`.
- `SessionService` (bảng `user_sessions`):
  - `create(userId) -> { token: string, expiresAt: Date }`;
  - `resolve(token) -> { sessionId, user: SessionUser, refreshedExpiresAt?: Date } | null` (R-AUT-10, R-AUT-11);
  - `revoke(token) -> void`; `revokeAllForUser(userId) -> void`; `deleteExpired() -> number`.
- `LoginThrottleService` (bảng `login_throttles`, R-AUT-06). Hàm ghi chạy trong transaction, khóa dòng của tên (`SELECT … FOR UPDATE`, tạo dòng nếu chưa có); tham số `tx` tùy chọn để chạy chung transaction của bên gọi:
  - `getLock(username) -> { lockedUntil: Date } | null`: đọc nhanh, không khóa dòng;
  - `recordFailure(username, tx?) -> { failedCount: number, lockedUntil: Date | null, isAlreadyLocked: boolean }`: đang khóa thì không đếm (`isAlreadyLocked` true); lần sai này làm khóa thì `failedCount` 5 và có `lockedUntil`;
  - `confirmSuccess(username, tx?) -> { lockedUntil: Date } | null`: đang khóa → trả khóa, không đổi gì; không khóa → xóa bộ đếm;
  - `reset(username, tx?) -> void`: xóa bộ đếm không điều kiện (`reset-password`); `deleteStale() -> number`.
- `AuthService`:
  - `login(input: LoginInput, currentToken?: string) -> { user: SessionUser, token: string, expiresAt: Date }`; lỗi `InvalidCredentialsError`, `LoginLockedError` (có `lockedUntil`);
  - `changePassword(userId, input: ChangePasswordInput) -> { token: string, expiresAt: Date }`; lỗi `CurrentPasswordIncorrectError`, `PasswordUnchangedError`, `LoginLockedError`.
  - Thuật toán: mục Trạng thái và thuật toán.
- `SessionsController`: `POST /api/v1/sessions`, `GET /api/v1/sessions/current`, `DELETE /api/v1/sessions/current`.
- `UsersController`: `POST /api/v1/users/me/change-password`.
- Phân quyền:
  - decorator `@Public()`, `@Roles(...roles: Role[])`, `@CurrentUser()` (lấy `SessionUser` từ request);
  - `AuthGuard` đăng ký global (`APP_GUARD`): đọc cookie, gọi `SessionService.resolve`, kiểm tra vai trò, gắn `req.user` (R-AUT-11, R-AUT-15);
  - `RouteAccessCheck`: chạy lúc khởi động, duyệt mọi route qua `DiscoveryService` (R-AUT-14).
- `SessionCookie` (`session-cookie.ts`): `set(res, token, expiresAt)`, `clear(res)` theo R-AUT-09; đọc cookie bằng `cookie-parser`.
- Lệnh CLI trong `src/modules/auth/cli/`, đăng ký vào bộ điều phối của `cli.ts`: `create-user`, `reset-password`, `list-users` (R-AUT-25 … R-AUT-27).

### `apps/api`, hạ tầng `src/core/http/` (bổ sung)

- `OriginCheckMiddleware`: R-AUT-17; đăng ký bằng `app.use` trong `main.ts` trước body parser, để chạy trước bước đọc thân request (R-AUT-15).
- `SecurityHeadersMiddleware`: R-AUT-18.
- Danh sách `redact` của pino thêm khóa mật khẩu mới (R-AUT-30).

### `apps/web` (`@mio/web`)

- `src/core/api-client.ts`: `apiFetch<T>(path, init) -> Promise<T>`; gửi `credentials: 'same-origin'`; lỗi trả về `ApiError { status, code, message, fields? }`; gặp 401 thì chuyển trang theo R-AUT-31; gặp 403 `FORBIDDEN` thì gọi `refresh()` (R-AUT-29).
- `src/modules/auth/`:
  - `auth-provider.tsx`: `useSession() -> { user: SessionUser | null, isLoading, refresh(), logout(), loginNotice }`; nạp `GET /api/v1/sessions/current` khi mở app; giữ cờ `mio.hadSession` (R-AUT-31) và banner info chờ hiện trên màn Đăng nhập (`loginNotice`, chỉ trong bộ nhớ);
  - `require-auth.tsx`: bọc route cần đăng nhập (R-AUT-28);
  - `require-role.tsx`: `<RequireRole roles={[...]}>` (R-AUT-29);
  - `login-page.tsx`, `change-password-page.tsx`.
- `src/app/`:
  - `app-shell.tsx`: thanh điều hướng + khối tài khoản + vùng nội dung;
  - `nav-items.ts`: `NAV_ITEMS: { label, path, roles: Role[] }[]`; mỗi tính năng có màn hình tự thêm mục của mình;
  - `home-page.tsx` (giữ chỗ Trang chính), `forbidden-page.tsx`, `not-found-page.tsx`.
- Dev: Vite proxy `/api` → `http://localhost:3000`, đặt lại header `Origin` thành `http://localhost:3000` để qua R-AUT-17.

## Thay đổi DB

- Thêm bảng `users`, `user_sessions`, `login_throttles`. Chi tiết: `docs/design/db-schema.md` mục tương ứng.
- Các thông tin người dùng của giai đoạn sau (PSID Messenger, thời điểm tin Messenger gần nhất, đăng ký web push, trạng thái khóa tài khoản) do tính năng của giai đoạn đó thêm cột hoặc bảng.

## API

- `POST /api/v1/sessions` – đăng nhập. Chi tiết: `docs/design/api/sessions.md`.
- `GET /api/v1/sessions/current` – người dùng của phiên hiện tại. Chi tiết: `docs/design/api/sessions.md`.
- `DELETE /api/v1/sessions/current` – đăng xuất. Chi tiết: `docs/design/api/sessions.md`.
- `POST /api/v1/users/me/change-password` – đổi mật khẩu. Chi tiết: `docs/design/api/users.md`.
- Mã lỗi dùng chung mới (khai báo ở đầu `docs/design/api/system.md`): `401 UNAUTHENTICATED`, `403 FORBIDDEN`, `403 INVALID_ORIGIN`.
- Mã lỗi riêng: `401 INVALID_CREDENTIALS`, `429 LOGIN_LOCKED`.

## Màn hình và quy tắc kiểm tra dữ liệu

Mockup làm ở `/ui-design auth`, khung 1440×900 theo `docs/design/ui-style.md`. Giai đoạn 0 chỉ mở được qua `127.0.0.1` trên máy local, nên chưa thiết kế giao diện điện thoại (ui-style mục Bố cục và breakpoint).

### Màn hình Đăng nhập (`/login`)

- Vai trò được dùng: chưa đăng nhập (đã đăng nhập thì chuyển đi, R-AUT-28).
- Nội dung: logo "Mio", tiêu đề "Đăng nhập", form, dòng phụ "Quên mật khẩu? Nhờ người quản trị app đặt lại."
- Trường:
  - Tên đăng nhập: chuỗi, bắt buộc, tối đa 32 ký tự sau khi bỏ khoảng trắng hai đầu, không kiểm định dạng ở bước đăng nhập, mặc định trống; `autocomplete="username"`, không tự viết hoa chữ đầu (`autocapitalize="none"`).
  - Mật khẩu: chuỗi, bắt buộc, tối đa 128 ký tự, không bỏ khoảng trắng, mặc định trống; ô ẩn ký tự có nút hiện/ẩn; `autocomplete="current-password"`.
- Nút "Đăng nhập" (primary); đang gửi: "Đang đăng nhập…", không bấm được.
- Lỗi theo trường hiện dưới ô (R-AUT-01 … R-AUT-04).
- Vùng thông báo: một banner nằm ngay sau ô Mật khẩu, trước nút "Đăng nhập"; mỗi lúc hiện tối đa một banner.
  - Lỗi `INVALID_CREDENTIALS`, `LOGIN_LOCKED`, `INVALID_ORIGIN`, `INTERNAL_ERROR`: banner danger, giữ nguyên tên đăng nhập, xóa ô mật khẩu. Mất mạng, cookie bị chặn: banner danger (mục Xử lý lỗi).
  - Banner info khi tới từ R-AUT-31 ("Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại") hoặc R-AUT-32 ("Bạn đã đăng xuất"). Banner lấy từ `loginNotice` của `auth-provider`, hiện một lần; tải lại trang thì không còn.

### Khung app (mọi trang sau khi đăng nhập)

- Vai trò được dùng: Quản lý, Thợ.
- Thanh điều hướng trái: logo "Mio", các mục trong `NAV_ITEMS` mà vai trò được dùng (R-AUT-29). Giai đoạn 0:
  - "Trang chính" (`/`): Quản lý, Thợ; `auth` làm trang giữ chỗ tiêu đề "Hôm nay", `emergency-stop` thêm khối "Trạng thái tự động hóa";
  - "Cài đặt" (`/settings`): Quản lý; `group-settings` thêm khi có trang con đầu tiên;
  - "Nhật ký hệ thống" (`/system-log`): Quản lý; `emergency-stop` thêm.
- Khối tài khoản cuối thanh điều hướng: tên hiển thị, badge vai trò (`ROLE_LABELS`), liên kết "Đổi mật khẩu", nút "Đăng xuất" (R-AUT-32).
- Không có trường nhập.
- Mở app, trong lúc `auth-provider` nạp `GET /api/v1/sessions/current`: màn hình chờ (logo "Mio", vòng xoay, "Đang tải…"), chưa vẽ thanh điều hướng vì chưa biết vai trò.
- Nạp phiên lỗi 500 hoặc mất mạng (không phải 401): màn hình lỗi với logo, thông báo "Lỗi hệ thống, vui lòng thử lại sau" (mất mạng: "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại.") và nút "Thử lại" (gọi lại `GET /api/v1/sessions/current`). Trả 401 thì theo R-AUT-28.
- Mockup: `docs/design/ui/app-shell/`, `login/`, `change-password/`, `forbidden/`, `not-found/`; thanh điều hướng là component `<mio-app-nav>` (`docs/design/components/app-nav.md`), ô mật khẩu là `<mio-password-field>` (`docs/design/components/password-field.md`).

### Màn hình Đổi mật khẩu (`/account/password`)

- Vai trò được dùng: Quản lý, Thợ (mỗi người đổi mật khẩu của chính mình; câu hỏi mở 3).
- Trường:
  - Mật khẩu hiện tại: chuỗi, bắt buộc, tối đa 128 ký tự, mặc định trống; `autocomplete="current-password"`.
  - Mật khẩu mới: chuỗi, bắt buộc, 8–128 ký tự, không trùng tên đăng nhập, khác mật khẩu hiện tại, mặc định trống; `autocomplete="new-password"`; gợi ý dưới ô "Ít nhất 8 ký tự".
  - Nhập lại mật khẩu mới: chuỗi, bắt buộc, phải giống Mật khẩu mới, mặc định trống.
- Cả ba ô có nút hiện/ẩn. Nút "Đổi mật khẩu" (primary).
- Bấm "Đổi mật khẩu": kiểm tra trên web (R-AUT-19, R-AUT-21 ba ý đầu, R-AUT-22); có lỗi thì hiện dưới ô, không mở hộp thoại. Hợp lệ thì mở hộp thoại xác nhận (R-AUT-34):
  - tiêu đề "Đổi mật khẩu";
  - nội dung "Bạn có muốn đăng xuất khỏi các thiết bị khác đang đăng nhập tài khoản này không? Nên chọn đăng xuất nếu bạn nghi có người khác biết mật khẩu cũ.";
  - nút "Đổi và đăng xuất thiết bị khác" (primary, được focus sẵn), "Chỉ đổi mật khẩu" (secondary), "Hủy" (ghost);
  - Esc hoặc bấm ra ngoài hộp thoại = "Hủy": đóng hộp thoại, không gửi gì, giữ dữ liệu trên form.
- Bấm một trong hai nút đổi: gửi API với `signOutOtherDevices` tương ứng; hai nút ở trạng thái loading ("Đang lưu…" trên nút vừa bấm), không đóng được hộp thoại trong lúc gửi.
- Thành công: đóng hộp thoại, xóa trắng form, ở lại trang, toast success:
  - đã chọn đăng xuất: "Đã đổi mật khẩu. Các thiết bị khác đã được đăng xuất.";
  - không chọn: "Đã đổi mật khẩu.".
- Lỗi: đóng hộp thoại; lỗi theo trường (ví dụ "Mật khẩu hiện tại không đúng") hiện dưới ô; `LOGIN_LOCKED` và lỗi khác hiện banner danger ngay sau ô Nhập lại mật khẩu mới, trước nút "Đổi mật khẩu" (vùng thông báo, giống màn Đăng nhập); giữ dữ liệu trên form.

### Màn hình Không có quyền

- Hiện trong khung app khi Thợ mở trang chỉ dành cho Quản lý (R-AUT-29): tiêu đề "Không có quyền truy cập", dòng "Trang này chỉ dành cho Quản lý.", nút "Về Trang chính".

### Màn hình Không tìm thấy trang

- Hiện trong khung app khi đường dẫn không khớp trang nào (chỉ sau khi đã đăng nhập; chưa đăng nhập thì R-AUT-28 chạy trước): tiêu đề "Không tìm thấy trang", nút "Về Trang chính".

### Quy tắc

Chung: mỗi trường chỉ có một lỗi, lấy ý đầu tiên vi phạm theo thứ tự các ý trong quy tắc của trường đó (trống → độ dài → trùng tên đăng nhập → khác mật khẩu hiện tại). Áp dụng cho lỗi dưới ô trên web, `fields` của API và dòng lỗi của CLI.

Đăng nhập:

- R-AUT-01: Tên đăng nhập trống (sau khi bỏ khoảng trắng hai đầu) → lỗi "Nhập tên đăng nhập".
- R-AUT-02: Tên đăng nhập đã chuẩn hóa (R-AUT-07: bỏ khoảng trắng hai đầu, đổi chữ thường) dài hơn 32 ký tự → lỗi "Tên đăng nhập tối đa 32 ký tự". Đo sau khi đổi chữ thường vì một số ký tự dài ra (ví dụ `İ` thành 2 code point), để tên lưu vào `login_throttles` không vượt 32.
- R-AUT-03: Mật khẩu là chuỗi rỗng → lỗi "Nhập mật khẩu". Mật khẩu chỉ gồm khoảng trắng không coi là rỗng.
- R-AUT-04: Mật khẩu dài hơn 128 ký tự → lỗi "Mật khẩu tối đa 128 ký tự".
  - Độ dài mọi chuỗi trong tính năng tính theo code point (`[...s].length`), không theo đơn vị UTF-16.
  - R-AUT-01 … R-AUT-04 trả 400 `VALIDATION_ERROR`, `message` "Dữ liệu đăng nhập không hợp lệ", `fields` theo trường; không đếm vào R-AUT-06. Trường không phải chuỗi hoặc thiếu → cùng thông báo như trống.
- R-AUT-05: Tên đăng nhập không tồn tại hoặc mật khẩu sai → 401 `INVALID_CREDENTIALS`, "Tên đăng nhập hoặc mật khẩu không đúng". Hai trường hợp trả giống hệt nhau; với tên không tồn tại vẫn chạy `verify` trên một chuỗi băm giả để thời gian xử lý tương đương.
- R-AUT-06: Giới hạn đăng nhập sai, tính theo tên đăng nhập đã chuẩn hóa (cả tên không tồn tại, để không lộ tên nào có thật):
  - 5 lần sai trong cửa sổ 15 phút (tính từ lần sai đầu của cửa sổ) → khóa 15 phút; lần sai thứ 5 trả ngay 429;
  - đang khóa: mọi lần đăng nhập tên đó (kể cả đúng mật khẩu) → 429 `LOGIN_LOCKED`, "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." (cùng câu cho màn Đăng nhập và Đổi mật khẩu, R-AUT-20), `<n>` = số phút còn lại làm tròn lên, tối thiểu 1; header `Retry-After` = số giây còn lại làm tròn lên. Không kiểm mật khẩu, không đếm thêm, không kéo dài khóa;
  - hết khóa: bộ đếm bắt đầu lại từ 0;
  - đăng nhập đúng → xóa bộ đếm của tên đó;
  - phiên đang có của tài khoản không bị ảnh hưởng;
  - nhập sai mật khẩu hiện tại khi đổi mật khẩu cũng đếm vào bộ đếm này (R-AUT-20);
  - đồng thời (câu hỏi mở 7): mọi lần đọc để ghi bộ đếm chạy trong transaction có khóa dòng (`SELECT … FOR UPDATE` / upsert) và kiểm lại khóa ngay trong transaction đó:
    - ghi lần sai (`recordFailure`): đang khóa → trả 429, không đếm, không kéo dài khóa;
    - đúng mật khẩu (`confirmSuccess`, cả đăng nhập và đổi mật khẩu): đang khóa → trả 429, không tạo phiên, không đổi mật khẩu;
    - nên nhiều request gửi cùng lúc chỉ có tối đa 5 lần sai được tính; request đã qua `verify` mà gặp khóa lúc ghi luôn nhận 429 dù mật khẩu đúng hay sai, nên người dò không biết kết quả của các lần đoán vượt quá 5.
- R-AUT-07: Tên đăng nhập được chuẩn hóa (bỏ khoảng trắng hai đầu, đổi chữ thường) trước khi tra cứu, đếm R-AUT-06 và lưu. Mật khẩu giữ nguyên, không bỏ khoảng trắng.
- R-AUT-08: Đăng nhập đúng → tạo phiên (R-AUT-09), trả 201 kèm người dùng. Nếu `needsRehash` của chuỗi băm đang lưu là đúng → băm lại mật khẩu bằng tham số hiện tại và lưu. Request mang cookie của một phiên còn hiệu lực (đăng nhập lại ở tab khác, đổi tài khoản qua API) → xóa phiên đó, phiên mới thay thế.

Phiên:

- R-AUT-09: Phiên và cookie (ADR 0015):
  - token: 32 byte ngẫu nhiên (`crypto.randomBytes`), mã hóa base64url; DB chỉ lưu SHA-256 dạng hex của token (`user_sessions.token_hash`);
  - cookie `mio_session`: `HttpOnly`, `SameSite=Lax`, `Path=/`, `Max-Age` = số giây tới `expires_at`; thêm `Secure` khi `PUBLIC_URL` bắt đầu bằng `https://`;
  - một người dùng có nhiều phiên cùng lúc (mỗi thiết bị một phiên).
- R-AUT-10: Hết hạn trượt: phiên hết hạn sau 90 ngày kể từ lần gia hạn gần nhất. Request hợp lệ mà lần gia hạn gần nhất (`updated_at`) cũ hơn 24 giờ → đặt `expires_at` = bây giờ + 90 ngày, `updated_at` = bây giờ, gửi lại cookie với `Max-Age` mới. Chỉ gia hạn ở route có `@Roles(...)`; route `@Public()` đọc phiên nhưng không gia hạn. Không có hạn tuyệt đối (câu hỏi mở 1).
- R-AUT-11: Request tới route không công khai mà không có cookie, token không khớp phiên nào, hoặc phiên đã hết hạn (`expires_at` ≤ bây giờ) → 401 `UNAUTHENTICATED`, "Bạn chưa đăng nhập hoặc phiên đăng nhập đã hết hạn". Có cookie nhưng không hợp lệ → response kèm xóa cookie (`Max-Age=0`). Phiên hết hạn gặp lúc kiểm tra thì xóa khỏi DB.
- R-AUT-12: Đăng xuất (`DELETE /api/v1/sessions/current`) là route công khai và idempotent: có phiên thì xóa phiên đó; luôn xóa cookie và trả 204, kể cả khi không có hoặc phiên đã hết hạn.
- R-AUT-13: Dọn dữ liệu, không cần job: mỗi lần đăng nhập thành công xóa mọi phiên đã hết hạn (`SessionService.deleteExpired`); mỗi lần xử lý đăng nhập xóa dòng `login_throttles` không còn khóa và có `updated_at` cũ hơn 24 giờ (`deleteStale`).

Phân quyền:

- R-AUT-14: Mặc định từ chối: mọi route dưới `/api/v1` phải có `@Public()` hoặc `@Roles(...)` (ở handler hoặc controller). Lúc khởi động, `RouteAccessCheck` liệt kê route thiếu khai báo → api ghi log lỗi và thoát mã 1, thông báo "Route chưa khai báo quyền: <METHOD> <path>" (mỗi route một dòng), không mở cổng.
- R-AUT-15: Đã đăng nhập nhưng vai trò không nằm trong `@Roles(...)` → 403 `FORBIDDEN`, "Bạn không có quyền thực hiện thao tác này". Thứ tự kiểm tra: R-AUT-17 → đọc thân request (`INVALID_JSON`, `PAYLOAD_TOO_LARGE`, R-SKL-15) → R-AUT-11 → R-AUT-15 → kiểm tra dữ liệu.
- R-AUT-16: Quyền của các route trong tính năng này:
  - công khai: `GET /api/v1/health` (R-SKL-13), `POST /api/v1/sessions`, `DELETE /api/v1/sessions/current`;
  - Quản lý, Thợ: `GET /api/v1/sessions/current`, `POST /api/v1/users/me/change-password`;
  - route của tính năng sau theo 07 mục 1 "Quyền của vai trò Thợ": Cài đặt và Nhật ký hệ thống chỉ Quản lý.
  - Đường dẫn `/api/...` không có route vẫn trả 404 `NOT_FOUND` (R-SKL-15) dù chưa đăng nhập. File tĩnh của web (R-SKL-14) không cần đăng nhập; dữ liệu chỉ lấy qua API có kiểm quyền.
- R-AUT-17: Chống CSRF (cùng `SameSite=Lax`): request `POST`, `PUT`, `PATCH`, `DELETE` tới `/api/` có header `Origin` khác origin của `PUBLIC_URL` (so scheme, host, cổng) → 403 `INVALID_ORIGIN`, "Yêu cầu bị từ chối: hãy mở app bằng địa chỉ <PUBLIC_URL>". Áp dụng cả route công khai. Request không có `Origin` (CLI, curl) được đi tiếp.
- R-AUT-18: Header bảo mật trên mọi response của api: `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin`. Mọi response của `/api/v1/sessions*` và `/api/v1/users/me/*` thêm `Cache-Control: no-store`.

Đổi mật khẩu:

- R-AUT-19: Mật khẩu hiện tại trống → lỗi "Nhập mật khẩu hiện tại"; dài hơn 128 ký tự → lỗi "Mật khẩu tối đa 128 ký tự".
- R-AUT-20: Mật khẩu hiện tại không đúng → 400 `VALIDATION_ERROR`, `message` "Dữ liệu đổi mật khẩu không hợp lệ", `fields.currentPassword` "Mật khẩu hiện tại không đúng"; đếm một lần sai vào R-AUT-06 theo tên đăng nhập của người dùng. Tên đăng nhập đang bị khóa → 429 `LOGIN_LOCKED` với thông báo như R-AUT-06, không kiểm mật khẩu.
- R-AUT-21: Mật khẩu mới:
  - trống → lỗi "Nhập mật khẩu mới";
  - ngắn hơn 8 hoặc dài hơn 128 ký tự → lỗi "Mật khẩu mới phải từ 8 đến 128 ký tự";
  - giống tên đăng nhập (so sau khi đổi chữ thường) → lỗi "Mật khẩu không được trùng tên đăng nhập";
  - giống mật khẩu hiện tại (kiểm bằng `verify` sau khi mật khẩu hiện tại đúng) → lỗi "Mật khẩu mới phải khác mật khẩu hiện tại".
  - `currentPassword`, `newPassword` không phải chuỗi hoặc thiếu → cùng thông báo như trống ("Nhập mật khẩu hiện tại", "Nhập mật khẩu mới").
  - Thứ tự: kiểm hình thức (R-AUT-19, R-AUT-21 ba ý đầu) trả hết lỗi theo trường cùng lúc → kiểm khóa và mật khẩu hiện tại (R-AUT-20) → kiểm "khác mật khẩu hiện tại". Mọi lỗi theo trường trả 400 `VALIDATION_ERROR`, `message` "Dữ liệu đổi mật khẩu không hợp lệ".
- R-AUT-22: Chỉ trên web: Nhập lại mật khẩu mới trống → lỗi "Nhập lại mật khẩu mới"; khác Mật khẩu mới → lỗi "Mật khẩu nhập lại không khớp". API không nhận trường này.
- R-AUT-23: Đổi thành công → lưu chuỗi băm mới, xóa phiên hiện tại, tạo phiên mới cho thiết bị đang dùng và đặt cookie mới, xóa bộ đếm R-AUT-06, trả 204.
  - Xếp hàng: kiểm khóa, kiểm mật khẩu hiện tại và mọi lần ghi chạy trong một transaction, khóa dòng `users` của người dùng (`lockById`) trước khi đọc chuỗi băm. Hai lần đổi cùng lúc (hai thiết bị, hoặc đổi cùng lúc với `reset-password`) chạy lần lượt; lần sau kiểm mật khẩu hiện tại với chuỗi băm lần trước vừa ghi, nên chỉ một lần báo thành công và mật khẩu dùng được đúng là mật khẩu của lần đó.
  - Phiên của các thiết bị khác:
    - `signOutOtherDevices` = `true`: xóa hết; các thiết bị đó nhận 401 ở request kế tiếp;
    - `signOutOtherDevices` = `false`: giữ nguyên, các thiết bị đó vẫn dùng được tới khi hết hạn hoặc đăng xuất;
  - `signOutOtherDevices` thiếu hoặc không phải boolean → 400 `VALIDATION_ERROR`, `fields.signOutOtherDevices` "Chọn có đăng xuất các thiết bị khác hay không" (web luôn gửi trường này, R-AUT-34).
- R-AUT-24: Đổi mật khẩu và đăng xuất trên thiết bị khác chạy đồng thời: phiên bị xóa trước khi request đổi mật khẩu kiểm tra phiên thì request đó nhận 401; đã qua kiểm tra phiên thì đổi mật khẩu vẫn thành công.

Lệnh CLI (chạy trong container api: `docker compose exec -it api node dist/cli.js <lệnh>`):

- R-AUT-25: `create-user --username <tên> --role <manager|technician> --display-name "<tên hiển thị>"`; mật khẩu nhập theo R-AUT-27. In mọi lỗi (mỗi lỗi một dòng) rồi thoát mã 1. Thứ tự:
  - kiểm tham số trước (thiếu, sai định dạng, tên đã tồn tại);
  - stdin là terminal: tham số có lỗi thì in lỗi và thoát, không hỏi mật khẩu; tham số đúng mới hỏi mật khẩu rồi kiểm mật khẩu;
  - stdin không phải terminal: vẫn đọc mật khẩu, in lỗi tham số và lỗi mật khẩu cùng lúc;
  - các lỗi:
    - thiếu `--username` → "Thiếu --username"; tên (sau R-AUT-07) không khớp `^[a-z0-9._-]{3,32}$` → "Tên đăng nhập phải dài 3–32 ký tự, chỉ gồm chữ thường không dấu, số, dấu chấm, gạch dưới, gạch ngang"; đã có → "Tên đăng nhập đã tồn tại: <tên>" (DB unique chặn cả khi tạo đồng thời);
    - thiếu `--role` → "Thiếu --role"; giá trị khác `manager`, `technician` → "Vai trò phải là manager hoặc technician";
    - thiếu `--display-name` → "Thiếu --display-name"; sau khi bỏ khoảng trắng hai đầu dài 0 hoặc hơn 50 ký tự → "Tên hiển thị phải từ 1 đến 50 ký tự";
    - mật khẩu: dài dưới 8 hoặc hơn 128 ký tự → "Mật khẩu phải từ 8 đến 128 ký tự"; giống tên đăng nhập → "Mật khẩu không được trùng tên đăng nhập";
  - thành công: in "Đã tạo tài khoản <tên> (<Quản lý|Thợ>)", thoát mã 0.
- R-AUT-26: `reset-password --username <tên>` (mật khẩu nhập theo R-AUT-27) và `list-users`:
  - thiếu `--username` → "Thiếu --username"; không có tài khoản → "Không tìm thấy tài khoản: <tên>", thoát mã 1; thứ tự kiểm tham số và hỏi mật khẩu như R-AUT-25;
  - mật khẩu: quy tắc như R-AUT-25;
  - thành công: trong một transaction khóa dòng `users` (`lockByUsername`, xếp hàng với đổi mật khẩu R-AUT-23), lưu chuỗi băm mới, xóa mọi phiên của tài khoản, xóa bộ đếm R-AUT-06 (`reset`), in "Đã đặt lại mật khẩu cho <tên>. Mọi phiên đăng nhập của tài khoản đã bị đăng xuất.", thoát mã 0.
  - `list-users`: in mỗi tài khoản một dòng "<tên đăng nhập> | <Quản lý|Thợ> | <tên hiển thị>", sắp theo tên đăng nhập; chưa có tài khoản nào → "Chưa có tài khoản nào."
- R-AUT-27: Nhập mật khẩu cho CLI (không nhận mật khẩu qua tham số dòng lệnh, để không lưu vào lịch sử shell):
  - stdin là terminal: hỏi "Mật khẩu: " rồi "Nhập lại mật khẩu: ", không hiện ký tự gõ; hai lần khác nhau → "Mật khẩu nhập lại không khớp", thoát mã 1;
  - stdin không phải terminal (dùng trong script, test): đọc dòng đầu tiên, bỏ `\r\n` cuối, không hỏi nhập lại; stdin rỗng → "Thiếu mật khẩu", thoát mã 1.
  - Tham số không biết (ví dụ `--password`) → "Tham số không hợp lệ: <tham số>", thoát mã 1.
- R-AUT-33: Lệnh CLI không đòi đăng nhập web: ai chạy được `docker compose exec api …` (có quyền vào máy chạy Docker) thì dùng được `create-user`, `reset-password`, `list-users` cho mọi tài khoản, kể cả tài khoản của chính mình. Đây là đường khôi phục duy nhất khi mọi Quản lý quên mật khẩu. Không có cổng mạng nào mở cho CLI.
- R-AUT-34: Đổi mật khẩu trên web luôn qua hộp thoại xác nhận "có đăng xuất các thiết bị khác không" (mục Màn hình Đổi mật khẩu); lựa chọn được gửi trong `signOutOtherDevices` (R-AUT-23). Lựa chọn mặc định (nút được focus sẵn) là đăng xuất.

Web:

- R-AUT-28: Chưa đăng nhập (`GET /api/v1/sessions/current` trả 401) mà mở trang cần đăng nhập → chuyển `/login?next=<đường dẫn + query hiện tại, mã hóa URL>`. Banner khi chuyển: theo R-AUT-31. Đăng nhập xong chuyển tới `next` nếu thỏa cả:
  - bắt đầu bằng `/`, không bắt đầu bằng `//` hay `/\`;
  - không chứa ký tự điều khiển (U+0000–U+001F, U+007F) hay khoảng trắng (trình duyệt tự bỏ tab, xuống dòng nên `/<tab>/evil.example` thành `//evil.example`);
  - không phải `/login`.
  - Không thỏa → chuyển `/`. Chuyển bằng router của app (`navigate`), không dùng `location.href`.
  - Đã đăng nhập mà mở `/login` → chuyển `/`.
- R-AUT-29: Thanh điều hướng chỉ hiện mục mà vai trò được dùng. Mở trực tiếp đường dẫn của trang không dành cho vai trò mình → màn hình Không có quyền (đường dẫn giữ nguyên). API trả 403 `FORBIDDEN` khi đang thao tác (theo `ui-style.md` mục "Vị trí thông báo", ADR 0016):
  - gửi form → banner danger với `message` của API ở vùng thông báo của form (ngay trên hàng nút gửi), giữ dữ liệu trên form;
  - thao tác không có form (nút trong danh sách, công tắc có hiệu lực ngay) → toast danger với `message` của API;
  - cả hai: gọi `refresh()` của `auth-provider` để thanh điều hướng và màn hình Không có quyền theo vai trò mới.
- R-AUT-30: Log (bổ sung R-SKL-17):
  - mọi sự kiện có trường `event` (tên sự kiện bên dưới) và `time`; sự kiện từ request HTTP có thêm `requestId` của R-SKL-17, `ip` (`req.ip`) và `userAgent` (header `User-Agent`, cắt còn 200 ký tự);
  - theo dõi tấn công dò mật khẩu (mỗi lần sai, mỗi lần bị chặn vì đang khóa, mỗi lần bắt đầu khóa đều có đúng một dòng log):
    - `auth.login.failed` (warn): `username` đã chuẩn hóa, `userExists` (true/false), `reason` = `invalid_credentials` (sai tên hoặc mật khẩu) hoặc `locked` (bị chặn vì đang khóa), `failedCount` (số lần sai trong cửa sổ tính cả lần này: 1–5; lần làm khóa ghi `5` kèm `lockedUntil`; không có khi `locked`), `lockedUntil` (khi `locked` hoặc lần này làm khóa);
    - `auth.lock.started` (warn): `username`, `userExists`, `source` = `login` hoặc `change_password`, `lockedUntil`; ghi ngay khi lần sai thứ 5 làm khóa (cùng request với dòng `failed` của lần đó);
    - `auth.password.change_failed` (warn): `userId`, `username`, `reason` = `current_password_incorrect` hoặc `locked`, `failedCount` / `lockedUntil` như trên;
  - sự kiện khác (info): `auth.login.succeeded` (`userId`, `username`), `auth.logout` (`userId` nếu có), `auth.password.changed` (`userId`, `signedOutOtherDevices`), `auth.cli.user_created`, `auth.cli.password_reset` (`username`);
  - log của lệnh CLI: lệnh chạy bằng `docker compose exec` là tiến trình riêng, stdout của nó chỉ ra terminal của người gõ. Vì vậy:
    - stdout của lệnh chỉ in thông báo cho người đọc (R-AUT-25 … R-AUT-27), không in dòng log JSON;
    - dòng log JSON (`auth.cli.*`, lỗi) ghi vào `/proc/1/fd/1` (stdout của tiến trình chính của container: Node là PID 1 theo R-SKL-22, cùng uid 1000) để vào log Docker của container api; mở `/proc/1/fd/1` không được thì ghi ra stderr của lệnh. Cần kiểm chứng khi implement;
    - sự kiện CLI không có `requestId`, `ip`, `userAgent`;
  - lọc khi điều tra: `docker compose logs api | grep '"event":"auth.'` ra cả sự kiện HTTP lẫn sự kiện CLI (log nằm trong log Docker của container api, giữ tối đa 10 MB × 5 file theo R-SKL-26);
  - giai đoạn 0 `ip` luôn là địa chỉ gateway của Docker (cổng chỉ mở trên `127.0.0.1`); khi triển khai sau reverse proxy phải bật `trust proxy` để `req.ip` là IP thật của người gửi;
  - không bao giờ ghi mật khẩu, token, chuỗi băm, giá trị cookie, thân request;
  - danh sách `redact` thêm `currentPassword`, `newPassword`, `confirmPassword` ở độ sâu 1 đến 3 (cùng cách khai báo với `password`).
- R-AUT-31: Phiên không còn dùng được → banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" (câu trung tính, đúng cho hết hạn, bị đăng xuất do đổi hoặc đặt lại mật khẩu, tài khoản bị xóa, cookie hỏng). Web không đọc được cookie (`HttpOnly`) và phiên hết hạn tự nhiên thì trình duyệt tự bỏ cookie, nên web dùng cờ `mio.hadSession` trong `localStorage` (câu hỏi mở 8):
  - đặt cờ khi `GET /api/v1/sessions/current` trả 200; xóa cờ khi bấm "Đăng xuất" (trước khi gọi API, R-AUT-32) và khi đã dùng cờ để hiện banner;
  - đọc, ghi cờ trong try/catch; lỗi (trình duyệt chặn lưu dữ liệu) thì coi như không có cờ, không báo lỗi;
  - mở hoặc tải lại app, `GET /api/v1/sessions/current` trả 401: có cờ → xóa cờ, chuyển `/login?next=…` kèm banner; không có cờ (chưa từng đăng nhập trên trình duyệt này, hoặc đã tự đăng xuất) → chuyển, không banner;
  - đang dùng (đã có người dùng trong `auth-provider`), request API bất kỳ trả 401 → xóa người dùng và cờ, chuyển `/login?next=<trang hiện tại>` kèm banner (không phụ thuộc cờ). Dữ liệu đang nhập dở trên form bị mất (chấp nhận);
  - banner giữ trong `loginNotice` (bộ nhớ của `auth-provider`), không đưa vào URL hay `history.state`; hiện một lần, tải lại `/login` thì không còn.
- R-AUT-32: Bấm "Đăng xuất" → xóa cờ `mio.hadSession`, gọi `DELETE /api/v1/sessions/current`:
  - 204 → chuyển `/login` kèm banner info "Bạn đã đăng xuất";
  - lỗi mạng hoặc 500 → vẫn chuyển `/login` nhưng không có banner "Bạn đã đăng xuất" (phiên và cookie có thể còn, lần mở sau sẽ tự vào lại; chấp nhận).

## Job và hàng đợi

Không áp dụng: không có việc chạy nền. Dọn phiên hết hạn và bộ đếm cũ làm ngay trong lúc đăng nhập (R-AUT-13).

## Trạng thái và thuật toán

### Phiên

- Trạng thái: không có phiên → còn hiệu lực → (hết hạn | bị xóa).
- Chuyển hợp lệ:
  - không có phiên → còn hiệu lực: đăng nhập đúng (R-AUT-08), đổi mật khẩu thành công (phiên mới thay phiên hiện tại, R-AUT-23);
  - còn hiệu lực → còn hiệu lực (gia hạn): R-AUT-10;
  - còn hiệu lực → hết hạn: 90 ngày không gia hạn;
  - còn hiệu lực → bị xóa: đăng xuất (R-AUT-12); đổi mật khẩu (phiên hiện tại luôn bị thay, phiên thiết bị khác khi chọn đăng xuất, R-AUT-23); `reset-password` (R-AUT-26);
  - hết hạn → bị xóa: R-AUT-11, R-AUT-13.
- Chuyển không hợp lệ: hết hạn hoặc bị xóa → còn hiệu lực (không khôi phục, phải đăng nhập lại).

### Bộ đếm đăng nhập sai (theo tên đăng nhập)

- Trạng thái: bình thường (không có dòng hoặc `failed_count` 0–4) → bị khóa (`locked_until` > bây giờ) → bình thường (hết khóa, bộ đếm từ 0).
- Chuyển hợp lệ:
  - bình thường → bình thường: lần sai thứ 1–4 trong cửa sổ; cửa sổ quá 15 phút thì bắt đầu lại; đăng nhập hoặc đổi mật khẩu đúng thì xóa bộ đếm;
  - bình thường → bị khóa: lần sai thứ 5 trong cửa sổ;
  - bị khóa → bình thường: hết 15 phút; `reset-password` (R-AUT-26).
- Chuyển không hợp lệ: bị khóa → bị khóa (kéo dài khóa hoặc đếm thêm khi đang khóa); bị khóa → bình thường do đăng nhập hoặc đổi mật khẩu đúng (vẫn trả 429).
- Thuật toán `recordFailure(username, tx?)` (trong transaction, khóa dòng):
  1. Đọc dòng của `username` bằng `SELECT … FOR UPDATE`; không có thì tạo `{ failed_count: 0, window_started_at: bây giờ }`.
  2. Nếu `locked_until` > bây giờ (đang khóa): không đổi gì; trả `{ isAlreadyLocked: true, lockedUntil }`.
  3. Nếu `window_started_at` ≤ bây giờ − 15 phút, hoặc `locked_until` không rỗng và ≤ bây giờ (khóa cũ đã hết): đặt `failed_count = 0`, `window_started_at = bây giờ`, `locked_until = null`.
  4. `failed_count += 1`; ghi nhớ giá trị này là `failedCount` trả về.
  5. Nếu `failed_count` ≥ 5: `locked_until = bây giờ + 15 phút`, `failed_count = 0`.
  6. Ghi lại, `updated_at = bây giờ`; trả `{ failedCount, lockedUntil, isAlreadyLocked: false }` (`lockedUntil` khác null nghĩa là lần này làm khóa).
- Thuật toán `confirmSuccess(username, tx?)` (trong transaction, khóa dòng): đọc dòng bằng `SELECT … FOR UPDATE`; `locked_until` > bây giờ → trả khóa, không đổi gì; ngược lại xóa dòng (nếu có).
- `getLock(username)`: có dòng và `locked_until` > bây giờ → trả khóa. Chỉ để trả 429 sớm, không thay cho bước kiểm lại trong transaction.

### Đăng nhập (`AuthService.login`)

1. Kiểm hình thức bằng `loginInputSchema` (R-AUT-01 … R-AUT-04); lỗi → 400.
2. Chuẩn hóa tên (R-AUT-07); dọn bộ đếm cũ (R-AUT-13).
3. `getLock` → đang khóa: 429 (R-AUT-06).
4. Tìm người dùng; không có → `verify` trên chuỗi băm giả, rồi bước 6.
5. `verify` (chuỗi băm hỏng → 500, mục Xử lý lỗi); đúng → bước 7.
6. Sai → `recordFailure`: `isAlreadyLocked` → 429 (log `reason: locked`); lần này làm khóa → 429; còn lại → 401.
7. Đúng → transaction: `confirmSuccess`; đang khóa → 429 (log `auth.login.failed`, `reason: locked`), không tạo phiên. Không khóa → băm lại nếu cần (R-AUT-08), xóa phiên của cookie đang gửi nếu còn hiệu lực (R-AUT-08), `deleteExpired`, tạo phiên; commit; đặt cookie, trả 201.

### Đổi mật khẩu (`AuthService.changePassword`)

1. Kiểm hình thức bằng `changePasswordInputSchema` (R-AUT-19, R-AUT-21 ba ý đầu, R-AUT-23 `signOutOtherDevices`); lỗi → 400 với mọi lỗi theo trường.
2. `getLock(username)` → đang khóa: 429.
3. Mở transaction; `lockById(tx, userId)` (xếp hàng với lần đổi khác và `reset-password`, R-AUT-23); không còn người dùng → 401.
4. `verify(currentPassword)` trên chuỗi băm vừa đọc (chuỗi băm hỏng → 500). Sai → `recordFailure(username, tx)`, commit; `isAlreadyLocked` hoặc lần này làm khóa → 429; còn lại → 400 `fields.currentPassword` "Mật khẩu hiện tại không đúng".
5. `confirmSuccess(username, tx)`; đang khóa → 429, không đổi gì.
6. `verify(newPassword)` trên chuỗi băm hiện tại đúng → 400 `fields.newPassword` "Mật khẩu mới phải khác mật khẩu hiện tại" (không đếm).
7. Lưu chuỗi băm mới; xóa phiên hiện tại; `signOutOtherDevices` = `true` thì xóa mọi phiên khác; tạo phiên mới; commit; đặt cookie, trả 204.

### Kiểm tra request (`AuthGuard`)

1. Route `@Public()` → đi tiếp (vẫn đọc phiên nếu có, để `DELETE /sessions/current` và `POST /sessions` biết phiên nào cần xóa; không gia hạn, R-AUT-10).
2. Lấy token từ cookie `mio_session`; không có → 401.
3. Tìm phiên theo `sha256(token)`, nối bảng `users`; không có hoặc hết hạn → xóa phiên hết hạn (nếu có), xóa cookie, 401.
4. Gia hạn nếu cần (R-AUT-10).
5. Kiểm vai trò theo `@Roles(...)` → sai: 403.
6. Gắn `req.user`.

## Tích hợp bên ngoài

Không áp dụng: đăng nhập không dùng dịch vụ ngoài (không đăng nhập bằng Facebook/Google, không gửi email đặt lại mật khẩu).

## Xử lý lỗi, log, bảo mật, phân quyền

- Lỗi:
  - DB không truy cập được khi đăng nhập hoặc kiểm phiên → 500 `INTERNAL_ERROR` (R-SKL-16, R-SKL-30); web hiện banner/toast "Lỗi hệ thống, vui lòng thử lại sau";
  - web mất mạng khi gửi form → banner danger "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại.", giữ dữ liệu trên form;
  - cookie bị tắt trên trình duyệt: đăng nhập trả 201 nhưng `GET /sessions/current` ngay sau đó trả 401 → web hiện banner danger "Trình duyệt đang chặn cookie. Bật cookie cho trang này rồi đăng nhập lại.";
  - `users.password_hash` không phải chuỗi PHC hợp lệ (câu hỏi mở 9): `verify` ném lỗi → 500 `INTERNAL_ERROR` (R-SKL-16), log mức error có `userId` (không có chuỗi băm); không đếm vào R-AUT-06, không ghi `auth.login.failed` / `auth.password.change_failed`; áp dụng cả đăng nhập và đổi mật khẩu. Sửa bằng `reset-password`.
- Log: R-AUT-30.
- Bảo mật:
  - băm mật khẩu argon2id (04 mục 7), tham số ở mục Tham số cài đặt; tự băm lại khi tham số đổi (R-AUT-08);
  - token phiên chỉ lưu dạng SHA-256, nên bản sao lưu DB không chứa token dùng được (ADR 0015);
  - chống dò tên đăng nhập: thông báo và thời gian giống nhau (R-AUT-05), giới hạn áp cả tên không tồn tại (R-AUT-06);
  - chống CSRF: `SameSite=Lax` + R-AUT-17; chống nhúng khung: R-AUT-18;
  - HTTPS và cookie `Secure` tự bật khi `PUBLIC_URL` là `https://` (lúc triển khai lên máy chủ, ADR 0009);
  - chưa giới hạn theo IP: giai đoạn 0 mọi request tới từ cùng một địa chỉ (cổng chỉ mở trên `127.0.0.1`, R-SKL-19), xem câu hỏi mở 2.
- Phân quyền: R-AUT-14, R-AUT-15, R-AUT-16, R-AUT-29.

## Tham số cài đặt

Tính năng không thêm khóa vào `app_settings` (07 mục 2 không liệt kê tham số đăng nhập để chỉnh trên web). Các hằng đặt trong `@mio/shared` (`src/auth/constants.ts`) hoặc api:

- Thời hạn phiên (trượt): 90 ngày. Nguồn: quyết định mới, hiện thực "giữ đăng nhập lâu dài trên điện thoại" (07 Yêu cầu chung); câu hỏi mở 1.
- Chu kỳ gia hạn phiên tối thiểu: 24 giờ. Nguồn: quyết định mới (giảm ghi DB).
- Giới hạn đăng nhập sai: 5 lần trong 15 phút, khóa 15 phút, theo tên đăng nhập. Nguồn: 04 mục 7 (có giới hạn), con số là quyết định mới; câu hỏi mở 2.
- Giữ dòng bộ đếm không khóa: 24 giờ. Nguồn: quyết định mới.
- Tên đăng nhập: 3–32 ký tự, `^[a-z0-9._-]+$`. Tên hiển thị: 1–50 ký tự. Mật khẩu: 8–128 ký tự. Nguồn: quyết định mới.
- argon2id: `memoryCost` 19456 KiB, `timeCost` 2, `parallelism` 1 (mức tối thiểu khuyến nghị của OWASP). Thư viện `@node-rs/argon2` (có bản dựng sẵn cho linux x64 và arm64, không cần biên dịch). Nguồn: 04 mục 7 (argon2 hoặc bcrypt), chọn argon2id là quyết định mới.
- Tên cookie: `mio_session`. Nguồn: ADR 0015.

## Câu hỏi mở

- [x] 1. Thời hạn giữ đăng nhập? — đã chốt 2026-10-31 theo đề xuất: hết hạn sau 90 ngày không mở app (mỗi lần dùng tự gia hạn), không có hạn tuyệt đối. Thợ chủ yếu dùng Messenger, có thể vài tuần mới mở web app.
- [x] 2. Giới hạn đăng nhập sai? — đã chốt 2026-10-31 theo đề xuất: 5 lần sai trong 15 phút thì khóa tên đăng nhập đó 15 phút; chưa giới hạn theo IP ở giai đoạn 0, bổ sung khi triển khai lên máy chủ (cần đọc IP thật qua reverse proxy).
- [x] 3. 07 mục 2 đặt "Đổi mật khẩu" trong Cài đặt (chỉ Quản lý), nhưng Thợ cũng cần đổi mật khẩu của mình. — đã chốt 2026-10-31 theo đề xuất: đưa "Đổi mật khẩu" ra khối tài khoản trên thanh điều hướng, cả hai vai trò dùng được; Cài đặt › Người dùng ở giai đoạn 2 chỉ còn quản lý tài khoản thợ.
- [x] 4. Quên mật khẩu? — đã chốt 2026-10-31 theo đề xuất: không có luồng tự đặt lại (không có email người dùng); người quản trị app (Hải) đặt lại bằng lệnh `reset-password` (R-AUT-26). Giai đoạn 2 thêm nút Quản lý đặt lại mật khẩu cho thợ trên web.
  - Bổ sung 2026-10-31 (người dùng hỏi: Hải cũng quên mật khẩu thì sao?): lệnh CLI không cần mật khẩu web, chỉ cần quyền vào máy chạy Docker (`docker compose exec`), nên Hải tự đặt lại mật khẩu của mình bằng `reset-password` như mọi tài khoản khác (R-AUT-33). Chỉ khi mất quyền vào máy (mật khẩu hệ điều hành, khóa SSH khi đã lên máy chủ) mới không đặt lại được; việc đó nằm ngoài app.
- [x] 5. ADR `0015-server-side-sessions` (phiên lưu trong PostgreSQL, cookie mang token, kiểm tra `Origin`) — đã chốt 2026-10-31: chấp nhận.
- [x] 6. Lưu sự kiện đăng nhập sai / bị khóa vào DB để Quản lý theo dõi trên web? — đã chốt 2026-10-31: giai đoạn 0 chỉ ghi log (R-AUT-30); lưu DB và hiển thị trên Nhật ký hệ thống để sau, khi làm Nhật ký hệ thống đầy đủ.
- [x] 7. (phát hiện ở `/test-case-design`, P0-AUT-023) Nhiều request sai gửi đồng thời: `getLock` nằm ngoài transaction và trước `verify`, `recordFailure` vẫn đếm khi đang khóa → có thể quá 5 lần đoán, khóa lần hai kéo dài khóa, request đúng mật khẩu lọt qua sau khi đã khóa. — đã chốt 2026-10-31: sửa thuật toán, kiểm khóa lại trong cùng transaction có khóa dòng; đang khóa thì trả 429, không đếm, không cho đăng nhập. Đã sửa R-AUT-06 và mục Trạng thái ở `/design-review` (RV-01).
- [x] 8. (phát hiện ở `/test-case-design`, P0-AUT-028) Phiên hết hạn hoặc bị xóa, phát hiện lúc mở hoặc tải lại app (chưa nạp người dùng) có hiện banner "Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại" không? — đã chốt 2026-10-31: có, mọi lần app tự đưa về `/login` vì phiên không còn dùng được đều hiện banner này. Chưa từng đăng nhập (không có cookie) thì không hiện. Đã sửa R-AUT-31 ở `/design-review` (RV-02): web dùng cờ `mio.hadSession` trong `localStorage`; trình duyệt chặn lưu dữ liệu thì không hiện banner (người dùng chấp nhận). Câu banner đổi thành "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" (RV-12).
- [x] 9. (phát hiện ở `/test-case-design`, P0-AUT-075) `password_hash` trong DB không phải chuỗi PHC hợp lệ → đã chốt 2026-10-31: 500 `INTERNAL_ERROR` (R-SKL-16), không coi là sai mật khẩu.

## Lịch sử thay đổi

- 2026-10-31: tạo mới
- 2026-10-31: chốt câu hỏi 1, 2, 3, 4, 5; ADR 0015 chuyển `chấp nhận`; thêm R-AUT-33 (CLI là đường khôi phục khi quên mật khẩu, trả lời câu hỏi 4)
- 2026-10-31: theo góp ý của người dùng: thêm hộp thoại xác nhận đăng xuất thiết bị khác khi đổi mật khẩu (R-AUT-34, sửa R-AUT-23, thêm trường `signOutOtherDevices`); R-AUT-30 bổ sung `ip`, `userAgent`, `userExists`, `failedCount`, sự kiện `auth.lock.started` có `source` để theo dõi tấn công dò mật khẩu
- 2026-10-31: chốt câu hỏi 6 (chỉ ghi log, lưu DB để sau); duyệt thiết kế
- 2026-10-31: `/ui-design auth`: thêm màn hình chờ và màn hình lỗi khi nạp phiên lúc mở app (mục Khung app), dẫn link mockup và component
- 2026-10-31: theo góp ý duyệt UI: vùng thông báo (banner) của màn Đăng nhập và Đổi mật khẩu chuyển xuống ngay trên nút gửi; thông báo `LOGIN_LOCKED` (R-AUT-06) đổi thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." để đúng nghĩa ở cả màn Đổi mật khẩu
- 2026-10-31: `/test-case-design auth`: thêm và chốt câu hỏi 7, 8, 9; nội dung quy tắc chưa sửa, chờ `/design-review`
- 2026-10-31: `/design-review auth` (`reviews/auth-review.md`):
  - RV-01: R-AUT-06 và thuật toán bộ đếm kiểm lại khóa trong transaction (`recordFailure`, `confirmSuccess`); thêm chuyển trạng thái, thuật toán đổi mật khẩu;
  - RV-02, RV-12: R-AUT-31 dùng cờ `mio.hadSession`, banner trong bộ nhớ, câu "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại";
  - RV-03: mục Xử lý lỗi thêm chuỗi băm hỏng;
  - RV-04: R-AUT-23, R-AUT-26 khóa dòng `users`;
  - RV-05: R-AUT-30 `failedCount` của lần làm khóa là 5;
  - RV-06: R-AUT-15 thêm bước đọc thân request; kiểm `Origin` trước body parser;
  - RV-07: R-AUT-21 trường sai kiểu;
  - RV-08: R-AUT-02 đo độ dài sau khi chuẩn hóa;
  - RV-09: R-AUT-30 log CLI ghi vào `/proc/1/fd/1`;
  - RV-10: R-AUT-32 chỉ hiện "Bạn đã đăng xuất" khi 204;
  - RV-11: R-AUT-29 403 khi gửi form hiện banner, gọi `refresh()`;
  - RV-13: quy tắc chung mỗi trường một lỗi;
  - RV-14: R-AUT-28 chặn ký tự điều khiển trong `next`, chuyển bằng router;
  - RV-15: R-AUT-08 đăng nhập thay phiên cũ, R-AUT-10 route công khai không gia hạn;
  - RV-16: R-AUT-25, R-AUT-26 kiểm tham số trước khi hỏi mật khẩu
- 2026-10-31: duyệt thiết kế sau `/design-review` (Hải)
