---
type: srs
feature: qdgctkh-bo-sung
goi_dev: qdgctkh
status: dang-review
updated: 2026-09-04
nguon:
  - docs/cuc-ql/srs/srs-qdgctkh-nam.md
  - docs/cuc-ql/brainstorming/brainstorm-qdgctkh-bo-sung.md
  - docs/cuc-ql/user-flow/userflow-qdgctkh-bo-sung.md
  - docs/cuc-ql/srs/srs-nhap-kho.md
  - docs/cuc-ql/srs/srs-bang-gia.md
  - docs/ngoai-giao/srs/srs-de-nghi-spmm.md
  - docs/reference/TongHop_DuAn_QLSPMM.md
---

# Đặc tả: Quyết định giao chỉ tiêu kế hoạch bổ sung (QĐGCTKH bổ sung)

**Figma:** file **BCY(2)** · Page 1 · khu vực 5 — **12 màn**, đánh số `BS 01`–`BS 10`, khung 1440.

> Quyết định bổ sung **dùng chung phần lớn đặc tả với quyết định năm**. Tài liệu này chỉ viết **những chỗ khác**; mọi thứ không nhắc tới thì đọc [`srs-qdgctkh-nam.md`](srs-qdgctkh-nam.md). Kết quả sau khi ban hành xem ở ba tab của quyết định năm, đặc tả tại `srs-qdgctkh-nam.md` Mục 5.12–5.14.

## 1. Phạm vi

Quyết định bổ sung **đổi chỉ tiêu đã giao** của một QĐGCTKH năm đã ban hành: thêm SPMM chưa có trong kế hoạch năm, tăng hoặc giảm số lượng của SPMM đã có, chuyển chỉ tiêu từ hệ này sang hệ khác.

Quyết định năm **không bị sửa** — nó đã đóng băng. Quyết định bổ sung là một văn bản riêng, mang các **dòng điều chỉnh có dấu**; phần mềm cộng dồn để ra *số hiện hành*.

**Đơn vị tính** là thuộc tính của SPMM trong danh mục SPMM — một SPMM một đơn vị tính, giống quyết định năm. ⚠️ Cách đếm một SPMM dạng *Hệ thống* (một hệ thống là một, hay tách theo từng thiết bị thành phần) **chưa chốt**; tài liệu này không chốt thay.

### 1.1 Bản triển khai

| Việc | Chạy ở bản |
|---|---|
| Lập · sửa · nhập số điều chỉnh và đơn giá · xuất phụ lục · ban hành · xoá | **Cục QL** |
| Xem quyết định bổ sung **đã ban hành**, và xem số hiện hành trên quyết định năm | **Cục QL và các cơ yếu đầu hệ**, phạm vi dữ liệu theo `srs-qdgctkh-nam.md` Mục 3.1 |

Quyết định bổ sung ở trạng thái *Mới* chỉ tồn tại trên bản Cục QL. Sau khi ban hành thì đi xuống các bản hệ qua đồng bộ định kỳ.

### 1.2 Ba văn bản, ba việc khác nhau

Ba loại văn bản, mỗi loại một việc:

| | **QĐGCTKH năm** | **QĐGCTKH bổ sung** | **QĐTK** |
|---|---|---|---|
| Trả lời câu | Năm nay giao bao nhiêu, cho những đâu | Đổi con số đã giao | Chuyển chỗ số đã có |
| Nguồn hàng | — | **Không có** — đổi chỉ tiêu trên giấy | Kho của **chính hệ đó**, hoặc **kho Cục QLKTNVMM** |
| Tổng của một hệ | Đặt ra | **Đổi được** | Không đổi (nguồn nội hệ) · **Tăng** (nguồn kho Cục QL) |
| Tổng toàn ngành | Đặt ra | **Đổi được** | **Không bao giờ đổi** |
| Chuyển giữa hai hệ | — | **Được** | **Cấm** |
| Phạm vi một văn bản | Toàn ngành | Toàn ngành | Đúng **một** cơ yếu đầu hệ |

**QĐTK chỉ chuyển chỗ hàng đã có. Quyết định bổ sung mới đổi tổng.**

Hai trường hợp đều là QĐTK:

1. Địa điểm A cần hàng, **kho của chính cơ yếu đầu hệ đó còn** → lấy từ đó. Tổng của hệ **không đổi**.
2. Địa điểm A cần hàng, **hệ hết, kho Cục QLKTNVMM còn** → Cục QL xuất cho hệ. Cột *Cục QLKTNVMM — Dự phòng* giảm, cột của hệ tăng, **tổng toàn ngành giữ nguyên**.

Lấy hàng **từ hệ khác** không phải QĐTK — phải lập quyết định bổ sung trước.

QĐTK **ngoài phạm vi tài liệu này**; ở đây chỉ ghi phần QĐTK chảy ngược lên số hiện hành.

### 1.3 Số hiện hành

> **`số hiện hành` của một cặp `SPMM × địa điểm triển khai × năm` = số của quyết định năm **+** tổng mọi dòng điều chỉnh có dấu của **các văn bản đã ban hành** cùng năm đó.**

- Nguồn dòng điều chỉnh: **quyết định bổ sung** và **QĐTK**. Văn bản còn *Mới* **không tính**.
- **Khoá tham chiếu là cặp `SPMM × địa điểm × năm`**, không phải "dòng thứ mấy của văn bản nào". Người lập không phải nhớ dòng đang hiệu lực nằm ở văn bản nào; SPMM chưa có trong kế hoạch năm thì tra ra `0`.
- **Cộng dồn khi xem, không lưu.** Không có cờ *Hiệu lực* hay *Đã bị thay thế* ở mức dòng — cờ thuộc mô hình *thay thế*, loại trừ với mô hình *cộng dồn*.
- Số hiện hành là căn cứ của **phiếu điều chuyển** và **phiếu cấp phát**; hai loại phiếu đó trỏ vào **quyết định năm**, không trỏ vào quyết định bổ sung hay QĐTK nào.

### 1.4 Tiền

**Tiền gắn với từng văn bản.** Mỗi quyết định giữ đơn giá và thành tiền của riêng nó, đóng băng theo văn bản đó.

Đơn giá đổi giữa các thời điểm — có thể điều chỉnh giá, hoặc SPMM thêm mới ở một quyết định bổ sung lấy giá tại lúc đó. Tab *Kế hoạch hiện hành* của quyết định năm vì thế **ẩn cột *Đơn giá*, chỉ để *Thành tiền*** — *Thành tiền* cộng được vì mỗi văn bản đã nhân xong theo giá của chính nó. Nghiệp vụ điều chỉnh đơn giá làm sau.

### 1.5 Ngoài phạm vi

- **QĐTK** — tầng triển khai, làm ở đợt riêng.
- **Điều chỉnh chỉ đơn giá, không đổi số lượng.**
- Lập công văn, trình ký, ký số, phê duyệt pháp lý — nằm ở **eOffice** của từng đơn vị.
- Quản lý ngân sách, đối soát với Vụ Tài chính. Kinh phí trong quyết định **chỉ là con số ghi nhận**, không có luật chặn nào quanh tiền.

### 1.6 Hai số hiệu

Giống quyết định năm (`srs-qdgctkh-nam.md` Mục 1.3), khác **tiền tố** và **dải đếm**:

| Tên | Định dạng | Bắt buộc |
|---|---|---|
| ***Số phiếu*** | `QĐGCTKH-BS/<mã đơn vị>/<năm>/<4 số>` | Luôn có, sinh khi *Lưu* lần đầu |
| ***Số QĐGCTKH*** | Theo số QĐ của Ban | Bắt buộc khi *Ban hành* |

Tiền tố `QĐGCTKH-BS` có **dải đếm riêng**, đếm lại từ `0001` mỗi năm và riêng theo từng đơn vị lập.

## 2. Quy trình nghiệp vụ

