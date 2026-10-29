# 0004 – Tên nhánh, commit message và cách merge

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước › Nhánh và commit; skill implement-task, bug-fix, change-request, review-code

## Bối cảnh

`review-code` suy ra task từ tên nhánh. Lịch sử `main` cần tra được theo task và vấn đề. Repo đã dùng Conventional Commits tiếng Anh.

## Các phương án

### Tên nhánh

#### A. `phase-<N>/t<nn>-<slug>`, `phase-<N>/fix-p<N>-iss-<nnn>`, `phase-<N>/cr-<slug>`
- Ưu: khớp sẵn với các skill; gom nhánh theo giai đoạn.
- Nhược: không lộ loại thay đổi (feat/fix) ở nhánh task.

#### B. `feat/phase-<N>-t<nn>-<slug>`, `fix/phase-<N>-p<N>-iss-<nnn>`
- Ưu: loại thay đổi thấy ngay ở tên.
- Nhược: phải sửa ví dụ trong các skill.

### Commit message

#### A. Conventional Commits, tiếng Anh
- Ưu: giống lịch sử hiện có, công cụ hiểu được.
- Nhược: chủ tiệm khó đọc.

#### B. Conventional Commits, tiếng Việt
- Ưu: dễ đọc với chủ tiệm.
- Nhược: lệch với commit cũ.

### Merge

#### A. Squash merge
- Ưu: mỗi task là một commit trên `main`, dễ revert theo task.
- Nhược: mất lịch sử đỏ → xanh chi tiết trên `main`.

#### B. Merge commit (`--no-ff`)
- Ưu: giữ đủ commit TDD.
- Nhược: lịch sử `main` dài và rối.

#### C. Rebase + fast-forward
- Ưu: lịch sử thẳng, giữ commit.
- Nhược: revert cả task phải revert nhiều commit.

## Quyết định

Tên nhánh A, commit A, merge A. Commit và PR không chứa dòng `Co-Authored-By` hay bất kỳ dấu vết Claude nào (yêu cầu của người dùng). Tiêu đề commit squash kèm mã task hoặc mã vấn đề.

## Hệ quả

- Được: tra commit theo task/vấn đề; revert theo task bằng một lệnh.
- Mất / rủi ro: lịch sử chi tiết chỉ còn trên nhánh, mất khi xóa nhánh.
