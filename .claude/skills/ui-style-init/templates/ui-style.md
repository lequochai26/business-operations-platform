# Style UI – Tiệm Nhà Mio

Nguồn chính về style của toàn hệ thống. `ui-tokens.css` được sinh từ khối `## Tokens` bằng `py tools/ui/gen_tokens.py`. Không sửa tay `ui-tokens.css`.

## Nguyên tắc

- Nền tảng hiện tại: web trên máy tính (khung chuẩn 1440×900). Responsive và app native làm sau, nên token đặt tên độc lập nền tảng.
- Giao diện vận hành: ưu tiên dễ đọc, dễ quét danh sách, trạng thái rõ ràng. Nhận diện của tiệm thể hiện ở màu, không ở trang trí.
- Mọi giá trị lấy từ token. Không viết cứng màu, cỡ chữ, khoảng cách.

## Tokens

```yaml
color:
  brand:
    primary: '#8FA284'
    primary-strong: '#4E6045'
    cream: '#FAF7F0'
  text:
    default: '#2B2B2B'
    muted: '#6B6B6B'
    on-primary: '#FFFFFF'
  surface:
    page: '#FAF7F0'
    card: '#FFFFFF'
    border: '#E2DED3'
  status:
    success: '#3C7A4A'
    warning: '#B7791F'
    danger: '#B23A3A'
    info: '#3B6E8F'
font:
  family:
    heading: "'Playfair Display', Georgia, serif"
    body: "'Be Vietnam Pro', system-ui, sans-serif"
    decorative: "'Dancing Script', cursive"
  size:
    xs: 12px
    sm: 14px
    md: 16px
    lg: 20px
    xl: 24px
    xxl: 32px
  weight:
    regular: '400'
    medium: '500'
    bold: '700'
line-height:
  tight: '1.25'
  normal: '1.5'
space:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
radius:
  sm: 4px
  md: 8px
  lg: 16px
  pill: 999px
shadow:
  card: 0 1px 3px rgba(0, 0, 0, 0.08)
  overlay: 0 8px 24px rgba(0, 0, 0, 0.16)
breakpoint:
  mobile: 480px
  tablet: 768px
  desktop: 1280px
```

## Typography

- Tiêu đề trang: `font-family-heading`, `font-size-xxl`.
- Tiêu đề khối: `font-family-body`, `font-size-lg`, `font-weight-bold`.
- Nội dung: `font-family-body`, `font-size-md`, `line-height-normal`.
- Chú thích, nhãn phụ: `font-size-sm`, `color-text-muted`.
- `font-family-decorative` chỉ dùng cho logo hoặc trang trí, không dùng cho chữ cần đọc.

## Bố cục và breakpoint

- Khung chuẩn 1440×900: thanh điều hướng trái, nội dung tối đa 1200px.
- Lưới khoảng cách theo bội số `space-sm`.
- Breakpoint định nghĩa sẵn cho giai đoạn responsive; hiện chưa thiết kế giao diện dưới `breakpoint-desktop`.

## Component cơ bản

- **Nút:** biến thể `primary` (nền `color-brand-primary-strong`), `secondary` (viền), `danger`, `ghost`; trạng thái bình thường, hover, focus, disabled, loading.
- **Ô nhập:** text, số, chọn, giờ; trạng thái bình thường, focus, lỗi (viền và chữ `color-status-danger`, thông báo ngay dưới ô), disabled.
- **Thẻ:** nền `color-surface-card`, bo `radius-md`, bóng `shadow-card`.
- **Thông báo:** success, warning, danger, info; dạng banner trong trang và toast.
- **Badge:** dùng cho trạng thái; màu theo nhóm `color-status`.

## Trạng thái tương tác

- Focus luôn nhìn thấy được (viền 2px `color-brand-primary-strong`).
- Disabled: giảm độ đậm, con trỏ `not-allowed`, không đổi bố cục.
- Loading: giữ kích thước nút, hiện vòng xoay.

## Khả năng truy cập

- Tương phản chữ thường tối thiểu 4.5:1, chữ lớn 3:1.
- Vùng bấm tối thiểu 32×32px trên máy tính (44×44px khi làm responsive).
- Không truyền đạt trạng thái chỉ bằng màu: badge luôn có chữ.

## Lịch sử thay đổi

- <YYYY-MM-DD>: tạo mới
