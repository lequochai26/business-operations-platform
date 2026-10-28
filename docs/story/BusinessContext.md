# Tiệm Nhà Mio – Tổng hợp context (cập nhật 27/10/2026)

> Tổng hợp từ ghi chú dự án "Mio" và các cuộc trò chuyện từ 27/09 đến 25/10/2026. Mục nào chưa có thông tin chính xác được ghi rõ là "chưa chốt" hoặc "chưa có".

---

## 0. Tóm tắt nhanh

- Tiệm nail nhỏ ở **Quận 11, TP.HCM**, làm nail tay/chân, **1 thợ**, giai đoạn đầu chủ yếu **nhận khách mẫu**.
- Giá mẫu hiện tại khoảng **89k–150k** tùy mẫu; các poster gần đây chủ yếu ở mức 89k / 99k / 110k / 120k.
- Liên hệ: **inbox Facebook Page** và SĐT **0911 897 965**.
- Kênh tìm khách chính: **comment vào bài tìm chỗ làm nail / tìm mẫu** trong các group Facebook, dẫn khách về Page.
- Page đã được dọn nội dung cũ (dessert, skincare) và đổi nhận diện sang **xanh sage #8FA284**.
- Toàn bộ poster nằm trong **một canvas Claude Design dùng chung**; mỗi mẫu nail mới = 1 poster mới + gói content (Page / group / comment).
- Đang dự định làm **web app nội bộ** để giải quyết vấn đề vận hành Page và tự động hóa marketing.

---

## 1. Thông tin tiệm

### Cơ bản
- **Tên:** Tiệm Nhà Mio. Tên hiển thị Page **chưa chốt**, phương án dẫn đầu: **"Tiệm Nhà Mio – Nail"** (các lựa chọn khác từng cân nhắc: "Tiệm Nail Nhà Mio", "Mio Nail", giữ nguyên "Tiệm Nhà Mio").
- **Khu vực:** Quận 11, TP.HCM. Chưa có địa chỉ cụ thể công khai trong context.
- **Dịch vụ:** nail tay và chân.
- **Nhân sự:** 1 thợ. Một số mẫu mất **2,5–3 tiếng/khách**, nên dễ bị dồn lịch.
- **Trên Facebook:** tên người vận hành hiển thị là Huỳnh Mio.

### Mô hình & định vị
- Giai đoạn hiện tại: **nhận khách mẫu nail** để luyện tay nghề, xây portfolio, lấy feedback và tạo uy tín ban đầu.
- Giá:
  - Theo file context ban đầu (27/09): phụ phí mẫu **85k–98k/bộ**.
  - Hiện tại: **89k–150k** tùy dịch vụ.
- **Định vị:** giá dễ tiếp cận nhưng chú trọng chất lượng và thẩm mỹ. **Không** định vị là "tiệm nail giá rẻ".
- **Khách mục tiêu:**
  - Khách ngân sách tốt nhưng ưu tiên giá trị.
  - Khách ngân sách trung bình, làm nail cho dịp đi chơi, lễ, Tết, du lịch.
  - Học sinh, sinh viên ngân sách thấp.

### Giọng thương hiệu
- Tiếng Việt, **thân thiện, gần gũi, nữ tính, tự nhiên**, không quá sang chảnh.
- Hay xưng "mình", gọi khách "bạn" / "nàng"; dùng emoji.
- CTA đơn giản: "ib mình", "nhắn Page", "inbox để giữ slot".
- Hashtag đã dùng: #TiemNhaMio, #NailQuan11, #Nail2010.

### Snapshot Facebook Page (27/09/2026)
- Khoảng 35 followers, 61 following, 2 đánh giá, trạng thái "Luôn mở cửa", có liên kết TikTok.
- Nội dung 2022–2023 về dessert (Panna Cotta) và skincare là lịch sử cũ của Page, không phải hoạt động hiện tại; sau đó đã được dọn.
- Bài lúc đó: nhận mẫu nail dịp Trung thu, có quà mang về.

---

## 2. Nhận diện thương hiệu

### Quyết định đã chốt
- Ban đầu brief đề xuất hướng pastel hồng nữ tính, sau đó **chốt màu chủ đạo xanh sage #8FA284** thay cho hồng.
- **Avatar:** chữ "Mio" viết tay (script) làm chủ đạo.
- **Banner Facebook:** 1640×624px, bố cục **khung oval ở giữa**, ảnh nail hai bên, có thanh liên hệ (tên Facebook + SĐT, đã bỏ Instagram), mỗi mục bật/tắt được. Đã chèn 4 ảnh nail thật.

