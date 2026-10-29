# Checklist – test-case-design

- [ ] Mọi `R-<ABC>-nn` của tính năng có ít nhất một case trong `traceability.md`.
- [ ] Đã xét đủ 12 khía cạnh trong `docs/testing/viewpoints.md`; khía cạnh không áp dụng có lý do.
- [ ] Mọi trường/tham số có khoảng giá trị có case dưới biên, đúng biên, trên biên, sai kiểu, rỗng.
- [ ] Mọi bước chuyển trạng thái hợp lệ có case; có case cho bước chuyển không hợp lệ quan trọng.
- [ ] Mọi vai trò không có quyền có case truy cập thẳng bằng URL và bằng API.
- [ ] Có case thao tác đồng thời (hai tab hoặc hai người) cho thao tác sửa/xóa.
- [ ] Có case phiên hết hạn hoặc mất cookie giữa chừng.
- [ ] Có case dữ liệu bất thường trong DB (bản ghi bị xóa, giá trị lạ) cho màn hình đọc dữ liệu.
- [ ] Có case cho phía Facebook/Messenger nếu tính năng có tích hợp.
- [ ] Mọi lằn ranh đỏ liên quan tới tính năng có case `Regression: có`.
- [ ] Mỗi bước có kết quả mong đợi cụ thể (thông báo nguyên văn, giá trị DB, trạng thái hiển thị).
- [ ] Bước cần evidence có `[evidence]`.
- [ ] Không có case đòi can thiệp vào luồng xử lý của code.
- [ ] Mã case liên tục, không trùng, đúng dạng `P<N>-<ABC>-<nnn>`.
