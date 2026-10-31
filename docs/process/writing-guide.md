# Hướng dẫn viết bản cho người đọc

AI đọc file này mỗi lần viết lại một mục trong `docs/reader/_rewrite/` (skill `reader-view`). Bản gốc không bao giờ bị sửa; chỉ bản viết lại theo hướng dẫn này.

## Trình bày

- Mỗi mục lớn (quy tắc, test case, task, vấn đề, quyết định, điểm review) mở đầu bằng **Tóm tắt** một đến hai câu: mục này nói gì.
- Có **Vì sao** khi bản gốc nêu lý do. Không tự bịa lý do bản gốc không có.
- Thứ tự: tóm tắt → vì sao → cách hoạt động → chi tiết kỹ thuật.
- Tên hàm, class, lệnh SQL, header HTTP, cấu hình, câu lệnh shell dồn vào phần **Chi tiết kỹ thuật** của mục đó.
- Danh sách lồng tối đa hai cấp.
- Test case: "Kiểm tra điều gì", "Chuẩn bị", "Các bước". Mỗi bước tách thao tác và dòng "Mong đợi:". Bước cần evidence ghi "📷 Chụp evidence."
- Giữ heading của bản gốc làm khung; được đổi chữ trong heading cho dễ hiểu nhưng phải giữ mã trong heading (ví dụ `### R-AUT-06: Giới hạn số lần đăng nhập sai`).

## Câu chữ

- Mỗi câu một ý. Câu có chủ ngữ và động từ.
- Không dùng ký hiệu thay chữ trong câu văn: không "→", "≈", "…", "=" để nối ý. Ký hiệu vẫn giữ nguyên trong `code` và trong câu nguyên văn.
- Tên biến không chen vào câu tiếng Việt; nếu cần thì đưa xuống Chi tiết kỹ thuật.
- Văn phong khách quan, không xưng "bạn" trong tài liệu thiết kế, review, quyết định. Hướng dẫn thao tác (bước test) được dùng câu mệnh lệnh ("Mở…", "Nhập…").
- Giữ thuật ngữ tiếng Anh kỹ sư Việt quen dùng: `transaction`, `cookie`, `request`, `deploy`, `commit`, `migration`… Không dịch tên môi trường (`production`, `staging`).
- Unicode NFC; một kiểu bỏ dấu trong cả tài liệu (kiểu mới: `hoà`, `thuỷ`).

## Bất biến (script `build` kiểm tra)

- Giữ nguyên mọi **mã**: `R-AUT-06`, `P0-AUT-012`, `P0-ISS-003`, `T06`, `RV-03`, `ADR 0015`, "câu hỏi mở 7". Khoảng mã như `R-AUT-01 … R-AUT-04` được giữ nguyên hoặc viết đủ từng mã.
- Giữ nguyên mọi **con số**, viết bằng chữ số ("5 lần", không "năm lần").
- Giữ nguyên văn mọi **chuỗi trong ngoặc kép** (thông báo lỗi, nhãn nút) và mọi đoạn **`code`**.
- Giữ nguyên mọi **đường dẫn file** và **URL**.
- Không thêm thông tin bản gốc không có.
- Không tự chú thích ý nghĩa của mã: script chèn phần *(ý nghĩa)* sau mã.

## Quy tắc riêng của bản viết lại

- Giữ nguyên mọi dòng marker `<!-- src-section: … -->`. Chỉ thay phần thân của khối có dòng `<!-- TODO: viết lại mục này -->`, rồi xóa dòng TODO đó.
- Không đụng vào khối không có dòng TODO.
- Giữ nguyên viết tắt của tài liệu (`<api>`, `<psql> "…"`, `<id mio>`…); script triển khai chúng thành giá trị đầy đủ.
- Không chép lại danh sách định nghĩa viết tắt (các dòng dạng `` `<tên>` = `<giá trị>` ``); bản đọc không cần danh sách này.

## Ví dụ

Bản gốc:

```markdown
- R-AUT-06: Giới hạn đăng nhập sai, tính theo tên đăng nhập đã chuẩn hóa (cả tên không tồn tại, để không lộ tên nào có thật):
  - 5 lần sai trong cửa sổ 15 phút (tính từ lần sai đầu của cửa sổ) → khóa 15 phút; lần sai thứ 5 trả ngay 429;
```

Bản viết lại:

```markdown
### R-AUT-06: Giới hạn số lần đăng nhập sai

**Tóm tắt.** Một tên đăng nhập bị nhập sai mật khẩu 5 lần trong vòng 15 phút thì bị khóa 15 phút.

**Vì sao.** Để chặn việc đoán mật khẩu bằng cách thử liên tục. Bộ đếm áp dụng cả với tên đăng nhập không tồn tại, nên người dò không biết được tên nào có thật.

**Cách hoạt động**
- Khoảng 15 phút bắt đầu tính từ lần sai đầu tiên. Ở lần sai thứ 5, tên đăng nhập bị khóa và người dùng nhận lỗi 429 ngay ở lần đó.
```
