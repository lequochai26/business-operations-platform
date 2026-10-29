# Checklist – review-code

## Đúng và đủ
- [ ] Làm đúng và đủ task: mọi `R-…` được gắn với task đã được hiện thực.
- [ ] Giá trị, thông báo lỗi, mã lỗi khớp nguyên văn thiết kế.
- [ ] Không có thay đổi ngoài phạm vi task mà không có lý do.

## Khớp thiết kế dùng chung
- [ ] Migration khớp `docs/design/db-schema.md` (bảng, cột, kiểu, null, mặc định, ràng buộc, index).
- [ ] Endpoint khớp `docs/design/api/openapi.yaml` (path, method, request, response, mã lỗi).
- [ ] UI khớp mockup; chỉ dùng biến từ `ui-tokens.css`; dùng component dùng chung thay vì viết lại.

## Test
- [ ] Mọi hành vi mới có test; test assert trên hành vi thật, không trên mock.
- [ ] Logic thời gian dùng đồng hồ truyền vào.
- [ ] Ràng buộc DB, hàng đợi có integration test với dịch vụ thật trong Docker.
- [ ] Không có test skip mà không in lý do; không báo pass khi thiếu fixture.

## Quy ước
- [ ] Đặt tên, cấu trúc thư mục, commit message theo `CLAUDE.md` mục `## Quy ước`.
- [ ] Lint, typecheck sạch.

## Lỗi và bảo mật
- [ ] Mọi lỗi từ bên ngoài (mạng, Facebook, Gemini, DB) được xử lý theo thiết kế, không nuốt lỗi.
- [ ] Không lộ secret (token, khóa API) trong code, log, test, fixture.
- [ ] Không log dữ liệu cá nhân của khách.
- [ ] Phân quyền kiểm tra ở API, không chỉ ẩn trên giao diện.

## Lằn ranh đỏ
- [ ] Không có đường nào để luồng tự động tạo hai lịch hẹn chồng nhau.
- [ ] Retry không thể gây comment, tin nhắn hay bài đăng trùng (kiểm tra đã tồn tại trước khi thử lại).
- [ ] AI không tự sinh giá, giờ, địa chỉ: mọi con số trong nội dung gửi ra lấy từ nguồn thật và được kiểm tra.
- [ ] Có tự dừng và cảnh báo khi phát hiện checkpoint, hết phiên, bị chặn.
