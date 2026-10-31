> Bản đọc sinh từ docs/testing/viewpoints.md (phiên bản 0d0b7b7, 2026-10-31 18:08). Không sửa tay.

<a id="s-0b0fa0b228"></a>

# Bảng khía cạnh test

**Tóm tắt.** Tài liệu này liệt kê các khía cạnh cần xét khi thiết kế manual test case cho một tính năng.

**Cách dùng**
- Mỗi lần chạy `/test-case-design` phải xét đủ các khía cạnh dưới đây.
- Nếu một khía cạnh không áp dụng cho tính năng, file test case phải ghi lý do.

**Phạm vi manual test**
- Manual test gồm mọi việc con người làm được bằng tay qua trình duyệt, DB, cookie, Facebook, Messenger và thiết bị thật.
- Manual test không gồm việc can thiệp vào luồng xử lý của code.

<a id="s-7aacdafb89"></a>

## 1. Hiển thị

**Tóm tắt.** Khía cạnh này kiểm tra màn hình, dữ liệu, ngày giờ, màu trạng thái và ảnh có hiển thị đúng và dễ dùng hay không.

<a id="s-87956d662c"></a>

### Câu hỏi gợi ý
- Màn hình có khớp mockup ở mọi trạng thái đã thiết kế không? Các trạng thái gồm trống, đang tải, có dữ liệu, lỗi và không có quyền.
- Dữ liệu hiển thị có đúng với bản ghi trong DB không? Cần soát số, giá, ngày giờ, trạng thái và tên.
- Chữ tiếng Việt có dấu, tên Facebook có emoji và chuỗi rất dài có bị vỡ dòng, tràn khung hay cắt mất chữ không?
- Bố cục có dùng được bằng ngón cái và không phải cuộn ngang không? Cần xem ở bề ngang điện thoại (iPhone của chủ tiệm, Android của thợ) và ở máy tính.
- Ngày giờ có hiển thị theo giờ Việt Nam không? Định dạng có thống nhất (thứ, ngày/tháng, 24h) không?
- Màu và nhãn trạng thái có phân biệt rõ không? Ví dụ: chưa duyệt, đã chốt và khung bận; chạy, tạm dừng và bị dừng.
- Ảnh có đúng ảnh, đúng chiều và không bị méo không? Cần xem ảnh gốc, ảnh đã chỉnh, poster và ảnh thu nhỏ.
- Khi đánh giá bằng mắt, poster có đúng nhận diện không (khổ 1080×1350, màu, font)? Chữ có đè lên vùng móng không? Giọng văn có đúng giọng tiệm không?

<a id="s-70fc1309bf"></a>

### Ví dụ
- Trang chính hiển thị số comment hôm nay so với giới hạn, ví dụ 7/15. Con số này phải khớp số bản ghi đã gửi trong DB. Chu kỳ quét thực tế phải hiển thị đúng.
- Trên lịch tuần ở iPhone, lịch ép chọn mang cảnh báo rõ. Lịch chưa duyệt và lịch đã chốt có màu khác nhau.
- Màn hình duyệt mẫu mới đặt ảnh gốc và ảnh đã chỉnh cạnh nhau để so. Poster chỉ ghi "99k trọn bộ" khi đã xác nhận là trọn bộ.
- Danh sách khách vẫn hiển thị gọn khi tên Facebook dài có emoji và tin nhắn gần nhất có nhiều dòng.

<a id="s-41ece91b56"></a>

## 2. Kiểm tra dữ liệu nhập

**Tóm tắt.** Khía cạnh này kiểm tra app xử lý thế nào khi người dùng nhập dữ liệu thiếu, sai, trùng hoặc bất thường.

<a id="s-d27392eaea"></a>

