---
name: component-design
description: Thiết kế component giao diện dùng chung, gắn với nghiệp vụ (ví dụ StatusBadge, ApprovalCard, SlotPicker) dưới dạng Web Component để mọi mockup nhúng lại. Được ui-design gọi khi một phần giao diện xuất hiện ở từ 2 màn hình trở lên, hoặc gọi tay. Use to design a reusable UI component.
argument-hint: "<TênComponent dạng PascalCase>"
---

# component-design

## Mục đích

Thiết kế một component dùng chung một lần, để mọi màn hình nhúng lại thay vì chép code; sửa component thì mọi mockup đổi theo.

## Điều kiện tiên quyết

- Đã có `docs/design/ui-style.md` và `docs/design/ui-tokens.css`.
- Phân vai: component cơ bản (nút, ô nhập, thẻ, thông báo, badge cơ bản) thuộc `ui-style.md`, không thiết kế ở đây. Skill này chỉ lo component ghép, gắn với nghiệp vụ.

## Input

- Tham số: tên component PascalCase. File dùng kebab-case (`StatusBadge` → `status-badge`), thẻ custom element `mio-<kebab>`.
- Nhu cầu từ `ui-design` (nếu được gọi): màn hình nào, dùng làm gì, cần hiện dữ liệu gì.
- `docs/design/ui-style.md`, `docs/design/ui-tokens.css`.
- `docs/design/components/index.md` (tạo từ `templates/components-index.md` nếu chưa có).

## Các bước

1. **Tra danh mục trước.** Đọc `docs/design/components/index.md` và các file component liên quan.
   - Có component phù hợp: dùng lại, hoặc thêm biến thể vào component đó (sửa file `.md`, `.js`, `.html` hiện có). Bỏ qua bước 2–3.
   - Chưa có: thiết kế mới.
2. Viết `docs/design/components/<kebab>.md` theo `templates/component.md`.
3. Viết `docs/design/components/<kebab>.js` theo `templates/component.js`:
   - class kế thừa `HTMLElement`, đăng ký thẻ `mio-<kebab>`;
   - đọc thuộc tính `variant`, `state` và các thuộc tính trong `.md`;
   - style chỉ dùng `var(--...)` từ `ui-tokens.css`;
   - nạp bằng `<script src>` thường, **không** dùng `type="module"` (Chromium chặn module khi mở bằng `file://`).
4. Viết `docs/design/components/<kebab>.html` theo `templates/component-gallery.html`: mọi biến thể × trạng thái.
5. Chụp: `py tools/ui/screenshot.py docs/design/components/<kebab>.html --out docs/design/components/screenshots`.
6. Cập nhật `docs/design/components/index.md` và mục `## Màn hình đang dùng` của component.
7. Nếu **sửa** component đang được dùng: đọc `## Màn hình đang dùng`, chụp lại ảnh từng màn hình đó (`py tools/ui/screenshot.py docs/design/ui/<màn hình> --out docs/design/ui/<màn hình>/screenshots`), liệt kê cho người dùng.

## Điểm dừng

Trước mỗi điểm dừng và trước báo cáo kết thúc: gọi `reader-view` cho các file trong `docs/` vừa ghi, gửi kèm link bản đọc Markdown và HTML.

- Component mới: người dùng duyệt ảnh gallery.
- Sửa component đang được dùng: người dùng duyệt thay đổi **trước** khi chụp lại các màn hình bị ảnh hưởng.

## Output

- `docs/design/components/<kebab>.md`, `.js`, `.html` và ảnh trong `docs/design/components/screenshots/` (ví dụ `.js`: `templates/example-status-badge.js`).
- `docs/design/components/index.md` đã cập nhật.

## Tự kiểm tra

- Không trùng chức năng với component đã có trong danh mục.
- `.js` không có mã màu, cỡ chữ, khoảng cách viết cứng.
- Gallery có đủ mọi biến thể và trạng thái ghi trong `.md`.
- Ảnh chụp hiển thị đúng (mở được bằng `file://`, không lỗi script).

## Cập nhật status.md

Không đổi trạng thái tính năng (component là một phần của bước UI).

## Báo cáo kết thúc

- Component đã tạo/sửa, các màn hình bị ảnh hưởng (nếu sửa).
- Cần người dùng quyết: duyệt component.
- Link bản đọc của các file vừa ghi.
- Bước tiếp theo: quay lại `/ui-design <slug>` đang làm dở.
