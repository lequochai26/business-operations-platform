# Chức năng 01 – Tự động đi comment trong group

## Mục đích
Thay chủ tiệm làm trọn vòng: lướt các group nail, tìm bài đang tuyển mẫu hoặc tìm thợ, chọn hoặc tạo nội dung phù hợp, rồi comment kèm poster. Kết quả mong muốn là bài phù hợp được comment sớm (trong khoảng 30 phút đầu) mà vẫn trông như người thật đang comment.

## Liên quan
- Đọc lịch trống: `03-schedule.md`
- Hỏi giá thợ: `02-technician-channel.md`
- Lấy bộ content và poster: `06-content-library.md`
- Cài đặt group, giới hạn và chế độ: `07-screens-and-settings.md`
- Kỹ thuật trình duyệt tự động và rủi ro: `../04-technical.md`

---

## 1. Luồng tổng quát

1. **Quét:** theo lịch, app mở lần lượt từng group đang bật và thu các bài mới (kế thừa crawler của POC).
2. **Lọc thô:** bỏ các bài đã từng xử lý, bài quá cũ, bài của chính tài khoản vận hành hoặc của Page.
3. **Phân loại bằng AI:** với mỗi bài còn lại, AI xác định bài có phải bài tìm mẫu/tìm thợ nail hay không, thuộc loại 1, 2 hay 3, và trích ra các thông tin cần thiết.
4. **Lọc theo khu vực:** bỏ các bài hỏi ở khu vực tiệm không phục vụ.
5. **Chuẩn bị comment** theo từng loại (mục 3 đến mục 5).
6. **Gửi hoặc chờ duyệt**, tùy chế độ (mục 7).
7. **Gửi comment** qua trình duyệt tự động, tuân theo phanh an toàn (mục 8).
8. **Ghi nhật ký:** lưu kết quả để không comment trùng và để làm thống kê (mục 9).

---

## 2. Quét group

### Group cần quét
- Chủ tiệm tự khai báo danh sách group trong app. Có thể dán link hoặc Group ID, giống `FB_GROUPS` của POC.
- Mỗi group có các thiết lập riêng:
  - **bật/tắt quét**;
  - **cho phép comment** (mặc định bật);
  - **cho phép đăng bài** (dùng cho chức năng 05);
  - **giới hạn comment/ngày riêng**, nếu có;
  - **ghi chú luật group**. Theo bài học của tiệm: phải kiểm tra luật từng group trước khi quảng cáo.

### Lịch quét
- Quét theo chu kỳ. Chu kỳ dày hơn trong các khung giờ vàng:
  - **11:30–13:00**, **17:30–19:00**, **20:00–22:30**: mặc định mỗi 10 phút.
  - Các khung khác trong giờ hoạt động: mặc định mỗi 30 phút.
  - **Giờ nghỉ** (mặc định 23:30–07:00): không quét.
  - Tất cả các mốc trên đều chỉnh được (quyết định của người viết).
- Mỗi lượt quét lần lượt từng group, không chạy song song. Giữ cách giãn cách ngẫu nhiên và các điều kiện dừng scroll của POC (`MAX_SCROLLS`, dừng khi gặp K bài đã biết, dừng khi feed hết).
- Thứ tự group trong mỗi lượt được xáo ngẫu nhiên (quyết định của người viết).

### Lọc thô (không cần AI)
- **Bỏ bài đã xử lý:** bài đã có trong cơ sở dữ liệu với trạng thái cuối, nhận diện theo `postId` như POC.
- **Bỏ bài quá cũ:**
  - Mặc định chỉ xét bài đăng trong vòng **24 giờ**, chỉnh được (quyết định của người viết).
  - Bài trong vòng 24 giờ nhưng đã quá **3 giờ** vẫn được comment, nhưng dùng giọng hướng tới người lướt xem thay vì chỉ nói với người đăng bài. Đây là bài học của tiệm.