### Câu hỏi gợi ý
- Trường bắt buộc bị để trống hoặc chỉ có dấu cách thì sao?
- Giá trị ngay dưới, bằng và ngay trên giới hạn dưới và giới hạn trên thì sao?
- Giá trị sai kiểu thì sao? Ví dụ: chữ vào ô số, số âm, số thập phân.
- Giá trị sai định dạng thì sao? Ví dụ: URL, số điện thoại, giờ.
- Giá trị trùng với bản ghi đã có thì sao?
- Chuỗi rất dài, emoji và tiếng Việt có dấu tổ hợp thì sao?
- Nội dung dán vào có ký tự xuống dòng hoặc khoảng trắng đầu/cuối thì sao?
- File tải lên sai loại, quá lớn hoặc là ảnh xoay theo EXIF thì sao?

<a id="s-0d887e6a64"></a>

### Ví dụ
- Cài đặt group: dán link `facebook.com/groups/abc?ref=share`, dán ID số, dán link không phải group và dán lại group đã có.
- Giới hạn comment/ngày: thử các giá trị 0, 1, 15, 16, -1, `abc`, `2.5`.
- Giờ làm việc: thử giờ kết thúc trước giờ bắt đầu và hai khoảng giờ chồng nhau trong cùng ngày. Thử cả các khoảng giờ buổi sáng/chiều/tối chồng nhau.
- Danh sách từ cấm và từ khóa lọc: nhập từ có dấu và không dấu, từ bị trùng và từ chỉ có dấu cách.

<a id="s-55fd30715f"></a>

## 3. Logic nghiệp vụ

**Tóm tắt.** Khía cạnh này kiểm tra các quy tắc nghiệp vụ trong thiết kế chạy đúng ở mọi nhánh, và thông tin app đưa ra có nguồn gốc rõ ràng.

<a id="s-9d7a0b25c4"></a>

### Câu hỏi gợi ý
- Mỗi quy tắc `R-<ABC>-<nn>` trong thiết kế đã có ít nhất một case cho nhánh đúng và một case cho nhánh sai chưa?
- Quy tắc nhiều điều kiện (bảng quyết định) đã đủ tổ hợp chưa? Cần tính cả tổ hợp "không điều kiện nào thỏa".
- Tham số cài đặt có thật sự được dùng không? Khi đổi giá trị trên web, hành vi của app phải đổi theo.
- Mọi thông tin app nói với khách (giá, giờ, địa chỉ, chính sách) có truy được về nguồn không? Nguồn gồm bộ thông tin tiệm đã xác nhận, lịch, kho và câu trả lời của thợ.
- Khi thiếu dữ liệu đầu vào, app có dừng đúng chỗ và báo đúng người không? Ví dụ: chưa có giờ làm, chưa bật bộ content, mục thông tin chưa xác nhận.
- Nội dung app sinh ra có tránh được từ tuyệt đối không? Nội dung có tránh ghi "trọn bộ như hình" hay "ảnh thật tại tiệm" khi điều đó không đúng không?
- Xoay vòng, giới hạn và giãn cách có được tính đúng theo phạm vi không? Phạm vi có thể là toàn tài khoản, từng group hoặc từng ngày.

<a id="s-ece5f533de"></a>

### Ví dụ
- Phân loại bài: thử bài loại 1, 2, 3. Bài vừa hỏi giờ vừa có ảnh phải là loại 3. Thử cả bài bán hàng của tiệm khác, bài tuyển nhân viên và bài tìm thợ mi.
- Lọc khu vực: thử bài không nhắc khu vực, bài nhắc Quận 11 và bài chỉ nhắc khu vực ngoài danh sách.
- Comment loại 2 có ba trường hợp:
  - ngày khách hỏi còn trống;
  - ngày đó không còn trống, app đề xuất tối đa 3 khung trải ở các buổi khác nhau;
  - không có khung nào trống trong 7 ngày, app không comment và ghi lý do.
- Inbox: khách hỏi chính sách cọc khi mục đó chưa được xác nhận. App phải chuyển cho người thật và không tự trả lời.

<a id="s-0f0817a68a"></a>

## 4. Chuyển trạng thái

**Tóm tắt.** Khía cạnh này kiểm tra các chuyển trạng thái hợp lệ chạy đúng, chuyển không hợp lệ bị chặn, và lịch sử thay đổi được ghi đủ.

