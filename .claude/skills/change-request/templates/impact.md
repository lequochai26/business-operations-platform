# Phân tích ảnh hưởng – <tóm tắt thay đổi>

- Ngày: <YYYY-MM-DD>
- Nguồn: <người dùng | feedback P<N>-ISS-<nnn> | bug-fix>
- Thay đổi: <trước> → <sau>
- Lý do: <…>
- Trạng thái tính năng sẽ lùi về: <slug>: <trạng thái>

## 1. Tài liệu khái quát (`docs/project/`)
- <file, mục>: <sửa gì> | không ảnh hưởng

## 2. Thiết kế tính năng
- <docs/phases/phase-N/design/<slug>.md, mục, R-…>: <sửa gì>

## 3. Thiết kế dùng chung (`docs/design/`)
- db-schema.md: <…> | không ảnh hưởng
- api/<resource>.md + openapi.yaml: <…> | không ảnh hưởng
- ui-style.md / components / ui: <…> | không ảnh hưởng

## 4. Test case và traceability
- <mã case>: <sửa | bỏ | thêm mới>

## 5. Kế hoạch code (`plan.md`)
- Task mới: <T.. tiêu đề>

## 6. Code và test
- <file/module>: <thay đổi> (làm qua /implement-task <T..>)
