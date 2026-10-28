# 04 – Kỹ thuật

Phần này ghi lại các quyết định kỹ thuật **đã chốt với chủ tiệm**, các **đề xuất của người viết** (có đánh dấu), và những gì **để người code tự quyết**.

---

## 1. Đã chốt

- **Người code:** Claude Code.
- **Nền tảng:** kế thừa POC `D:\Personal\Projects\fb-post-crawler-poc`. POC dùng Node.js + TypeScript, Playwright + Chromium với phiên đăng nhập lưu lại, zod, vitest.
- **Kiến trúc** theo file ý tưởng `D:\Personal\Files\facebook-group-auto-promotion-playwright-idea.md`:
  - NestJS làm backend: lịch chạy, API, xử lý nghiệp vụ;
  - BullMQ + Redis làm hàng đợi;
  - PostgreSQL làm cơ sở dữ liệu;
  - worker trình duyệt chạy Playwright.
- **Nơi chạy:** **Oracle Cloud Free Tier**, một máy ảo chạy 24/7. Ưu tiên không tốn tiền máy chủ.
- **AI:**
  - **Phần chữ** (phân loại bài, trích ngày giờ, mô tả 1 dòng từ ảnh, viết content, hiểu tin nhắn khách và thợ): **Google Gemini, gói miễn phí**, model Flash hoặc Flash-Lite.
  - **Phần chỉnh ảnh:** **Google Gemini Nano Banana 2.1, ảnh 2K, trả phí theo lượt** (khoảng 6 USD/tháng với 4 ảnh/ngày). Dự phòng: chủ tiệm tự chỉnh rồi tải ảnh lên.
- **Group Facebook:** tự động hóa **hoàn toàn** bằng trình duyệt. Chủ tiệm chấp nhận rủi ro và sẽ thử trước bằng tài khoản phụ.
- **Inbox khách:** tiệm chưa có giấy phép kinh doanh, nên dùng **trình duyệt tự động trên Meta Business Suite** (mục 4.3). Kênh thợ và đăng Page vẫn dùng đường chính thức.
- **Thiết bị:** chủ tiệm dùng **iPhone**, thợ dùng **Android**.
- **Giá:** phiên bản này không tự ước tính. Luôn hỏi thợ.

---

## 2. Tái sử dụng POC

Những phần dùng lại gần như nguyên vẹn, chuyển thành module trong app:
- `browser.ts`: mở persistent context, kiểm tra trạng thái đăng nhập.
- `crawler/capture.ts`, `crawler/group-page.ts`, `crawler/group-crawler.ts`, `crawler/stop-condition.ts`, `crawler/dom-check.ts`: quét group bằng cách bắt các response GraphQL và JSON nhúng trong trang.
- `parser/story-parser.ts`: biến payload thô thành `Post`.
- Cách phân loại lỗi trong `errors.ts`: `SessionExpiredError`, `CheckpointError`, `GroupInaccessibleError`.
- Cơ chế debug dump (ảnh màn hình và HTML khi lỗi), script ẩn thông tin cá nhân trong fixture, các test dựa trên fixture thật.

Những phần thay đổi:
- `post-store.ts` (ghi file JSON) được thay bằng PostgreSQL, nhưng **giữ nguyên quy tắc merge**: không ghi đè `firstSeenAt`, không ghi đè bằng `null`.
- `cli/crawl.ts` (chạy một lần) được thay bằng job định kỳ trong hàng đợi.
- Cấu hình chuyển từ `.env` sang cài đặt trong cơ sở dữ liệu. Chỉ giữ các khóa bí mật và đường dẫn trong `.env`.

Những việc POC chưa trả lời được và cần kiểm chứng sớm (giai đoạn 0 và 1, xem `05-roadmap.md`):
- Chạy Chromium + Playwright trên máy ARM của Oracle.
- Phiên đăng nhập có ổn định khi chạy 24/7 từ IP máy chủ không.
- Comment và đăng bài group bằng Playwright, kèm ảnh.
- Mỗi chu kỳ quét cần scroll bao nhiêu là đủ.

---

## 3. Kiến trúc đề xuất

(Đề xuất của người viết. Người code được điều chỉnh nếu có lý do.)