<a id="s-f31a3bd3b4"></a>

### Câu hỏi gợi ý
- Mọi chuyển trạng thái hợp lệ trong sơ đồ đã có case chưa?
- Chuyển không hợp lệ có bị chặn và báo rõ không? Ví dụ: từ trạng thái cuối quay lại trạng thái trước.
- Thao tác trên bản ghi đã ở trạng thái cuối (đã hủy, đã hết hạn, đã bỏ) thì sao?
- Trạng thái liên quan có được cập nhật theo không? Ví dụ: lịch hẹn kéo theo trạng thái khách, báo giá kéo theo trạng thái bài.
- Lịch sử thay đổi có ghi đủ ai đổi, lúc nào, qua kênh nào và giá trị cũ là gì không?
- Cùng một chuyển trạng thái làm qua web và qua Messenger có cho kết quả giống nhau không?

<a id="s-bef49381c8"></a>

### Ví dụ
- Lịch hẹn:
  - đi từ chưa duyệt sang đã chốt, rồi sang đã làm xong;
  - đi từ chưa duyệt sang đã hủy;
  - thử đánh dấu "đã làm xong" cho lịch chưa duyệt, thao tác này phải bị chặn.
- Bài trong group:
  - đang chờ báo giá, thợ báo "bỏ", bài chuyển sang bỏ qua;
  - đang chờ duyệt mà quá tuổi tối đa, bài tự hết hạn;
  - bài thất bại thì comment lại.
- Khách:
  - đi lần lượt qua mới, đang trao đổi, đã giữ chỗ, đã chốt lịch, đã xong;
  - đang trao đổi mà 3 ngày không có tin thì chuyển sang ngừng trao đổi.
- Yêu cầu báo giá đã hết hạn: thợ trả lời "99k" thì giá không được áp dụng, và app báo lại cho thợ.

<a id="s-e9afe29016"></a>

## 5. Phân quyền

**Tóm tắt.** Khía cạnh này kiểm tra mỗi vai trò chỉ làm được đúng việc của mình, trên web lẫn trên Messenger.

<a id="s-e8d29097b9"></a>

### Câu hỏi gợi ý
- Vai trò Thợ có thấy hoặc bấm được những gì chỉ Quản lý được làm không? Cần thử cả nút trên màn hình lẫn gõ thẳng URL.
- Gọi thẳng API của chức năng chỉ dành cho Quản lý bằng phiên Thợ thì nhận lỗi gì?
- Mở URL bên trong app khi chưa đăng nhập thì sao?
- Trên Messenger, người lạ (không phải thợ, không phải chủ tiệm) nhắn mã ghép nối hoặc lệnh của thợ thì sao?
- Tin nhắn từ thợ hoặc chủ tiệm có bao giờ bị xử lý như tin của khách không?
- Tài khoản thợ bị chủ tiệm khóa hoặc xóa thì phiên đang mở còn dùng được không?

<a id="s-cd7c404c5d"></a>

### Ví dụ
- Đăng nhập vai trò Thợ rồi thử mở URL `/settings`, bấm nút dừng khẩn cấp và gọi API duyệt comment. Cả ba thao tác đều phải bị chặn.
- Thợ được thao tác Lịch, Báo giá, Khách và tải mẫu mới. Thợ không được duyệt mẫu mới và không được sửa comment group.
- Khách nhắn "duyệt" hoặc "#G12 99k" vào Page. Tin này không được tính là thợ báo giá hay thợ duyệt lịch.

<a id="s-9844f73856"></a>

## 6. Phiên đăng nhập và cookie

**Tóm tắt.** Khía cạnh này kiểm tra app xử lý đúng khi phiên đăng nhập của web app, Facebook hoặc Meta Business Suite bị mất hay hết hạn.

<a id="s-80b93f6e02"></a>

