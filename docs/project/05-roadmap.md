# 05 – Lộ trình

App được code **từng giai đoạn**. Xong giai đoạn nào thì chủ tiệm dùng được giai đoạn đó ngay.

**Thứ tự đã thống nhất với chủ tiệm:** comment group → lịch + kênh thợ → inbox Page → mẫu mới + kho content.

Mỗi giai đoạn nên được lên kế hoạch và code riêng. Có thể tách mỗi giai đoạn thành một bản kế hoạch triển khai.

---

## Giai đoạn 0 – Nền móng

**Mục tiêu:** có khung app chạy được bằng Docker trên máy local, dời được lên máy chủ sau này mà không sửa code, và kiểm chứng những điều kiện kỹ thuật lớn.

> Cập nhật 2026-10-29 (ADR `0009-local-first-deployment`): chưa đăng ký được Oracle Free, nên giai đoạn 0 chạy trên máy local. Việc dựng máy chủ chuyển sang mục "Triển khai lên máy chủ" bên dưới.

- Dựng project: NestJS, PostgreSQL, Redis, BullMQ, Docker Compose. Image build được cho cả linux/amd64 (máy local) và linux/arm64 (Oracle A1). Mọi khác biệt giữa các máy nằm ở biến môi trường và volume.
- Chuyển các module crawler của POC vào app.
- **Hoàn thành checklist nghiệm thu còn dở của POC** (trong spec của POC), và kiểm chứng thêm:
  - sắp xếp `CHRONOLOGICAL` có chạy ở các group thật không;
  - `createdAt` có đáng tin không;
  - nội dung bài có bị cắt ngắn không;
  - có lấy được ảnh đính kèm cỡ đầy đủ không (cần cho bài loại 3).
- **Worker trình duyệt chạy được như một tiến trình tách riêng**, chỉ kết nối tới Redis và PostgreSQL. Như vậy, nếu IP Oracle bị Facebook chặn nhiều, có thể chuyển worker về một máy ở nhà mà không sửa code.
- Thiết lập Xvfb + noVNC trong container worker trình duyệt để đăng nhập tài khoản vận hành. Cách này dùng chung cho máy local và máy chủ.
- Web app tối thiểu:
  - đăng nhập hai vai trò;
  - trang Cài đặt cho danh sách group và các tham số quét;
  - trạng thái tài khoản vận hành;
  - nút dừng khẩn cấp.
- Email khẩn cho chủ tiệm khi app tự dừng (làm sớm từ giai đoạn 1, chốt 2026-10-29), để biết ngay khi chạy thử không có người theo dõi.
- Job quét định kỳ ghi bài vào PostgreSQL.
- Sao lưu hằng đêm ra thư mục cấu hình được. Đẩy lên Object Storage là tùy chọn, bật khi có máy chủ.

**Xong khi:**
- Chạy quét bằng Docker trên máy local, **tổng cộng ít nhất 24 giờ** (có thể chia nhiều lần), bằng tài khoản phụ mà không bị đăng xuất, hoặc nếu bị thì app tự dừng và báo đúng.
- Bài mới trong group xuất hiện trong cơ sở dữ liệu trong vòng 1 chu kỳ quét.
- Ghi lại mức RAM và CPU thực tế của từng container, để ước lượng cho máy chủ.

---

## Triển khai lên máy chủ (chưa xếp lịch)

**Mục tiêu:** chuyển app từ máy local lên máy chủ chạy 24/7, khi đã đăng ký được Oracle Free (ADR `0009-local-first-deployment`).

- Tạo máy ảo Oracle Free (Ampere A1), build image linux/arm64.
- Thiết lập HTTPS: tên miền cố định + Caddy (hoặc Cloudflare Tunnel có tên miền).
- Khôi phục dữ liệu từ bản sao lưu. Không copy profile trình duyệt; đăng nhập lại tài khoản vận hành trên máy chủ qua noVNC.
- Gán thư mục dữ liệu (`MIO_DATA_DIR`) cho uid:gid `1000:1000` (`chown -R 1000:1000`) trước lần chạy đầu và sau khi khôi phục, vì các container chạy bằng uid này (thiết kế `app-skeleton` R-SKL-20).
- Bật đẩy bản sao lưu lên Oracle Object Storage.