### Design tokens (dùng trong mọi poster)
- Nền chính: sage **#8FA284**
- Nền thẻ/kem: **#FAF7F0**
- Xanh nhấn đậm: **#4E6045**
- Font tiêu đề: **Playfair Display**
- Font chữ viết tay: **Dancing Script**
- Font nội dung: **Be Vietnam Pro**
- Khổ poster chuẩn: **1080×1350px**

### Không được làm (từ design brief)
- Không dùng yếu tố dessert/bánh.
- Không dùng từ tuyệt đối như "tốt nhất", "rẻ nhất", "đẹp nhất".
- Không tự thêm thông tin chưa có: địa chỉ cụ thể, giờ mở cửa, khuyến mãi, số lượng khách.
- Không dùng ảnh nail từ nguồn khác như thể sản phẩm của tiệm.

---

## 3. Hệ thống poster (canvas Claude Design)

### Vị trí
- Canvas artifact ID: `03808feb-165b-432a-a5a2-a5ad1111f8da`
- Link: https://claude.ai/artifact/1S5pKqTHByy47ppzv4qmPX

### Cách làm việc với canvas
- Mỗi poster là một file `.dc.html` trong thư mục `project/`.
- `project/canvas.json` quản lý bố cục: `boards` (theo tên file, có x/y/w/h/title), `order` (thứ tự), `notes` (tiêu đề nhóm).
- Poster mới được tạo bằng cách **copy poster gần nhất cùng kiểu** rồi thay: tiêu đề, tag mẫu, giá, ảnh (`/_blob/<id>`), alt text, sticker.
- Ảnh: xoay đúng chiều (EXIF), crop để thấy đủ móng, tránh vùng chữ/sticker đè lên tay, xem preview trước khi chốt.
- Ảnh được upload thành asset của canvas trước, sau đó mới tham chiếu trong poster.
- Poster có thuộc tính chỉnh nhanh (màu nhấn, bật/tắt SĐT, sticker, lịch 20/10…) để chủ tiệm tự sửa không cần đụng code.
- Khi chủ tiệm sửa trực tiếp trên canvas, cần đọc lại file poster trước khi viết content để content khớp với poster.

### Danh sách poster theo thời gian
- **Poster 1** – Lưới portfolio nail (dùng đi comment).
- **Poster 2** – Lịch slot trong tuần, các ô chỉnh được.
- **Sao xanh + da beo + đá bạc** (29/09) – giá ưu đãi trọn bộ.
- **Mắt mèo bạc + nơ đỏ + charm đỏ/bạc** (30/09) – 120k. Ảnh gốc có watermark AI, đã crop.
- **Chấm bi xanh – đen, nơ nổi 3D, form móng bầu** (01/10) – 89k. Content group theo trend trời mưa: "Đưa tay lên là phải đẹp".
- **Poster 6 – French hồng nude, đầu trắng, nhũ vàng, nơ bạc, form nhọn** (03/10) – 99k trọn bộ. Có sticker "khách mê đến mức đăng story".
- **Poster 7 – Hoa đính đá & viền ngọc trai, nền trắng sữa, French hồng nude** (05/10) – 99k, gắn 20/10.
- **French nền thạch hồng & mắt mèo** (06/10, file `PosterFrenchAnhHong`) – chủ tiệm tự sửa tên mẫu trên canvas; có thêm bản content vè vần, chơi chữ "mắt mèo", dạng công thức.
- **Poster 10 – Sơn thạch gạo & ẩn xà cừ** (10/10) – 89k. Layout mới "vé hẹn 20/10": lịch "20 – Tháng 10", ô giá kiểu vé, nhãn "Cuối tuần sắp kín slot".
- **Poster tổng 20/10 – 4 đề xuất** (10/10): A "Menu móng xinh", B "Bó hoa trên tay", C "Vé hẹn xinh", D "Đếm ngược 20/10". **Chưa chọn hướng.**
- **Poster 11 – Thạch gạo + French mắt mèo nâu + vẽ da beo** (14/10) – 110k. Hook: "hiền như mèo, móng dữ như beo".
- **Poster 12 – Thạch hồng, French tráng gương ngọc trai, đính bi** (19/10) – 99k, nhãn "Mẫu mới đón 20/10". Content viết lại cho đăng đúng ngày 20/10.
- **Poster 13 – Mint green tráng gương** (19/10) – 89k, lịch "20 – Thứ Ba".
- **Poster 14 – Đỏ + mắt mèo champagne + chấm bi** (21/10) – 99k. Sticker lịch 20/10 thay bằng "Đỏ – màu mùa lễ" để dùng tới cuối năm.
- **Poster 15 – Nâu mắt mèo + flash giấy gạo nhũ + đính đá** (25/10) – 99k, badge "Tone Thu Đông – Nâu". Content có câu Halloween, chỉ dùng tới 31/10.
- **Poster chung "Bìa tạp chí MIO"** (25/10) – style mới: nền kem, màu nhấn hồng đất, chữ MIO lớn, "Móng xinh từ 89k", dải 4 ảnh "Mẫu khác ở tiệm", nút "IB PAGE CHỌN MẪU". Đổi được ảnh chính, màu nhấn (hồng đất / sage đậm / nâu ca cao), bật/tắt SĐT.