### Câu hỏi gợi ý
- Xóa cookie phiên web app giữa chừng rồi thao tác tiếp thì sao? Dữ liệu đang nhập có bị mất âm thầm không?
- Đăng nhập sai nhiều lần có bị giới hạn không?
- Đăng nhập lâu dài trên điện thoại có giữ được sau khi tắt mở PWA hay khởi động lại máy không?
- Đổi mật khẩu thì các phiên cũ ở thiết bị khác ra sao?
- Phiên Facebook của tài khoản vận hành hết hạn thì app có tự dừng và báo khẩn không? Có thể giả lập bằng cách xóa cookie trong profile hoặc đăng xuất từ thiết bị khác.
- Phiên Meta Business Suite của tài khoản inbox hết hạn thì worker inbox có dừng và báo không? App có gửi nhầm gì cho khách không?
- Sau khi đăng nhập lại qua noVNC và bấm "chạy lại", app có hoạt động lại đúng không?

<a id="s-67abab1da8"></a>

### Ví dụ
- Đăng xuất tài khoản vận hành khỏi Facebook từ một điện thoại khác. Lượt quét kế tiếp phải phát hiện hết phiên. App tắt toàn bộ tác vụ tự động, lưu ảnh màn hình và báo chủ tiệm qua Messenger và email.
- Xóa cookie web app khi đang sửa comment chờ duyệt, rồi bấm lưu. App đưa người dùng về trang đăng nhập và không lưu nửa vời.
- Đăng nhập sai mật khẩu liên tiếp vượt giới hạn. Tài khoản bị khóa tạm và app thông báo rõ.

<a id="s-f3a10b99bf"></a>

## 7. Thao tác đồng thời

**Tóm tắt.** Khía cạnh này kiểm tra kết quả vẫn đúng và nhất quán khi nhiều thao tác cùng nhắm vào một bản ghi hoặc một khung giờ.

<a id="s-e15d925776"></a>

### Câu hỏi gợi ý
- Bấm gửi hoặc duyệt hai lần liên tiếp thì có tạo hai bản ghi hoặc gửi hai lần không?
- Hai tab (hoặc hai người) cùng sửa một bản ghi thì ai thắng? Người kia có được báo không?
- Thợ thao tác qua Messenger đúng lúc chủ tiệm thao tác cùng bản ghi trên web thì sao?
- Hai luồng tự động cùng muốn chiếm một khung giờ thì sao? Ví dụ: hai khách inbox cùng xin một slot.
- Người thật trả lời khách từ Page đúng lúc app chuẩn bị gửi tin tự động thì sao?
- Bấm Back hoặc tải lại trang trong lúc đang xử lý thì kết quả có nhất quán không?

<a id="s-0160ccea53"></a>

### Ví dụ
- Hai khách nhắn gần như cùng lúc để xin 14h thứ Ba. Chỉ một khách được giữ chỗ. Khách kia được đề xuất khung khác.
- Thợ bấm "Duyệt" trên Messenger trong khi chủ tiệm bấm "Hủy" trên web cho cùng một lịch. Thao tác đến trước được áp dụng. Thao tác đến sau nhận thông báo "lịch đã thay đổi".
- Chủ tiệm bấm "Duyệt" comment hai lần thật nhanh. Chỉ một comment được gửi lên bài.
- Hai tab cùng sửa giờ làm việc tuần rồi lưu. Dữ liệu không bị mất âm thầm.

<a id="s-2b06cb8504"></a>

## 8. Dữ liệu bất thường trong DB

**Tóm tắt.** Khía cạnh này kiểm tra app vẫn chạy ổn khi dữ liệu trong DB bị xóa, bị sửa tay, ở trạng thái lạ hoặc có số lượng lớn.

<a id="s-c05ab1f71c"></a>

