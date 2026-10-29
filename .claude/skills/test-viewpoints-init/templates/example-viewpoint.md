## 2. Kiểm tra dữ liệu nhập

### Câu hỏi gợi ý
- Trường bắt buộc để trống, chỉ có dấu cách thì sao?
- Giá trị ngay dưới, bằng, ngay trên giới hạn dưới và trên?
- Sai kiểu (chữ vào ô số, số âm, số thập phân)?
- Sai định dạng (URL, số điện thoại, giờ)?
- Trùng với bản ghi đã có?
- Chuỗi rất dài, emoji, tiếng Việt có dấu tổ hợp?
- Dán nội dung có ký tự xuống dòng hoặc khoảng trắng đầu/cuối?

### Ví dụ
- Cài đặt group: dán link `facebook.com/groups/abc?ref=share`, dán ID số, dán link không phải group.
- Giới hạn comment/ngày: 0, 1, 50, 51, -1, `abc`.
- Giờ làm việc: giờ kết thúc trước giờ bắt đầu, khoảng giờ chồng nhau trong cùng ngày.
