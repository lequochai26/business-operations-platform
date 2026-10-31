# 0011 – Worker trình duyệt chỉ kết nối Redis

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: phase-0 app-skeleton, fb-account-session, group-crawl-job, emergency-stop; docs/project/05-roadmap.md giai đoạn 0; 04-technical.md mục 2, 3, 4.2; ADR 0002, 0009

## Bối cảnh

- Roadmap: browser-worker là tiến trình tách riêng, "chỉ kết nối tới Redis và PostgreSQL", để có thể dời về máy ở nhà nếu IP máy chủ bị Facebook chặn.
- `CLAUDE.md`: schema Drizzle và migration nằm trong `apps/api`.
- Quy tắc merge bài của POC (không ghi đè `firstSeenAt`, không ghi đè bằng `null`) là nghiệp vụ, cần nằm một chỗ.

## Các phương án

### A. Worker chỉ kết nối Redis; dữ liệu vào/ra qua dữ liệu và kết quả job
- Ưu: worker là adapter thuần (mở trình duyệt, thao tác, trả dữ liệu thô); nghiệp vụ và ghi DB chỉ ở api; schema DB chỉ một chỗ; dời worker về máy nhà chỉ cần mở đường tới Redis, không phải mở PostgreSQL ra ngoài.
- Nhược: kết quả job đi qua Redis (vài chục bài mỗi group, nhỏ); worker không tự đọc cài đặt mà nhận trong dữ liệu job; file (ảnh màn hình, HTML lỗi, ảnh tải về) ghi trên máy chạy worker.

### B. Worker kết nối cả Redis và PostgreSQL, tự đọc cài đặt và ghi bài
- Ưu: đúng nguyên văn roadmap; không phải đóng gói kết quả vào job.
- Nhược: worker phải dùng schema của `apps/api` (phụ thuộc chéo giữa hai app hoặc phải tách package schema, trái `CLAUDE.md`); nghiệp vụ merge có thể bị viết ở hai nơi; dời worker ra ngoài phải mở PostgreSQL qua mạng.

## Quyết định

Chọn A vì giữ nghiệp vụ và DB ở một nơi, worker đơn giản, và việc dời worker ra máy khác ít rủi ro bảo mật hơn. A vẫn thỏa roadmap ("chỉ kết nối tới Redis và PostgreSQL" — A là tập con).

Cách trả kết quả (chốt cùng ngày):
- Mỗi hàng đợi trình duyệt có một hàng đợi kết quả: `fb-browser` → `fb-browser-results`, `fb-inbox` → `fb-inbox-results`. Worker xong việc thì thêm một job vào hàng đợi kết quả (`outcome` `ok` kèm dữ liệu, hoặc `failed` kèm lỗi đã phân loại); api xử lý job kết quả và ghi DB.
- Không dùng giá trị trả về của job + sự kiện `completed`, vì api tắt đúng lúc đó sẽ bỏ lỡ sự kiện và mất kết quả. Job kết quả nằm trong Redis tới khi api xử lý.
- Worker chết giữa chừng (không kịp gửi kết quả): api nghe sự kiện `failed` của hàng đợi gốc và xử lý như kết quả lỗi.
- Chi tiết: docs/phases/phase-0/design/app-skeleton.md R-SKL-28, R-SKL-29.

## Hệ quả

- Được: `apps/browser-worker` không có Drizzle, không có `DATABASE_URL`; api xử lý kết quả job (lưu bài, đếm lượt quét, tự dừng khi lỗi phiên).
- Mất / rủi ro:
  - Lỗi được trả về api qua job thất bại có phân loại (`SessionExpiredError`, `CheckpointError`, `GroupInaccessibleError`); api phải lắng nghe sự kiện job để phản ứng.
  - Nếu sau này worker chạy trên máy khác api, file debug dump và ảnh không nằm cùng máy với web; khi đó cần thiết kế cách chuyển file (chưa làm ở phiên bản này).