### Câu hỏi gợi ý
- Bản ghi liên quan bị xóa (bộ content, poster, group, khách) thì màn hình và luồng tự động phản ứng thế nào?
- Trường không bắt buộc bị để NULL hoặc chuỗi rỗng thì có lỗi hiển thị hay lỗi xử lý không?
- Dữ liệu ở trạng thái "lạ" mà UI không tạo ra được thì app có crash không? Ví dụ: lịch chồng nhau không có cờ ép chọn, trạng thái không khớp lịch sử.
- Sửa thời điểm trong DB để giả lập thời gian trôi qua thì job hẹn giờ có chạy đúng không?
- Dữ liệu cũ đã "lưu trữ" có còn được liên kết từ lịch sử comment và bài đăng không?
- Khi số lượng lớn (hàng nghìn bài, hàng trăm khách), danh sách, lọc và tìm kiếm có còn dùng được không?

<a id="s-d9b2ac604a"></a>

### Ví dụ
- Xóa poster đang được bộ content loại 1 dùng. Lượt comment kế tiếp không được gửi comment thiếu ảnh và phải báo chủ tiệm.
- Sửa `created_at` của lịch chưa duyệt lùi 2 giờ. App phải nhắc thợ.
- Chèn tay hai lịch đã chốt chồng nhau mà không có cờ ép chọn. Màn hình lịch vẫn mở được và hiện cảnh báo.
- Đổi một mục thông tin tiệm đã xác nhận về "chưa xác nhận". Inbox không được dùng mục đó nữa.

<a id="s-61fcfb2bb2"></a>

## 9. Phía Facebook và Messenger

**Tóm tắt.** Khía cạnh này kiểm tra app phản ứng đúng với những thay đổi và sự cố đến từ Facebook, Messenger và cách thợ nhắn tin.

<a id="s-71851ed036"></a>

### Câu hỏi gợi ý
- Bài gốc bị xóa, bị tắt comment hoặc bị chuyển sang riêng tư trước khi app comment thì sao?
- Tài khoản vận hành rời group, bị kick, hoặc group bị khóa hay chuyển sang duyệt bài thì sao?
- Facebook bắt checkpoint, chặn comment hoặc báo spam thì app có tự dừng toàn bộ và báo khẩn không?
- Người thật trả lời khách từ Page (Business Suite, app Messenger) thì app có nhận ra và ngừng tự trả lời không?
- Thợ trả lời sai cú pháp, trả lời mơ hồ, trả lời yêu cầu đã hết hạn, gửi tin thoại hoặc gửi ảnh không kèm chữ thì sao?
- App có ghép đúng yêu cầu không khi thợ vuốt để trả lời đúng tin, bấm nút nhanh, nhắn có mã, hoặc nhắn không mã lúc có nhiều yêu cầu cùng chờ?
- Khi cửa sổ 24 giờ của Messenger đã đóng, thông báo có đi qua web push và email không?
- Comment và bài đăng thật trên Facebook có hiện đúng chữ, đúng poster, đúng group và không bị lặp không?

<a id="s-3fe23a1280"></a>

### Ví dụ
- Xóa bài trong group riêng tư dùng để thử, sau khi app đã đưa comment vào hàng đợi. Comment không được gửi và bài được đánh dấu bỏ qua.
- Hai yêu cầu báo giá `#G12` và `#G13` cùng đang chờ. Thợ nhắn "99k" mà không kèm mã. App hỏi lại "Giá 99k này cho mẫu nào?" kèm nút chọn.
- Chủ tiệm nhắn cho khách từ Meta Business Suite. App tạm dừng tự trả lời cuộc trò chuyện đó 12 giờ và không chen ngang.
- Thợ gửi tin thoại. App trả lời "Mình chưa nghe được tin thoại, bạn nhắn chữ giúp mình nha".

<a id="s-6f73d0d7b0"></a>

## 10. Thời gian

**Tóm tắt.** Khía cạnh này kiểm tra các mốc giờ, ngày tương đối, hạn chờ, múi giờ và việc reset theo ngày được tính đúng.

<a id="s-c5e6484446"></a>

