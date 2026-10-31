> Bản đọc sinh từ docs/phases/phase-0/status.md (phiên bản dbdfe09, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# Giai đoạn 0 – Nền móng

**Tóm tắt.** Trang theo dõi giai đoạn 0: phạm vi, tiêu chí hoàn thành, danh sách tính năng, vấn đề đang chặn và nhật ký duyệt.

<a id="s-48616d4e75"></a>

## Phạm vi

**Tóm tắt.** Giai đoạn 0 dựng khung app chạy được bằng Docker trên máy local. Khung này phải dời được lên máy chủ sau này mà không sửa code, và phải kiểm chứng được những điều kiện kỹ thuật lớn.

**Trong phạm vi**
- App chạy bằng Docker Compose trên máy local (x64).
- Image phải build được cho cả linux/amd64 và linux/arm64 (ADR `0009-local-first-deployment`).
- Email khẩn khi app tự dừng được làm sớm từ giai đoạn 1. Phần này thuộc tính năng `emergency-stop`.

**Ngoài phạm vi**
- Dựng VM Oracle, HTTPS và tên miền: chuyển sang mục "Triển khai lên máy chủ" của roadmap. Lý do là chưa đăng ký được Oracle Free.
- Lọc từ khoá, lọc tuổi bài, phân loại AI và comment: làm ở giai đoạn 1.
- Cài PWA và web push: làm ở giai đoạn 1 vì cần HTTPS.
- Màn hình quản lý tài khoản thợ: làm ở giai đoạn 2, khi thợ bắt đầu dùng app. Giai đoạn 0 tạo tài khoản bằng lệnh CLI.
- Trang chính đầy đủ và Nhật ký hệ thống đầy đủ: giai đoạn 0 chỉ có khối "Trạng thái tự động hóa" và sự kiện tự dừng.

<a id="s-367ffe870c"></a>

## Tiêu chí Xong khi

**Tóm tắt.** Giai đoạn 0 xong khi việc quét chạy ổn định đủ thời gian, bài mới vào DB kịp thời và đã đo được tài nguyên của từng container.

- Chạy quét bằng Docker trên máy local **tổng cộng ít nhất 24 giờ**, có thể chia thành nhiều lần. Việc quét dùng tài khoản phụ và không bị đăng xuất. Nếu bị đăng xuất, app phải tự dừng và báo đúng.
- Bài mới trong group xuất hiện trong cơ sở dữ liệu trong vòng 1 chu kỳ quét.
- Mức RAM và CPU thực tế của từng container được ghi lại để ước lượng cho máy chủ.

<a id="s-6a0f83aaf4"></a>

## Tính năng

**Tóm tắt.** Giai đoạn 0 có 9 tính năng. Tính năng `app-skeleton` và `auth` đã duyệt thiết kế, các tính năng còn lại chưa bắt đầu.

**Thứ tự thiết kế đề xuất**
1. app-skeleton
2. auth
3. crawler-verification
4. group-settings
5. crawl-settings
6. fb-account-session
7. group-crawl-job
8. emergency-stop
9. backup

Bảng dưới liệt kê từng tính năng với mã, việc có màn hình hay không, tài liệu liên quan và trạng thái hiện tại.

| Slug | Mã | Có màn hình | Tài liệu liên quan | Trạng thái |
|---|---|---|---|---|
| app-skeleton | SKL | không | 04-technical.md mục 1, 3; 05-roadmap.md giai đoạn 0; [ADR 0009](../../decisions/0009-local-first-deployment.md "Chạy trên máy local trước, giữ khả năng dời lên Oracle") *(Chạy trên máy local trước, giữ khả năng dời lên Oracle)* | đã duyệt thiết kế |
| auth | AUT | có | 07-screens-and-settings.md Yêu cầu chung, mục 2 Người dùng; 03-data-model.md mục 1; 04 mục 7 | đã duyệt thiết kế |
| crawler-verification | VRF | không | 05-roadmap.md giai đoạn 0; 04 mục 2; spec POC mục 9 (checklist), mục 10 | chưa bắt đầu |
| group-settings | GRP | có | 07 mục 2 Group; 01-group-auto-comment.md mục 2; 03 mục 2 | chưa bắt đầu |
| crawl-settings | CRS | có | 07 mục 2 Quét và comment (lịch quét); 01 mục 2 Lịch quét, Giới hạn lượt quét | chưa bắt đầu |
| fb-account-session | ACC | có | 07 mục 2 Tài khoản vận hành; 04 mục 4.2 | chưa bắt đầu |
| group-crawl-job | CRW | không | 01 mục 2, 10; 03 mục 2, 7; 04 mục 2, 3 | chưa bắt đầu |
| emergency-stop | STP | có | 01 mục 8; 07 Yêu cầu chung (email khẩn), mục 1.1; 03 mục 7 | chưa bắt đầu |
| backup | BAK | không | 04 mục 7; [ADR 0009](../../decisions/0009-local-first-deployment.md "Chạy trên máy local trước, giữ khả năng dời lên Oracle") *(Chạy trên máy local trước, giữ khả năng dời lên Oracle)* | chưa bắt đầu |

**Phạm vi từng tính năng**
- `app-skeleton`: dựng monorepo, NestJS, PostgreSQL, Redis, BullMQ và Docker Compose đa kiến trúc. `browser-worker` là tiến trình riêng, chỉ nối với Redis ([ADR 0011](../../decisions/0011-browser-worker-redis-only.md "Worker trình duyệt chỉ kết nối Redis") *(Worker trình duyệt chỉ kết nối Redis)*). Tính năng còn gồm bảng cài đặt chung, `Clock` và cách đo RAM/CPU của từng container.
- `auth`: đăng nhập cho 2 vai trò, giữ phiên lâu, giới hạn đăng nhập sai, đổi mật khẩu và tạo tài khoản bằng CLI. Tính năng còn gồm khung app và menu theo vai trò.
- `crawler-verification`: chạy bằng code POC. Tính năng hoàn thành 7 mục còn dở của checklist nghiệm thu thủ công. Tính năng cũng kiểm chứng `CHRONOLOGICAL`, `createdAt`, nội dung bị cắt và ảnh cỡ đầy đủ. Kết quả được đưa vào thiết kế `group-crawl-job`.
- `group-settings`: thêm và xoá group, các công tắc, giới hạn riêng, ghi chú luật và trạng thái truy cập.
- `crawl-settings`: giờ vàng, chu kỳ trong và ngoài giờ vàng, giờ nghỉ, số lượt mở group tối đa mỗi ngày và giới hạn scroll.
- `fb-account-session`: trạng thái phiên, kiểm tra phiên định kỳ, Xvfb và noVNC trong container, hướng dẫn đăng nhập lại.
- `group-crawl-job`: chuyển crawler POC, chạy job quét định kỳ không chồng chu kỳ, xáo thứ tự group, merge bài theo quy tắc POC, lưu lượt quét và xử lý group không truy cập được.
- `emergency-stop`: nút dừng khẩn cấp và nút chạy lại. App tự dừng khi phiên hết hạn hoặc gặp checkpoint, đồng thời lưu ảnh màn hình và HTML. Tính năng còn gồm email khẩn và khối "Trạng thái tự động hóa" trên trang chính.
- `backup`: hằng đêm sao lưu bằng `pg_dump` cùng ảnh ra thư mục cấu hình được, giữ 7 bản. Việc đẩy lên Object Storage là tuỳ chọn. Debug dump cũ hơn 14 ngày được dọn đi.

<a id="s-47d95d164b"></a>

## Vấn đề đang chặn

**Tóm tắt.** Có 3 vấn đề đang chặn: Docker chưa dùng được từ dòng lệnh, còn thiếu danh sách group cùng tài khoản phụ, và còn thiếu tài khoản Gmail để gửi email khẩn.

- Docker Desktop đã cài nhưng lệnh `docker` chưa có trong PATH, hoặc Docker Desktop chưa chạy.
  - Ảnh hưởng: app-skeleton và mọi tính năng cần `pnpm test:int`.
  - Người xử lý: Hải.
- Cần danh sách 6 group (link hoặc ID) và tài khoản phụ sẵn sàng để tự đăng nhập qua trình duyệt.
  - Ảnh hưởng: crawler-verification, fb-account-session, group-crawl-job.
  - Người xử lý: chủ tiệm.
- Cần tài khoản Gmail gửi thư, kèm mật khẩu ứng dụng, cho email khẩn.
  - Ảnh hưởng: emergency-stop.
  - Người xử lý: Hải.

<a id="s-b3001d5acc"></a>

## Nhật ký duyệt

Các lần duyệt của giai đoạn 0 theo thứ tự thời gian.

- 2026-10-29: Hải mở giai đoạn.
- 2026-10-29: Hải duyệt thiết kế chi tiết của app-skeleton.
- 2026-10-31: Hải duyệt thiết kế của app-skeleton.
- 2026-10-31: Hải duyệt thiết kế chi tiết của auth.
- 2026-10-31: Hải duyệt UI của auth.
- 2026-10-31: Hải duyệt việc đổi style cho cả giai đoạn: thêm quy ước vị trí thông báo, không đổi token ([ADR 0016](../../decisions/0016-form-message-placement.md "Vị trí và câu chữ thông báo trên màn hình") *(Vị trí và câu chữ thông báo trên màn hình)*).
- 2026-10-31: Hải duyệt thiết kế của auth.