- **Bỏ bài của chính mình:** bài do tài khoản vận hành hoặc Page đăng.
- **Ưu tiên bài mới:** trong một lượt, bài mới hơn được xử lý trước.
- **Lọc từ khóa trước khi gọi AI** (quyết định của người viết):
  - Chỉ gửi cho AI những bài có ít nhất một từ khóa liên quan, ví dụ "nail", "móng", "mẫu", "tuyển mẫu", "mphi", "ppmini", "sơn gel"… So khớp không dấu.
  - Mục đích là tiết kiệm hạn mức Gemini miễn phí.
  - Danh sách từ khóa chỉnh được trong cài đặt.

### Giới hạn lượt quét
- Quét cũng là thao tác trên tài khoản vận hành, nên cũng có phanh:
  - **tối đa số lượt mở group mỗi ngày**, chỉnh được;
  - nếu một chu kỳ chưa quét xong thì chu kỳ sau **không chồng lên**, mà bắt đầu khi chu kỳ trước xong.
- Comment được ưu tiên hơn quét trong hàng đợi trình duyệt, để không lỡ mốc 30 phút.
- Chu kỳ 10 phút chỉ là mục tiêu. Với nhiều group, chu kỳ thực tế sẽ dài hơn, và app hiển thị chu kỳ thực tế trên trang chính.

---

## 3. Phân loại bài bằng AI

### Đầu vào
- Nội dung chữ của bài, ảnh đính kèm nếu có, thời điểm đăng bài, tên group.

### Đầu ra (dạng dữ liệu có cấu trúc)
- **Có phải bài tìm mẫu / tìm thợ nail không:** có hoặc không, kèm độ tin cậy.
- **Loại bài:**
  - **Loại 1, chung chung:** ví dụ "Có ac nào tuyển mẫu nail không ạ", "Có ai tuyển mẫu nail mphi hay ppmini ở khu vực…".
  - **Loại 2, có hỏi thời gian:** ví dụ "Mai / T2 / T3 / tối nay… có ac nào tuyển mẫu nail không".
  - **Loại 3, xin báo giá một mẫu cụ thể, có ảnh:** ví dụ "Mai có ac nào tuyển mẫu nail này không ạ? Báo giá giúp em".
  - Bài vừa hỏi thời gian vừa có ảnh mẫu xin báo giá được xếp **loại 3**. Phần thời gian vẫn được trích ra và kiểm tra lịch như loại 2 (quyết định của người viết).
- **Thời gian khách hỏi** (loại 2 và 3):
  - Ngày cụ thể, ví dụ "mai", "thứ 3", "20/10".
  - Buổi hoặc giờ nếu có, ví dụ "sáng", "tối", "sau 6h".
  - Ngày tương đối phải được quy đổi **theo thời điểm bài được đăng**, không theo thời điểm app quét. Ví dụ: bài đăng tối thứ Hai ghi "mai" thì "mai" là thứ Ba.
- **Khu vực khách nhắc tới,** nếu có.
- **Loại dịch vụ khách muốn,** nếu có: tay, chân, mẫu miễn phí (mphi), phụ phí mini (ppmini)…
- **Lý do phân loại,** một câu ngắn để chủ tiệm xem lại khi cần.

### Quy tắc
- Không chắc là bài tìm mẫu thì **không comment**. Độ tin cậy dưới ngưỡng (chỉnh được) được tính là "không phù hợp".
- Các bài sau đều tính là **không phù hợp**:
  - bài bán hàng hoặc quảng cáo của tiệm khác;
  - bài hỏi học nghề;
  - bài khoe móng;
  - bài tìm thợ cho dịch vụ khác (mi, tóc…);
  - bài tuyển nhân viên.
- Kết quả phân loại được lưu kèm bài, để chủ tiệm xem lại và đánh dấu "phân loại sai". Các đánh dấu này dùng để chỉnh prompt về sau.

