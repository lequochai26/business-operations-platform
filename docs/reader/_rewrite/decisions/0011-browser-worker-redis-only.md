<!-- src-section: 0b0fa0b228 52e396226267 -->
# 0011 – Worker trình duyệt chỉ kết nối Redis

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan:
  - phase-0 app-skeleton, fb-account-session, group-crawl-job, emergency-stop;
  - docs/project/05-roadmap.md giai đoạn 0;
  - 04-technical.md mục 2, 3, 4.2;
  - ADR 0002, 0009.

**Tóm tắt.** Worker trình duyệt chỉ kết nối Redis, nhận dữ liệu qua job và trả kết quả qua một hàng đợi kết quả. Nhờ vậy nghiệp vụ và DB chỉ nằm ở api, worker đơn giản, và việc dời worker sang máy khác ít rủi ro bảo mật hơn.

<!-- src-section: 0bc81167ac b5a8cff8f7d8 -->
## Bối cảnh

- Roadmap mô tả browser-worker là tiến trình tách riêng, "chỉ kết nối tới Redis và PostgreSQL". Mục đích là có thể dời worker về máy ở nhà nếu IP máy chủ bị Facebook chặn.
- Theo `CLAUDE.md`, schema Drizzle và migration nằm trong `apps/api`.
- POC có quy tắc merge bài: không ghi đè `firstSeenAt` và không ghi đè bằng `null`. Đây là nghiệp vụ, nên cần nằm ở một chỗ.

<!-- src-section: 1be8f16534 d5428cea36cd -->
## Các phương án

<!-- src-section: 04ccf5ad6d 29e695dffe15 -->
### A. Worker chỉ kết nối Redis, dữ liệu vào và ra đi qua job

**Ưu**

- Worker là adapter thuần: mở trình duyệt, thao tác, rồi trả dữ liệu thô.
- Nghiệp vụ và việc ghi DB chỉ nằm ở api. Schema DB chỉ ở một chỗ.
- Dời worker về máy nhà chỉ cần mở đường tới Redis, không phải mở PostgreSQL ra ngoài.

**Nhược**

- Kết quả job đi qua Redis. Dữ liệu này nhỏ, khoảng vài chục bài mỗi group.
- Worker không tự đọc cài đặt mà nhận cài đặt trong dữ liệu job.
- File như ảnh màn hình, HTML lỗi, ảnh tải về được ghi trên máy chạy worker.

<!-- src-section: 03d7c91c04 a34384fac5f4 -->
### B. Worker kết nối cả Redis và PostgreSQL, tự đọc cài đặt và ghi bài

**Ưu**

- Đúng nguyên văn roadmap.
- Không phải đóng gói kết quả vào job.

**Nhược**

- Worker phải dùng schema của `apps/api`. Khi đó hoặc có phụ thuộc chéo giữa hai app, hoặc phải tách package schema, trái với `CLAUDE.md`.
- Nghiệp vụ merge có thể bị viết ở hai nơi.
- Dời worker ra ngoài thì phải mở PostgreSQL qua mạng.

<!-- src-section: 254160d409 93f6f9e926bd -->
## Quyết định

Chọn phương án A.

**Vì sao.** Phương án A giữ nghiệp vụ và DB ở một nơi, và worker đơn giản. Việc dời worker sang máy khác cũng ít rủi ro bảo mật hơn. Phương án A vẫn thoả roadmap ("chỉ kết nối tới Redis và PostgreSQL"), vì chỉ kết nối Redis là tập con của yêu cầu đó.

**Cách trả kết quả** (chốt cùng ngày)

- Mỗi hàng đợi trình duyệt có một hàng đợi kết quả riêng. Worker làm xong việc thì thêm một job vào hàng đợi kết quả. Job này báo thành công kèm dữ liệu, hoặc báo thất bại kèm lỗi đã phân loại. api xử lý job kết quả và ghi DB.
- Không dùng giá trị trả về của job kết hợp với sự kiện `completed`. Lý do là nếu api tắt đúng lúc đó thì sẽ bỏ lỡ sự kiện và mất kết quả. Ngược lại, job kết quả nằm trong Redis tới khi api xử lý.
- Nếu worker chết giữa chừng và không kịp gửi kết quả, api nghe sự kiện `failed` của hàng đợi gốc và xử lý như một kết quả lỗi.
- Chi tiết nằm ở docs/phases/phase-0/design/app-skeleton.md R-SKL-28, R-SKL-29.

**Chi tiết kỹ thuật**

- Hàng đợi `fb-browser` có hàng đợi kết quả `fb-browser-results`.
- Hàng đợi `fb-inbox` có hàng đợi kết quả `fb-inbox-results`.
- Trường `outcome` của job kết quả là `ok` kèm dữ liệu, hoặc `failed` kèm lỗi đã phân loại.

<!-- src-section: 58c5fdb1ed 48914ae56ccf -->
## Hệ quả

**Được**

- `apps/browser-worker` không có Drizzle và không có `DATABASE_URL`.
- api xử lý kết quả job: lưu bài, đếm lượt quét, tự dừng khi lỗi phiên.

**Mất và rủi ro**

- Lỗi được trả về api qua job thất bại có phân loại (`SessionExpiredError`, `CheckpointError`, `GroupInaccessibleError`). api phải lắng nghe sự kiện job để phản ứng.
- Nếu sau này worker chạy trên máy khác api thì file debug dump và ảnh không nằm cùng máy với web. Khi đó cần thiết kế cách chuyển file. Phiên bản này chưa làm việc đó.