```text
Oracle Cloud Free VM (Ampere A1 ARM, tối đa 4 OCPU / 24GB RAM)
│
├── Reverse proxy HTTPS (Caddy + tên miền, hoặc Cloudflare Tunnel miễn phí)
│     ├── Web app (PWA) cho chủ tiệm và thợ
│     └── Webhook Messenger của Meta (chỉ cho kênh thợ)
│
├── NestJS (API + lịch chạy + nghiệp vụ)
├── Worker hàng đợi (BullMQ)
│     ├── fb-browser   (concurrency = 1): quét group, comment, đăng group
│     ├── fb-inbox     (concurrency = 1): đọc/trả lời inbox khách trên Business Suite
│     │                 (gộp với fb-browser nếu dùng chung tài khoản; inbox ưu tiên cao nhất)
│     ├── ai-text      : phân loại, trích xuất, viết content, hiểu tin nhắn
│     ├── ai-image     : chỉnh ảnh
│     ├── render       : render poster HTML → PNG
│     ├── messenger    : gửi tin qua Send API, có retry
│     └── page-publish : đăng Page qua Graph API
├── Redis
├── PostgreSQL
└── Ổ đĩa: ảnh gốc, ảnh đã chỉnh, poster, debug dump
```

Ghi chú về các thành phần:
- **Mọi thao tác dùng tài khoản vận hành** (quét, comment, đăng group) đi qua **một hàng đợi duy nhất, chạy từng việc một**, dùng **một** persistent context. Như vậy tài khoản không bao giờ làm hai việc cùng lúc, và phanh an toàn được áp dụng ở một chỗ.
- **Render poster** dùng một Chromium riêng, không gắn profile Facebook.
- **Đóng gói:** đề xuất Docker Compose cho toàn bộ dịch vụ. Image Playwright phải là bản linux/arm64.
- **Giao diện web:** đề xuất một SPA (ví dụ React + Vite) có PWA và web push, do NestJS phục vụ. Người code tự chọn framework.
- **HTTPS là bắt buộc**, vì webhook của Meta và web push đều yêu cầu.
  - Cần một **tên miền cố định**. Quick tunnel của Cloudflare đổi URL mỗi lần chạy nên không dùng được cho webhook.
  - Đề xuất miễn phí: tên miền phụ của **DuckDNS** (hoặc dịch vụ DNS động miễn phí tương tự) + Caddy tự lấy chứng chỉ Let's Encrypt.
  - Nếu chủ tiệm mua tên miền riêng (khoảng vài trăm nghìn đồng/năm) thì dùng tên miền đó.
- **Vùng Oracle:** Oracle không có vùng ở Việt Nam. Chọn vùng gần nhất còn máy Ampere A1 (ví dụ Singapore). Đăng nhập Facebook từ IP nước ngoài làm tăng nguy cơ checkpoint, cần theo dõi ở giai đoạn 0.
- **Giờ hệ thống:** mọi lịch chạy dùng múi giờ `Asia/Ho_Chi_Minh`.

---

## 4. Facebook: hai phần với mức rủi ro khác nhau

### 4.1 Phần chính thức (Page): Messenger Platform và Graph API
Dùng cho **kênh thợ** và **đăng bài lên Page**. Inbox khách **không** dùng phần này (xem 4.3).

**Cần chuẩn bị:**
- Tạo **Meta app** trên developers.facebook.com.
- Kết nối với Page, lấy **Page access token dài hạn**.
- Đăng ký webhook (`messages`, `messaging_postbacks`, `message_echoes`, `message_reads` nếu cần).
- **Kiểm tra chữ ký** `X-Hub-Signature-256` của mọi webhook.

**Quyền cần có:**
- `pages_messaging`, `pages_manage_metadata`, `pages_read_engagement`, `pages_manage_posts`, `pages_show_list`.
- Tên quyền chính xác cần kiểm tra lại theo tài liệu hiện hành của Meta.

**Chế độ phát triển (không xin App Review):**
- Khi Meta app còn ở **chế độ phát triển**, app chỉ nhắn tin được với những người **có vai trò trong Meta app** (admin, developer, tester).
  - → Thêm thợ và chủ tiệm làm tester, thì **kênh thợ chạy được ngay**, không cần duyệt.
  - → Đăng bài lên Page của chính mình *có lẽ* cũng chạy được ở chế độ này. **Cần xác minh.**