| # | Ai làm | Làm gì | Ở đâu |
|:--:|---|---|---|
| 1 | Đơn vị cấp N trong một hệ | Phát sinh nhu cầu thay đổi, gửi lên cấp trên trực tiếp N+1. Lặp lại tới **Cục cơ yếu đầu hệ** | Trên phần mềm hoặc bằng công văn ngoài phần mềm |
| 2 | Cục cơ yếu đầu hệ | Tổng hợp nhu cầu của toàn hệ gửi Cục QLKTNVMM. Ca **xin thêm** lập kèm phiếu đề nghị SPMM loại *Kế hoạch bổ sung* | Trên phần mềm (`srs-de-nghi-spmm.md`) hoặc bằng công văn ngoài phần mềm |
| 3 | Cục QLKTNVMM | Đối chiếu nhu cầu để chọn luồng. **Đổi địa điểm triển khai trong nội bộ hệ**, hoặc **hệ còn tồn kho**, hoặc **rút từ kho Cục QLKTNVMM** → chuyển sang luồng **QĐTK**, dừng ở đây. **Cần sản xuất hoặc mua thêm SPMM ngoài kế hoạch năm**, hoặc **tăng giảm số lượng giữa các hệ** → lập **QĐGCTKH bổ sung** | — |
| 4 | Cục QLKTNVMM | Tạo quyết định, chọn *Loại kế hoạch* là **Kế hoạch bổ sung** và *Năm áp dụng*. Chọn *Căn cứ QĐGCTKH năm*. Chọn phiếu đề nghị nếu có | `5.2` · `5.4` |
| 5 | Cục QLKTNVMM | Đưa các cặp `SPMM × địa điểm` cần điều chỉnh vào lưới, chọn *Tăng* hoặc *Giảm*, nhập *Số lượng điều chỉnh* | `5.2` · `5.5` |
| 6 | Phần mềm | Cộng lên *Phân bổ theo hệ — số thay đổi* và *Tổng hợp thay đổi toàn ngành*, gợi ý *Đơn giá* theo dấu của số ròng | `5.2` |
| 7 | Cục QLKTNVMM | Xuất phụ lục, trình ký ngoài phần mềm (Vụ Tài chính, rồi Lãnh đạo Ban) | `5.2` → eOffice |
| 8 | Cục QLKTNVMM | Đính kèm bản đã ký, nhập *Số QĐGCTKH* và *Ngày chứng từ*, bấm *Ban hành* | `5.2` · `5.9` |
| 9 | Phần mềm | Dòng điều chỉnh bắt đầu tính vào **số hiện hành** của quyết định năm, và quyết định bổ sung xuất hiện ở tab *Lịch sử điều chỉnh* | `srs-qdgctkh-nam.md` `5.12` · `5.14` |

Bước 7 và 8 dùng lại nguyên `BR-qdgctkh-005`, `BR-qdgctkh-006`, `NFR-qdgctkh-004` của quyết định năm.

## 3. Phân quyền

**Dùng nguyên Mục 3 của [`srs-qdgctkh-nam.md`](srs-qdgctkh-nam.md)** — phạm vi dữ liệu theo cây tổ chức, bốn quyền *Xem* · *Lập* · *Ban hành* · *Xoá*, bảng thao tác theo trạng thái. Quyết định bổ sung **không có quyền riêng**: tài khoản có quyền *Lập QĐGCTKH* thì lập được cả hai loại. Ánh xạ tên thao tác: *Sửa Thông tin chung* và *Sửa Số lượng cấp · thêm và xoá dòng chi tiết* của bảng đó đọc thành **sửa các ô ở `5.2` Thông tin chung** và **sửa lưới điều chỉnh, thêm và xoá dòng ở `5.2` `[21]`–`[24]`**.

Hai bảng *Phân bổ theo hệ — số thay đổi* và *Tổng hợp thay đổi toàn ngành* **chỉ hiện với Cục QLKTNVMM**, ẩn hoàn toàn với mọi đơn vị khác (`BR-qdgctkh-018`).

Quyết định còn *Mới* chỉ Cục QLKTNVMM thấy. Sau khi ban hành, các hệ thấy nhưng **chỉ dòng của đơn vị mình và cấp con**, không thấy hai bảng tổng hợp, **không sửa, không xoá** — quyết định là căn cứ để họ lập phiếu điều chuyển và phiếu cấp phát.

## 4. Vòng đời trạng thái

Hai trạng thái: ***Mới*** → ***Đã ban hành***. Không có nấc trung gian, không có đường lùi.

| Từ | Đến | Kích hoạt bằng | Điều kiện | Hệ quả |
|---|---|---|---|---|
| *(chưa có)* | ***Mới*** | *Lưu* lần đầu ở `5.2` | *Loại kế hoạch* · *Năm áp dụng* · *Căn cứ QĐGCTKH năm* · **ít nhất một dòng điều chỉnh**, và mọi dòng đủ *Loại điều chỉnh* + *Số lượng điều chỉnh* hợp lệ (`5.6`, `5.7`) | Sinh ***Số phiếu***. **Chưa tính vào số hiện hành** |
| ***Mới*** | ***Đã ban hành*** | *Ban hành* ở `5.2`, xác nhận ở `5.9` | **Chạy lại toàn bộ kiểm của *Lưu***, cộng ba mục *Số QĐGCTKH* · *Ngày chứng từ* · tệp bản đã ký, cộng **mọi dòng phải có *Đơn giá*** | Đóng băng hết (`NFR-qdgctkh-004`). **Dòng điều chỉnh bắt đầu tính vào số hiện hành.** Quyết định hiện ở tab *Lịch sử điều chỉnh* của quyết định năm |
| ***Mới*** | *(xoá hẳn)* | Icon xoá ở `5.1`, xác nhận ở `5.11` | — | Xoá bản ghi. Số hiện hành không đổi vì quyết định *Mới* chưa từng tính vào |

Quyết định bổ sung đã ban hành **không thu hồi, không thay thế, không xoá**. Sai thì lập quyết định bổ sung tiếp theo để bù trừ.

## 5. Màn hình

**12 mục**, đã vẽ đủ trên Figma. Mọi màn chạy ở **bản Cục QL**; riêng `5.12` chạy cả ở bản của các cơ yếu đầu hệ theo phạm vi dữ liệu ở Mục 1.1.

Lưới chi tiết dùng lại lưới của phiếu đề nghị SPMM — ba cách xem, hàng công cụ, hàng lọc trong lưới, hàng thêm nhanh, dòng đếm chân lưới. Hành vi từng thành phần đặc tả ở [`srs-de-nghi-spmm.md`](../../ngoai-giao/srs/srs-de-nghi-spmm.md); ở đây chỉ ghi chỗ khác.

### 5.1 Danh sách quyết định

**Figma:** [BS 01 · Danh sách quyết định](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1144-61511) · **Bước:** điểm vào · **Slug:** `danh-sach-qd`

> **Dùng chung một màn với quyết định năm** — `srs-qdgctkh-nam.md` `5.1`. Hai loại nằm chung một danh sách, phân biệt bằng cột *Loại kế hoạch*.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Loại kế hoạch | Text | Danh mục | Hai giá trị: *Kế hoạch năm* · ***Kế hoạch bổ sung***. Lọc được ở hàng lọc |
| 2 | Số phiếu | Link | Chuỗi | Dòng loại *Kế hoạch bổ sung* mang tiền tố `QĐGCTKH-BS`. **Bấm là XEM, không phải sửa** (`BR-qdgctkh-007`): dòng *Mới* mở `5.2` ở **chế độ chỉ xem**, trong đó có icon bút mở sang chế độ nhập; dòng *Đã ban hành* mở `5.12`. Vào thẳng chế độ nhập bằng **icon bút trên dòng** ở danh sách |
| 3 | Tạo QĐGCTKH | Button | — | Mở màn tạo với *Loại kế hoạch* mặc định *Kế hoạch năm*; đổi sang *Kế hoạch bổ sung* thì màn chuyển sang bố cục `5.2` |
| — | Các cột và thao tác còn lại | — | — | Y hệt `srs-qdgctkh-nam.md` `5.1`, không thêm cột nào cho loại bổ sung |