### Lọc khu vực
- Chủ tiệm khai báo **danh sách khu vực nhận khách**, ví dụ Quận 11 và các quận lân cận.
- Xử lý theo khu vực trong bài:
  - **Bài không nhắc khu vực:** vẫn comment.
  - **Bài nhắc khu vực nằm trong danh sách:** comment, và được ưu tiên trước.
  - **Bài chỉ nhắc khu vực nằm ngoài danh sách:** bỏ qua.

---

## 4. Loại 1 – Bài chung chung

- Dùng **các bộ content cố định** do chủ tiệm cấu hình. Mỗi bộ gồm nội dung comment và một ảnh poster. Có thể bật từ 1 đến 3 bộ cùng lúc. Xem `06-content-library.md`.
- **Xoay vòng:** chọn bộ ít được dùng gần đây nhất trong group đó.
  - Khi có từ 2 bộ trở lên, không dùng cùng một bộ cho hai bài liên tiếp trong cùng group.
  - Khi chỉ bật 1 bộ, vẫn dùng bộ đó. Nhờ bước viết lại nhẹ bên dưới, chữ không lặp y hệt.
- **Viết lại nhẹ trước khi gửi** (quyết định của người viết): mỗi lần gửi, AI đổi cách mở đầu hoặc câu kết, nhưng giữ nguyên thông tin (tên mẫu, giá, CTA). Mục đích là không có hai comment giống hệt nhau, đúng bài học "đổi cách viết comment giữa các bài". Chủ tiệm tắt được tính năng này cho từng bộ content.
- Dòng đầu luôn bắt đầu bằng "Tiệm Nhà Mio nhận làm…" (hoặc câu mở đầu do chủ tiệm cấu hình), vì Facebook cắt bớt comment dài.

---

## 5. Loại 2 – Bài có hỏi thời gian

1. Lấy ngày (và buổi/giờ nếu có) mà AI đã trích ra.
2. Hỏi lịch thợ (`03-schedule.md`) xem còn khung trống phù hợp không:
   - **Khách hỏi ngày mà không nói giờ:** chỉ cần trong ngày còn ít nhất một khung trống là đủ.
   - **Khách hỏi buổi hoặc giờ:** phải còn khung trống bắt đầu trong buổi hoặc giờ đó.
   - Thời lượng dùng để tính một lượt làm là **thời lượng mặc định** trong cài đặt (mặc định 2,5 giờ, chỉnh được).
3. **Còn trống:** comment xác nhận đúng ngày (và giờ) khách hỏi. Ví dụ: "Tiệm Nhà Mio nhận làm thứ 3 nè bạn ơi, chiều thứ 3 mình còn slot 14h – 17h nha 💅 ib Page để giữ slot nha!". Kèm poster lấy từ các bộ content loại 1 (hoặc bộ content riêng cho loại 2 nếu chủ tiệm cấu hình).
4. **Không còn trống:** vẫn comment, nhưng đề xuất **các khung trống gần nhất** với thời gian khách hỏi. Mặc định tối đa 2–3 khung, ưu tiên cùng ngày rồi đến ngày gần nhất.
   - Ví dụ: "Tiệm Nhà Mio nhận làm nè, thứ 3 mình kín lịch mất rồi 🥺 mình còn trống tối thứ 4 (18h) hoặc sáng thứ 5 (9h) nha…".
5. **Không có khung trống nào trong khoảng N ngày tới** (mặc định 7): không comment, ghi lý do vào nhật ký.
6. App **không giữ chỗ** khi comment. Lịch chỉ được tạo khi khách nhắn Page (xem `04-page-inbox.md`).
   - Vì vậy, ngay trước khi gửi, app **kiểm tra lại lịch một lần nữa**. Nếu lịch đã thay đổi thì viết lại comment.
7. Mọi ngày và giờ trong comment phải lấy từ lịch thật. AI chỉ được diễn đạt lại, không được tự sinh ra giờ.