- **Không xin App Review.** Muốn nhắn với khách thật qua đường chính thức thì cần Advanced Access cho `pages_messaging`, mà việc này thường đòi **xác minh doanh nghiệp**. Tiệm chưa có giấy phép kinh doanh nên không làm được.
  - Ở chế độ phát triển, Meta **chỉ gửi webhook tin nhắn của người có vai trò trong Meta app**. Tin của khách thật không về tới app, kể cả khi chỉ muốn đọc.
  - → App giữ Meta app ở **chế độ phát triển vĩnh viễn**, chỉ dùng cho thợ và chủ tiệm (tester).
  - Khi tiệm có giấy phép, có thể xin quyền và chuyển inbox khách sang đường chính thức. Nhờ lớp "kênh inbox" tách riêng (4.3), phần nghiệp vụ không phải sửa.
- **Cần xác minh ở giai đoạn 2:** webhook có gửi tin nhắn của tester về ổn định khi Page cũng đang được một trình duyệt tự động đọc hay không. Việc trình duyệt mở inbox có thể đánh dấu tin là đã đọc, nhưng không được ảnh hưởng tới webhook.

**Cửa sổ 24 giờ:**
- Page chỉ được nhắn tự động trong 24 giờ kể từ tin gần nhất của người kia. Xem cách xử lý ở chức năng 02, mục 7.
- Không dùng message tag để lách quy định.

**Nhận ra người thật đã trả lời:**
- Dùng `message_echoes`. Tin echo không do app gửi (kiểm tra `app_id` hoặc metadata do app gắn) thì coi là người thật trả lời.

**Trả lời trực tiếp vào tin nhắn:**
- Khi thợ vuốt để trả lời một tin, webhook có trường `reply_to.mid`. Dùng trường này để ghép câu trả lời với yêu cầu.
- Có nút bấm nhanh (quick reply) để thợ chọn.

### 4.2 Phần không chính thức (group): trình duyệt tự động
- Facebook **không có API** để đọc bài trong group hay comment bằng tài khoản cá nhân. Điều khiển Facebook bằng tool tự động **vi phạm Điều khoản của Meta**, nên tài khoản có thể bị checkpoint hoặc khóa. Chủ tiệm đã biết và chấp nhận rủi ro này.
- **Đăng nhập trên máy chủ không có màn hình:**
  - Đề xuất chạy màn hình ảo (Xvfb) và **noVNC**, truy cập qua SSH tunnel. Chủ tiệm mở trình duyệt từ xa để đăng nhập lần đầu và tự giải checkpoint khi bị yêu cầu.
  - Không nên đăng nhập trên máy cá nhân rồi copy profile lên máy chủ, vì đổi IP đột ngột dễ bị checkpoint.
- **IP máy chủ:** IP datacenter của Oracle dễ bị Facebook nghi ngờ hơn IP nhà mạng.
  - Cần theo dõi trong giai đoạn thử.
  - Nếu bị chặn nhiều, phương án là dùng proxy dân cư (tốn phí) hoặc một máy ở nhà làm worker trình duyệt. Chưa làm ở phiên bản này.
- **Comment và đăng bài bằng thao tác giao diện:**
  - Selector dễ hỏng khi Facebook đổi giao diện.
  - Ưu tiên selector theo vai trò hoặc nhãn (`role`, `aria-label`) thay vì class.
  - Luôn lưu ảnh màn hình và HTML khi lỗi, như POC.
  - Có test với trang HTML lưu sẵn.
- **Nhịp thao tác:** làm như người thật. Giãn cách ngẫu nhiên, gõ từng đoạn, giới hạn số lượng, có giờ nghỉ, tự dừng khi bất thường (chức năng 01, mục 8).
  - Phạm vi là **giới hạn tốc độ và hành vi hợp lý**.
  - Không làm giả dấu vân tay trình duyệt, không xoay vòng nhiều tài khoản.
- **Khối lượng hiện tại:** 6 group (có thể tăng), khoảng 50–100 bài mới mỗi ngày.
  - Mỗi chu kỳ quét mất khoảng 6–8 phút, nên mục tiêu 10 phút trong giờ vàng khả thi.
  - Sau khi lọc từ khóa, số lượt gọi Gemini cho phân loại nằm trong khoảng vài chục đến 100 mỗi ngày, vừa với gói miễn phí.
  - Khi số group tăng lên đáng kể (ví dụ trên 12), cần xem lại chu kỳ quét.