### 5.2 Lập / sửa quyết định bổ sung

**Figma:** [BS 02a · Lập QĐ bổ sung — Nhóm theo SPMM](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=834-540) · **Bước:** 4–8 · **Slug:** `qd-bs-nhap`

> Bốn khối gập xếp dọc: *Thông tin chung* · *Thông tin chi tiết* · *Phân bổ theo hệ — số thay đổi* · *Tổng hợp thay đổi toàn ngành*. Lưới chi tiết là nơi nhập; hai bảng dưới tự tính, chỉ có một ô nhập là *Đơn giá*.
>
> Màn có **hai chế độ**: **chỉ xem** (vào từ *Số phiếu* ở `5.1`; mọi ô khoá, icon bút chuyển sang chế độ nhập) và **nhập** (vào từ icon bút). Chế độ chỉ xem theo khuôn `srs-qdgctkh-nam.md` `5.2`; bản vẽ dưới đây là chế độ nhập.
>
> **Ba bảng đều nằm trong một khối gập có khung bao riêng**, tiêu đề khối đặt trong khung.

**Thông tin chung**

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Nhãn trạng thái | Tag | Danh mục | *Mới* cho tới khi ban hành |
| 2 | Số phiếu | Input (chỉ đọc) | Chuỗi | Hệ sinh khi *Lưu* lần đầu, dạng `QĐGCTKH-BS/<mã đơn vị>/<năm>/<4 số>` |
| 3 | Số QĐGCTKH | Textbox | Chuỗi | **Bắt buộc khi *Ban hành*, không bắt buộc khi *Lưu***. Còn *Mới* thì để trống, chữ mờ *"Nhập số quyết định"*. Thiếu lúc bấm *Ban hành* → tô đỏ ô và báo đỏ ngay dưới ô: *"Chưa có Số QĐGCTKH."* **Chặn** — xem `5.8` |
| 4 | Ngày chứng từ | Datepicker | Ngày | **Bắt buộc khi *Ban hành***. Thiếu lúc bấm *Ban hành* → *"Chưa có Ngày chứng từ."* **Chặn** |
| 5 | Loại kế hoạch | Dropdown | Danh mục | Bắt buộc. Giá trị ***Kế hoạch bổ sung***. Chỉ đổi được khi còn *Mới*; đổi thì bỏ hết dòng điều chỉnh, qua hộp thoại xác nhận như `srs-qdgctkh-nam.md` `5.11` |
| 6 | Năm áp dụng | Dropdown | Số | Bắt buộc. Năm kế hoạch được điều chỉnh, **không phải năm lập**. Cùng luật đổi giá trị với `[5]` |
| 7 | Căn cứ QĐGCTKH năm | Dropdown | Danh sách | **Bắt buộc, chọn đúng một quyết định.** Danh sách gồm các quyết định loại *Kế hoạch năm* **đã ban hành** của đúng *Năm áp dụng* ở `[6]`. **Không có luật chặn "một năm chỉ được một quyết định năm"** — có nhiều thì chọn ra một. Đây là quyết định mà số hiện hành được cộng vào. **Đổi *Năm áp dụng* thì ô này trống lại** (và dòng điều chỉnh đã bị bỏ theo `[6]`). **Đổi sang một quyết định năm khác cùng năm** thì cột *Số lượng cấp hiện tại* `[20]` và *Số lượng cấp sau điều chỉnh* `[23]` của mọi dòng tính lại theo quyết định mới, **dòng điều chỉnh giữ nguyên** |
| 8 | Phiếu đề nghị SPMM | Dropdown chọn nhiều | Danh sách | **Không bắt buộc** — không có dấu `*`. Chọn được **nhiều phiếu**, kể cả phiếu của các hệ khác nhau. Chưa chọn thì hiện chữ mờ *"Chưa chọn phiếu nào"*; đã chọn thì bày thành thẻ mang số phiếu. Danh sách lọc theo bốn điều kiện của `BR-qdgctkh-019`, với *Loại kế hoạch* là *Kế hoạch bổ sung*. Phiếu đã chọn đổ *Số đề nghị* vào cột `[19]` của đúng dòng tương ứng |
| 9 | Mô tả | Textarea | Chuỗi | Không bắt buộc. Nơi ghi số công văn căn cứ, ví dụ *"Điều chỉnh chỉ tiêu kế hoạch năm 2027 theo công văn số 214/CV-CYĐCQ ngày 03/03/2027"* |
| 10 | Tài liệu đính kèm | Button | Tệp | Nút kèm số đếm tệp. **Bắt buộc có tệp bản quyết định đã ký khi *Ban hành***. Thiếu → *"Chưa đính kèm bản quyết định đã ký."* **Chặn** |
| — | *Phương thức tạo* | — | — | **Không có ở loại bổ sung.** Quyết định bổ sung không phân biệt tạo từ phiếu hay tạo tay — ô *Phiếu đề nghị SPMM* luôn hiện và luôn không bắt buộc |

**Nút trên đầu màn**

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 11 | Xuất phụ lục | Button | — | Một tệp Excel theo khuôn 7 sheet của quyết định năm (`BR-qdgctkh-006`), khác ba chỗ. (1) **Chỉ chứa dòng có điều chỉnh.** (2) **Sheet *Phân bổ theo hệ* và 5 sheet chi tiết mỗi sheet có HAI BẢNG riêng** — *Bảng 1 — Điều chỉnh tăng* và *Bảng 2 — Điều chỉnh giảm*, mỗi bảng một hàng tiêu đề và số thứ tự riêng; **số trong bảng luôn dương**, chiều tăng hay giảm đọc ở tên bảng chứ không ở dấu của con số. Bảng nào không có dòng thì ghi *"Không có điều chỉnh tăng."* / *"Không có điều chỉnh giảm."*. (3) Sheet *Tổng hợp thay đổi toàn ngành* tách ba cột ***Tăng*** · ***Giảm*** (đều dương) · ***Chênh lệch***, rồi mới tới *Đơn giá* và *Thành tiền* — tiền tính trên chênh lệch nên hai cột này mang dấu. **Dùng được ngay ở *Mới***, lưu trước rồi mới xuất. **Không có hộp thoại chọn bản xuất** — quyết định bổ sung chỉ có một bản, khác quyết định năm (`srs-qdgctkh-nam.md` `5.15`). Khuôn mẫu `PhuLuc_QDGCTKH_BoSung_Mau.xlsx` **đang hoàn thiện, chưa giao kèm gói này** |
| 12 | Hủy | Button | — | Rời màn, bỏ thay đổi chưa lưu. Còn thay đổi chưa lưu thì hỏi lại trước khi rời |
| 13 | Lưu | Button | — | Lưu số liệu, giữ trạng thái *Mới*. Kiểm khi lưu: *Loại kế hoạch* · *Năm áp dụng* · *Căn cứ QĐGCTKH năm* · **có ít nhất một dòng điều chỉnh** · mọi dòng đủ *Loại điều chỉnh* và *Số lượng điều chỉnh*, số phải khác `0` (`5.6`) và không giảm dưới mốc đã nhập kho (`5.7`). Thiếu thì tô đỏ ô và báo đỏ ngay trong ô đó, con trỏ nhảy về ô đầu tiên, **chặn**. **Không kiểm *Số QĐGCTKH*, *Ngày chứng từ*, *Đơn giá* khi lưu** |
| 14 | Ban hành | Button | — | **Lưu phần đang sửa trước, rồi chạy lại toàn bộ kiểm của *Lưu***, rồi kiểm thêm: *Số QĐGCTKH* `[3]` · *Ngày chứng từ* `[4]` · tệp bản đã ký `[10]` · **mọi dòng ở bảng *Tổng hợp* phải có *Đơn giá*** `[26]`. Đủ hết thì mở `5.9`; thiếu bất kỳ mục nào thì tô đỏ tại chỗ, **không có hộp thoại và không có thông báo nổi** — xem `5.8` |

