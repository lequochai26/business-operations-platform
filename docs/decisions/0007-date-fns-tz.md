# 0007 – date-fns + @date-fns/tz cho xử lý ngày giờ

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước › Test tự động (Đồng hồ, Ngày giờ); docs/project/04-technical.md mục 3, 8

## Bối cảnh

Nghiệp vụ nhiều phép tính ngày giờ: tìm khung trống, chống trùng lịch, quy đổi ngày tương đối ("mai", "T3", "tối nay"), giờ nghỉ của phanh an toàn. Mọi lịch dùng múi giờ `Asia/Ho_Chi_Minh`. Đồng hồ phải truyền vào qua `Clock`.

## Các phương án

### A. date-fns + @date-fns/tz
- Ưu: hàm thuần, tree-shake; dùng `Date` gốc nên hợp với `Clock` và Drizzle.
- Nhược: API múi giờ hơi rời rạc.

### B. Luxon
- Ưu: `DateTime` bất biến, múi giờ rõ ràng.
- Nhược: phải chuyển qua lại với `Date` ở biên DB và `Clock`.

### C. Temporal (polyfill)
- Ưu: chuẩn tương lai, chính xác nhất.
- Nhược: polyfill nặng; Drizzle, zod chưa hỗ trợ sẵn.

## Quyết định

Chọn A. Múi giờ lấy từ hằng `APP_TIME_ZONE = 'Asia/Ho_Chi_Minh'`; DB lưu `timestamptz`.

## Hệ quả

- Được: một kiểu `Date` xuyên suốt từ `Clock` tới DB.
- Mất / rủi ro: `Date` thay đổi được (mutable), phải dùng hàm date-fns thay vì sửa trực tiếp; khi Temporal phổ biến có thể cần chuyển.