### Câu hỏi gợi ý
- Thao tác rơi đúng mốc biên thì sao? Mốc biên gồm bắt đầu và kết thúc của giờ nghỉ, giờ vàng, giờ làm, và nửa đêm.
- Ngày tương đối ("mai", "thứ 3", "tối nay") có được quy đổi theo thời điểm bài hoặc tin được đăng, không theo lúc app xử lý không? Bài đăng lúc 23:50 ghi "mai" thì sao?
- Các hạn chờ có kích hoạt đúng lúc và chỉ một lần không? Các hạn chờ gồm nhắc thợ, hết hạn báo giá, comment chờ duyệt quá tuổi và lịch chưa duyệt bị bỏ quên.
- Nội dung, nhãn và bộ content có hạn dùng có tự tắt đúng ngày không? Ví dụ: Halloween hết hạn sau 31/10.
- Mọi giờ hiển thị và lưu có đúng múi giờ `Asia/Ho_Chi_Minh` không, kể cả khi máy chủ ở Singapore và điện thoại để múi giờ khác?
- Khung trống có tôn trọng khoảng cách tối thiểu tính từ hiện tại không? Mặc định là 2 giờ.
- Ngày đặc biệt (nghỉ Tết, làm giờ khác) có ghi đè giờ làm tuần đúng không?
- Khi chạy thật nhiều ngày liên tục, giới hạn theo ngày có reset đúng lúc 00:00 giờ Việt Nam không?

<a id="s-7a012294bd"></a>

### Ví dụ
- Giờ nghỉ là 23:30–07:00. Thử comment đến lượt gửi lúc 23:29 và lúc 23:31. Trong giờ nghỉ, app không quét và không gửi.
- Bài đăng tối thứ Hai ghi "mai tuyển mẫu", app quét vào sáng thứ Ba. "mai" vẫn phải hiểu là thứ Ba.
- Sửa DB để lùi thời điểm gửi yêu cầu báo giá:
  - lùi 45 phút thì app nhắc thợ một lần và báo chủ tiệm;
  - lùi 3 giờ thì app bỏ qua bài.
- Lịch hẹn kết thúc lúc 16:30. Khoảng 17:00, app hỏi thợ "Khách … lịch 14h đã làm xong chưa?".

<a id="s-68cae7cddb"></a>

## 11. Lỗi mạng và lỗi hệ thống bên ngoài

**Tóm tắt.** Khía cạnh này kiểm tra app xử lý đúng khi mạng, dịch vụ bên ngoài hoặc dịch vụ nội bộ gặp sự cố.

<a id="s-173f778e49"></a>

### Câu hỏi gợi ý
- Điện thoại mất mạng giữa lúc gửi form thì người dùng có biết thao tác chưa thành công không? Gửi lại có bị trùng không?
- Máy chủ mất mạng khi đang comment, đăng bài hoặc gửi tin cho khách thì sao? Sau khi có mạng lại, app có thử lại hoặc đánh dấu thất bại đúng thiết kế không?
- Gemini lỗi, sai khóa API hoặc vượt hạn mức chi tiêu tháng thì app có chuyển sang dự phòng không? Dự phòng gồm sao chép prompt và tải ảnh lên tay. App có báo chủ tiệm không?
- Graph API đăng Page lỗi thì app có báo và cho bấm đăng lại không?
- Messenger Send API lỗi hoặc web push không tới được iPhone thì thông báo khẩn có còn tới qua email không?
- Một dịch vụ trong `compose.yml` (Redis, PostgreSQL, browser-worker) dừng rồi chạy lại thì job đang dở có bị mất hoặc chạy hai lần không?
- Ổ đĩa đầy hoặc sao lưu hằng đêm thất bại thì có cảnh báo không?

<a id="s-ce44fdf083"></a>

### Ví dụ
- Đặt hạn mức chi tiêu chỉnh ảnh rất thấp trong Cài đặt. Mẫu mới tiếp theo chuyển sang dự phòng tải ảnh lên tay và chủ tiệm được báo.
- Tắt Wi-Fi điện thoại khi bấm "Duyệt" lịch. App báo lỗi rõ. Bật lại mạng và bấm lại thì lịch chỉ được duyệt một lần.
- Dừng container browser-worker khi có comment trong hàng đợi, rồi chạy lại. Comment được gửi đúng một lần, hoặc được đánh dấu thất bại kèm lý do.
- Đổi khóa Gemini trong `.env` thành khóa sai rồi khởi động lại. Bước phân loại bài báo lỗi hệ thống và app không comment bừa.