**Thông tin chi tiết — lưới điều chỉnh**

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 15 | Dải tab hệ | Tabs | — | Năm tab cố định: *Cơ yếu Đảng chính quyền* · *Cơ yếu Bộ Công an* · *Cơ yếu Quân đội* · *Cơ yếu Bộ ngoại giao* · *Cục QLKTNVMM*. Số trong ngoặc là **số dòng điều chỉnh của riêng tab đó**. Mở mặc định tab đầu. Mọi thao tác trên lưới áp cho tab đang mở |
| 16 | Xem theo | Dropdown | Danh mục | Ba cách xem: ***Nhóm theo SPMM*** (mặc định, mọi nhóm **thu gọn** khi mở màn) · *Nhóm theo địa điểm triển khai* · *Trải phẳng* (`5.3`). Đổi cách xem không đổi dữ liệu |
| 17 | Khung cuộn của lưới | — | — | **Không phân trang.** Lưới có chiều cao cố định, cuộn dọc bên trong khung, **hàng tiêu đề dính đầu khung**. Ba bảng cuộn độc lập nhau. |
| 18 | Hiện trạng | Text (chỉ đọc) | Số nguyên | **Phần mềm nạp, không nhập.** Số SPMM **đã nhập kho Cục QLKTNVMM** theo các **phiếu nhập kho ở trạng thái *Đã xác nhận***, tính cho đúng cặp `SPMM × địa điểm`. Đây là **mốc chặn giảm** ở `5.7`. Dòng nhóm hiện tổng của các dòng con. Dòng đếm chân lưới kèm nhãn *"Hiện trạng cập nhật đến `<ngày>`"* (`BR-qdgctkh-010`) |
| 19 | Số đề nghị | Text (chỉ đọc) | Số nguyên | Số mà hệ xin thêm cho đúng cặp `SPMM × địa điểm`, đọc từ các phiếu đề nghị đã chọn ở `[8]`. **Chưa chọn phiếu nào thì cả cột để trống.** Dòng chỉ do Cục QL tự thêm cũng để trống. **Không kiểm gì so với *Số lượng điều chỉnh*** — cấp nhiều hơn, bằng hay ít hơn đề nghị đều được |
| 20 | Số lượng cấp hiện tại | Text (chỉ đọc) | Số nguyên | **Số hiện hành** của cặp `SPMM × địa điểm × năm` tại thời điểm mở màn — đã cộng cả quyết định bổ sung trước đó và cả QĐTK (Mục 1.3). **Không đọc thẳng quyết định năm.** Cặp chưa có trong kế hoạch năm thì **để trống**, không hiện `0` — ô trống nghĩa là *chưa từng được giao*, khác với `0` |
| 21 | Loại điều chỉnh | Dropdown | Danh mục | **Bắt buộc.** Hai giá trị: ***Tăng*** · ***Giảm***. Quyết định dấu của số ở `[22]`. |
| 22 | Số lượng điều chỉnh | Input số | Số nguyên dương | **Bắt buộc. Chỉ nhập ở dòng con — dòng nhóm SPMM không gõ tay được**, số của nó là tổng các dòng con. **Bàn phím chặn ngay chữ cái và dấu trừ** — không gõ vào ô được, không phải gõ xong mới báo lỗi. Dấu do `[21]` quyết định. Bằng `0` → tô đỏ ô, báo đỏ **trong chính ô đó**: *"Phải khác 0."* **Chặn *Lưu*** (`5.6`). |
| 23 | Số lượng cấp sau điều chỉnh | Text (chỉ đọc) | Số nguyên | Tự tính: `[20]` cộng hoặc trừ `[22]` theo `[21]`. Dòng nhóm hiện tổng của các dòng con. Nhỏ hơn *Hiện trạng* `[18]` → báo lỗi ở `5.7` |
| 24 | Xoá dòng điều chỉnh | Icon button | — | Ở cuối mỗi dòng con **và ở dòng nhóm**. **Dòng con xoá thẳng, không hỏi**; **dòng nhóm mở `5.10` xác nhận** vì xoá một lượt nhiều dòng. Xoá dòng con cuối cùng của một nhóm thì nhóm đó biến mất khỏi cả ba bảng |
| — | + Thêm hàng loạt · Nhập Excel · Thêm 1 dòng | — | — | Hàng công cụ trên lưới và hàng thêm nhanh ghim đáy lưới. *+ Thêm hàng loạt* mở `5.5`; **chưa chọn *Căn cứ QĐGCTKH năm* thì nút mờ** — hai danh sách ở `5.5` lọc theo quyết định căn cứ. **Không có *Điền một số cho nhiều dòng*** và **không có ô tích ở đầu dòng** |
| — | Dòng đếm chân lưới | Label | — | *"`<N>` loại SPMM · `<M>` dòng điều chỉnh"* của **tab đang mở**, kèm nhãn *"Hiện trạng cập nhật đến `<ngày>`"* |
| — | Dòng *`<Đơn vị>` — Dự phòng* | — | — | Mỗi đơn vị có kho đều có một dòng địa điểm tên ***`<Tên đơn vị>` — Dự phòng***, dùng cho phần hàng để tồn chưa gắn điểm triển khai nào. Chọn được như mọi địa điểm khác ở `5.5` |
| — | Lưới khi tab chưa có dòng nào | Label | — | Giữa khung lưới hiện *"Chưa có dòng điều chỉnh nào cho hệ này."* Hàng công cụ và hàng thêm nhanh vẫn hiện |

**Phân bổ theo hệ — số thay đổi**

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 25 | Bảng *Phân bổ theo hệ* | Table | Số nguyên có dấu | Cột: SPMM (`Mã - Tên`) · ĐVT · bốn cột cơ yếu đầu hệ · hai cột của Cục QLKTNVMM là ***Triển khai*** và ***Dự phòng*** · Tổng · dòng *Tổng cộng*. **Hiện số thay đổi có dấu** (`+70`, `−100`), **không hiện số hiện hành mới**. Hệ không có điều chỉnh thì **để trống ô**, không điền `–` cũng không điền `0`. **Tự cộng từ lưới chi tiết, không có ô nhập nào.** **Bốn hệ không tách triển khai / dự phòng thành cột riêng** — dự phòng của một hệ chỉ hiện ở lưới chi tiết |

**Tổng hợp thay đổi toàn ngành**

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 26 | Đơn giá | Input số | Số tiền | **Bắt buộc khi *Ban hành***, không bắt buộc khi *Lưu*. **Một dòng SPMM một đơn giá**, tính trên **phần ròng** ở `[27]`. Phần mềm **gợi ý sẵn theo dấu của số ròng**: ròng **dương** → giá trong **bảng giá đang ở trạng thái *Hiệu lực***; ròng **âm** → **đơn giá của quyết định năm** cho SPMM đó. Người dùng **sửa tay tự do**; đã sửa thì ô **khoá giá trị**. **Xoá trắng ô** thì trả về chế độ tự gợi ý. Đang ở chế độ sửa tay mà dấu của số ròng **đảo chiều** thì hiện cảnh báo mềm ngay dưới ô, **không chặn**. Không có SPMM đó trong bảng giá và ròng dương → ô để trống, bấm *Ban hành* thì tô đỏ: *"Chưa có Đơn giá."* **Chặn** |
| 27 | Tổng thay đổi | Text | Số nguyên có dấu | Cộng cả bốn hệ và hai cột Cục QLKTNVMM của cùng SPMM ở `[25]`. Đây là **số ròng** |
| 28 | Thành tiền | Text | Số tiền có dấu | `[27]` nhân `[26]`. Ròng âm thì thành tiền âm |
| 29 | Tổng tiền thay đổi | Table footer | Số tiền có dấu | Cộng cột *Thành tiền*. **Ra số âm là hợp lệ** khi giảm nhiều hơn tăng — kinh phí chỉ là con số ghi nhận |
| — | Bảng khi chưa có dòng điều chỉnh nào | Label | — | Cả hai bảng *Phân bổ theo hệ* và *Tổng hợp thay đổi toàn ngành* hiện *"Chưa có số liệu — nhập dòng điều chỉnh ở lưới trên."* Khối vẫn gập mở được |

