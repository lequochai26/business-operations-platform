<!-- src-section: 0b0fa0b228 3706e44f93c1 -->
# 0007 – date-fns + @date-fns/tz cho xử lý ngày giờ

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan:
  - CLAUDE.md mục Quy ước › Test tự động (Đồng hồ, Ngày giờ);
  - docs/project/04-technical.md mục 3, 8.

**Tóm tắt.** Xử lý ngày giờ dùng date-fns và @date-fns/tz. Lý do là hai thư viện này dùng `Date` gốc, nên một kiểu `Date` đi xuyên suốt từ `Clock` tới DB.

<!-- src-section: 0bc81167ac a1b6ffdc225f -->
## Bối cảnh

Nghiệp vụ có nhiều phép tính ngày giờ:
- tìm khung trống;
- chống trùng lịch;
- quy đổi ngày tương đối như "mai", "T3", "tối nay";
- giờ nghỉ của phanh an toàn.

Mọi lịch dùng múi giờ `Asia/Ho_Chi_Minh`. Đồng hồ phải được truyền vào qua `Clock`.

<!-- src-section: 1be8f16534 d5428cea36cd -->
## Các phương án

<!-- src-section: 3b426ad02d 4ffd88c87a14 -->
### A. date-fns và @date-fns/tz

**Ưu**

- Hàm thuần, tree-shake được.
- Dùng `Date` gốc nên hợp với `Clock` và Drizzle.

**Nhược**

- API múi giờ hơi rời rạc.

<!-- src-section: 3f43e9347e fdda94567616 -->
### B. Luxon

**Ưu**

- `DateTime` bất biến.
- Múi giờ rõ ràng.

**Nhược**

- Phải chuyển qua lại với `Date` ở biên DB và ở `Clock`.

<!-- src-section: 8a42b0cfc6 8e77a6534b20 -->
### C. Temporal (polyfill)

**Ưu**

- Là chuẩn của tương lai và chính xác nhất.

**Nhược**

- Polyfill nặng.
- Drizzle và zod chưa hỗ trợ sẵn.

<!-- src-section: 254160d409 0d838070b020 -->
## Quyết định

Chọn phương án A. Múi giờ lấy từ một hằng số dùng chung. DB lưu thời gian kiểu `timestamptz`.

**Chi tiết kỹ thuật**

- Hằng múi giờ: `APP_TIME_ZONE = 'Asia/Ho_Chi_Minh'`.

<!-- src-section: 58c5fdb1ed 4a0ad6be04a8 -->
## Hệ quả

**Được**

- Một kiểu `Date` dùng xuyên suốt từ `Clock` tới DB.

**Mất và rủi ro**

- `Date` thay đổi được (mutable), nên phải dùng hàm của date-fns thay vì sửa trực tiếp.
- Khi Temporal phổ biến thì có thể cần chuyển sang.