<a id="s-d76a0acab9"></a>

## 12. Regression

**Tóm tắt.** Khía cạnh này xác định case nào cần gắn cờ regression và phần nào cần chạy lại khi có thay đổi.

<a id="s-be915b9101"></a>

### Câu hỏi gợi ý
- Case nào là cốt lõi của tính năng và phải gắn cờ regression?
- Tính năng mới đụng tới phần dùng chung nào? Ví dụ: tìm khung trống, phanh an toàn, kênh thợ, bộ thông tin tiệm, kho content. Case regression của các phần đó đã được chạy lại chưa?
- Thay đổi schema DB hoặc migration có làm hỏng dữ liệu của tính năng cũ không?
- Đổi prompt AI có làm kết quả phân loại, giọng văn hoặc mô tả mẫu xấu đi trên các bài và ảnh đã từng đúng không?
- Đổi style UI hoặc component dùng chung có làm vỡ màn hình nào khác không?
- Lỗi đã sửa (`P<N>-ISS-<nnn>`) đã có case test lại chưa? Case đó đã gắn cờ regression chưa?

<a id="s-4da66deaa3"></a>

### Ví dụ
- Sửa phép tính khung trống cho inbox thì chạy lại case regression của comment loại 2 và của tóm tắt lịch đầu ngày.
- Thêm loại thông báo mới cho chủ tiệm thì kiểm tra lại cửa sổ 24 giờ và kênh dự phòng web push, email.
- Đổi prompt phân loại bài thì chạy lại bộ bài mẫu đã biết loại (loại 1, 2, 3, không phù hợp) và so kết quả.
- Đổi màu token trạng thái thì xem lại Lịch, Trang chính và Khách trên iPhone.

<a id="s-7afbf6c958"></a>

## Lằn ranh đỏ

**Tóm tắt.** Đây là những lỗi không được để xảy ra. Mỗi lằn ranh được giữ bởi một số khía cạnh test ở trên.

- **Nói sai với khách.** App nói sai giá, sai ngày giờ trống, sai địa chỉ, hoặc tự bịa thông tin chưa có (địa chỉ cụ thể, giờ mở cửa, khuyến mãi, số lượng khách, chính sách cọc…). Giữ bởi khía cạnh 3, 10.
- **Nhận trùng lịch.** App hứa với hai khách cùng một khung giờ. Giữ bởi khía cạnh 3, 7, 8.
- **Comment giống spam.** App lặp y hệt câu chữ, comment hai lần vào cùng một bài, comment vào bài không liên quan hoặc comment dồn dập. Giữ bởi khía cạnh 3, 7, 9.
- **Làm mất kênh tìm khách.** Tài khoản Facebook tìm khách hoặc trả lời inbox bị khóa mà không có cảnh báo hay cơ chế dừng. Tệ hơn là mất quyền quản lý Page. Giữ bởi khía cạnh 6, 9, 11.
- **Ảnh chỉnh sai mẫu.** Ảnh AI chỉnh khác mẫu móng thật (sai màu, sai form, thừa ngón), hoặc ảnh đã chỉnh bị ghi "ảnh thật tại tiệm". Giữ bởi khía cạnh 1, 3.
- **Vi phạm nguyên tắc minh bạch.** App viết review giả, dùng từ tuyệt đối ("tốt nhất", "rẻ nhất", "đẹp nhất"), hoặc ghi "trọn bộ như hình" khi chưa rõ đã gồm nối móng. Giữ bởi khía cạnh 1, 3.
- **Chen ngang.** App trả lời khách trong khi thợ hoặc chủ tiệm đang nói chuyện với khách đó. Giữ bởi khía cạnh 7, 9.

<a id="s-80b54c0db6"></a>

## Lịch sử thay đổi

- 2026-10-29: tạo mới.