**Bắt buộc xong trước:** bật web push ở giai đoạn 1 (iPhone cần HTTPS và tên miền cố định) và webhook Messenger ở giai đoạn 2. Nếu tới lúc đó vẫn chưa có Oracle thì chọn phương án HTTPS tạm và ghi ADR riêng.

**Xong khi:**
- Chạy quét liên tục **ít nhất 3 ngày** trên máy chủ bằng tài khoản phụ mà không bị đăng xuất, hoặc nếu bị thì app tự dừng và báo đúng (kiểm chứng rủi ro IP datacenter).
- Ghi lại mức RAM và CPU thực tế trên máy chủ.

---

## Giai đoạn 1 – Tự động comment bài loại 1

**Mục tiêu:** bỏ được việc lướt group. Đây là việc tốn thời gian nhất của chủ tiệm.

- Phân loại bài bằng Gemini (cả 3 loại), lọc khu vực, ghi lý do.
  - Ở giai đoạn này **chỉ comment bài loại 1**. Bài loại 2 và 3 được ghi nhận và hiển thị để chủ tiệm tự xử lý.
- Kho content tối thiểu: tải lên poster, tạo bộ content, bật 1–3 bộ cho loại 1.
- Tạo comment: xoay vòng, AI viết lại nhẹ, kiểm tra từ cấm.
- Chế độ duyệt trước và tự gửi. Danh sách chờ duyệt trên web.
- Gửi comment bằng Playwright, kèm ảnh.
- Phanh an toàn đầy đủ, tự dừng khi bất thường.
- Nhật ký và thống kê cơ bản.
- Thông báo cho chủ tiệm qua web push. Thông báo khẩn gửi thêm qua email, vì chủ tiệm dùng iPhone (kênh email đã có từ giai đoạn 0, giai đoạn này mở rộng cho các loại thông báo khẩn khác). Messenger chưa có ở giai đoạn này.
- Bộ đánh giá phân loại từ bài thật.

**Xong khi:**
- Một tuần chạy trên tài khoản phụ ở chế độ duyệt trước, tỷ lệ comment nhầm bài không phù hợp dưới 2%.
- Sau đó chạy tự gửi ít nhất 3 ngày mà không bị checkpoint, hoặc nếu bị thì đã tự dừng đúng.
- Chủ tiệm quyết định có chuyển sang tài khoản chính hay không (xem `06-open-issues-and-assumptions.md`).

---

## Giai đoạn 2 – Lịch làm, kênh thợ, bài loại 2 và 3

**Mục tiêu:** một lịch thống nhất, và báo giá không còn phải chờ qua chủ tiệm.

- Lịch:
  - giờ làm theo tuần, ngày đặc biệt, khung bận, lịch hẹn và các trạng thái;
  - tìm khung trống, chống trùng;
  - màn hình lịch.
- Meta app + webhook Messenger.
  - Thợ và chủ tiệm là tester trong Meta app.
  - Ghép nối bằng mã.
- Kênh thợ:
  - hỏi giá (với mã yêu cầu, quick reply, reply_to);
  - hiểu câu trả lời và xác nhận lại;
  - khóa giờ bận qua tin nhắn;
  - tóm tắt đầu ngày, nút giữ cửa sổ 24 giờ.
- Thông báo cho chủ tiệm chuyển sang Messenger, giữ web push làm dự phòng.
- **Bật comment loại 2** (đọc lịch) và **loại 3** (báo giá qua thợ).
- **Ảnh mẫu mới thợ gửi qua Messenger:** ở giai đoạn này chỉ lưu lại và xác nhận "đã nhận". Luồng xử lý đầy đủ làm ở giai đoạn 4.
- Meta app ở chế độ phát triển, **không xin App Review** (tiệm chưa có giấy phép kinh doanh).

