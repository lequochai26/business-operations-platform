<!-- src-section: 0b0fa0b228 12cad558ba29 -->
# 0004 – Tên nhánh, commit message và cách merge

- Ngày: 2026-10-29
- Trạng thái: chấp nhận
- Liên quan: CLAUDE.md mục Quy ước › Nhánh và commit; skill implement-task, bug-fix, change-request, review-code

**Tóm tắt.** Tên nhánh được gom theo giai đoạn, commit message theo Conventional Commits tiếng Anh, và nhánh được squash merge vào `main`. Cách này khớp với các skill hiện có và cho phép tra cứu, revert theo task hoặc theo vấn đề.

<!-- src-section: 0bc81167ac dccae680260a -->
## Bối cảnh

Bước `review-code` suy ra task từ tên nhánh. Lịch sử `main` cần tra được theo task và theo vấn đề. Repo đã dùng Conventional Commits viết bằng tiếng Anh.

<!-- src-section: 1be8f16534 d5428cea36cd -->
## Các phương án

<!-- src-section: f1a17b4da1 d16ed45e0425 -->
### Tên nhánh

#### A. Gom nhánh theo giai đoạn

Các mẫu tên: `phase-<N>/t<nn>-<slug>`, `phase-<N>/fix-p<N>-iss-<nnn>`, `phase-<N>/cr-<slug>`.

**Ưu**

- Khớp sẵn với các skill.
- Nhánh được gom theo giai đoạn.

**Nhược**

- Tên nhánh task không cho thấy loại thay đổi (feat hay fix).

#### B. Đặt loại thay đổi ở đầu tên nhánh

Các mẫu tên: `feat/phase-<N>-t<nn>-<slug>`, `fix/phase-<N>-p<N>-iss-<nnn>`.

**Ưu**

- Thấy ngay loại thay đổi qua tên nhánh.

**Nhược**

- Phải sửa ví dụ trong các skill.

<!-- src-section: 1f0266541c 5bf27c32038b -->
### Commit message

#### A. Conventional Commits, tiếng Anh

**Ưu**

- Giống lịch sử hiện có.
- Công cụ hiểu được định dạng này.

**Nhược**

- Chủ tiệm khó đọc.

#### B. Conventional Commits, tiếng Việt

**Ưu**

- Chủ tiệm dễ đọc.

**Nhược**

- Lệch với các commit cũ.

<!-- src-section: 682ab10801 833e8f3667cf -->
### Merge

#### A. Squash merge

**Ưu**

- Mỗi task là một commit trên `main`, dễ revert theo task.

**Nhược**

- Trên `main` mất lịch sử chi tiết của các bước từ đỏ sang xanh.

#### B. Merge commit (`--no-ff`)

**Ưu**

- Giữ đủ các commit TDD.

**Nhược**

- Lịch sử `main` dài và rối.

#### C. Rebase rồi fast-forward

**Ưu**

- Lịch sử thẳng mà vẫn giữ commit.

**Nhược**

- Muốn revert cả task thì phải revert nhiều commit.

<!-- src-section: 254160d409 4648410281ed -->
## Quyết định

- Tên nhánh theo phương án A.
- Commit message theo phương án A.
- Merge theo phương án A (squash merge).

Commit và PR không chứa dòng `Co-Authored-By` hay bất kỳ dấu vết Claude nào. Đây là yêu cầu của người dùng. Tiêu đề commit squash kèm mã task hoặc mã vấn đề.

<!-- src-section: 58c5fdb1ed 34368ac7d8b1 -->
## Hệ quả

**Được**

- Tra được commit theo task hoặc theo vấn đề.
- Revert một task chỉ cần một lệnh.

**Mất và rủi ro**

- Lịch sử chi tiết chỉ còn trên nhánh và mất khi xoá nhánh.