### 5.3 Lưới chi tiết — cách xem *Trải phẳng*

**Figma:** [BS 02b · Lập QĐ bổ sung — Trải phẳng](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1115-51372) · **Bước:** 5 · **Slug:** `qd-bs-trai-phang`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Toàn màn | — | — | Y hệt `5.2`, chỉ đổi giá trị ô *Xem theo* `5.2` `[16]`. **Không có dòng nhóm** — mỗi dòng lặp lại cột SPMM. Đúng cùng bộ cột, cùng số liệu, cùng luật nhập |

### 5.4 Lập quyết định có phiếu đề nghị

**Figma:** [BS 02c · Lập QĐ bổ sung — có phiếu đề nghị](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1143-54723) · **Bước:** 4–5 · **Slug:** `qd-bs-co-phieu`

> Cùng màn `5.2`, khác ở chỗ ô *Phiếu đề nghị SPMM* đã chọn phiếu.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Phiếu đề nghị SPMM | Dropdown chọn nhiều | Danh sách | Đã chọn thì bày **thẻ mang số phiếu**, mỗi phiếu một thẻ. Chọn được phiếu của **nhiều hệ khác nhau** trong cùng một quyết định |
| 2 | Số đề nghị | Text (chỉ đọc) | Số nguyên | Có giá trị ở dòng nào mà phiếu đã chọn có nhắc tới cặp `SPMM × địa điểm` đó. Dòng Cục QL tự thêm và **mọi dòng *Giảm*** để trống — phiếu đề nghị chỉ dùng cho ca xin thêm |
| 3 | Bỏ một thẻ phiếu | Icon button | — | Bỏ phiếu khỏi quyết định. **Dòng điều chỉnh đã nhập giữ nguyên**, chỉ cột *Số đề nghị* của các dòng thuộc phiếu đó trở về trống — dòng điều chỉnh là do Cục QL quyết, không phải do phiếu sinh ra |

### 5.5 Hộp thoại *Thêm hàng loạt*

**Figma:** [BS 03 · Thêm hàng loạt](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1114-49285) · **Bước:** 5 · **Slug:** `them-hang-loat`

> Hai cột chọn song song: *Địa điểm triển khai* bên trái, *SPMM* bên phải. Sinh ra tích Descartes của hai bên.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Thêm SPMM và địa điểm ngoài QĐ năm | Checkbox | Chọn | **Mặc định tắt.** Tắt thì hai danh sách chỉ hiện những SPMM và địa điểm **đã có trong quyết định năm căn cứ**. Bật thì hiện **toàn bộ** danh mục SPMM và toàn bộ cây tổ chức — dùng cho ca thêm SPMM mới hoặc điểm triển khai mới |
| 2 | Danh sách *Địa điểm triển khai* | Checkbox list | Chọn nhiều | Có ô *Tìm địa điểm* và dòng ***Tất cả (`<N>`)*** ở đầu để tích hết. Tìm không ra thì hiện *"Không tìm thấy địa điểm nào."*, dòng *Tất cả* ẩn theo. Đầu danh sách kèm dòng đếm *"`<k>`/`<N>` địa điểm đang chọn"* |
| 3 | Danh sách *SPMM* | Checkbox list | Chọn nhiều | Có ô *Tìm SPMM* và dòng ***Tất cả (`<N>`)***. Tìm không ra thì hiện *"Không tìm thấy SPMM nào."* Mỗi dòng hiện `Mã - Tên` và ĐVT. Dòng đếm *"`<k>`/`<N>` SPMM đang chọn"* |
| 4 | Dòng đếm kết quả | Label | — | *"Số dòng sinh ra: `<a>` địa điểm × `<b>` SPMM = `<a×b>` dòng"*, cập nhật ngay khi tích |
| 5 | Huỷ | Button | — | Đóng, không thêm dòng nào |
| 6 | Thêm | Button | — | Sinh `a × b` dòng vào lưới của **tab tương ứng với hệ của từng địa điểm**. **Cột *Loại điều chỉnh* và *Số lượng điều chỉnh* để trống** — chọn là chọn *chỗ*, nhập số là việc riêng. Cặp `SPMM × địa điểm` **đã có trong quyết định** thì bỏ qua, **không ghi đè số đã nhập**. Chưa tích đủ hai bên thì nút mờ |
| — | Cột *Số lượng cấp hiện tại* trong danh sách địa điểm | — | — | **Không có.** Một địa điểm có nhiều SPMM nên không tồn tại một con số "hiện tại" của riêng địa điểm đó |

### 5.6 *Lưu* bị chặn — số lượng bằng 0

**Figma:** [BS 04 · Lưu bị chặn — còn ô trống](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1144-58617) · **Bước:** 5 · **Slug:** `luu-chan-so-khong`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Ô *Số lượng điều chỉnh* lỗi | Input số | Số nguyên | Viền ô tô đỏ, **câu lỗi nằm ngay bên trong ô**, dưới chỗ nhập. Nguyên văn: ***"Phải khác 0."*** |
| 2 | Số lượng cấp sau điều chỉnh | Text | Số nguyên | **Để trống** khi dòng đang lỗi |
| 3 | Dòng nhóm | Text | Số nguyên | *Số lượng cấp sau điều chỉnh* của nhóm tính lại **bỏ qua dòng đang lỗi** |
| 4 | Hành vi *Lưu* | — | — | Không lưu gì, con trỏ nhảy về ô lỗi đầu tiên. Nhiều dòng lỗi thì **tô đỏ hết cùng lúc**, không báo từng cái một |

### 5.7 *Lưu* bị chặn — giảm dưới mốc đã nhập kho

**Figma:** [BS 05 · Giảm dưới mốc đã nhập kho — bị chặn](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1144-59575) · **Bước:** 5 · **Slug:** `giam-duoi-moc-chan`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Luật | — | — | *Số lượng cấp sau điều chỉnh* `5.2` `[23]` **không được nhỏ hơn *Hiện trạng*** `5.2` `[18]` của cùng dòng |
| 2 | Mốc tính | — | — | **Phiếu nhập kho ở trạng thái *Đã xác nhận*.** Phiếu nhập kho còn *Mới* **không tính**. Không lấy mốc ký hợp đồng, không lấy mốc sản xuất |
| 3 | Ô lỗi | Input số | Số nguyên | Viền đỏ, câu lỗi trong ô: ***"Dưới mốc đã nhập kho."*** **Không chèn lại con số** |
| 4 | Số lượng cấp sau điều chỉnh | Text | Số nguyên | **Vẫn hiện số đã tính** |
| 5 | Hành vi *Lưu* | — | — | **Chặn**. Kiểm này **chạy lại lúc *Ban hành*** |

### 5.8 *Ban hành* bị chặn

**Figma:** [BS 06 · Ban hành bị chặn — thiếu số văn bản](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1147-61964) · **Bước:** 8 · **Slug:** `ban-hanh-chan`