### Gói content đi kèm mỗi poster
- 1 bài đăng Page.
- 2–3 biến thể bài đăng group (bản dài / bản ngắn / bản kể chuyện), xoay vòng giữa các group để tránh trùng.
- 3–5 mẫu comment xoay vòng để đi comment các bài tìm khách.
- Thường kèm ngữ cảnh thời sự: thời tiết (mưa), 20/10, Halloween, mùa thu đông, mùa lễ cuối năm.

---

## 4. Chiến lược tìm khách & bài học

### Cách tìm khách hiện tại
- Comment vào bài trong group của người đang tìm chỗ làm nail / tìm mẫu, kèm poster/ảnh thật, dẫn về inbox Page.
- Page đóng vai trò **xây niềm tin** khi khách bấm vào xem; comment trong group là **kênh khám phá chính**.

### Diễn biến
- Trước khi làm lại Page: lượng khách giảm từ 1–2 khách/ngày xuống 1–2 khách/tuần. Nguyên nhân chính: Page không có nội dung nail thuyết phục khi khách bấm vào từ comment, và comment không có hình.
- Sau một tuần dùng content mới (cuối tháng 9): chưa có khách phản hồi, dẫn tới việc rà soát số lượng comment, khung giờ, khu vực bài nhắm tới và độ đồng bộ của Page.

### Bài học đã rút ra
- Page mới có reach tự nhiên thấp, nên đừng kỳ vọng Page tự kéo khách.
- Comment cụ thể (gọi đúng tên mẫu, ảnh thật, giá rõ) trông thật, không giống spam. Dòng đầu nên nói rõ "Tiệm Nhà Mio nhận làm…" vì Facebook cắt bớt comment dài.
- Bài cũ vài ngày nên dùng comment hướng tới người lướt xem, không chỉ người đăng bài.
- **Thứ 5 – Chủ nhật** có tương tác đặt lịch tốt hơn đầu tuần.
- Khung giờ tốt: **20:00–22:30**, **11:30–13:00**, **17:30–19:00**. Comment trong **30 phút** đầu sau khi bài được đăng quan trọng hơn giờ chính xác.
- Mục tiêu tham khảo: 10–15 comment/ngày, kiểm tra 2–3 lần/ngày.
- Theo dõi ít nhất **1 tuần** (số comment so với số tin nhắn) trước khi kết luận content không hiệu quả.
- Đổi cách viết comment giữa các bài, không lặp y hệt.
- Kiểm tra luật từng group trước khi đăng quảng cáo.

### Nguyên tắc minh bạch
- Nói rõ các khoản phát sinh, ví dụ **phí phá gel / tháo móng cũ**.
- Với mẫu móng dài/nhọn: xác nhận giá đã gồm **nối móng** chưa trước khi ghi "trọn bộ như hình".
- Chỉ nói "giá tương tự" khi mẫu thực sự tương đương độ khó.
- Khi chưa chắc giá cho mẫu khách gửi, ghi "báo giá qua tin nhắn" thay vì cam kết mức giá thấp nhất.
- **Không viết review giả** đóng vai khách. Thay vào đó, nhắn khách thật xin review bằng tin nhắn mẫu.
- Ảnh chỉnh bằng AI: crop watermark, so kỹ với ảnh gốc để không sai mẫu, nên đăng kèm ảnh thật; không ghi "ảnh thật tại tiệm" nếu ảnh đã chỉnh.