---

## 6. Loại 3 – Bài xin báo giá một mẫu cụ thể

1. **AI viết mô tả mẫu đúng 1 dòng** từ ảnh trong bài. Ví dụ: "Thạch hồng, French tráng gương, đính bi bạc, form bầu". Không viết thành đoạn văn.
2. **Gửi cho thợ qua kênh thợ:** ảnh mẫu, mô tả 1 dòng, link bài, thời gian khách hỏi (nếu có) và tình trạng lịch ngày đó. Xem `02-technician-channel.md`.
3. Bài chuyển sang trạng thái **"chờ báo giá"**.
4. **Thợ trả lời:**
   - **Chỉ có giá** (ví dụ "120k"): giữ mô tả của app.
   - **Mô tả mới kèm giá** (ví dụ "thạch hồng, mắt mèo, không đính đá, 99k"): dùng mô tả của thợ.
   - **Từ chối** (ví dụ "không làm được", "bỏ"): bài được đánh dấu "bỏ qua" và không comment.
5. **Tạo comment riêng cho bài đó:** dòng mở đầu "Tiệm Nhà Mio nhận làm…", mô tả mẫu, giá thợ báo, CTA "ib Page" và poster quảng cáo tiệm.
   - Chữ do AI viết riêng cho bài.
   - Poster lấy xoay vòng từ **danh sách poster dùng khi báo giá** (1–3 poster chung, ví dụ "Bìa tạp chí MIO" hoặc lưới portfolio, xem `06-content-library.md`, mục 2).
   - Nếu bài có hỏi thời gian thì thêm thông tin lịch như loại 2.
   - **Quy tắc minh bạch:**
     - Không ghi "trọn bộ như hình" trừ khi thợ đã xác nhận giá trọn bộ.
     - Nếu mẫu có móng dài hoặc nhọn mà thợ không nói rõ đã gồm nối móng chưa, comment ghi "giá chưa gồm nối móng / ib mình tư vấn thêm nha" (quyết định của người viết, có thể chỉnh trong bộ thông tin tiệm).
     - Nhắc phí phá gel nếu bộ thông tin tiệm có ghi.
6. **Hết thời gian chờ:**
   - Sau **45 phút** (chỉnh được) mà thợ chưa trả lời, app nhắc thợ một lần và báo cho chủ tiệm.
   - Sau **3 giờ** (chỉnh được) vẫn chưa có giá:
     - Mặc định: bỏ qua bài.
     - Tùy chọn (mặc định tắt): comment không kèm giá, mô tả mẫu + "ib mình báo giá chi tiết nha", đúng nguyên tắc "khi chưa chắc giá thì ghi báo giá qua tin nhắn".
   - Đây là quyết định của người viết.
7. **Nhiều bài cùng chờ:** mỗi bài là một yêu cầu riêng trong kênh thợ. Câu trả lời của thợ phải gắn đúng yêu cầu (xem cách ghép câu trả lời ở chức năng 02).

---

## 7. Chế độ gửi

- **Tự gửi:** comment hợp lệ được đưa vào hàng đợi và gửi theo phanh an toàn.
- **Duyệt trước:** comment được đưa vào danh sách "chờ duyệt" trên web app. Chủ tiệm có thể:
  - xem bài gốc (có link), phân loại và comment đề xuất;
  - **sửa chữ**, **đổi poster**, **duyệt**, hoặc **bỏ**.
- Chế độ chọn được **cho toàn app** và **cho từng loại bài**. Ví dụ: loại 1 tự gửi, loại 3 duyệt trước.
- **Mặc định khi mới cài: duyệt trước cho mọi loại.** Lý do: chủ tiệm cần thời gian thử với tài khoản phụ (quyết định của người viết).
- Comment chờ duyệt mà quá "tuổi tối đa" của bài thì tự hết hạn.