> **Không có hộp thoại, không có thông báo nổi.** Thiếu gì thì tô đỏ đúng chỗ đó, cùng khuôn với phiếu nhập kho và hợp đồng.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Số QĐGCTKH | Textbox | Chuỗi | Viền đỏ, báo đỏ ngay dưới ô: ***"Chưa có Số QĐGCTKH."*** |
| 2 | Ngày chứng từ | Datepicker | Ngày | Viền đỏ, báo đỏ ngay dưới ô: ***"Chưa có Ngày chứng từ."*** |
| 3 | Đơn giá | Input số | Số tiền | Viền đỏ, báo đỏ trong ô: ***"Chưa có Đơn giá."*** Chỉ xảy ra khi SPMM chưa có trong bảng giá và số ròng dương |
| 4 | Tài liệu đính kèm | Button | Tệp | Báo đỏ dưới nút: ***"Chưa đính kèm bản quyết định đã ký."*** |
| 5 | Thứ tự kiểm | — | — | **Chạy lại toàn bộ kiểm của *Lưu* trước** (`5.6`, `5.7`), rồi mới tới bốn mục trên. Mọi lỗi tô đỏ **cùng một lượt**, con trỏ nhảy về mục đầu tiên |
| 6 | Sau khi sửa đủ | — | — | Bấm lại *Ban hành* thì mở `5.9` |

### 5.9 Hộp thoại xác nhận ban hành

**Figma:** [BS 07 · Ban hành — xác nhận](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1143-55690) · **Bước:** 8 · **Slug:** `ban-hanh-xac-nhan`

> Ba hộp thoại `5.9`–`5.11` theo khuôn ở `docs/design.md` Mục 9.4: tiêu đề là cụm động từ · dòng nhận diện · câu hệ quả · nút chính mang đúng chữ của tiêu đề.

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Xác nhận ban hành"* |
| 2 | Dòng nhận diện | Label | — | *"Số phiếu `<số phiếu>` — Số QĐGCTKH `<giá trị>`."* |
| 3 | Câu hệ quả | Label | — | Nguyên văn *"Sau khi ban hành, toàn bộ số liệu bị khoá và không sửa được. Vui lòng xác nhận."* |
| 4 | Huỷ | Button | — | Đóng, không ban hành |
| 5 | Xác nhận ban hành | Button | — | Chuyển sang *Đã ban hành*, mở `5.12`. **Dòng điều chỉnh bắt đầu tính vào số hiện hành** và quyết định xuất hiện ở tab *Lịch sử điều chỉnh* của quyết định năm. Ghi lại người bấm và thời điểm |

### 5.10 Hộp thoại xoá nhóm

**Figma:** [BS 08 · Xoá nhóm — xác nhận](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1143-56667) · **Bước:** 5 · **Slug:** `xoa-dong-xac-nhan`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Xoá nhóm"* — **không nói nhóm theo gì**, vì cùng một hộp thoại dùng cho cả hai cách xem có nhóm |
| 2 | Dòng nhận diện | Label | — | *"Nhóm `<nhãn của dòng nhóm đang xoá>`."* — lấy **đúng chữ đang hiện trên dòng nhóm** |
| 3 | Câu hệ quả | Label | — | Nguyên văn *"Sau khi xoá, toàn bộ dòng con của nhóm này không khôi phục được. Vui lòng xác nhận."* |
| 4 | Huỷ | Button | — | Đóng, không xoá gì |
| 5 | Xoá nhóm | Button | — | Xoá, ba bảng tính lại |
| — | Xoá một dòng con lẻ | — | — | **Không mở hộp thoại**, xoá thẳng. Chỉ xoá cả nhóm mới hỏi. Cách xem *Trải phẳng* không có dòng nhóm nên không có ca này |

### 5.11 Hộp thoại xoá quyết định

**Figma:** [BS 09 · Xoá quyết định — xác nhận](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1143-57642) · **Bước:** ngoài luồng chính · **Slug:** `xoa-qd-xac-nhan`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Tiêu đề | Label | — | Nguyên văn *"Xoá quyết định"* |
| 2 | Dòng nhận diện | Label | — | *"Số phiếu `<số phiếu>`."* |
| 3 | Câu hệ quả | Label | — | Nguyên văn *"Sau khi xoá, quyết định không khôi phục được. Vui lòng xác nhận."* |
| 4 | Huỷ | Button | — | Đóng, không xoá gì |
| 5 | Xoá quyết định | Button | — | Xoá hẳn. Chỉ xoá được quyết định ở trạng thái *Mới*, nên **số hiện hành không đổi** |

### 5.12 Quyết định bổ sung đã ban hành