---

## 5. Chụp & chỉnh ảnh nail

- Ảnh gốc thường có bối cảnh đời thường (đèn UV, bàn gỗ, giá đỡ điện thoại).
- Đã có bộ prompt chỉnh ảnh (tiếng Anh, cho Gemini / ChatGPT…) theo các style: studio tối giản nền sage, lụa + hoa + ngọc trai, lifestyle ánh nắng + ly latte, macro editorial, tối kiểu quảng cáo nước hoa. Prompt luôn có quy tắc **giữ nguyên mẫu, form, màu móng** và ràng buộc giải phẫu bàn tay (không thừa ngón).
- Gợi ý chụp: móng chiếm khoảng 1/3 khung hình, đặt tay trên vải trơn hoặc giấy màu, dùng ánh sáng cửa sổ thay cho đèn flash, có thể quay clip ngắn để thấy hiệu ứng mắt mèo/tráng gương.

---

## 6. Nhắn tin với khách (cách chủ tiệm hay xử lý)

- **Hẹn lại sang hôm sau**, có bản xin lỗi khi đang bận khách khác, kèm **quà nhỏ** làm bù.
- **Giải thích thời gian chờ** do chỉ có 1 thợ: đề xuất hẹn lệch giờ (khách sau tới sau khoảng 2,5 tiếng), hoặc bản cho trường hợp hai khách muốn đi cùng và chờ tại tiệm.
- **Khách gửi mẫu quá phức tạp / quá giá:** gợi ý mẫu đơn giản hơn cùng tông màu, hoặc giữ lại vài chi tiết chính ở dạng đơn giản, hoặc đưa 2 lựa chọn kèm giá.
- Thói quen chung: đưa **giải pháp thay thế** (mẫu khác, hẹn lệch giờ, quà nhỏ) thay vì từ chối thẳng.
- Thích có **nhiều biến thể tin nhắn**: để khách tự chọn giờ hoặc đưa sẵn khung sáng/chiều/tối; bản chi tiết hoặc bản ngắn.

---

## 7. Việc đang mở / cần xác nhận

- Chốt **tên hiển thị Page** ("Tiệm Nhà Mio – Nail" đang dẫn đầu).
- Chọn 1 trong 4 hướng **Poster tổng 20/10** (A–D), hoặc chuyển sang dùng poster "Bìa tạp chí MIO".
- **Poster feedback/testimonial**: đang chờ ảnh chụp feedback thật của khách.
- **Web app nội bộ**: đang soạn tài liệu định nghĩa yêu cầu để giải quyết vấn đề vận hành Page và tự động hóa marketing tối đa.
- Các điểm từng được đánh dấu cần chủ tiệm kiểm tra:
  - Giá 99k/110k cho mẫu móng dài đã gồm nối móng chưa.
  - SĐT 0911 897 965 có dùng được Zalo không.
  - Có báo trước phí phá gel không.
  - Câu "nail xinh cả tháng" và "Mỗi ngày Mio chỉ nhận vài khách" (poster tổng 20/10) có đúng thực tế không.
  - Câu "tới là làm, không phải chờ" và dòng "Ấn bản thu đông" trên poster Bìa tạp chí.
  - Nhãn "kịp xinh đón 20/10" / "Mẫu mới đón 20/10" trên Poster 12 và câu Halloween trên Poster 15 đã hết hạn.

### Thông tin còn thiếu (không tự suy đoán)
- Địa chỉ đầy đủ, giờ nhận khách.
- Bảng giá chính thức ngoài giá mẫu; danh sách dịch vụ và chất liệu.
- Chính sách cọc / hủy / bảo hành.
- Số khách và số feedback cụ thể.
- Link TikTok chính xác.

---

## 8. Cách làm việc ưa thích (khi nhờ Claude)

- Dựa trên template poster/canvas có sẵn, giữ nhận diện đồng bộ, không làm lại từ đầu.
- Content luôn bằng tiếng Việt, giọng ấm áp, thân thiện.
- Muốn câu trả lời gọn; khi tóm tắt dài thì rút ngắn.
- Không thích bảng; thích trình bày bằng heading và gạch đầu dòng.
- Với tài liệu dạng định nghĩa yêu cầu / spec: cần **bản đầy đủ + bản tóm tắt ngắn** để review nhanh.
- Có giữ file `tiem-nha-mio-context.md` và file design brief markdown để duy trì ngữ cảnh.