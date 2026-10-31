> Bản đọc sinh từ docs/phases/phase-0/design/auth.md (phiên bản f58a178, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# Thiết kế chi tiết – Đăng nhập và phân quyền (`auth`, `AUT`)

- **Giai đoạn:** 0.
- **Trạng thái:** đã duyệt ngày 2026-10-31, sau bước duyệt thiết kế `/design-review`.
- **Tài liệu khái quát làm nền:**
  - 07-screens-and-settings.md: phần "Yêu cầu chung" (Đăng nhập, HTTPS), mục 1 "Quyền của vai trò Thợ", mục 1.9, 1.10 và mục 2 "Người dùng";
  - 03-data-model.md mục 1 "Người dùng";
  - 04-technical.md mục 7;
  - 05-roadmap.md giai đoạn 0 (đăng nhập hai vai trò);
  - 01-overview.md mục 6;
  - [ADR 0011](../../../decisions/0011-browser-worker-redis-only.md "Worker trình duyệt chỉ kết nối Redis") *(Worker trình duyệt chỉ kết nối Redis)*, 0012, 0015;
  - thiết kế `app-skeleton` ([R-SKL-14](app-skeleton.md#s-0f1edd606c "api phục vụ web") *(api phục vụ web)*, [R-SKL-15](app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*, [R-SKL-16](app-skeleton.md#s-0f1edd606c "lỗi không lường trước") *(lỗi không lường trước)*, [R-SKL-17](app-skeleton.md#s-0f1edd606c "log là JSON một dòng ra stdout") *(log là JSON một dòng ra stdout)*, `cli.ts`).

<a id="s-0100e30d6f"></a>

## Tóm tắt

- Chủ tiệm (vai trò Quản lý) và thợ (vai trò Thợ) đăng nhập web app bằng tên đăng nhập và mật khẩu.
- Đăng nhập được giữ lâu dài trên thiết bị. Người dùng tự đăng xuất và tự đổi mật khẩu được.
- Hệ thống chặn việc đoán mật khẩu bằng cách giới hạn số lần đăng nhập sai.
- Tính năng cung cấp cơ chế phân quyền theo vai trò cho mọi endpoint và màn hình của các tính năng sau. Tính năng cũng dựng khung app, gồm thanh điều hướng theo vai trò.
- Ở giai đoạn 0, tài khoản được tạo và đặt lại mật khẩu bằng lệnh CLI. Màn hình quản lý tài khoản thợ làm ở giai đoạn 2.

<a id="s-d14dee88c8"></a>

## Module và interface

Mục này mô tả các module và interface của tính năng, chia theo từng package.

<a id="s-b25af40da7"></a>

### `packages/shared` (`@mio/shared`), thư mục `src/auth/`

**Tóm tắt.** Package dùng chung chứa danh sách vai trò, các zod schema kiểm tra dữ liệu và hàm chuẩn hóa tên đăng nhập. API, web và CLI cùng dùng các schema này.

**Chi tiết kỹ thuật**

- Vai trò: `ROLES = ['manager', 'technician'] as const`, kiểu `type Role` và nhãn hiển thị `ROLE_LABELS = { manager: 'Quản lý', technician: 'Thợ' }`.
- Các zod schema dùng chung cho API, web và CLI. Thông báo lỗi lấy nguyên văn theo [mục Quy tắc](#s-0f1edd606c).
  - `loginInputSchema` nhận `{ username, password }` ([R-AUT-01](#s-0f1edd606c "Tên đăng nhập trống") *(Tên đăng nhập trống)*, [R-AUT-02](#s-0f1edd606c "Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự") *(Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự)*, [R-AUT-03](#s-0f1edd606c "Mật khẩu là chuỗi rỗng") *(Mật khẩu là chuỗi rỗng)*, [R-AUT-04](#s-0f1edd606c "Mật khẩu dài hơn 128 ký tự") *(Mật khẩu dài hơn 128 ký tự)*, [R-AUT-07](#s-0f1edd606c "Tên đăng nhập được chuẩn hóa trước khi tra cứu") *(Tên đăng nhập được chuẩn hóa trước khi tra cứu)*).
  - `changePasswordInputSchema` nhận `{ currentPassword, newPassword, signOutOtherDevices }` ([R-AUT-20](#s-0f1edd606c "Mật khẩu hiện tại không đúng") *(Mật khẩu hiện tại không đúng)*, [R-AUT-21](#s-0f1edd606c "Mật khẩu mới") *(Mật khẩu mới)*, [R-AUT-23](#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*).
  - `changePasswordFormSchema` thêm trường `confirmPassword` và chỉ web dùng ([R-AUT-22](#s-0f1edd606c "Chỉ trên web") *(Chỉ trên web)*).
  - `usernameSchema`, `displayNameSchema`, `passwordSchema` dành cho CLI ([R-AUT-25](#s-0f1edd606c "create-user --username <tên> --role <manager\|technician> --…") *(create-user --username \<tên\> --role \<manager\|technician\> --…)*).
  - `sessionUserSchema` mô tả người dùng của phiên: `{ id, username, displayName, role }`.
- `normalizeUsername(raw: string) -> string` bỏ khoảng trắng hai đầu và đổi sang chữ thường ([R-AUT-07](#s-0f1edd606c "Tên đăng nhập được chuẩn hóa trước khi tra cứu") *(Tên đăng nhập được chuẩn hóa trước khi tra cứu)*).

<a id="s-a05c9f45b5"></a>

### `apps/api` (`@mio/api`), module `src/modules/auth/`

**Tóm tắt.** Module `auth` của API lo việc băm mật khẩu, quản lý phiên, đếm số lần đăng nhập sai, xử lý đăng nhập và đổi mật khẩu. Module cũng phân quyền cho mọi route và cung cấp lệnh CLI quản lý tài khoản.

**Chi tiết kỹ thuật**

- `PasswordHasher` (`password-hasher.ts`) băm bằng argon2id qua thư viện `@node-rs/argon2`. Tham số nằm ở [mục Tham số cài đặt](#s-d0d46a0edb).
  - `hash(plain: string) -> Promise<string>` trả chuỗi PHC.
  - `verify(hash: string, plain: string) -> Promise<boolean>`.
  - `needsRehash(hash: string) -> boolean` trả đúng khi tham số trong chuỗi PHC khác tham số hiện tại.
- `UsersRepository` có các hàm:
  - `findByUsername(username) -> User | null` và `findById(id) -> User | null`;
  - `lockById(tx, id) -> User | null` và `lockByUsername(tx, username) -> User | null`. Hai hàm này chạy `SELECT … FOR UPDATE` trong transaction của bên gọi ([R-AUT-23](#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*, [R-AUT-26](#s-0f1edd606c "reset-password --username <tên> và list-users") *(reset-password --username \<tên\> và list-users)*);
  - `create(input) -> User`, `updatePasswordHash(id, hash) -> void`, `list() -> User[]`.
- `SessionService` làm việc với bảng `user_sessions`:
  - `create(userId) -> { token: string, expiresAt: Date }`;
  - `resolve(token) -> { sessionId, user: SessionUser, refreshedExpiresAt?: Date } | null` ([R-AUT-10](#s-0f1edd606c "Hết hạn trượt") *(Hết hạn trượt)*, [R-AUT-11](#s-0f1edd606c "Request tới route không công khai mà không có cookie") *(Request tới route không công khai mà không có cookie)*);
  - `revoke(token) -> void`, `revokeAllForUser(userId) -> void`, `deleteExpired() -> number`.
- `LoginThrottleService` làm việc với bảng `login_throttles` ([R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)*). Các hàm ghi chạy trong transaction và khóa dòng của tên đăng nhập bằng `SELECT … FOR UPDATE`. Dòng chưa có thì được tạo. Tham số `tx` là tùy chọn, dùng khi cần chạy chung transaction của bên gọi.
  - `getLock(username) -> { lockedUntil: Date } | null` đọc nhanh và không khóa dòng.
  - `recordFailure(username, tx?) -> { failedCount: number, lockedUntil: Date | null, isAlreadyLocked: boolean }` ghi một lần sai. Nếu tên đang bị khóa thì hàm không đếm và trả `isAlreadyLocked` là true. Nếu lần sai này gây khóa thì `failedCount` là 5 và có `lockedUntil`.
  - `confirmSuccess(username, tx?) -> { lockedUntil: Date } | null` xác nhận một lần nhập đúng. Nếu tên đang bị khóa thì hàm trả thông tin khóa và không đổi gì. Nếu không bị khóa thì hàm xóa bộ đếm.
  - `reset(username, tx?) -> void` xóa bộ đếm không điều kiện, dùng cho `reset-password`. Ngoài ra có `deleteStale() -> number`.
- `AuthService`:
  - `login(input: LoginInput, currentToken?: string) -> { user: SessionUser, token: string, expiresAt: Date }`. Hàm có thể ném `InvalidCredentialsError` hoặc `LoginLockedError` (kèm `lockedUntil`).
  - `changePassword(userId, input: ChangePasswordInput) -> { token: string, expiresAt: Date }`. Hàm có thể ném `CurrentPasswordIncorrectError`, `PasswordUnchangedError`, `LoginLockedError`.
  - Thuật toán của hai hàm nằm ở [mục Trạng thái và thuật toán](#s-44dde0ce1e).
- `SessionsController` phục vụ `POST /api/v1/sessions`, `GET /api/v1/sessions/current` và `DELETE /api/v1/sessions/current`.
- `UsersController` phục vụ `POST /api/v1/users/me/change-password`.
- Phân quyền:
  - Có 3 decorator: `@Public()`, `@Roles(...roles: Role[])` và `@CurrentUser()`. `@CurrentUser()` lấy `SessionUser` từ request.
  - `AuthGuard` được đăng ký global qua `APP_GUARD`. Guard đọc cookie, gọi `SessionService.resolve`, kiểm tra vai trò rồi gắn `req.user` ([R-AUT-11](#s-0f1edd606c "Request tới route không công khai mà không có cookie") *(Request tới route không công khai mà không có cookie)*, [R-AUT-15](#s-0f1edd606c "Đã đăng nhập nhưng vai trò không nằm trong @Roles") *(Đã đăng nhập nhưng vai trò không nằm trong @Roles)*).
  - `RouteAccessCheck` chạy lúc khởi động và duyệt mọi route qua `DiscoveryService` ([R-AUT-14](#s-0f1edd606c "Mặc định từ chối") *(Mặc định từ chối)*).
- `SessionCookie` (`session-cookie.ts`) có `set(res, token, expiresAt)` và `clear(res)`, theo [R-AUT-09](#s-0f1edd606c "Phiên và cookie") *(Phiên và cookie)*. Cookie được đọc bằng `cookie-parser`.
- Các lệnh CLI nằm trong `src/modules/auth/cli/` và được đăng ký vào bộ điều phối của `cli.ts`: `create-user`, `reset-password`, `list-users` ([R-AUT-25](#s-0f1edd606c "create-user --username <tên> --role <manager\|technician> --…") *(create-user --username \<tên\> --role \<manager\|technician\> --…)*, [R-AUT-26](#s-0f1edd606c "reset-password --username <tên> và list-users") *(reset-password --username \<tên\> và list-users)*, [R-AUT-27](#s-0f1edd606c "Nhập mật khẩu cho CLI") *(Nhập mật khẩu cho CLI)*).

<a id="s-bab0cc1c26"></a>

### `apps/api`, hạ tầng `src/core/http/` (bổ sung)

**Tóm tắt.** Tính năng bổ sung hai middleware bảo mật vào hạ tầng HTTP của API và mở rộng danh sách che thông tin trong log.

**Chi tiết kỹ thuật**

- `OriginCheckMiddleware` thực hiện [R-AUT-17](#s-0f1edd606c "Chống CSRF") *(Chống CSRF)*. Middleware được đăng ký bằng `app.use` trong `main.ts`, trước body parser. Nhờ vậy nó chạy trước bước đọc thân request ([R-AUT-15](#s-0f1edd606c "Đã đăng nhập nhưng vai trò không nằm trong @Roles") *(Đã đăng nhập nhưng vai trò không nằm trong @Roles)*).
- `SecurityHeadersMiddleware` thực hiện [R-AUT-18](#s-0f1edd606c "Header bảo mật trên mọi response của api") *(Header bảo mật trên mọi response của api)*.
- Danh sách `redact` của pino thêm các khóa mật khẩu mới ([R-AUT-30](#s-0f1edd606c "Log") *(Log)*).

<a id="s-2a89c6e954"></a>

### `apps/web` (`@mio/web`)

**Tóm tắt.** Phía web có lớp gọi API chung, module `auth` và khung app. Module `auth` giữ trạng thái phiên, chặn route và chứa hai màn hình. Khung app gồm thanh điều hướng và các trang chung.

**Chi tiết kỹ thuật**

- `src/core/api-client.ts` cung cấp `apiFetch<T>(path, init) -> Promise<T>`.
  - Mọi request gửi kèm `credentials: 'same-origin'`.
  - Lỗi trả về dạng `ApiError { status, code, message, fields? }`.
  - Gặp 401 thì chuyển trang theo [R-AUT-31](#s-0f1edd606c "Phiên không còn dùng được") *(Phiên không còn dùng được)*. Gặp 403 `FORBIDDEN` thì gọi `refresh()` ([R-AUT-29](#s-0f1edd606c "Thanh điều hướng chỉ hiện mục mà vai trò được dùng") *(Thanh điều hướng chỉ hiện mục mà vai trò được dùng)*).
- `src/modules/auth/`:
  - `auth-provider.tsx` cung cấp `useSession() -> { user: SessionUser | null, isLoading, refresh(), logout(), loginNotice }`. Khi mở app, provider nạp `GET /api/v1/sessions/current`. Provider giữ cờ `mio.hadSession` ([R-AUT-31](#s-0f1edd606c "Phiên không còn dùng được") *(Phiên không còn dùng được)*) và banner info chờ hiện trên màn Đăng nhập (`loginNotice`, chỉ nằm trong bộ nhớ).
  - `require-auth.tsx` bọc các route cần đăng nhập ([R-AUT-28](#s-0f1edd606c "Chưa đăng nhập mà mở trang cần đăng nhập") *(Chưa đăng nhập mà mở trang cần đăng nhập)*).
  - `require-role.tsx` cung cấp `<RequireRole roles={[...]}>` ([R-AUT-29](#s-0f1edd606c "Thanh điều hướng chỉ hiện mục mà vai trò được dùng") *(Thanh điều hướng chỉ hiện mục mà vai trò được dùng)*).
  - `login-page.tsx` và `change-password-page.tsx` là hai màn hình của tính năng.
- `src/app/`:
  - `app-shell.tsx` gồm thanh điều hướng, khối tài khoản và vùng nội dung.
  - `nav-items.ts` khai báo `NAV_ITEMS: { label, path, roles: Role[] }[]`. Mỗi tính năng có màn hình tự thêm mục của mình.
  - `home-page.tsx` là trang giữ chỗ cho Trang chính. Ngoài ra có `forbidden-page.tsx` và `not-found-page.tsx`.
- Khi dev, Vite proxy chuyển `/api` tới `http://localhost:3000`. Proxy đặt lại header `Origin` thành `http://localhost:3000` để request qua được [R-AUT-17](#s-0f1edd606c "Chống CSRF") *(Chống CSRF)*.

<a id="s-51a2c0ad01"></a>

## Thay đổi DB

**Tóm tắt.** Tính năng thêm 3 bảng: `users`, `user_sessions` và `login_throttles`. Chi tiết từng bảng nằm ở `docs/design/db-schema.md`, mục tương ứng.

- Các thông tin người dùng của giai đoạn sau chưa có trong các bảng này. Đó là PSID Messenger, thời điểm tin Messenger gần nhất, đăng ký web push và trạng thái khóa tài khoản.
- Tính năng của giai đoạn đó sẽ tự thêm cột hoặc bảng.

<a id="s-c501d518d6"></a>

## API

**Tóm tắt.** Tính năng có 4 endpoint: đăng nhập, xem phiên hiện tại, đăng xuất và đổi mật khẩu. Tính năng cũng thêm một số mã lỗi.

- Endpoint:
  - `POST /api/v1/sessions`: đăng nhập. Chi tiết ở `docs/design/api/sessions.md`.
  - `GET /api/v1/sessions/current`: trả người dùng của phiên hiện tại. Chi tiết ở `docs/design/api/sessions.md`.
  - `DELETE /api/v1/sessions/current`: đăng xuất. Chi tiết ở `docs/design/api/sessions.md`.
  - `POST /api/v1/users/me/change-password`: đổi mật khẩu. Chi tiết ở `docs/design/api/users.md`.
- Mã lỗi dùng chung mới được khai báo ở đầu `docs/design/api/system.md`: `401 UNAUTHENTICATED`, `403 FORBIDDEN`, `403 INVALID_ORIGIN`.
- Mã lỗi riêng của tính năng: `401 INVALID_CREDENTIALS`, `429 LOGIN_LOCKED`.

<a id="s-730c79b0e4"></a>

## Màn hình và quy tắc kiểm tra dữ liệu

- Mockup được làm ở bước `/ui-design auth`, khung 1440×900, theo `docs/design/ui-style.md`.
- Ở giai đoạn 0, app chỉ mở được qua `127.0.0.1` trên máy local. Vì vậy giai đoạn này chưa thiết kế giao diện điện thoại (ui-style mục Bố cục và breakpoint).

<a id="s-db090478ec"></a>

### Màn hình Đăng nhập (`/login`)

**Tóm tắt.** Người chưa đăng nhập nhập tên đăng nhập và mật khẩu ở màn hình này. Lỗi hiện dưới từng ô, hoặc trong một banner ngay trên nút "Đăng nhập".

- **Ai dùng:** người chưa đăng nhập. Người đã đăng nhập mở trang này thì được chuyển đi ([R-AUT-28](#s-0f1edd606c "Chưa đăng nhập mà mở trang cần đăng nhập") *(Chưa đăng nhập mà mở trang cần đăng nhập)*).
- **Nội dung:** logo "Mio", tiêu đề "Đăng nhập", form và dòng phụ "Quên mật khẩu? Nhờ người quản trị app đặt lại."
- **Trường nhập:**
  - Tên đăng nhập: chuỗi, bắt buộc, mặc định trống. Tên dài tối đa 32 ký tự sau khi bỏ khoảng trắng hai đầu. Bước đăng nhập không kiểm định dạng. Ô không tự viết hoa chữ đầu.
  - Mật khẩu: chuỗi, bắt buộc, mặc định trống. Mật khẩu dài tối đa 128 ký tự và không bị bỏ khoảng trắng. Ô ẩn ký tự và có nút hiện/ẩn.
- **Nút "Đăng nhập"** (primary). Trong lúc gửi, nút đổi chữ thành "Đang đăng nhập…" và không bấm được.
- **Lỗi theo trường** hiện dưới ô ([R-AUT-01](#s-0f1edd606c "Tên đăng nhập trống") *(Tên đăng nhập trống)*, [R-AUT-02](#s-0f1edd606c "Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự") *(Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự)*, [R-AUT-03](#s-0f1edd606c "Mật khẩu là chuỗi rỗng") *(Mật khẩu là chuỗi rỗng)*, [R-AUT-04](#s-0f1edd606c "Mật khẩu dài hơn 128 ký tự") *(Mật khẩu dài hơn 128 ký tự)*).
- **Vùng thông báo** là một banner nằm ngay sau ô Mật khẩu, trước nút "Đăng nhập". Mỗi lúc chỉ hiện tối đa một banner.
  - Lỗi `INVALID_CREDENTIALS`, `LOGIN_LOCKED`, `INVALID_ORIGIN`, `INTERNAL_ERROR` hiện banner danger. Form giữ nguyên tên đăng nhập và xóa ô mật khẩu. Mất mạng hoặc cookie bị chặn cũng hiện banner danger (mục Xử lý lỗi).
  - Banner info hiện khi người dùng tới từ [R-AUT-31](#s-0f1edd606c "Phiên không còn dùng được") *(Phiên không còn dùng được)* ("Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại") hoặc từ [R-AUT-32](#s-0f1edd606c "Bấm 'Đăng xuất'") *(Bấm "Đăng xuất")* ("Bạn đã đăng xuất"). Banner lấy từ `loginNotice` của `auth-provider` và chỉ hiện một lần. Tải lại trang thì banner không còn.

**Chi tiết kỹ thuật**

- Ô Tên đăng nhập: `autocomplete="username"`, `autocapitalize="none"`.
- Ô Mật khẩu: `autocomplete="current-password"`.

<a id="s-62810bff29"></a>

### Khung app (mọi trang sau khi đăng nhập)

**Tóm tắt.** Mọi trang sau khi đăng nhập nằm trong khung app, gồm thanh điều hướng trái, khối tài khoản và vùng nội dung. Thanh điều hướng chỉ hiện mục mà vai trò được dùng.

- **Ai dùng:** Quản lý, Thợ.
- **Thanh điều hướng trái** gồm logo "Mio" và các mục trong `NAV_ITEMS` mà vai trò được dùng ([R-AUT-29](#s-0f1edd606c "Thanh điều hướng chỉ hiện mục mà vai trò được dùng") *(Thanh điều hướng chỉ hiện mục mà vai trò được dùng)*). Giai đoạn 0 có 3 mục:
  - "Trang chính" (`/`) dành cho Quản lý và Thợ. Tính năng `auth` làm trang giữ chỗ với tiêu đề "Hôm nay". Tính năng `emergency-stop` thêm khối "Trạng thái tự động hóa".
  - "Cài đặt" (`/settings`) chỉ dành cho Quản lý. Tính năng `group-settings` thêm mục này khi có trang con đầu tiên.
  - "Nhật ký hệ thống" (`/system-log`) chỉ dành cho Quản lý. Tính năng `emergency-stop` thêm mục này.
- **Khối tài khoản** nằm cuối thanh điều hướng. Khối gồm tên hiển thị, badge vai trò (`ROLE_LABELS`), liên kết "Đổi mật khẩu" và nút "Đăng xuất" ([R-AUT-32](#s-0f1edd606c "Bấm 'Đăng xuất'") *(Bấm "Đăng xuất")*).
- Khung app không có trường nhập.
- **Lúc mở app:** trong lúc `auth-provider` nạp `GET /api/v1/sessions/current`, app hiện màn hình chờ gồm logo "Mio", vòng xoay và chữ "Đang tải…". Thanh điều hướng chưa được vẽ vì chưa biết vai trò.
- **Nạp phiên lỗi:**
  - Nạp phiên lỗi 500 hoặc mất mạng (không phải 401) thì app hiện màn hình lỗi với logo, thông báo và nút "Thử lại". Thông báo là "Lỗi hệ thống, vui lòng thử lại sau". Khi mất mạng, thông báo là "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại.". Nút "Thử lại" gọi lại `GET /api/v1/sessions/current`.
  - Nạp phiên trả 401 thì app xử lý theo [R-AUT-28](#s-0f1edd606c "Chưa đăng nhập mà mở trang cần đăng nhập") *(Chưa đăng nhập mà mở trang cần đăng nhập)*.
- **Mockup:** `docs/design/ui/app-shell/`, `login/`, `change-password/`, `forbidden/`, `not-found/`.
  - Thanh điều hướng là component `<mio-app-nav>` (`docs/design/components/app-nav.md`).
  - Ô mật khẩu là component `<mio-password-field>` (`docs/design/components/password-field.md`).

<a id="s-420e1e2320"></a>

### Màn hình Đổi mật khẩu (`/account/password`)

**Tóm tắt.** Mỗi người dùng tự đổi mật khẩu của chính mình ở màn hình này. Trước khi gửi, app hỏi có đăng xuất các thiết bị khác hay không.

- **Ai dùng:** Quản lý, Thợ. Mỗi người chỉ đổi mật khẩu của chính mình ([câu hỏi mở 3](#s-505f20bb78 "07 mục 2 đặt 'Đổi mật khẩu' trong Cài đặt") *(07 mục 2 đặt "Đổi mật khẩu" trong Cài đặt)*).
- **Trường nhập.** Cả ba ô đều mặc định trống và có nút hiện/ẩn.
  - Mật khẩu hiện tại: chuỗi, bắt buộc, tối đa 128 ký tự.
  - Mật khẩu mới: chuỗi, bắt buộc, dài 8–128 ký tự. Mật khẩu mới không được trùng tên đăng nhập và phải khác mật khẩu hiện tại. Dưới ô có gợi ý "Ít nhất 8 ký tự".
  - Nhập lại mật khẩu mới: chuỗi, bắt buộc, phải giống Mật khẩu mới.
- **Nút "Đổi mật khẩu"** (primary).

**Cách hoạt động**

1. Người dùng bấm "Đổi mật khẩu". Web kiểm tra dữ liệu trước ([R-AUT-19](#s-0f1edd606c "Mật khẩu hiện tại trống") *(Mật khẩu hiện tại trống)*, [R-AUT-21](#s-0f1edd606c "Mật khẩu mới") *(Mật khẩu mới)* ba ý đầu, [R-AUT-22](#s-0f1edd606c "Chỉ trên web") *(Chỉ trên web)*). Có lỗi thì lỗi hiện dưới ô và hộp thoại không mở.
2. Dữ liệu hợp lệ thì web mở hộp thoại xác nhận ([R-AUT-34](#s-0f1edd606c "Đổi mật khẩu trên web luôn qua hộp thoại xác nhận 'có đăng…") *(Đổi mật khẩu trên web luôn qua hộp thoại xác nhận "có đăng…)*):
   - tiêu đề "Đổi mật khẩu";
   - nội dung "Bạn có muốn đăng xuất khỏi các thiết bị khác đang đăng nhập tài khoản này không? Nên chọn đăng xuất nếu bạn nghi có người khác biết mật khẩu cũ.";
   - 3 nút: "Đổi và đăng xuất thiết bị khác" (primary, được focus sẵn), "Chỉ đổi mật khẩu" (secondary) và "Hủy" (ghost);
   - bấm Esc hoặc bấm ra ngoài hộp thoại có tác dụng như "Hủy". Hộp thoại đóng, web không gửi gì và form giữ dữ liệu.
3. Người dùng bấm một trong hai nút đổi thì web gửi API với `signOutOtherDevices` tương ứng. Trong lúc gửi, hai nút ở trạng thái loading và nút vừa bấm hiện "Đang lưu…". Hộp thoại không đóng được trong lúc này.
4. Thành công thì hộp thoại đóng, form được xóa trắng và người dùng ở lại trang. App hiện toast success:
   - nếu đã chọn đăng xuất: "Đã đổi mật khẩu. Các thiết bị khác đã được đăng xuất.";
   - nếu không chọn: "Đã đổi mật khẩu.".
5. Có lỗi thì hộp thoại đóng và form giữ dữ liệu.
   - Lỗi theo trường hiện dưới ô, ví dụ "Mật khẩu hiện tại không đúng".
   - `LOGIN_LOCKED` và các lỗi khác hiện banner danger ngay sau ô Nhập lại mật khẩu mới, trước nút "Đổi mật khẩu". Đây là vùng thông báo, giống màn Đăng nhập.

**Chi tiết kỹ thuật**

- Ô Mật khẩu hiện tại: `autocomplete="current-password"`.
- Ô Mật khẩu mới: `autocomplete="new-password"`.

<a id="s-a9731829c2"></a>

### Màn hình Không có quyền

**Tóm tắt.** Màn hình hiện trong khung app khi Thợ mở một trang chỉ dành cho Quản lý ([R-AUT-29](#s-0f1edd606c "Thanh điều hướng chỉ hiện mục mà vai trò được dùng") *(Thanh điều hướng chỉ hiện mục mà vai trò được dùng)*).

- Màn hình có tiêu đề "Không có quyền truy cập", dòng "Trang này chỉ dành cho Quản lý." và nút "Về Trang chính".

<a id="s-16eeb5053e"></a>

### Màn hình Không tìm thấy trang

**Tóm tắt.** Màn hình hiện trong khung app khi đường dẫn không khớp trang nào.

- Màn hình chỉ hiện sau khi đã đăng nhập. Với người chưa đăng nhập, [R-AUT-28](#s-0f1edd606c "Chưa đăng nhập mà mở trang cần đăng nhập") *(Chưa đăng nhập mà mở trang cần đăng nhập)* chạy trước.
- Màn hình có tiêu đề "Không tìm thấy trang" và nút "Về Trang chính".

<a id="s-0f1edd606c"></a>

### Quy tắc

**Quy tắc chung.** Mỗi trường chỉ hiện một lỗi. Lỗi được chọn là ý đầu tiên bị vi phạm, theo thứ tự các ý trong quy tắc của trường đó: trống, rồi độ dài, rồi trùng tên đăng nhập, rồi khác mật khẩu hiện tại. Quy tắc này áp dụng cho lỗi dưới ô trên web, cho `fields` của API và cho dòng lỗi của CLI.

#### Đăng nhập

**R-AUT-01: Tên đăng nhập trống.** Tên đăng nhập trống sau khi bỏ khoảng trắng hai đầu thì báo lỗi "Nhập tên đăng nhập".

**R-AUT-02: Tên đăng nhập quá dài.** Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự thì báo lỗi "Tên đăng nhập tối đa 32 ký tự". Chuẩn hóa theo [R-AUT-07](#s-0f1edd606c "Tên đăng nhập được chuẩn hóa trước khi tra cứu") *(Tên đăng nhập được chuẩn hóa trước khi tra cứu)* gồm bỏ khoảng trắng hai đầu và đổi chữ thường.

- Vì sao: độ dài được đo sau khi đổi chữ thường vì một số ký tự dài ra, ví dụ `İ` thành 2 code point. Đo như vậy để tên lưu vào `login_throttles` không vượt 32.

**R-AUT-03: Mật khẩu trống.** Mật khẩu là chuỗi rỗng thì báo lỗi "Nhập mật khẩu". Mật khẩu chỉ gồm khoảng trắng không bị coi là rỗng.

**R-AUT-04: Mật khẩu quá dài.** Mật khẩu dài hơn 128 ký tự thì báo lỗi "Mật khẩu tối đa 128 ký tự".

- Độ dài của mọi chuỗi trong tính năng được tính theo code point (`[...s].length`), không theo đơn vị UTF-16.
- Các lỗi [R-AUT-01](#s-0f1edd606c "Tên đăng nhập trống") *(Tên đăng nhập trống)*, [R-AUT-02](#s-0f1edd606c "Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự") *(Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự)*, [R-AUT-03](#s-0f1edd606c "Mật khẩu là chuỗi rỗng") *(Mật khẩu là chuỗi rỗng)*, [R-AUT-04](#s-0f1edd606c "Mật khẩu dài hơn 128 ký tự") *(Mật khẩu dài hơn 128 ký tự)* trả 400 `VALIDATION_ERROR` với `message` "Dữ liệu đăng nhập không hợp lệ" và `fields` theo từng trường. Các lỗi này không được đếm vào [R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)*.
- Trường không phải chuỗi hoặc bị thiếu nhận cùng thông báo như khi trống.

**R-AUT-05: Sai tên đăng nhập hoặc sai mật khẩu.** Tên đăng nhập không tồn tại hoặc mật khẩu sai thì API trả 401 `INVALID_CREDENTIALS` với thông báo "Tên đăng nhập hoặc mật khẩu không đúng".

- Hai trường hợp trả về giống hệt nhau.
- Với tên không tồn tại, API vẫn chạy `verify` trên một chuỗi băm giả để thời gian xử lý tương đương.

**R-AUT-06: Giới hạn số lần đăng nhập sai.** Một tên đăng nhập bị nhập sai 5 lần trong vòng 15 phút thì bị khóa 15 phút.

*Vì sao.* Bộ đếm tính theo tên đăng nhập đã chuẩn hóa, kể cả tên không tồn tại, để không lộ tên nào có thật.

*Cách hoạt động*

- Cửa sổ 15 phút tính từ lần sai đầu tiên của cửa sổ. Lần sai thứ 5 làm tên bị khóa và nhận 429 ngay ở lần đó.
- Trong lúc khóa, mọi lần đăng nhập bằng tên đó đều nhận 429 `LOGIN_LOCKED`, kể cả khi đúng mật khẩu. API không kiểm mật khẩu, không đếm thêm và không kéo dài khóa.
- Thông báo khi bị khóa là "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút.". Màn Đăng nhập và màn Đổi mật khẩu dùng chung câu này ([R-AUT-20](#s-0f1edd606c "Mật khẩu hiện tại không đúng") *(Mật khẩu hiện tại không đúng)*).
- Hết khóa thì bộ đếm bắt đầu lại từ 0.
- Đăng nhập đúng thì bộ đếm của tên đó bị xóa.
- Các phiên đang có của tài khoản không bị ảnh hưởng.
- Nhập sai mật khẩu hiện tại khi đổi mật khẩu cũng được đếm vào bộ đếm này ([R-AUT-20](#s-0f1edd606c "Mật khẩu hiện tại không đúng") *(Mật khẩu hiện tại không đúng)*).

*Khi nhiều request tới cùng lúc ([câu hỏi mở 7](#s-505f20bb78 "Nhiều request sai gửi đồng thời") *(Nhiều request sai gửi đồng thời)*).* Mọi lần đọc để ghi bộ đếm chạy trong transaction có khóa dòng. Trong transaction đó, khóa được kiểm lại ngay.

- Khi ghi lần sai (`recordFailure`): nếu đang khóa thì trả 429, không đếm và không kéo dài khóa.
- Khi đúng mật khẩu (`confirmSuccess`, ở cả đăng nhập và đổi mật khẩu): nếu đang khóa thì trả 429, không tạo phiên và không đổi mật khẩu.
- Nhờ vậy, khi nhiều request gửi cùng lúc, chỉ có tối đa 5 lần sai được tính.
- Request đã qua `verify` mà gặp khóa lúc ghi luôn nhận 429, dù mật khẩu đúng hay sai. Người dò vì thế không biết kết quả của các lần đoán vượt quá 5.

*Chi tiết kỹ thuật*

- `<n>` là số phút còn lại, làm tròn lên, tối thiểu 1.
- Header `Retry-After` chứa số giây còn lại, làm tròn lên.
- Khóa dòng dùng `SELECT … FOR UPDATE` / upsert.

**R-AUT-07: Chuẩn hóa tên đăng nhập.** Tên đăng nhập được chuẩn hóa trước khi tra cứu, trước khi đếm theo [R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)* và trước khi lưu. Chuẩn hóa gồm bỏ khoảng trắng hai đầu và đổi chữ thường. Mật khẩu giữ nguyên, không bị bỏ khoảng trắng.

**R-AUT-08: Đăng nhập đúng.** Đăng nhập đúng thì API tạo phiên ([R-AUT-09](#s-0f1edd606c "Phiên và cookie") *(Phiên và cookie)*) và trả 201 kèm thông tin người dùng.

- Nếu `needsRehash` của chuỗi băm đang lưu trả đúng, API băm lại mật khẩu bằng tham số hiện tại và lưu chuỗi mới.
- Nếu request mang cookie của một phiên còn hiệu lực thì phiên đó bị xóa và phiên mới thay thế. Trường hợp này xảy ra khi đăng nhập lại ở tab khác, hoặc khi đổi tài khoản qua API.

#### Phiên

**R-AUT-09: Phiên và cookie ([ADR 0015](../../../decisions/0015-server-side-sessions.md "Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…") *(Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…)*).** Mỗi phiên có một token, gửi cho trình duyệt qua cookie. DB chỉ lưu mã băm của token. Một người dùng có thể có nhiều phiên cùng lúc, mỗi thiết bị một phiên.

- Token gồm 32 byte ngẫu nhiên (`crypto.randomBytes`), mã hóa base64url. DB chỉ lưu SHA-256 dạng hex của token, trong cột `user_sessions.token_hash`.
- Cookie `mio_session` có các thuộc tính `HttpOnly`, `SameSite=Lax`, `Path=/`. `Max-Age` bằng số giây tới `expires_at`. Cookie có thêm `Secure` khi `PUBLIC_URL` bắt đầu bằng `https://`.

**R-AUT-10: Hết hạn trượt.** Phiên hết hạn sau 90 ngày kể từ lần gia hạn gần nhất. Không có hạn tuyệt đối ([câu hỏi mở 1](#s-505f20bb78 "Thời hạn giữ đăng nhập? — đã chốt 2026-10-31 theo đề xuất") *(Thời hạn giữ đăng nhập? — đã chốt 2026-10-31 theo đề xuất)*).

- Phiên được gia hạn khi có request hợp lệ và lần gia hạn gần nhất (`updated_at`) đã cũ hơn 24 giờ. Khi đó `expires_at` được đặt thành bây giờ cộng 90 ngày, `updated_at` được đặt thành bây giờ, và cookie được gửi lại với `Max-Age` mới.
- Chỉ route có `@Roles(...)` mới gia hạn phiên. Route `@Public()` đọc phiên nhưng không gia hạn.

**R-AUT-11: Request chưa xác thực.** Request tới route không công khai nhận 401 `UNAUTHENTICATED` với thông báo "Bạn chưa đăng nhập hoặc phiên đăng nhập đã hết hạn". Điều này xảy ra khi không có cookie, khi token không khớp phiên nào, hoặc khi phiên đã hết hạn (`expires_at` nhỏ hơn hoặc bằng bây giờ).

- Có cookie nhưng cookie không hợp lệ thì response kèm lệnh xóa cookie (`Max-Age=0`).
- Phiên hết hạn phát hiện lúc kiểm tra thì bị xóa khỏi DB.

**R-AUT-12: Đăng xuất.** Đăng xuất (`DELETE /api/v1/sessions/current`) là route công khai và idempotent.

- Nếu có phiên thì phiên đó bị xóa.
- API luôn xóa cookie và trả 204, kể cả khi không có phiên hoặc phiên đã hết hạn.

**R-AUT-13: Dọn dữ liệu cũ.** Dữ liệu cũ được dọn ngay trong lúc đăng nhập, không cần job.

- Mỗi lần đăng nhập thành công, API xóa mọi phiên đã hết hạn (`SessionService.deleteExpired`).
- Mỗi lần xử lý đăng nhập, API xóa các dòng `login_throttles` không còn khóa và có `updated_at` cũ hơn 24 giờ (`deleteStale`).

#### Phân quyền

**R-AUT-14: Mặc định từ chối.** Mọi route dưới `/api/v1` phải khai báo `@Public()` hoặc `@Roles(...)`, ở handler hoặc ở controller.

- Lúc khởi động, `RouteAccessCheck` liệt kê các route thiếu khai báo. Nếu có route thiếu, api ghi log lỗi, thoát mã 1 và không mở cổng.
- Thông báo là "Route chưa khai báo quyền: <METHOD> <path>", mỗi route một dòng.

**R-AUT-15: Sai vai trò.** Người đã đăng nhập nhưng vai trò không nằm trong `@Roles(...)` nhận 403 `FORBIDDEN` với thông báo "Bạn không có quyền thực hiện thao tác này".

- Thứ tự kiểm tra một request:
  1. R-AUT-17;
  2. đọc thân request (`INVALID_JSON`, `PAYLOAD_TOO_LARGE`, [R-SKL-15](app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*);
  3. R-AUT-11;
  4. R-AUT-15;
  5. kiểm tra dữ liệu.

**R-AUT-16: Quyền của các route trong tính năng.**

- Route công khai: `GET /api/v1/health` ([R-SKL-13](app-skeleton.md#s-0f1edd606c "GET /api/v1/health không cần đăng nhập") *(GET /api/v1/health không cần đăng nhập)*), `POST /api/v1/sessions`, `DELETE /api/v1/sessions/current`.
- Route cho Quản lý và Thợ: `GET /api/v1/sessions/current`, `POST /api/v1/users/me/change-password`.
- Route của các tính năng sau theo 07 mục 1 "Quyền của vai trò Thợ": Cài đặt và Nhật ký hệ thống chỉ dành cho Quản lý.
- Đường dẫn `/api/...` không có route vẫn trả 404 `NOT_FOUND` ([R-SKL-15](app-skeleton.md#s-0f1edd606c "mọi lỗi API trả thân { 'code'") *(mọi lỗi API trả thân { "code")*), dù chưa đăng nhập.
- File tĩnh của web ([R-SKL-14](app-skeleton.md#s-0f1edd606c "api phục vụ web") *(api phục vụ web)*) không cần đăng nhập. Dữ liệu chỉ lấy được qua API có kiểm quyền.

**R-AUT-17: Chống CSRF.** Cùng với `SameSite=Lax`, API kiểm tra header `Origin` để chống CSRF.

- Request `POST`, `PUT`, `PATCH`, `DELETE` tới `/api/` có header `Origin` khác origin của `PUBLIC_URL` thì nhận 403 `INVALID_ORIGIN`. Hai origin được so theo scheme, host và cổng.
- Thông báo là "Yêu cầu bị từ chối: hãy mở app bằng địa chỉ <PUBLIC_URL>".
- Quy tắc áp dụng cả cho route công khai.
- Request không có `Origin`, ví dụ từ CLI hay curl, được đi tiếp.

**R-AUT-18: Header bảo mật.** Mọi response của api có các header bảo mật. Response của các route phiên và tài khoản không được cache.

- Mọi response có `X-Frame-Options: DENY`, `X-Content-Type-Options: nosniff`, `Referrer-Policy: same-origin`.
- Mọi response của `/api/v1/sessions*` và `/api/v1/users/me/*` có thêm `Cache-Control: no-store`.

#### Đổi mật khẩu

**R-AUT-19: Mật khẩu hiện tại.** Mật khẩu hiện tại trống thì báo lỗi "Nhập mật khẩu hiện tại". Mật khẩu hiện tại dài hơn 128 ký tự thì báo lỗi "Mật khẩu tối đa 128 ký tự".

**R-AUT-20: Mật khẩu hiện tại không đúng.**

- API trả 400 `VALIDATION_ERROR` với `message` "Dữ liệu đổi mật khẩu không hợp lệ" và `fields.currentPassword` "Mật khẩu hiện tại không đúng".
- Lần sai này được đếm một lần vào [R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)*, theo tên đăng nhập của người dùng.
- Nếu tên đăng nhập đang bị khóa thì API trả 429 `LOGIN_LOCKED` với thông báo như [R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)* và không kiểm mật khẩu.

**R-AUT-21: Mật khẩu mới.**

- Trống: báo lỗi "Nhập mật khẩu mới".
- Ngắn hơn 8 hoặc dài hơn 128 ký tự: báo lỗi "Mật khẩu mới phải từ 8 đến 128 ký tự".
- Giống tên đăng nhập (so sau khi đổi chữ thường): báo lỗi "Mật khẩu không được trùng tên đăng nhập".
- Giống mật khẩu hiện tại: báo lỗi "Mật khẩu mới phải khác mật khẩu hiện tại". Ý này được kiểm bằng `verify`, sau khi mật khẩu hiện tại đã đúng.
- `currentPassword` hoặc `newPassword` không phải chuỗi hoặc bị thiếu thì nhận cùng thông báo như khi trống ("Nhập mật khẩu hiện tại", "Nhập mật khẩu mới").
- Thứ tự kiểm:
  1. Kiểm hình thức ([R-AUT-19](#s-0f1edd606c "Mật khẩu hiện tại trống") *(Mật khẩu hiện tại trống)*, [R-AUT-21](#s-0f1edd606c "Mật khẩu mới") *(Mật khẩu mới)* ba ý đầu) và trả hết lỗi theo trường cùng lúc.
  2. Kiểm khóa và mật khẩu hiện tại ([R-AUT-20](#s-0f1edd606c "Mật khẩu hiện tại không đúng") *(Mật khẩu hiện tại không đúng)*).
  3. Kiểm "khác mật khẩu hiện tại".
- Mọi lỗi theo trường trả 400 `VALIDATION_ERROR` với `message` "Dữ liệu đổi mật khẩu không hợp lệ".

**R-AUT-22: Nhập lại mật khẩu mới (chỉ trên web).** Ô Nhập lại mật khẩu mới trống thì báo lỗi "Nhập lại mật khẩu mới". Giá trị khác Mật khẩu mới thì báo lỗi "Mật khẩu nhập lại không khớp". API không nhận trường này.

**R-AUT-23: Đổi mật khẩu thành công.** API lưu chuỗi băm mới, xóa phiên hiện tại, tạo phiên mới cho thiết bị đang dùng và đặt cookie mới. API cũng xóa bộ đếm [R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)* và trả 204.

- **Xếp hàng.** Việc kiểm khóa, kiểm mật khẩu hiện tại và mọi lần ghi chạy trong một transaction. Transaction khóa dòng `users` của người dùng (`lockById`) trước khi đọc chuỗi băm.
  - Hai lần đổi cùng lúc chạy lần lượt. Ví dụ: đổi từ hai thiết bị, hoặc đổi cùng lúc với `reset-password`.
  - Lần sau kiểm mật khẩu hiện tại với chuỗi băm mà lần trước vừa ghi. Vì vậy chỉ một lần báo thành công, và mật khẩu dùng được đúng là mật khẩu của lần đó.
- **Phiên của các thiết bị khác:**
  - `signOutOtherDevices` là `true`: các phiên này bị xóa hết. Các thiết bị đó nhận 401 ở request kế tiếp.
  - `signOutOtherDevices` là `false`: các phiên này giữ nguyên. Các thiết bị đó vẫn dùng được tới khi hết hạn hoặc đăng xuất.
- `signOutOtherDevices` thiếu hoặc không phải boolean thì API trả 400 `VALIDATION_ERROR` với `fields.signOutOtherDevices` "Chọn có đăng xuất các thiết bị khác hay không". Web luôn gửi trường này ([R-AUT-34](#s-0f1edd606c "Đổi mật khẩu trên web luôn qua hộp thoại xác nhận 'có đăng…") *(Đổi mật khẩu trên web luôn qua hộp thoại xác nhận "có đăng…)*).

**R-AUT-24: Đổi mật khẩu và đăng xuất trên thiết bị khác cùng lúc.**

- Phiên bị xóa trước khi request đổi mật khẩu kiểm tra phiên: request đó nhận 401.
- Request đã qua bước kiểm tra phiên: đổi mật khẩu vẫn thành công.

#### Lệnh CLI

Các lệnh chạy trong container api: `docker compose exec -it api node dist/cli.js <lệnh>`.

**R-AUT-25: Lệnh tạo tài khoản.** Lệnh `create-user --username <tên> --role <manager|technician> --display-name "<tên hiển thị>"` tạo tài khoản mới. Mật khẩu nhập theo [R-AUT-27](#s-0f1edd606c "Nhập mật khẩu cho CLI") *(Nhập mật khẩu cho CLI)*. Có lỗi thì lệnh in mọi lỗi, mỗi lỗi một dòng, rồi thoát mã 1.

- **Thứ tự kiểm:**
  - Tham số được kiểm trước: thiếu, sai định dạng, tên đã tồn tại.
  - Khi stdin là terminal: tham số có lỗi thì lệnh in lỗi và thoát, không hỏi mật khẩu. Tham số đúng thì lệnh mới hỏi mật khẩu rồi kiểm mật khẩu.
  - Khi stdin không phải terminal: lệnh vẫn đọc mật khẩu, rồi in lỗi tham số và lỗi mật khẩu cùng một lượt.
- **Lỗi của `--username`:**
  - thiếu: "Thiếu --username";
  - tên (sau [R-AUT-07](#s-0f1edd606c "Tên đăng nhập được chuẩn hóa trước khi tra cứu") *(Tên đăng nhập được chuẩn hóa trước khi tra cứu)*) không khớp `^[a-z0-9._-]{3,32}$`: "Tên đăng nhập phải dài 3–32 ký tự, chỉ gồm chữ thường không dấu, số, dấu chấm, gạch dưới, gạch ngang";
  - tên đã có: "Tên đăng nhập đã tồn tại: <tên>". Ràng buộc unique của DB chặn cả khi tạo đồng thời.
- **Lỗi của `--role`:** thiếu thì báo "Thiếu --role". Giá trị khác `manager`, `technician` thì báo "Vai trò phải là manager hoặc technician".
- **Lỗi của `--display-name`:** thiếu thì báo "Thiếu --display-name". Sau khi bỏ khoảng trắng hai đầu mà dài 0 hoặc hơn 50 ký tự thì báo "Tên hiển thị phải từ 1 đến 50 ký tự".
- **Lỗi của mật khẩu:** dài dưới 8 hoặc hơn 128 ký tự thì báo "Mật khẩu phải từ 8 đến 128 ký tự". Giống tên đăng nhập thì báo "Mật khẩu không được trùng tên đăng nhập".
- **Thành công:** lệnh in "Đã tạo tài khoản <tên> (<Quản lý|Thợ>)" và thoát mã 0.

**R-AUT-26: Lệnh đặt lại mật khẩu và lệnh liệt kê tài khoản.**

- `reset-password --username <tên>` đặt lại mật khẩu. Mật khẩu nhập theo [R-AUT-27](#s-0f1edd606c "Nhập mật khẩu cho CLI") *(Nhập mật khẩu cho CLI)*.
  - Thiếu `--username` thì báo "Thiếu --username". Không có tài khoản thì báo "Không tìm thấy tài khoản: <tên>" và thoát mã 1. Thứ tự kiểm tham số và hỏi mật khẩu giống [R-AUT-25](#s-0f1edd606c "create-user --username <tên> --role <manager\|technician> --…") *(create-user --username \<tên\> --role \<manager\|technician\> --…)*.
  - Mật khẩu theo cùng quy tắc như [R-AUT-25](#s-0f1edd606c "create-user --username <tên> --role <manager\|technician> --…") *(create-user --username \<tên\> --role \<manager\|technician\> --…)*.
  - Thành công: lệnh mở một transaction khóa dòng `users` (`lockByUsername`, xếp hàng với đổi mật khẩu [R-AUT-23](#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*). Trong transaction, lệnh lưu chuỗi băm mới, xóa mọi phiên của tài khoản và xóa bộ đếm [R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)* (`reset`). Sau đó lệnh in "Đã đặt lại mật khẩu cho <tên>. Mọi phiên đăng nhập của tài khoản đã bị đăng xuất." và thoát mã 0.
- `list-users` in mỗi tài khoản một dòng "<tên đăng nhập> | <Quản lý|Thợ> | <tên hiển thị>", sắp theo tên đăng nhập. Chưa có tài khoản nào thì lệnh in "Chưa có tài khoản nào."

**R-AUT-27: Nhập mật khẩu cho CLI.** CLI không nhận mật khẩu qua tham số dòng lệnh, để mật khẩu không bị lưu vào lịch sử shell.

- Khi stdin là terminal: lệnh hỏi "Mật khẩu: " rồi "Nhập lại mật khẩu: " và không hiện ký tự gõ. Hai lần nhập khác nhau thì lệnh báo "Mật khẩu nhập lại không khớp" và thoát mã 1.
- Khi stdin không phải terminal (dùng trong script, test): lệnh đọc dòng đầu tiên, bỏ `\r\n` ở cuối và không hỏi nhập lại. stdin rỗng thì lệnh báo "Thiếu mật khẩu" và thoát mã 1.
- Tham số không biết (ví dụ `--password`): lệnh báo "Tham số không hợp lệ: <tham số>" và thoát mã 1.

**R-AUT-33: CLI không đòi đăng nhập web.**

- Ai chạy được `docker compose exec api …` (tức có quyền vào máy chạy Docker) thì dùng được `create-user`, `reset-password`, `list-users` cho mọi tài khoản, kể cả tài khoản của chính mình.
- Đây là đường khôi phục duy nhất khi mọi Quản lý đều quên mật khẩu.
- Không có cổng mạng nào mở cho CLI.

**R-AUT-34: Hộp thoại xác nhận khi đổi mật khẩu.** Đổi mật khẩu trên web luôn đi qua hộp thoại xác nhận "có đăng xuất các thiết bị khác không" (mục Màn hình Đổi mật khẩu). Lựa chọn được gửi trong `signOutOtherDevices` ([R-AUT-23](#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*). Lựa chọn mặc định là đăng xuất; đó là nút được focus sẵn.

#### Web

**R-AUT-28: Chuyển về trang đăng nhập.** Người chưa đăng nhập mở trang cần đăng nhập thì bị chuyển tới `/login`, kèm đường dẫn để quay lại sau khi đăng nhập.

- Chưa đăng nhập nghĩa là `GET /api/v1/sessions/current` trả 401. Khi đó app chuyển tới `/login?next=<đường dẫn + query hiện tại, mã hóa URL>`. Banner khi chuyển theo [R-AUT-31](#s-0f1edd606c "Phiên không còn dùng được") *(Phiên không còn dùng được)*.
- Đăng nhập xong, app chuyển tới `next` nếu giá trị này thỏa cả 3 điều kiện:
  - bắt đầu bằng `/`, không bắt đầu bằng `//` hay `/\`;
  - không chứa ký tự điều khiển (U+0000–U+001F, U+007F) hay khoảng trắng. Lý do: trình duyệt tự bỏ tab và xuống dòng, nên `/<tab>/evil.example` thành `//evil.example`;
  - không phải `/login`.
- Không thỏa thì app chuyển tới `/`.
- Việc chuyển trang dùng router của app (`navigate`), không dùng `location.href`.
- Người đã đăng nhập mà mở `/login` thì được chuyển tới `/`.

**R-AUT-29: Hiển thị theo vai trò.**

- Thanh điều hướng chỉ hiện mục mà vai trò được dùng.
- Mở trực tiếp đường dẫn của trang không dành cho vai trò mình thì app hiện màn hình Không có quyền. Đường dẫn giữ nguyên.
- API trả 403 `FORBIDDEN` khi người dùng đang thao tác thì web xử lý theo `ui-style.md` mục "Vị trí thông báo" ([ADR 0016](../../../decisions/0016-form-message-placement.md "Vị trí và câu chữ thông báo trên màn hình") *(Vị trí và câu chữ thông báo trên màn hình)*):
  - khi gửi form: banner danger với `message` của API hiện ở vùng thông báo của form, ngay trên hàng nút gửi. Form giữ dữ liệu;
  - khi thao tác không có form (nút trong danh sách, công tắc có hiệu lực ngay): toast danger với `message` của API;
  - cả hai trường hợp đều gọi `refresh()` của `auth-provider`, để thanh điều hướng và màn hình Không có quyền theo vai trò mới.

**R-AUT-30: Log.** Tính năng ghi log có cấu trúc cho các sự kiện đăng nhập, để theo dõi tấn công dò mật khẩu. Quy tắc này bổ sung [R-SKL-17](app-skeleton.md#s-0f1edd606c "log là JSON một dòng ra stdout") *(log là JSON một dòng ra stdout)*.

- **Trường chung.** Mọi sự kiện có trường `event` (tên sự kiện bên dưới) và `time`. Sự kiện từ request HTTP có thêm `requestId` của [R-SKL-17](app-skeleton.md#s-0f1edd606c "log là JSON một dòng ra stdout") *(log là JSON một dòng ra stdout)*, `ip` (`req.ip`) và `userAgent` (header `User-Agent`, cắt còn 200 ký tự).
- **Theo dõi tấn công dò mật khẩu.** Mỗi lần sai, mỗi lần bị chặn vì đang khóa và mỗi lần bắt đầu khóa đều có đúng một dòng log.
  - `auth.login.failed` (warn) ghi `username` đã chuẩn hóa, `userExists` (true/false), `reason`, `failedCount` và `lockedUntil`. `reason` là `invalid_credentials` khi sai tên hoặc mật khẩu, là `locked` khi bị chặn vì đang khóa. `failedCount` là số lần sai trong cửa sổ, tính cả lần này, từ 1–5. Lần làm khóa ghi `5` kèm `lockedUntil`. Khi `locked` thì không có `failedCount`. `lockedUntil` có khi `locked` hoặc khi lần này làm khóa.
  - `auth.lock.started` (warn) ghi `username`, `userExists`, `source` và `lockedUntil`; `source` là `login` hoặc `change_password`. Dòng này được ghi ngay khi lần sai thứ 5 làm khóa, cùng request với dòng `failed` của lần đó.
  - `auth.password.change_failed` (warn) ghi `userId`, `username`, `reason` và `failedCount` / `lockedUntil` như trên. `reason` là `current_password_incorrect` hoặc `locked`.
- **Sự kiện khác** ở mức info: `auth.login.succeeded` (`userId`, `username`), `auth.logout` (`userId` nếu có), `auth.password.changed` (`userId`, `signedOutOtherDevices`), `auth.cli.user_created`, `auth.cli.password_reset` (`username`).
- **Log của lệnh CLI.** Lệnh chạy bằng `docker compose exec` là một tiến trình riêng. stdout của lệnh chỉ ra terminal của người gõ. Vì vậy:
  - stdout của lệnh chỉ in thông báo cho người đọc ([R-AUT-25](#s-0f1edd606c "create-user --username <tên> --role <manager\|technician> --…") *(create-user --username \<tên\> --role \<manager\|technician\> --…)*, [R-AUT-26](#s-0f1edd606c "reset-password --username <tên> và list-users") *(reset-password --username \<tên\> và list-users)*, [R-AUT-27](#s-0f1edd606c "Nhập mật khẩu cho CLI") *(Nhập mật khẩu cho CLI)*), không in dòng log JSON;
  - dòng log JSON (`auth.cli.*`, lỗi) được ghi vào `/proc/1/fd/1`, tức stdout của tiến trình chính của container. Node là PID 1 theo [R-SKL-22](app-skeleton.md#s-0f1edd606c "nhận SIGTERM") *(nhận SIGTERM)* và chạy cùng uid 1000. Nhờ vậy dòng log vào được log Docker của container api. Nếu không mở được `/proc/1/fd/1` thì lệnh ghi ra stderr của chính nó. Cách này cần kiểm chứng khi implement;
  - sự kiện CLI không có `requestId`, `ip`, `userAgent`.
- **Lọc khi điều tra.** Lệnh `docker compose logs api | grep '"event":"auth.'` lọc ra cả sự kiện HTTP lẫn sự kiện CLI. Log nằm trong log Docker của container api, giữ tối đa 10 MB × 5 file theo [R-SKL-26](app-skeleton.md#s-0f1edd606c "Docker giới hạn log mỗi container") *(Docker giới hạn log mỗi container)*.
- **Địa chỉ IP.** Ở giai đoạn 0, `ip` luôn là địa chỉ gateway của Docker, vì cổng chỉ mở trên `127.0.0.1`. Khi triển khai sau reverse proxy, phải bật `trust proxy` để `req.ip` là IP thật của người gửi.
- **Không bao giờ ghi** mật khẩu, token, chuỗi băm, giá trị cookie hay thân request.
- Danh sách `redact` thêm `currentPassword`, `newPassword`, `confirmPassword` ở độ sâu 1 đến 3, cùng cách khai báo với `password`.

**R-AUT-31: Phiên không còn dùng được.** Khi app đưa người dùng về trang đăng nhập vì phiên không còn dùng được, trang đăng nhập hiện banner info "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại".

- Câu này trung tính. Nó đúng cho mọi trường hợp: phiên hết hạn, bị đăng xuất do đổi hoặc đặt lại mật khẩu, tài khoản bị xóa, cookie hỏng.

*Vì sao cần cờ.* Web không đọc được cookie vì cookie là `HttpOnly`. Khi phiên hết hạn tự nhiên, trình duyệt cũng tự bỏ cookie. Vì vậy web dùng cờ `mio.hadSession` trong `localStorage` ([câu hỏi mở 8](#s-505f20bb78 "Phiên hết hạn hoặc bị xóa") *(Phiên hết hạn hoặc bị xóa)*).

*Cách hoạt động*

- Web đặt cờ khi `GET /api/v1/sessions/current` trả 200. Web xóa cờ khi người dùng bấm "Đăng xuất" (trước khi gọi API, [R-AUT-32](#s-0f1edd606c "Bấm 'Đăng xuất'") *(Bấm "Đăng xuất")*) và khi đã dùng cờ để hiện banner.
- Web đọc và ghi cờ trong try/catch. Nếu lỗi (trình duyệt chặn lưu dữ liệu) thì coi như không có cờ và không báo lỗi.
- Khi mở hoặc tải lại app mà `GET /api/v1/sessions/current` trả 401:
  - có cờ: web xóa cờ, chuyển tới `/login?next=…` kèm banner;
  - không có cờ (chưa từng đăng nhập trên trình duyệt này, hoặc đã tự đăng xuất): web chuyển trang nhưng không có banner.
- Khi đang dùng app (đã có người dùng trong `auth-provider`) mà request API bất kỳ trả 401: web xóa người dùng và cờ, rồi chuyển tới `/login?next=<trang hiện tại>` kèm banner, không phụ thuộc cờ. Dữ liệu đang nhập dở trên form bị mất; điều này được chấp nhận.
- Banner được giữ trong `loginNotice` (bộ nhớ của `auth-provider`), không đưa vào URL hay `history.state`. Banner hiện một lần; tải lại `/login` thì không còn.

**R-AUT-32: Đăng xuất trên web.** Người dùng bấm "Đăng xuất" thì web xóa cờ `mio.hadSession` rồi gọi `DELETE /api/v1/sessions/current`.

- API trả 204: web chuyển tới `/login` kèm banner info "Bạn đã đăng xuất".
- Lỗi mạng hoặc 500: web vẫn chuyển tới `/login` nhưng không có banner "Bạn đã đăng xuất". Phiên và cookie có thể còn, nên lần mở sau người dùng sẽ tự vào lại; điều này được chấp nhận.

<a id="s-9ce7add77d"></a>

## Job và hàng đợi

Không áp dụng, vì tính năng không có việc chạy nền. Việc dọn phiên hết hạn và bộ đếm cũ được làm ngay trong lúc đăng nhập ([R-AUT-13](#s-0f1edd606c "Dọn dữ liệu") *(Dọn dữ liệu)*).

<a id="s-44dde0ce1e"></a>

## Trạng thái và thuật toán

Mục này mô tả vòng đời của phiên, của bộ đếm đăng nhập sai, và các thuật toán chính của tính năng.

<a id="s-9bddb6d695"></a>

### Phiên

**Tóm tắt.** Một phiên đi qua các trạng thái: không có phiên, còn hiệu lực, rồi hết hạn hoặc bị xóa. Phiên đã hết hạn hoặc bị xóa không khôi phục được.

**Chuyển trạng thái hợp lệ**

- Từ không có phiên sang còn hiệu lực: đăng nhập đúng ([R-AUT-08](#s-0f1edd606c "Đăng nhập đúng") *(Đăng nhập đúng)*), hoặc đổi mật khẩu thành công (phiên mới thay phiên hiện tại, [R-AUT-23](#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*).
- Còn hiệu lực và được gia hạn, vẫn còn hiệu lực: [R-AUT-10](#s-0f1edd606c "Hết hạn trượt") *(Hết hạn trượt)*.
- Từ còn hiệu lực sang hết hạn: 90 ngày không gia hạn.
- Từ còn hiệu lực sang bị xóa:
  - đăng xuất ([R-AUT-12](#s-0f1edd606c "Đăng xuất là route công khai và idempotent") *(Đăng xuất là route công khai và idempotent)*);
  - đổi mật khẩu: phiên hiện tại luôn bị thay; phiên của thiết bị khác bị xóa khi chọn đăng xuất ([R-AUT-23](#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*);
  - `reset-password` ([R-AUT-26](#s-0f1edd606c "reset-password --username <tên> và list-users") *(reset-password --username \<tên\> và list-users)*).
- Từ hết hạn sang bị xóa: [R-AUT-11](#s-0f1edd606c "Request tới route không công khai mà không có cookie") *(Request tới route không công khai mà không có cookie)*, [R-AUT-13](#s-0f1edd606c "Dọn dữ liệu") *(Dọn dữ liệu)*.

**Chuyển không hợp lệ.** Phiên hết hạn hoặc bị xóa không quay lại trạng thái còn hiệu lực. Người dùng phải đăng nhập lại.

<a id="s-ac5b970f48"></a>

### Bộ đếm đăng nhập sai (theo tên đăng nhập)

**Tóm tắt.** Mỗi tên đăng nhập có một bộ đếm ở một trong hai trạng thái: bình thường hoặc bị khóa. Hết khóa thì bộ đếm trở lại bình thường và đếm lại từ 0.

**Trạng thái**

- Bình thường: không có dòng, hoặc `failed_count` trong khoảng 0–4.
- Bị khóa: `locked_until` lớn hơn bây giờ.

**Chuyển trạng thái hợp lệ**

- Từ bình thường sang bình thường: lần sai thứ 1–4 trong cửa sổ. Cửa sổ quá 15 phút thì bắt đầu lại. Đăng nhập hoặc đổi mật khẩu đúng thì bộ đếm bị xóa.
- Từ bình thường sang bị khóa: lần sai thứ 5 trong cửa sổ.
- Từ bị khóa sang bình thường: hết 15 phút, hoặc chạy `reset-password` ([R-AUT-26](#s-0f1edd606c "reset-password --username <tên> và list-users") *(reset-password --username \<tên\> và list-users)*).

**Chuyển không hợp lệ**

- Từ bị khóa sang bị khóa: không được kéo dài khóa hay đếm thêm khi đang khóa.
- Từ bị khóa sang bình thường do đăng nhập hoặc đổi mật khẩu đúng: không được xảy ra; API vẫn trả 429.

**Chi tiết kỹ thuật**

Thuật toán `recordFailure(username, tx?)` chạy trong transaction và khóa dòng:

1. Đọc dòng của `username` bằng `SELECT … FOR UPDATE`. Không có dòng thì tạo `{ failed_count: 0, window_started_at: bây giờ }`.
2. Nếu `locked_until` lớn hơn bây giờ (đang khóa) thì không đổi gì và trả `{ isAlreadyLocked: true, lockedUntil }`.
3. Nếu `window_started_at` không muộn hơn bây giờ trừ 15 phút, hoặc `locked_until` khác rỗng và không muộn hơn bây giờ (khóa cũ đã hết), thì đặt `failed_count = 0`, `window_started_at = bây giờ`, `locked_until = null`.
4. Tăng `failed_count += 1`. Giá trị này được nhớ lại làm `failedCount` để trả về.
5. Nếu `failed_count` từ 5 trở lên thì đặt `locked_until = bây giờ + 15 phút` và `failed_count = 0`.
6. Ghi lại với `updated_at = bây giờ`, rồi trả `{ failedCount, lockedUntil, isAlreadyLocked: false }`. `lockedUntil` khác null nghĩa là lần này làm khóa.

Thuật toán `confirmSuccess(username, tx?)` cũng chạy trong transaction và khóa dòng. Hàm đọc dòng bằng `SELECT … FOR UPDATE`. Nếu `locked_until` lớn hơn bây giờ thì hàm trả khóa và không đổi gì. Ngược lại, hàm xóa dòng nếu có.

Hàm `getLock(username)` trả khóa khi có dòng và `locked_until` lớn hơn bây giờ. Hàm này chỉ để trả 429 sớm, không thay cho bước kiểm lại trong transaction.

<a id="s-039bb83697"></a>

### Đăng nhập (`AuthService.login`)

**Tóm tắt.** Hàm kiểm dữ liệu, kiểm khóa, kiểm mật khẩu, rồi ghi lần sai hoặc tạo phiên trong một transaction.

1. Kiểm hình thức bằng `loginInputSchema` ([R-AUT-01](#s-0f1edd606c "Tên đăng nhập trống") *(Tên đăng nhập trống)*, [R-AUT-02](#s-0f1edd606c "Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự") *(Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự)*, [R-AUT-03](#s-0f1edd606c "Mật khẩu là chuỗi rỗng") *(Mật khẩu là chuỗi rỗng)*, [R-AUT-04](#s-0f1edd606c "Mật khẩu dài hơn 128 ký tự") *(Mật khẩu dài hơn 128 ký tự)*). Có lỗi thì trả 400.
2. Chuẩn hóa tên ([R-AUT-07](#s-0f1edd606c "Tên đăng nhập được chuẩn hóa trước khi tra cứu") *(Tên đăng nhập được chuẩn hóa trước khi tra cứu)*) và dọn bộ đếm cũ ([R-AUT-13](#s-0f1edd606c "Dọn dữ liệu") *(Dọn dữ liệu)*).
3. Gọi `getLock`. Nếu đang khóa thì trả 429 ([R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)*).
4. Tìm người dùng. Không có người dùng thì chạy `verify` trên chuỗi băm giả, rồi sang bước 6.
5. Chạy `verify`. Chuỗi băm hỏng thì trả 500 (mục Xử lý lỗi). Mật khẩu đúng thì sang bước 7.
6. Mật khẩu sai thì gọi `recordFailure`:
   - `isAlreadyLocked` là đúng: trả 429 và ghi log `reason: locked`;
   - lần này làm khóa: trả 429;
   - các trường hợp còn lại: trả 401.
7. Mật khẩu đúng thì mở transaction và gọi `confirmSuccess`.
   - Đang khóa: trả 429, ghi log `auth.login.failed` với `reason: locked` và không tạo phiên.
   - Không khóa: băm lại mật khẩu nếu cần ([R-AUT-08](#s-0f1edd606c "Đăng nhập đúng") *(Đăng nhập đúng)*), xóa phiên của cookie đang gửi nếu phiên đó còn hiệu lực ([R-AUT-08](#s-0f1edd606c)), gọi `deleteExpired` rồi tạo phiên. Sau khi commit, API đặt cookie và trả 201.

<a id="s-5eab17c3ba"></a>

### Đổi mật khẩu (`AuthService.changePassword`)

**Tóm tắt.** Hàm kiểm dữ liệu, kiểm khóa, rồi kiểm mật khẩu hiện tại và ghi mật khẩu mới trong một transaction có khóa dòng `users`.

1. Kiểm hình thức bằng `changePasswordInputSchema` ([R-AUT-19](#s-0f1edd606c "Mật khẩu hiện tại trống") *(Mật khẩu hiện tại trống)*, [R-AUT-21](#s-0f1edd606c "Mật khẩu mới") *(Mật khẩu mới)* ba ý đầu, [R-AUT-23](#s-0f1edd606c "Đổi thành công") *(Đổi thành công)* `signOutOtherDevices`). Có lỗi thì trả 400 kèm mọi lỗi theo trường.
2. Gọi `getLock(username)`. Nếu đang khóa thì trả 429.
3. Mở transaction và gọi `lockById(tx, userId)`. Bước này xếp hàng với lần đổi khác và với `reset-password` ([R-AUT-23](#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*). Không còn người dùng thì trả 401.
4. Chạy `verify(currentPassword)` trên chuỗi băm vừa đọc. Chuỗi băm hỏng thì trả 500.
   - Mật khẩu hiện tại sai: gọi `recordFailure(username, tx)` rồi commit.
   - Nếu `isAlreadyLocked` hoặc lần này làm khóa thì trả 429. Các trường hợp còn lại trả 400 với `fields.currentPassword` "Mật khẩu hiện tại không đúng".
5. Gọi `confirmSuccess(username, tx)`. Nếu đang khóa thì trả 429 và không đổi gì.
6. Chạy `verify(newPassword)` trên chuỗi băm hiện tại. Nếu khớp thì trả 400 với `fields.newPassword` "Mật khẩu mới phải khác mật khẩu hiện tại"; lần này không bị đếm.
7. Lưu chuỗi băm mới và xóa phiên hiện tại. Nếu `signOutOtherDevices` là `true` thì xóa mọi phiên khác. Tạo phiên mới rồi commit. Cuối cùng API đặt cookie và trả 204.

<a id="s-7a7ee9d737"></a>

### Kiểm tra request (`AuthGuard`)

**Tóm tắt.** Guard kiểm tra mọi request theo 6 bước: route công khai, cookie, phiên, gia hạn, vai trò, rồi gắn người dùng vào request.

1. Route `@Public()` được đi tiếp. Guard vẫn đọc phiên nếu có, để `DELETE /sessions/current` và `POST /sessions` biết phiên nào cần xóa. Route công khai không gia hạn phiên ([R-AUT-10](#s-0f1edd606c "Hết hạn trượt") *(Hết hạn trượt)*).
2. Lấy token từ cookie `mio_session`. Không có token thì trả 401.
3. Tìm phiên theo `sha256(token)`, nối với bảng `users`. Không có phiên hoặc phiên hết hạn thì xóa phiên hết hạn (nếu có), xóa cookie và trả 401.
4. Gia hạn phiên nếu cần ([R-AUT-10](#s-0f1edd606c "Hết hạn trượt") *(Hết hạn trượt)*).
5. Kiểm vai trò theo `@Roles(...)`. Sai vai trò thì trả 403.
6. Gắn `req.user`.

<a id="s-2b1fe40749"></a>

## Tích hợp bên ngoài

Không áp dụng. Đăng nhập không dùng dịch vụ ngoài: không đăng nhập bằng Facebook/Google và không gửi email đặt lại mật khẩu.

<a id="s-a2cb20bfc7"></a>

## Xử lý lỗi, log, bảo mật, phân quyền

**Lỗi**

- DB không truy cập được khi đăng nhập hoặc khi kiểm phiên: API trả 500 `INTERNAL_ERROR` ([R-SKL-16](app-skeleton.md#s-0f1edd606c "lỗi không lường trước") *(lỗi không lường trước)*, [R-SKL-30](app-skeleton.md#s-0f1edd606c "kết nối PostgreSQL và Redis") *(kết nối PostgreSQL và Redis)*). Web hiện banner hoặc toast "Lỗi hệ thống, vui lòng thử lại sau".
- Web mất mạng khi gửi form: web hiện banner danger "Không kết nối được máy chủ. Kiểm tra mạng rồi thử lại." và giữ dữ liệu trên form.
- Cookie bị tắt trên trình duyệt: đăng nhập trả 201 nhưng `GET /sessions/current` ngay sau đó trả 401. Web hiện banner danger "Trình duyệt đang chặn cookie. Bật cookie cho trang này rồi đăng nhập lại.".
- `users.password_hash` không phải chuỗi PHC hợp lệ ([câu hỏi mở 9](#s-505f20bb78 "password_hash trong DB không phải chuỗi PHC hợp lệ") *(password\_hash trong DB không phải chuỗi PHC hợp lệ)*):
  - `verify` ném lỗi và API trả 500 `INTERNAL_ERROR` ([R-SKL-16](app-skeleton.md#s-0f1edd606c "lỗi không lường trước") *(lỗi không lường trước)*);
  - log ở mức error có `userId`, không có chuỗi băm;
  - lỗi này không được đếm vào [R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)* và không ghi `auth.login.failed` / `auth.password.change_failed`;
  - cách xử lý này áp dụng cho cả đăng nhập và đổi mật khẩu. Cách sửa là chạy `reset-password`.

**Log:** theo [R-AUT-30](#s-0f1edd606c "Log") *(Log)*.

**Bảo mật**

- Mật khẩu được băm bằng argon2id (04 mục 7). Tham số nằm ở [mục Tham số cài đặt](#s-d0d46a0edb). Khi tham số đổi, mật khẩu tự được băm lại ([R-AUT-08](#s-0f1edd606c "Đăng nhập đúng") *(Đăng nhập đúng)*).
- Token phiên chỉ được lưu dạng SHA-256. Vì vậy bản sao lưu DB không chứa token dùng được ([ADR 0015](../../../decisions/0015-server-side-sessions.md "Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…") *(Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…)*).
- Chống dò tên đăng nhập: thông báo và thời gian xử lý giống nhau ([R-AUT-05](#s-0f1edd606c "Tên đăng nhập không tồn tại hoặc mật khẩu sai") *(Tên đăng nhập không tồn tại hoặc mật khẩu sai)*). Giới hạn đăng nhập sai áp dụng cả với tên không tồn tại ([R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)*).
- Chống CSRF bằng `SameSite=Lax` cùng [R-AUT-17](#s-0f1edd606c "Chống CSRF") *(Chống CSRF)*. Chống nhúng khung bằng [R-AUT-18](#s-0f1edd606c "Header bảo mật trên mọi response của api") *(Header bảo mật trên mọi response của api)*.
- HTTPS và cookie `Secure` tự bật khi `PUBLIC_URL` là `https://`, tức là lúc triển khai lên máy chủ ([ADR 0009](../../../decisions/0009-local-first-deployment.md "Chạy trên máy local trước, giữ khả năng dời lên Oracle") *(Chạy trên máy local trước, giữ khả năng dời lên Oracle)*).
- Chưa giới hạn theo IP. Ở giai đoạn 0, mọi request tới từ cùng một địa chỉ, vì cổng chỉ mở trên `127.0.0.1` ([R-SKL-19](app-skeleton.md#s-0f1edd606c "compose") *(compose)*). Xem [câu hỏi mở 2](#s-505f20bb78 "Giới hạn đăng nhập sai? — đã chốt 2026-10-31 theo đề xuất") *(Giới hạn đăng nhập sai? — đã chốt 2026-10-31 theo đề xuất)*.

**Phân quyền:** [R-AUT-14](#s-0f1edd606c "Mặc định từ chối") *(Mặc định từ chối)*, [R-AUT-15](#s-0f1edd606c "Đã đăng nhập nhưng vai trò không nằm trong @Roles") *(Đã đăng nhập nhưng vai trò không nằm trong @Roles)*, [R-AUT-16](#s-0f1edd606c "Quyền của các route trong tính năng này") *(Quyền của các route trong tính năng này)*, [R-AUT-29](#s-0f1edd606c "Thanh điều hướng chỉ hiện mục mà vai trò được dùng") *(Thanh điều hướng chỉ hiện mục mà vai trò được dùng)*.

<a id="s-d0d46a0edb"></a>

## Tham số cài đặt

**Tóm tắt.** Tính năng không thêm khóa vào `app_settings`, vì 07 mục 2 không liệt kê tham số đăng nhập để chỉnh trên web. Các hằng được đặt trong `@mio/shared` (`src/auth/constants.ts`) hoặc trong api.

- **Thời hạn phiên (trượt):** 90 ngày. Nguồn: quyết định mới, hiện thực yêu cầu "giữ đăng nhập lâu dài trên điện thoại" (07 Yêu cầu chung); [câu hỏi mở 1](#s-505f20bb78 "Thời hạn giữ đăng nhập? — đã chốt 2026-10-31 theo đề xuất") *(Thời hạn giữ đăng nhập? — đã chốt 2026-10-31 theo đề xuất)*.
- **Chu kỳ gia hạn phiên tối thiểu:** 24 giờ. Nguồn: quyết định mới, để giảm ghi DB.
- **Giới hạn đăng nhập sai:** 5 lần trong 15 phút thì khóa 15 phút, tính theo tên đăng nhập. Nguồn: 04 mục 7 yêu cầu có giới hạn; con số là quyết định mới; [câu hỏi mở 2](#s-505f20bb78 "Giới hạn đăng nhập sai? — đã chốt 2026-10-31 theo đề xuất") *(Giới hạn đăng nhập sai? — đã chốt 2026-10-31 theo đề xuất)*.
- **Thời gian giữ dòng bộ đếm không khóa:** 24 giờ. Nguồn: quyết định mới.
- **Độ dài:** tên đăng nhập 3–32 ký tự, theo mẫu `^[a-z0-9._-]+$`; tên hiển thị 1–50 ký tự; mật khẩu 8–128 ký tự. Nguồn: quyết định mới.
- **argon2id:** `memoryCost` 19456 KiB, `timeCost` 2, `parallelism` 1. Đây là mức tối thiểu khuyến nghị của OWASP. Thư viện là `@node-rs/argon2`; thư viện có bản dựng sẵn cho linux x64 và arm64 nên không cần biên dịch. Nguồn: 04 mục 7 cho phép argon2 hoặc bcrypt; chọn argon2id là quyết định mới.
- **Tên cookie:** `mio_session`. Nguồn: [ADR 0015](../../../decisions/0015-server-side-sessions.md "Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…") *(Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…)*.

<a id="s-505f20bb78"></a>

## Câu hỏi mở

Cả 9 câu hỏi đều đã được chốt.

- [x] **1. Thời hạn giữ đăng nhập?** Đã chốt 2026-10-31 theo đề xuất. Phiên hết hạn sau 90 ngày không mở app. Mỗi lần dùng, phiên tự gia hạn. Không có hạn tuyệt đối. Lý do: thợ chủ yếu dùng Messenger, có thể vài tuần mới mở web app.
- [x] **2. Giới hạn đăng nhập sai?** Đã chốt 2026-10-31 theo đề xuất. Nhập sai 5 lần trong 15 phút thì tên đăng nhập đó bị khóa 15 phút. Giai đoạn 0 chưa giới hạn theo IP. Giới hạn theo IP được bổ sung khi triển khai lên máy chủ, vì cần đọc IP thật qua reverse proxy.
- [x] **3. Ai được đổi mật khẩu?** 07 mục 2 đặt "Đổi mật khẩu" trong Cài đặt (chỉ Quản lý), nhưng Thợ cũng cần đổi mật khẩu của mình. Đã chốt 2026-10-31 theo đề xuất: đưa "Đổi mật khẩu" ra khối tài khoản trên thanh điều hướng, để cả hai vai trò dùng được. Cài đặt › Người dùng ở giai đoạn 2 chỉ còn quản lý tài khoản thợ.
- [x] **4. Quên mật khẩu?** Đã chốt 2026-10-31 theo đề xuất. Không có luồng tự đặt lại, vì không có email người dùng. Người quản trị app (Hải) đặt lại bằng lệnh `reset-password` ([R-AUT-26](#s-0f1edd606c "reset-password --username <tên> và list-users") *(reset-password --username \<tên\> và list-users)*). Giai đoạn 2 thêm nút để Quản lý đặt lại mật khẩu cho thợ trên web.
  - Bổ sung 2026-10-31, khi người dùng hỏi: Hải cũng quên mật khẩu thì sao? Lệnh CLI không cần mật khẩu web, chỉ cần quyền vào máy chạy Docker (`docker compose exec`). Vì vậy Hải tự đặt lại mật khẩu của mình bằng `reset-password` như mọi tài khoản khác ([R-AUT-33](#s-0f1edd606c "Lệnh CLI không đòi đăng nhập web") *(Lệnh CLI không đòi đăng nhập web)*). Chỉ khi mất quyền vào máy (mật khẩu hệ điều hành, khóa SSH khi đã lên máy chủ) thì mới không đặt lại được; việc đó nằm ngoài app.
- [x] **5. ADR `0015-server-side-sessions`** (phiên lưu trong PostgreSQL, cookie mang token, kiểm tra `Origin`). Đã chốt 2026-10-31: chấp nhận.
- [x] **6. Có lưu sự kiện đăng nhập sai và bị khóa vào DB để Quản lý theo dõi trên web không?** Đã chốt 2026-10-31: giai đoạn 0 chỉ ghi log ([R-AUT-30](#s-0f1edd606c "Log") *(Log)*). Việc lưu DB và hiển thị trên Nhật ký hệ thống để sau, khi làm Nhật ký hệ thống đầy đủ.
- [x] **7. Nhiều request sai gửi đồng thời** (phát hiện ở `/test-case-design`, [P0-AUT-023](../test/cases/auth.md#s-c4d0d9075b "Nhiều lần đăng nhập sai gửi đồng thời") *(Nhiều lần đăng nhập sai gửi đồng thời)*).
  - Vấn đề: `getLock` nằm ngoài transaction và chạy trước `verify`, còn `recordFailure` vẫn đếm khi đang khóa. Hậu quả có thể là quá 5 lần đoán, lần khóa thứ hai kéo dài khóa, và request đúng mật khẩu lọt qua sau khi đã khóa.
  - Đã chốt 2026-10-31: sửa thuật toán để kiểm khóa lại trong cùng transaction có khóa dòng. Đang khóa thì trả 429, không đếm và không cho đăng nhập. [R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)* và mục Trạng thái đã được sửa ở `/design-review` ([RV-01](reviews/auth-review.md#s-548465f277 "R-AUT-06 và thuật toán bộ đếm chưa sửa theo câu hỏi mở 7") *(R-AUT-06 và thuật toán bộ đếm chưa sửa theo câu hỏi mở 7)*).
- [x] **8. Phiên hết hạn hoặc bị xóa, phát hiện lúc mở hoặc tải lại app (chưa nạp người dùng), có hiện banner "Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại" không?** (phát hiện ở `/test-case-design`, [P0-AUT-028](../test/cases/auth.md#s-d1822d6a99 "Phiên hết hạn") *(Phiên hết hạn)*).
  - Đã chốt 2026-10-31: có. Mọi lần app tự đưa về `/login` vì phiên không còn dùng được đều hiện banner này. Người chưa từng đăng nhập (không có cookie) thì không thấy banner.
  - R-AUT-31 đã được sửa ở `/design-review` ([RV-02](reviews/auth-review.md#s-49b8d93df9 "R-AUT-28, R-AUT-31 chưa nêu cách web biết phiên vừa mất (câ…") *(R-AUT-28, R-AUT-31 chưa nêu cách web biết phiên vừa mất (câ…)*): web dùng cờ `mio.hadSession` trong `localStorage`. Trình duyệt chặn lưu dữ liệu thì không hiện banner; người dùng chấp nhận điều này.
  - Câu banner đổi thành "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại" ([RV-12](reviews/auth-review.md#s-5becdb5c01 "Câu 'Phiên đăng nhập đã hết hạn' dùng cả khi phiên bị xóa") *(Câu "Phiên đăng nhập đã hết hạn" dùng cả khi phiên bị xóa)*).
- [x] **9. `password_hash` trong DB không phải chuỗi PHC hợp lệ** (phát hiện ở `/test-case-design`, [P0-AUT-075](../test/cases/auth.md#s-49b2222098 "Chuỗi băm mật khẩu trong DB bị hỏng") *(Chuỗi băm mật khẩu trong DB bị hỏng)*). Đã chốt 2026-10-31: trả 500 `INTERNAL_ERROR` ([R-SKL-16](app-skeleton.md#s-0f1edd606c "lỗi không lường trước") *(lỗi không lường trước)*), không coi là sai mật khẩu.

<a id="s-80b54c0db6"></a>

## Lịch sử thay đổi

- 2026-10-31: tạo mới.
- 2026-10-31: chốt câu hỏi 1, 2, 3, 4, 5. [ADR 0015](../../../decisions/0015-server-side-sessions.md "Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…") *(Phiên đăng nhập lưu phía server trong PostgreSQL, cookie ma…)* chuyển sang `chấp nhận`. Thêm [R-AUT-33](#s-0f1edd606c "Lệnh CLI không đòi đăng nhập web") *(Lệnh CLI không đòi đăng nhập web)*: CLI là đường khôi phục khi quên mật khẩu, trả lời câu hỏi 4.
- 2026-10-31: sửa theo góp ý của người dùng.
  - Thêm hộp thoại xác nhận đăng xuất thiết bị khác khi đổi mật khẩu ([R-AUT-34](#s-0f1edd606c "Đổi mật khẩu trên web luôn qua hộp thoại xác nhận 'có đăng…") *(Đổi mật khẩu trên web luôn qua hộp thoại xác nhận "có đăng…)*, sửa [R-AUT-23](#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*, thêm trường `signOutOtherDevices`).
  - R-AUT-30 bổ sung `ip`, `userAgent`, `userExists`, `failedCount` và sự kiện `auth.lock.started` có `source`, để theo dõi tấn công dò mật khẩu.
- 2026-10-31: chốt câu hỏi 6 (chỉ ghi log, lưu DB để sau); duyệt thiết kế.
- 2026-10-31: bước `/ui-design auth` thêm màn hình chờ và màn hình lỗi khi nạp phiên lúc mở app (mục Khung app), dẫn link mockup và component.
- 2026-10-31: sửa theo góp ý duyệt UI.
  - Vùng thông báo (banner) của màn Đăng nhập và Đổi mật khẩu chuyển xuống ngay trên nút gửi.
  - Thông báo `LOGIN_LOCKED` ([R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)*) đổi thành "Nhập sai mật khẩu quá nhiều lần. Thử lại sau <n> phút." để đúng nghĩa ở cả màn Đổi mật khẩu.
- 2026-10-31: bước `/test-case-design auth` thêm và chốt câu hỏi 7, 8, 9. Nội dung quy tắc chưa sửa, chờ `/design-review`.
- 2026-10-31: bước `/design-review auth` (`reviews/auth-review.md`):
  - [RV-01](reviews/auth-review.md#s-548465f277 "R-AUT-06 và thuật toán bộ đếm chưa sửa theo câu hỏi mở 7") *(R-AUT-06 và thuật toán bộ đếm chưa sửa theo câu hỏi mở 7)*: [R-AUT-06](#s-0f1edd606c "Giới hạn đăng nhập sai") *(Giới hạn đăng nhập sai)* và thuật toán bộ đếm kiểm lại khóa trong transaction (`recordFailure`, `confirmSuccess`); thêm chuyển trạng thái và thuật toán đổi mật khẩu;
  - [RV-02](reviews/auth-review.md#s-49b8d93df9 "R-AUT-28, R-AUT-31 chưa nêu cách web biết phiên vừa mất (câ…") *(R-AUT-28, R-AUT-31 chưa nêu cách web biết phiên vừa mất (câ…)*, [RV-12](reviews/auth-review.md#s-5becdb5c01 "Câu 'Phiên đăng nhập đã hết hạn' dùng cả khi phiên bị xóa") *(Câu "Phiên đăng nhập đã hết hạn" dùng cả khi phiên bị xóa)*: [R-AUT-31](#s-0f1edd606c "Phiên không còn dùng được") *(Phiên không còn dùng được)* dùng cờ `mio.hadSession`, banner nằm trong bộ nhớ, câu banner là "Phiên đăng nhập đã kết thúc, vui lòng đăng nhập lại";
  - [RV-03](reviews/auth-review.md#s-c007295390 "Câu hỏi mở 9 chưa đưa vào mục Xử lý lỗi") *(Câu hỏi mở 9 chưa đưa vào mục Xử lý lỗi)*: mục Xử lý lỗi thêm trường hợp chuỗi băm hỏng;
  - [RV-04](reviews/auth-review.md#s-a6d1239d02 "Hai lần đổi mật khẩu đồng thời có thể mất cập nhật") *(Hai lần đổi mật khẩu đồng thời có thể mất cập nhật)*: [R-AUT-23](#s-0f1edd606c "Đổi thành công") *(Đổi thành công)*, [R-AUT-26](#s-0f1edd606c "reset-password --username <tên> và list-users") *(reset-password --username \<tên\> và list-users)* khóa dòng `users`;
  - [RV-05](reviews/auth-review.md#s-c02158d7d3 "failedCount của lần sai làm khóa chưa rõ") *(failedCount của lần sai làm khóa chưa rõ)*: [R-AUT-30](#s-0f1edd606c "Log") *(Log)* ghi `failedCount` của lần làm khóa là 5;
  - [RV-06](reviews/auth-review.md#s-808024fba1 "Thứ tự kiểm tra chưa tính bước đọc thân request") *(Thứ tự kiểm tra chưa tính bước đọc thân request)*: [R-AUT-15](#s-0f1edd606c "Đã đăng nhập nhưng vai trò không nằm trong @Roles") *(Đã đăng nhập nhưng vai trò không nằm trong @Roles)* thêm bước đọc thân request; kiểm `Origin` trước body parser;
  - [RV-07](reviews/auth-review.md#s-a02048905c "Đổi mật khẩu: trường sai kiểu chưa có quy tắc") *(Đổi mật khẩu: trường sai kiểu chưa có quy tắc)*: [R-AUT-21](#s-0f1edd606c "Mật khẩu mới") *(Mật khẩu mới)* xử lý trường sai kiểu;
  - [RV-08](reviews/auth-review.md#s-5fc14e1926 "Tên đăng nhập dài hơn 32 ký tự sau khi đổi chữ thường làm l…") *(Tên đăng nhập dài hơn 32 ký tự sau khi đổi chữ thường làm l…)*: [R-AUT-02](#s-0f1edd606c "Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự") *(Tên đăng nhập đã chuẩn hóa dài hơn 32 ký tự)* đo độ dài sau khi chuẩn hóa;
  - [RV-09](reviews/auth-review.md#s-50f58f0b24 "Log của lệnh CLI không nằm trong docker compose logs api") *(Log của lệnh CLI không nằm trong docker compose logs api)*: [R-AUT-30](#s-0f1edd606c "Log") *(Log)* ghi log CLI vào `/proc/1/fd/1`;
  - [RV-10](reviews/auth-review.md#s-0d67ff357a "Đăng xuất lỗi: chưa rõ có hiện 'Bạn đã đăng xuất' không") *(Đăng xuất lỗi: chưa rõ có hiện "Bạn đã đăng xuất" không)*: [R-AUT-32](#s-0f1edd606c "Bấm 'Đăng xuất'") *(Bấm "Đăng xuất")* chỉ hiện "Bạn đã đăng xuất" khi API trả 204;
  - [RV-11](reviews/auth-review.md#s-5c756ce928 "403 khi gửi form hiện bằng toast, trái quy ước vị trí thông…") *(403 khi gửi form hiện bằng toast, trái quy ước vị trí thông…)*: [R-AUT-29](#s-0f1edd606c "Thanh điều hướng chỉ hiện mục mà vai trò được dùng") *(Thanh điều hướng chỉ hiện mục mà vai trò được dùng)* khi gặp 403 lúc gửi form thì hiện banner và gọi `refresh()`;
  - [RV-13](reviews/auth-review.md#s-c731f7368d "Một trường có hai lỗi cùng lúc: chưa nói hiện lỗi nào") *(Một trường có hai lỗi cùng lúc: chưa nói hiện lỗi nào)*: thêm quy tắc chung mỗi trường một lỗi;
  - [RV-14](reviews/auth-review.md#s-a5227a25e1 "Kiểm tra next chưa chặn ký tự điều khiển") *(Kiểm tra next chưa chặn ký tự điều khiển)*: [R-AUT-28](#s-0f1edd606c "Chưa đăng nhập mà mở trang cần đăng nhập") *(Chưa đăng nhập mà mở trang cần đăng nhập)* chặn ký tự điều khiển trong `next` và chuyển trang bằng router;
  - [RV-15](reviews/auth-review.md#s-0d0fe48bc0 "Phiên khi gọi route công khai lúc đang có cookie") *(Phiên khi gọi route công khai lúc đang có cookie)*: [R-AUT-08](#s-0f1edd606c "Đăng nhập đúng") *(Đăng nhập đúng)* đăng nhập thay phiên cũ; [R-AUT-10](#s-0f1edd606c "Hết hạn trượt") *(Hết hạn trượt)* route công khai không gia hạn;
  - [RV-16](reviews/auth-review.md#s-957cb7b3be "CLI: thứ tự hỏi mật khẩu và kiểm tham số") *(CLI: thứ tự hỏi mật khẩu và kiểm tham số)*: [R-AUT-25](#s-0f1edd606c "create-user --username <tên> --role <manager\|technician> --…") *(create-user --username \<tên\> --role \<manager\|technician\> --…)*, [R-AUT-26](#s-0f1edd606c "reset-password --username <tên> và list-users") *(reset-password --username \<tên\> và list-users)* kiểm tham số trước khi hỏi mật khẩu.
- 2026-10-31: duyệt thiết kế sau `/design-review` (Hải).
