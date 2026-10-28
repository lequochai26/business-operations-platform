# Tóm tắt – Web app vận hành marketing Tiệm Nhà Mio

*Bản ngắn để xem nhanh. Chi tiết nằm ở các file 01 đến 06.*

## App để làm gì
- Tiệm có 1 thợ. Chủ tiệm một mình lo hết phần marketing:
  - lướt group tìm bài tuyển mẫu, comment;
  - làm poster và content, đăng bài;
  - trả lời khách, chuyển lời giữa khách và thợ.
- Tất cả tốn rất nhiều thời gian, lịch bị lệch giữa chủ tiệm và thợ, báo giá phải chờ thợ nên bài trôi mất.
- App gánh phần việc lặp lại. **Chủ tiệm chỉ duyệt và quyết định. Thợ chỉ trả lời ngắn qua Messenger.**

## Các phần chính
- **Tự đi comment group:**
  - App tự lướt các group nail và nhận ra 3 loại bài:
    - **Loại 1, chung chung:** comment bằng 1–3 bộ content cố định, có xoay vòng.
    - **Loại 2, có hỏi ngày giờ:** tra lịch thợ. Còn trống thì xác nhận đúng giờ khách hỏi, hết chỗ thì đề xuất giờ trống gần nhất.
    - **Loại 3, xin báo giá một mẫu:** AI viết mô tả 1 dòng rồi gửi kèm ảnh cho thợ qua Messenger. Thợ trả lời giá (có thể sửa mô tả), app tự comment.
  - Có phanh an toàn (giới hạn, giãn cách, giờ nghỉ, tự dừng) và công tắc **tự gửi / duyệt trước**.
- **Kênh thợ qua Messenger:**
  - Thợ báo giá, duyệt/hủy/dời lịch, khóa giờ bận, gửi ảnh mẫu mới, báo khách đã xong.
  - Thợ có thể bấm nút hoặc nhắn câu ngắn. App xác nhận lại mọi thay đổi.
- **Lịch làm của thợ:** một lịch duy nhất cho mọi việc.
  - Trạng thái lịch hẹn: chưa duyệt (giữ chỗ) → đã chốt → đã làm xong.
  - Có chống trùng lịch.
- **Inbox Page:**
  - Tự trả lời câu hỏi có thông tin cố định (chỉ dùng bộ thông tin tiệm đã xác nhận, không bịa).
  - Giữ chỗ khi khách hỏi lịch.
  - Câu khó thì nhờ khách chờ thật thân thiện và gọi người thật. Không chen ngang khi người thật đang nhắn.
  - Theo dõi trạng thái từng khách. "Xong" nghĩa là đã chốt lịch và đã làm xong.
- **Tạo và đăng mẫu mới:**
  - Thợ gửi ảnh, app chỉnh ảnh, làm poster theo mẫu có sẵn, viết gói content.
  - **Chủ tiệm duyệt một lần**, rồi app tự đăng Page và đăng group theo đợt (tối đa 3 group mỗi đợt).
  - Từ khoảng 15 phút xuống khoảng 1–2 phút.
- **Kho content:** mọi poster và content ở một chỗ, tìm được bằng chữ không dấu, lọc theo tag, có hạn dùng và lịch sử sử dụng.
- **Web app trên điện thoại:** hai vai trò Quản lý và Thợ, có thông báo đẩy, cài đặt mọi tham số.

## Không làm ở bản này
- Tự ước tính giá (bổ sung khi có bảng giá).
- Thu tiền, quảng cáo trả phí, kênh khác ngoài Facebook, nhiều thợ.

## Công nghệ
- Kế thừa POC `fb-post-crawler-poc`: Node.js + TypeScript + Playwright.
- NestJS, BullMQ + Redis, PostgreSQL, chạy trên **Oracle Cloud Free**.
- **Gemini miễn phí** cho phần chữ. **Gemini Nano Banana 2.1 trả phí** cho chỉnh ảnh, khoảng 6 USD/tháng. Dự phòng: tự chỉnh ảnh rồi tải lên.
- **Group:** dùng trình duyệt tự động, có rủi ro bị khóa tài khoản. Thử bằng tài khoản phụ trước.
- Hiện có 6 group, khoảng 50–100 bài mới mỗi ngày. Mỗi chu kỳ quét mất khoảng 6–8 phút.
- **Inbox khách:** tiệm chưa có giấy phép kinh doanh nên không xin được quyền chính thức của Meta. App đọc và trả lời inbox bằng **trình duyệt tự động** trên Meta Business Suite, dùng một tài khoản riêng chỉ có quyền nhắn tin, có cùng rủi ro như phần group.
- **Kênh thợ và đăng Page:** dùng kết nối chính thức của Meta (thợ và chủ tiệm là tester).
- **Thông báo:** chủ tiệm dùng iPhone nên thông báo khẩn được gửi thêm qua email. Thợ dùng Android.

## Thứ tự làm
0. Nền móng trên Oracle, kiểm chứng phiên đăng nhập chạy 24/7.
1. Tự comment bài loại 1.
2. Lịch + kênh thợ, bật loại 2 và 3.
3. Inbox Page.
4. Mẫu mới, đăng bài, kho content đầy đủ.

## Cần chủ tiệm bổ sung hoặc quyết định
- Giờ nhận khách, địa chỉ, phí phá gel, nối móng, chính sách cọc/hủy, Zalo.
- Tài khoản Facebook nào sẽ chạy thật sau khi thử.
- Có để app nói mình là trợ lý tự động khi khách hỏi không.
- Có chấp nhận gửi tin nhắn khách qua Gemini miễn phí không.
- Tài khoản nào chạy worker inbox (dùng chung hay tách riêng).
- Dùng tên miền miễn phí (DuckDNS) hay mua tên miền riêng.
- Danh sách quyết định người viết tự đưa ra: `06-open-issues-and-assumptions.md`.