### 4.3 Inbox khách: trình duyệt tự động trên Meta Business Suite
- **Đã chốt với chủ tiệm** (phương án b): đọc và trả lời inbox Page bằng Playwright trên Meta Business Suite. Rủi ro tương tự phần group.
- **Tài khoản dùng cho inbox** (quyết định của người viết):
  - Không dùng tài khoản đang **sở hữu Page** (Huỳnh Mio) cho tự động. Nếu tài khoản đó bị khóa, tiệm mất quyền quản lý Page.
  - Thêm một **tài khoản riêng** vào Page, chỉ cấp quyền nhắn tin (task access "Tin nhắn"), và dùng tài khoản này cho worker inbox. Có thể dùng chung tài khoản vận hành của group, hoặc dùng một tài khoản khác để tách rủi ro. Chủ tiệm chọn.
- **Hàng đợi:**
  - Mỗi tài khoản có hàng đợi trình duyệt riêng, chạy từng việc một.
  - Nếu dùng chung tài khoản với group, inbox được **ưu tiên cao nhất**, vì khách đang chờ.
- **Lớp "kênh inbox" tách riêng:**
  - Nghiệp vụ (hiểu ý, trả lời, lịch, trạng thái khách) chỉ làm việc với interface "đọc tin mới / gửi tin / đọc lịch sử cuộc trò chuyện".
  - Bản cài đặt hiện tại dùng trình duyệt. Sau này có thể thay bằng Messenger Platform.
- **Định danh khách:** dùng ID cuộc trò chuyện hoặc ID người dùng lấy được từ Business Suite (từ URL hoặc dữ liệu GraphQL, cách làm giống crawler của POC). Ưu tiên bắt dữ liệu mạng hơn đọc giao diện.
- **Gửi ảnh** (ví dụ poster) qua inbox: hỗ trợ đính kèm file, giống lúc comment.
- **Tự dừng khi bất thường:** giống phần group. Inbox dừng thì báo khẩn cho chủ tiệm.

---

## 5. Gemini

**Hai project Google tách biệt:**
- **Project miễn phí** (không bật thanh toán) cho phần chữ.
- **Project trả phí** chỉ dùng cho Nano Banana.
- Lý do: Google tính miễn phí hay trả phí theo từng project. Bật thanh toán cho một project thì mọi lượt gọi trong project đó đều tính tiền.

**Lưu ý về dữ liệu:** với gói miễn phí, dữ liệu gửi lên có thể được Google dùng để cải thiện sản phẩm. Dữ liệu này gồm cả tin nhắn của khách. Xem `06-open-issues-and-assumptions.md`.

**Giới hạn lượt gọi của gói miễn phí:**
- Hàng đợi `ai-text` phải tôn trọng giới hạn mỗi phút và mỗi ngày, có backoff khi bị trả lỗi 429.
- Ưu tiên theo thứ tự: tin nhắn khách và thợ > phân loại bài > viết content.

**Đầu ra có cấu trúc:** mọi tác vụ phân loại và trích xuất dùng **JSON schema** (structured output), rồi validate lại bằng zod.

**Prompt:**
- Lưu prompt thành file trong repo, có phiên bản.
- Các phần chủ tiệm chỉnh được (giọng tiệm, từ cấm, bộ prompt ảnh) lấy từ cài đặt và ghép vào prompt.

**Thay nhà cung cấp:** tách lớp "nhà cung cấp AI" (chữ và ảnh) thành interface. Sau này đổi sang Groq, OpenRouter hoặc model local thì không phải sửa nghiệp vụ.

**Theo dõi chi phí:**
- Ghi số lượt và chi phí ước tính của phần ảnh.
- Có hạn mức tháng. Vượt hạn mức thì chuyển sang dự phòng tải ảnh lên tay.

**Tên model và giá có thể đổi.** Lấy tên model từ cài đặt, không viết cứng trong code.

---

## 6. Render poster