**Figma:** [BS 10 · QĐ bổ sung đã ban hành](https://www.figma.com/design/uYUO7YWV28C8X5hhiqHo6j/BCY-2-?node-id=1144-60533) · **Bước:** sau 8 · **Slug:** `qd-bs-da-ban-hanh`

| # | Items | Control type | Data type | Description |
|---|---|---|---|---|
| 1 | Nhãn trạng thái | Tag | Danh mục | *Đã ban hành* |
| 2 | Toàn màn | — | — | Cùng bố cục `5.2` ở chế độ **chỉ đọc**. Không sửa bảng nào, không sửa *Đơn giá*, ô *Phiếu đề nghị SPMM* không xổ được. Đổi tab và đổi *Xem theo* vẫn dùng được. **Khối nào hiện và dòng nào hiện cắt theo `srs-qdgctkh-nam.md` Mục 3.1** |
| 3 | Cột *Hiện trạng* | — | — | **Không hiện.** Cùng luật với các tab đã ban hành của quyết định năm |
| 4 | Xuất phụ lục | Button | — | Dùng được, cùng khuôn `5.2` `[11]` |
| 5 | Tài liệu đính kèm | Button | Tệp | Mở xem bản đã ký. **Không thêm, không bớt tệp** |
| — | *Hủy* · *Lưu* · *Ban hành* · *+ Thêm hàng loạt* · *Nhập Excel* · *Thêm 1 dòng* · icon xoá dòng | — | — | **Không có.** Trên đầu màn chỉ còn *Xuất phụ lục* |

## 6. Yêu cầu chức năng không thuộc màn hình nào

| ID | Yêu cầu | Cách kiểm |
|---|---|---|
| `FR-qdgctkh-bo-sung-001` | **Số hiện hành cộng dồn khi xem, không lưu:** `số của quyết định năm + tổng delta của mọi văn bản đã ban hành cùng năm`, khoá là cặp `SPMM × địa điểm × năm`. Nguồn delta gồm quyết định bổ sung và QĐTK | Ban hành một quyết định bổ sung → tab *Kế hoạch hiện hành* của quyết định năm đổi đúng phần chênh; xoá quyết định bổ sung khi còn *Mới* → số hiện hành không đổi |
| `FR-qdgctkh-bo-sung-002` | **Ba bảng tính một chiều:** lưới chi tiết → *Phân bổ theo hệ — số thay đổi* → *Tổng hợp thay đổi toàn ngành*. Ô nhập duy nhất ở hai bảng dưới là *Đơn giá* | Sửa một ô *Số lượng điều chỉnh* → cả hai bảng dưới đổi ngay; không có cách nào sửa hai bảng dưới để làm đổi lưới |
| `FR-qdgctkh-bo-sung-003` | **Gợi ý đơn giá theo dấu của số ròng, khoá lại khi người dùng sửa tay** (`5.2` `[26]`) | Nhập một dòng tăng → đơn giá nhảy ra giá của bảng giá đang *Hiệu lực*. Sửa tay rồi đổi số cho ròng thành âm → đơn giá **giữ nguyên** giá đã gõ, có cảnh báo mềm. Xoá trắng ô → nhảy về đơn giá của quyết định năm |
| `FR-qdgctkh-bo-sung-004` | ***Hiện trạng* đọc từ phiếu nhập kho ở trạng thái *Đã xác nhận*** về kho Cục QLKTNVMM, theo cặp `SPMM × địa điểm`. Phiếu nhập kho còn *Mới* không tính | Lập một phiếu nhập kho và chỉ *Lưu* → cột *Hiện trạng* không đổi. Xác nhận phiếu đó → *Hiện trạng* tăng đúng số lượng |
| `FR-qdgctkh-bo-sung-005` | **Mọi luật kiểm chạy lại tại thời điểm *Ban hành***, không chỉ lúc *Lưu* | Lưu thành công một quyết định giảm sát mốc, xác nhận một phiếu nhập kho cho cùng SPMM, rồi bấm *Ban hành* → bị chặn ở `5.7` |
| `FR-qdgctkh-bo-sung-006` | **Quyết định bổ sung không sửa bản ghi của quyết định năm;** tab *Kế hoạch năm* luôn hiện đúng bản ban hành gốc | Ban hành ba quyết định bổ sung liên tiếp → tab *Kế hoạch năm* của quyết định năm không đổi một con số nào |
| `FR-qdgctkh-bo-sung-007` | **Phụ lục của quyết định bổ sung chỉ chứa dòng có điều chỉnh**, và tách **hai bảng riêng** *Điều chỉnh tăng* / *Điều chỉnh giảm* với số luôn dương | Xuất phụ lục một quyết định có 9 dòng điều chỉnh trên tổng 411 dòng kế hoạch → tệp chỉ có 9 dòng, xếp thành hai bảng, không con số nào mang dấu trừ |

## 7. Quy tắc nghiệp vụ

Chỉ những quy tắc **xuyên nhiều màn** hoặc **không thuộc màn nào**. Luật của từng ô nằm trong bảng mô tả màn ở Mục 5, không nhắc lại ở đây. Quy tắc `BR-qdgctkh-001`–`031`, yêu cầu `FR-qdgctkh-001`–`007` và `NFR-qdgctkh-001`–`004` của quyết định năm **vẫn áp** trừ chỗ tài liệu này nói khác.

| ID | Quy tắc | Áp ở | Căn cứ |
|---|---|---|---|
| `BR-qdgctkh-bo-sung-001` | **Tiêu chí phân định ba văn bản là *tổng toàn ngành có đổi không*** (Mục 1.2). QĐTK không bao giờ đổi tổng toàn ngành; nguồn hàng chỉ được là kho của chính hệ nhận hoặc kho Cục QLKTNVMM, và khi rút từ kho Cục QLKTNVMM thì **tổng của hệ nhận tăng**. Lấy từ hệ khác phải lập quyết định bổ sung trước | Mục 1.2 | @quynhdtn17 chốt 03/09/2026, thay tiêu chí *"còn tồn kho để cấp ngay"* của biên bản 04/08/2026 |
| `BR-qdgctkh-bo-sung-003` | **Quyết định bổ sung luôn ghi chi tiết tới địa điểm triển khai**, kể cả khi bản giấy chỉ in gộp tới mức hệ. Khoá tham chiếu là cặp `SPMM × địa điểm triển khai × năm` | `5.2` `[20]`, `srs-qdgctkh-nam.md` `5.12` | @quynhdtn17 chốt 04/09/2026 |
| `BR-qdgctkh-bo-sung-004` | **Số hiện hành cộng dồn khi xem, không lưu, không có cờ hiệu lực ở mức dòng** | `5.2`, `srs-qdgctkh-nam.md` `5.12` | @quynhdtn17 chốt 26/08/2026, thay mô hình ba lớp có cờ của biên bản 04/08/2026 |
| `BR-qdgctkh-bo-sung-006` | **Tiền gắn với từng văn bản.** *Đơn giá* không cộng được giữa các văn bản, *Thành tiền* thì cộng được | Mục 1.4, `srs-qdgctkh-nam.md` `5.12` | @quynhdtn17 chốt 26/08/2026 |
| `BR-qdgctkh-bo-sung-007` | **Tiền chỉ phát sinh trên phần ròng**, một dòng SPMM một đơn giá. Ròng dương lấy giá của bảng giá đang *Hiệu lực*, ròng âm lấy đơn giá của quyết định năm | `5.2` `[26]` `[27]` `[28]` | @quynhdtn17 chốt 02/09/2026 |
| `BR-qdgctkh-bo-sung-011` | **Báo lỗi tô đỏ tại trường, câu lỗi nằm trong chính ô đó.** Không thông báo nổi, không hộp thoại liệt kê. Nhiều lỗi tô đỏ cùng một lượt; ô báo lỗi vẫn căn phải như bình thường | `5.6`–`5.8` | @quynhdtn17 chốt 02/09/2026 |
| `BR-qdgctkh-bo-sung-017` | **Phiếu đề nghị được chọn thì bị chiếm** — quyết định khác không chọn được nữa. Bỏ thẻ phiếu, hoặc xoá quyết định khi còn *Mới*, thì phiếu nhả ra | `5.2` `[8]`, `5.4` | @quynhdtn17 chốt 27/08/2026 |
| `BR-qdgctkh-bo-sung-020` | **Cặp `SPMM × địa điểm` chỉ có một dòng trong một quyết định bổ sung** | `5.2`, `5.5` `[6]` | @quynhdtn17 chốt 01/09/2026 |
| `BR-qdgctkh-bo-sung-023` | **Cột *Hiện trạng* chỉ hiện ở màn đang lập**, không hiện ở màn đã ban hành và ở các tab của quyết định năm | `5.2` `[18]`, `5.12` `[3]` | @quynhdtn17 chốt 03/09/2026 |
| `BR-qdgctkh-bo-sung-025` | **Quyết định bổ sung đã ban hành không thu hồi, không thay thế, không xoá.** Sai thì lập quyết định bổ sung tiếp theo để bù trừ | Mục 4, `5.12` | `BR-qdgctkh-016` |

## 8. Yêu cầu phi chức năng

| ID | Yêu cầu | Cách kiểm |
|---|---|---|
| `NFR-qdgctkh-bo-sung-001` | **Số hiện hành tính lại trong vòng 2 giây** khi mở tab *Kế hoạch hiện hành* của một quyết định năm đã có nhiều văn bản điều chỉnh | Ban hành 10 quyết định bổ sung cho cùng một năm, mở tab *Kế hoạch hiện hành*, đo thời gian tới lúc lưới hiện đủ |
| `NFR-qdgctkh-bo-sung-002` | **Ba bảng của quyết định bổ sung tính lại trong vòng 1 giây** sau khi sửa một ô *Số lượng điều chỉnh* | Nhập một quyết định 50 dòng, sửa một ô, đo tới lúc *Tổng tiền thay đổi* đổi |
| `NFR-qdgctkh-bo-sung-003` | **Ban hành đóng băng hết**, giống `NFR-qdgctkh-004`: cả số lượng, *Đơn giá*, *Thành tiền*, lẫn tên SPMM, ĐVT, tên địa điểm và dòng đó thuộc hệ nào | Đổi tên một SPMM trong danh mục → quyết định đã ban hành vẫn hiện tên cũ |
| `NFR-qdgctkh-bo-sung-004` | **Mọi hành động đổi trạng thái ghi lại được ai làm và lúc nào** | Ban hành một quyết định → tra ra được người bấm và thời điểm |

## 9. Tiêu chí thành công

| # | Tiêu chí | Cách đo |
|:--:|---|---|
| 1 | **Một màn biết năm nay đã đổi gì và tổng còn bao nhiêu** | Mở tab *Kế hoạch hiện hành* của quyết định năm → số của mọi dòng đã cộng đủ mọi văn bản đã ban hành; mở tab *Lịch sử điều chỉnh* → thấy đủ danh sách văn bản đã tác động |
| 2 | **Không rút được chỉ tiêu xuống dưới phần hàng đã về kho** | Lập một dòng giảm xuống dưới *Hiện trạng* → bị chặn ở cả *Lưu* lẫn *Ban hành* |
| 3 | **Đọc ra ngay số tiền phát sinh thêm để trình Vụ Tài chính** | Nhập một quyết định vừa tăng vừa giảm → *Tổng tiền thay đổi* bằng đúng tổng của cột *Thành tiền*, và bằng tổng phần ròng nhân đơn giá tương ứng |
| 4 | **Quyết định năm không bị đụng tới** | Ban hành nhiều quyết định bổ sung → tab *Kế hoạch năm* của quyết định năm giữ nguyên từng con số |
| 5 | **Bản giấy và phụ lục khớp nhau** | Xuất phụ lục → hai khối *Điều chỉnh tăng* / *Điều chỉnh giảm* và bảng *Phân bổ theo hệ* khớp đúng bản giấy đã ký |

## 10. Chưa làm ở đợt này

- **QĐTK** — tầng triển khai, đặc tả riêng. Tài liệu này chỉ ghi phần QĐTK chảy ngược lên số hiện hành. **Bốn điểm bàn giao cho đội QĐTK:** (1) cột *Số theo QĐGCTKH* phải đọc **số hiện hành cộng dồn** theo cặp `SPMM × địa điểm nhận`, không đọc từ một văn bản căn cứ; (2) ban hành QĐTK phải đẩy chênh lệch vào số hiện hành của quyết định năm; (3) kho cấp bắt buộc là kho của chính hệ nhận hoặc kho Cục QLKTNVMM; (4) các cột *người nhận · chức vụ · đơn vị công tác · hình thức sử dụng* thuộc cấp phát người dùng cuối, không thuộc QĐTK. QĐTK ghi số tuyệt đối hay có dấu đều được, miễn tổng toàn ngành không đổi.
- **Điều chỉnh chỉ đơn giá, không đổi số lượng.**
- **Chế độ chỉ xem của `5.2` chưa có frame Figma riêng** — dùng khuôn `QĐGCTKH 02` của quyết định năm.
- **Kiểm tầng hai của mốc chặn giảm:** dòng của một địa điểm không xuống dưới phần **đã cấp phát cho chính địa điểm đó**. Chạy được khi module cấp phát có; đợt này chỉ kiểm tầng một.
- **Cảnh báo khi tổng tầng triển khai của một hệ vượt chỉ tiêu hiện hành** — *cảnh báo, không chặn*, thuộc màn QĐTK.
- **Cột *Học viện* trong bảng phân bổ theo hệ** — làm cùng đợt sửa bảng phân bổ của quyết định năm.
- **Cấp dưới tự điều chuyển trước, QĐTK hợp thức hoá sau** — mô hình chốt 04/08/2026 cho Công an và Quân đội, thuộc màn QĐTK.

## 📝 Changelog

| Ngày cập nhật | Loại thay đổi | Nguồn/brainstorming liên quan | Người yêu cầu | Nội dung thay đổi |
|---|---|---|---|---|
| 2026-09-04 | cập nhật | `docs/reference/PhuLuc_QDGCTKH_BoSung_Mau.xlsx` · @quynhdtn17 chốt 04/09/2026 | @quynhdtn17 | `5.2` `[11]` và `FR-qdgctkh-bo-sung-007`: phụ lục tách **hai bảng riêng trong một sheet** — *Điều chỉnh tăng* và *Điều chỉnh giảm*, số luôn dương, chiều đọc ở tên bảng; sheet *Tổng hợp* tách ba cột *Tăng* · *Giảm* · *Chênh lệch*. Khuôn mẫu `PhuLuc_QDGCTKH_BoSung_Mau.xlsx` chưa giao kèm gói này **Bảng *Phân bổ theo hệ* bỏ hẳn dấu `–`** — hệ không có số thì để trống ô, sửa cả trên Figma (185 ô). |
| 2026-09-03 | thêm mới | `docs/cuc-ql/brainstorming/brainstorm-qdgctkh-bo-sung.md` · 12 frame Figma khu vực 5 file BCY(2) · soát toàn bộ bản vẽ 03/09/2026 | @quynhdtn17 | Bản đầu tiên, tách khỏi `srs-qdgctkh-nam.md`. Mục 5 gồm 12 màn đã vẽ. Ghi các quyết định 01–03/09: **luật tiền tính trên phần ròng** và cách chọn đơn giá theo dấu · **đơn giá tự gợi ý rồi khoá khi sửa tay** · **mốc chặn giảm theo phiếu nhập kho *Đã xác nhận*** · **tách chặn *Lưu* và *Ban hành*** · **báo lỗi tô đỏ tại trường, câu lỗi trong ô** · **cuộn trong khung thay phân trang** · **bỏ ô tích đầu dòng và *Điền một số cho nhiều dòng*** · **ô *Phiếu đề nghị SPMM* chọn nhiều, không bắt buộc** · **bảng phân vai ba văn bản** với luật *QĐTK không đổi tổng toàn ngành, nguồn chỉ được là kho hệ hoặc kho Cục QL*. Bỏ thiết kế hai mục *Điều chỉnh tăng* / *Điều chỉnh giảm* tách rời và hai nút *Chọn nơi cần điều chỉnh* / *Thêm dòng mới* của bản nháp 26–27/08. Soát bằng bốn agent review rồi sửa theo: mốc chặn đọc phiếu nhập kho ***Đã xác nhận*** (không phải "đã ban hành"), màn nhập có **hai chế độ xem và sửa** theo `BR-qdgctkh-007`, phiếu đề nghị **bị chiếm** khi được chọn, ghi rõ bản 03–04/09 thay hai điểm biên bản 04/08. **Chốt hết câu hỏi mở, xoá Mục 10** — còn 10 mục. Soát câu chữ: cắt câu giải thích lý do khắp Mục 1 và Mục 5, **Mục 7 từ 25 quy tắc còn 10** sau khi bỏ những quy tắc chỉ chép lại luật đã có ở bảng mô tả màn. Mục 1.4 viết lại theo lý do thật (đơn giá đổi giữa các thời điểm); bỏ định dạng của *Số QĐGCTKH*; ba bước đầu Mục 2 viết lại — bước 1 và 2 làm trên phần mềm hoặc bằng công văn ngoài phần mềm, bước 3 nêu rõ tiêu chí chọn luồng QĐTK hay bổ sung; Mục 3 thêm phạm vi dữ liệu của các hệ. Bịt ba lỗ hổng Dev/QA sẽ hỏi: **dòng nhóm SPMM không gõ tay được** (`5.2` `[22]`), **đổi *Năm áp dụng* thì ô *Căn cứ QĐGCTKH năm* trống lại, đổi riêng *Căn cứ* thì hai cột số tính lại nhưng dòng điều chỉnh giữ nguyên** (`[7]`), **chưa chọn *Căn cứ* thì nút *+ Thêm hàng loạt* mờ**. Ghi rõ **quyết định bổ sung chưa có tệp khuôn mẫu phụ lục** — khuôn đi kèm gói là của quyết định năm. Nút *Xuất phụ lục* của bản bổ sung **không có hộp thoại chọn bản xuất**. Chuẩn hoá câu hệ quả và nhãn nút của ba hộp thoại theo `design.md` Mục 9.4, sửa cả trên Figma. **`5.10` gom thành hộp thoại *Xoá nhóm* dùng chung cho cả hai cách xem có nhóm.** Thêm tệp khuôn mẫu phụ lục riêng cho quyết định bổ sung — `PhuLuc_QDGCTKH_BoSung_Mau.xlsx`, 7 sheet, cột số có dấu, mỗi sheet chi tiết tách hai khối tăng giảm. Sửa mâu thuẫn ở `5.2` `[24]`: **dòng con xoá thẳng, chỉ dòng nhóm mới hỏi** — trước đó `[24]` ghi mọi dòng con đều mở hộp thoại, ngược với `5.10` |