**Xong khi:**
- Thợ báo giá được bằng một tin nhắn, và comment loại 3 được tạo ngay sau đó: gửi luôn nếu đang ở chế độ tự gửi, hoặc vào danh sách chờ duyệt.
- Comment loại 2 luôn khớp với lịch. Có test chứng minh các luồng tự động không thể tạo hai lịch chồng nhau.
- Thợ duyệt, dời, hủy được lịch qua Messenger, và app xác nhận lại đúng.

---

## Giai đoạn 3 – Inbox Page

**Mục tiêu:** khách được trả lời ngay những câu hỏi đơn giản, và không khách nào bị bỏ quên.

- Bộ thông tin của tiệm (có trạng thái xác nhận).
- Hiểu ý tin nhắn khách, trả lời thông tin cố định, giữ chỗ bằng lịch chưa duyệt, đề xuất khung trống gần nhất.
- Báo giá cho khách qua kênh thợ.
- Chuyển cho người thật với tin nhờ chờ thân thiện. Nhận ra người thật đã trả lời để không chen ngang.
- Danh sách khách và trạng thái. Gợi ý trả lời cho người thật.
- Hỏi thợ "khách đã làm xong chưa" sau mỗi lịch.
- **Worker inbox bằng trình duyệt trên Meta Business Suite** (`04-technical.md`, mục 4.3):
  - tài khoản riêng chỉ có quyền nhắn tin trên Page;
  - kiểm tra tin mới theo chu kỳ, gửi tin và ảnh;
  - nhận ra người thật đã trả lời;
  - tự dừng khi bất thường.
- Lớp "kênh inbox" tách riêng, để sau này chuyển sang Messenger Platform khi tiệm có giấy phép.
- **Bắt đầu bằng chế độ "chỉ gợi ý"**: app đọc và soạn câu trả lời nhưng không tự gửi, trong vài ngày, để kiểm tra chất lượng. Sau đó mới bật tự gửi (quyết định của người viết).

**Xong khi:**
- Các câu hỏi đã có trong bộ thông tin được tự trả lời đúng.
- Câu hỏi ngoài bộ thông tin luôn được chuyển cho người thật.
- Không có trường hợp app trả lời chen vào lúc người thật đang nói chuyện với khách.
- Thời gian từ lúc khách nhắn đến lúc app trả lời: khoảng 2–3 phút trong giờ hoạt động.
- Worker inbox chạy ít nhất 1 tuần mà không bị checkpoint, hoặc nếu bị thì đã tự dừng và báo đúng.
- Mọi khách có trạng thái đúng. Khách "đã xong" khớp với lịch đã làm xong.

---

## Giai đoạn 4 – Mẫu mới, đăng bài, kho content đầy đủ

**Mục tiêu:** một mẫu mới chỉ còn một lần duyệt.

- Nhận mẫu mới từ Messenger hoặc tải lên.
- Chỉnh ảnh bằng Nano Banana 2.1, bộ prompt, dự phòng tải ảnh lên tay, hạn mức chi phí.
- Các mẫu poster HTML (chuyển từ canvas), render ra PNG.
- Viết gói content, hạn dùng, lịch dịp lễ.
- Màn hình duyệt một lần.
- Đăng Page qua Graph API. Đăng group theo đợt bằng Playwright.
- Kho content đầy đủ: tìm không dấu, lọc, lịch sử sử dụng, đăng lại.
- (Tùy chọn) Nhập dữ liệu cũ từ Excel và từ canvas.

**Xong khi:**
- Từ lúc thợ gửi ảnh đến lúc bài lên Page, chủ tiệm chỉ phải bấm duyệt (cộng với sửa nhỏ nếu muốn).
- Poster đúng nhận diện, chữ tiếng Việt hiển thị đúng.
- Content không có từ cấm, và có hạn dùng khi nhắc tới dịp.

---

## Sau các giai đoạn trên (chưa làm)

- Gợi ý giá tự động, khi chủ tiệm đã chốt bảng giá.
- Gợi ý giờ đăng và nội dung dựa trên số liệu hiệu quả.
- Theo dõi khách đến từ comment nào.
- Xử lý tin nhắn thoại.