---

## 8. Gửi comment và phanh an toàn

### Cách gửi
- Mở bài bằng trình duyệt tự động, dùng đúng phiên đăng nhập của tài khoản vận hành.
- Nhập chữ theo nhịp giống người: gõ từng đoạn, có khoảng nghỉ ngắn.
- Đính kèm ảnh poster, rồi gửi.
- Sau khi gửi, xác nhận comment đã hiện ra và lấy link hoặc ID comment nếu được.

### Phanh an toàn (tất cả đều chỉnh được)
- **Tối đa comment mỗi ngày** cho toàn tài khoản. Mặc định 15, theo mục tiêu tham khảo 10–15 comment/ngày của tiệm.
- **Tối đa comment mỗi group mỗi ngày.** Mặc định 3.
- **Khoảng cách tối thiểu giữa hai comment:** ngẫu nhiên trong một khoảng, mặc định 4–12 phút.
- **Giờ nghỉ:** không gửi trong giờ nghỉ.
- **Không comment hai lần vào cùng một bài,** kể cả khi bài được quét lại.
- **Tự dừng khi có dấu hiệu bất thường:**
  - phiên đăng nhập hết hạn;
  - Facebook bắt xác minh (checkpoint);
  - comment bị chặn hoặc bị báo spam;
  - gửi thất bại liên tiếp nhiều lần.

  Khi dừng, app **tắt toàn bộ tác vụ tự động trên tài khoản vận hành**, lưu ảnh màn hình, và báo ngay cho chủ tiệm. Chỉ chạy lại khi chủ tiệm bấm "chạy lại".
- **Nút dừng khẩn cấp** trên web app.

### Gửi thất bại
- Gửi lỗi thì thử lại 1 lần sau vài phút.
- Vẫn lỗi thì đánh dấu thất bại, ghi lý do và ảnh màn hình.
- Lỗi thuộc nhóm "dấu hiệu bất thường" ở trên thì dừng toàn bộ.

---

## 9. Nhật ký và thống kê

Mỗi bài app đã xét được lưu lại cùng các thông tin sau:
- group, link bài, người đăng, nội dung, thời điểm đăng, thời điểm app phát hiện;
- kết quả phân loại, lý do;
- trạng thái: không phù hợp / bỏ qua (kèm lý do) / chờ báo giá / chờ duyệt / đã comment / thất bại;
- nội dung comment đã gửi, poster đã dùng, bộ content đã dùng, thời điểm gửi;
- khoảng thời gian từ lúc bài được đăng đến lúc comment.

Thống kê theo ngày và theo group:
- số bài đã quét, số bài phù hợp, số comment đã gửi;
- thời gian trung bình từ lúc bài được đăng đến lúc comment;
- số tin nhắn mới vào Page trong cùng ngày, đặt cạnh số comment để so sánh. App chưa xác định được chính xác khách nào đến từ comment nào. *Gợi ý của người viết:* khi khách nhắn Page, AI có thể hỏi khéo "bạn thấy tiệm ở đâu nè?", nhưng tính năng này để sau.

---

## 10. Trường hợp đặc biệt

- **Bài bị xóa hoặc không mở được khi gửi:** đánh dấu bỏ qua.
- **Bài đã tắt comment:** đánh dấu bỏ qua.
- **Group không truy cập được** (bị kick hoặc group bị khóa): tắt quét group đó và báo chủ tiệm.
- **Bài sửa nội dung sau khi app đã comment:** không làm gì thêm.
- **Bài có nhiều ảnh mẫu (loại 3):** gửi tối đa 4 ảnh cho thợ. Mô tả 1 dòng tả mẫu chính. Nếu các ảnh là các mẫu khác nhau thì ghi "khách gửi nhiều mẫu", và thợ có thể báo giá theo khoảng (quyết định của người viết).
- **Khách đã có tiệm khác comment:** vẫn comment bình thường.