- Mẫu poster là HTML/CSS có các trường điền vào. Dùng Playwright mở trang rồi chụp ảnh đúng khổ **1080×1350**.
- **Font đặt sẵn trong máy** (Playfair Display, Dancing Script, Be Vietnam Pro), không tải từ internet lúc render. Phải hiển thị đúng tiếng Việt có dấu.
- Ảnh trong mẫu dùng `object-fit: cover` với vị trí chỉnh được.
- Mẫu đầu tiên được chuyển từ các file `.dc.html` trên canvas Claude Design (xem chức năng 05, mục 3).

---

## 7. Lưu trữ, sao lưu, bảo mật

- **Ảnh và debug dump:** lưu trên block volume của máy ảo. Dọn debug dump cũ hơn 14 ngày.
- **Sao lưu hằng đêm** (đề xuất): `pg_dump` và thư mục ảnh lên **Oracle Object Storage**, trong hạn mức miễn phí. Giữ 7 bản gần nhất.
- **Khóa bí mật** (Page token, Meta app secret, khóa Gemini, mật khẩu cơ sở dữ liệu) để trong biến môi trường hoặc file bí mật, không đưa vào repo.
- **Profile trình duyệt** chứa phiên đăng nhập Facebook của tài khoản vận hành. Thư mục này chỉ người chạy dịch vụ được đọc, và không đưa vào bản sao lưu công khai.
- **Web app:** mật khẩu băm (argon2 hoặc bcrypt), phiên đăng nhập an toàn, giới hạn số lần đăng nhập sai.

---

## 8. Kiểm thử

Giữ cách làm của POC: vitest và fixture thật đã ẩn thông tin cá nhân.

**Unit test bắt buộc cho:**
- tìm khung trống và chống trùng lịch, kể cả thời gian đệm, ngày đặc biệt, buổi;
- quy đổi ngày tương đối ("mai", "T3", "tối nay") theo thời điểm bài được đăng;
- ghép câu trả lời của thợ với yêu cầu (mục 4 của chức năng 02);
- chuyển trạng thái lịch hẹn và trạng thái khách;
- phanh an toàn (đếm giới hạn, giờ nghỉ);
- kiểm tra từ cấm;
- xử lý webhook Messenger (fixture JSON), gồm echo, reply_to, quick reply.

**Bộ đánh giá phân loại bài:**
- Lấy 100–200 bài thật từ các lượt quét đầu, chủ tiệm gắn nhãn (không phù hợp / loại 1 / 2 / 3).
- Dùng để đo độ chính xác mỗi khi đổi prompt.
- Mục tiêu đề xuất: **không comment nhầm bài không phù hợp quá 2%**.

**Test thủ công trên tài khoản phụ** cho các thao tác comment và đăng group, trước khi bật chế độ tự gửi.

---

## 9. Rủi ro chính

- **Tài khoản vận hành bị checkpoint hoặc khóa.** Giảm thiểu bằng: thử với tài khoản phụ, phanh an toàn, tự dừng, mặc định chế độ duyệt trước.
- **Tài khoản dùng cho inbox bị khóa**, nên khách không được tự trả lời. Giảm thiểu: dùng tài khoản riêng chỉ có quyền nhắn tin, tự dừng và báo khẩn, người thật trả lời thay.
- **Cửa sổ 24 giờ** làm kênh thợ bị gián đoạn. Giảm thiểu: nút giữ cửa sổ, web push.
- **Facebook đổi cấu trúc GraphQL hoặc giao diện.** Giảm thiểu: parser theo dấu hiệu, debug dump, báo lỗi rõ ràng.
- **IP datacenter bị nghi ngờ.** Theo dõi trong giai đoạn thử.
- **Gói miễn phí Gemini bị giảm hạn mức hoặc đổi chính sách.** Giảm thiểu: interface nhà cung cấp, hàng đợi có ưu tiên.
- **AI hiểu sai** thời gian, giá, ý định. Giảm thiểu: lấy dữ liệu từ nguồn thật (lịch, bộ thông tin, câu trả lời của thợ), AI chỉ diễn đạt lại; có xác nhận lại với thợ; có bộ đánh giá.
- **Tài nguyên máy Oracle Free** (ARM, RAM chung cho Chromium, PostgreSQL, Redis). Kiểm chứng ở giai đoạn 0.
