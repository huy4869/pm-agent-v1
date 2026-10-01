---
type: srs
feature: dieu-chuyen-spmm-v2
status: draft
updated: 2026-09-06
---

# Điều chuyển SPMM

## 1. Phạm vi

**Trong phạm vi:**

- Chức năng **"Điều chuyển SPMM"** (đổi tên trên hệ thống từ "Căn cứ điều chuyển SPMM"), gồm **4 loại điều chuyển**, mỗi loại có **căn cứ pháp lý riêng**:
  1. **"Chuyển từ ĐVSX về Kho Đơn vị đặt hàng"** — căn cứ: **Hợp đồng sản xuất** (được chọn nhiều hợp đồng cho 1 phiếu).
  2. **"Chuyển từ Cục xuống các cơ yếu Đầu hệ"** — căn cứ: **Quyết định giao chỉ tiêu kế hoạch (QĐGCTKH)** (được chọn nhiều QĐGCTKH cho 1 phiếu).
  3. **"Chuyển kho giữa các đơn vị cơ yếu"** — căn cứ: **QĐGCTKH** (được chọn nhiều QĐGCTKH cho 1 phiếu).
  4. **"Chuyển kho trong đơn vị"** (chuyển giữa 2 kho khác nhau của cùng 1 đơn vị — Đơn vị nhận luôn = Đơn vị xuất, Kho nhận chọn khác Kho xuất) — căn cứ: **Số công văn quyết định** (nhập text).

## 2. Actors

| Actor | Loại | Mục tiêu | Đơn vị cụ thể theo loại | Đặc tả chi tiết? |
|-------|------|----------|--------------------------|---------------|
| Cán bộ đơn vị xuất | người | Lập phiếu điều chuyển (chọn căn cứ, SPMM, Serial, số lượng), sửa/Bỏ duyệt lại phiếu do chính mình tạo | (1) Nhà máy · (2) Trung tâm bảo đảm - Cục · (3) Cơ yếu đầu hệ/đơn vị cơ yếu gửi · (4) Đơn vị có nhu cầu chuyển kho nội bộ | Có |
| Người có thẩm quyền phê duyệt | người | Phê duyệt hoặc Bỏ duyệt (kèm Lý do) phiếu điều chuyển của đơn vị xuất | (1) Lãnh đạo/Quản lý Nhà máy · (2) Lãnh đạo Trung tâm bảo đảm - Cục · (3) Lãnh đạo Cơ yếu đầu hệ · (4) Người có quyền phê duyệt trong đơn vị | Có |
| Đơn vị nhận | người/đơn vị | Xem các phiếu điều chuyển có Đơn vị nhận là đơn vị mình | Cả 4 loại — chỉ xem, không thao tác | Có |
| Hệ thống | hệ thống | Tự cập nhật tồn kho khi phiếu chuyển "Đã duyệt" (giảm bên xuất, tăng bên nhận), ghi nhật ký thao tác | Cả 4 loại | Có |

## 3. Quy trình nghiệp vụ

1. **Lập phiếu**: Chọn loại điều chuyển, căn cứ, đơn vị/kho xuất–nhận và thông tin liên quan. Bấm **"Lưu"** để tạo phiếu trạng thái **Mới**; **"Hủy bỏ"** để thoát mà không lưu.
2. **Chọn tồn kho/Serial**: Chọn thủ công theo chứng từ, phân bổ tự động theo FIFO hoặc quét Serial. Số lượng và Serial thực tế được xác nhận theo từng dòng SPMM.
3. **Phê duyệt**: Hệ thống kiểm tra số lượng không vượt hạn mức còn lại, bằng tổng Serial đã ghi nhận, và từng Serial còn tại Kho xuất (tự cập nhật vị trí nếu đổi chỗ, chặn nếu không còn). Hợp lệ, phiếu chuyển sang **Đã duyệt** và cập nhật tồn kho từng Serial từ kho xuất sang kho nhận.
4. **Bỏ duyệt**: Chỉ thực hiện khi toàn bộ Serial còn tại kho nhận. Người dùng nhập lý do; hệ thống tạo giao dịch hoàn tác, giữ lịch sử và chuyển phiếu về **Mới**. Nếu có Serial đã được điều chuyển tiếp, hệ thống chặn và thông báo Serial, phiếu liên quan.
5. **Bàn giao**: Việc vận chuyển, bàn giao và ký nhận thực hiện ngoài hệ thống.

## 4. Phân quyền

### 4.1 Phạm vi dữ liệu

| Đối tượng | Phạm vi phiếu được xem | Ghi chú |
|---|---|---|
| Đơn vị xuất | Các Phiếu điều chuyển do chính đơn vị mình tạo | Không phụ thuộc trạng thái phiếu |
| Đơn vị nhận | Các Phiếu điều chuyển có Đơn vị nhận thuộc đơn vị mình | Chỉ xem, không thao tác |
| Người được phân quyền xem toàn bộ | Tất cả Phiếu điều chuyển trong phạm vi hệ thống | Quyền xem toàn bộ không đồng nghĩa với quyền thao tác |

Trường hợp một người đồng thời thỏa mãn nhiều phạm vi, phạm vi dữ liệu được xem là hợp của các phạm vi được cấp.

### 4.2 Quyền thao tác theo vai trò

| Vai trò | Hành động được phép | Hành động bị chặn |
|---|---|---|
| Cán bộ đơn vị xuất | Lập phiếu; sửa nội dung phiếu khi "Mới"; chọn/xóa dòng tồn kho hoặc Serial (qua modal "Danh sách tồn kho chi tiết", "Phân bổ tồn kho" hoặc quét Serial trực tiếp) | Phê duyệt hoặc Bỏ duyệt phiếu do chính đơn vị mình lập; thao tác trên phiếu của đơn vị khác |
| Người có thẩm quyền phê duyệt | Phê duyệt phiếu ở trạng thái "Mới"; Bỏ duyệt phiếu ở trạng thái "Đã duyệt" (bắt buộc nhập Lý do bỏ duyệt) | Sửa nội dung chi tiết phiếu (căn cứ, SPMM, Serial, số lượng) |
| Đơn vị nhận | Xem các phiếu có Đơn vị nhận là đơn vị mình | Mọi thao tác sửa/Phê duyệt/Bỏ duyệt |
| Người có quyền Xem toàn bộ | Xem tất cả Phiếu điều chuyển | Không phát sinh thêm quyền thao tác chỉ từ quyền Xem toàn bộ |

> Quyền xem dữ liệu và quyền thao tác là độc lập.

### 4.3 Quyền thao tác theo trạng thái

| Trạng thái | Đối tượng được thao tác | Hành động |
|---|---|---|
| Mới | Cán bộ đơn vị xuất | Sửa nội dung phiếu, chọn/xóa dòng tồn kho hoặc Serial |
| Mới | Người có thẩm quyền phê duyệt | Phê duyệt |
| Đã duyệt | Người có thẩm quyền phê duyệt | Bỏ duyệt (bắt buộc nhập Lý do bỏ duyệt) |
| Đã duyệt | Mọi đối tượng có phạm vi xem (Mục 4.1) | Chỉ xem |

## 5. Vòng đời trạng thái

| Entity | Từ trạng thái | Sang trạng thái | Trigger | Quay lại được? |
|--------|-----------------|--------------------|---------|-------------------|
| Phiếu điều chuyển | (đang nhập liệu, chưa lưu) | Mới | Cán bộ đơn vị xuất bấm "Lưu" | — |
| Phiếu điều chuyển | Mới | Đã duyệt | Người có thẩm quyền phê duyệt bấm "Phê duyệt", đạt validate: Số lượng chuyển ≤ tổng SL đề nghị còn lại theo căn cứ đã chọn, Số lượng chuyển = tổng Serial đã ghi nhận mỗi dòng, mỗi Serial còn tại Kho xuất (tự cập nhật vị trí nếu đổi chỗ, chặn nếu không còn), VÀ tổng SL chuyển theo SPMM/Kho xuất không vượt tồn kho thực tế — hệ thống cập nhật tồn kho ngay theo từng Serial (giảm bên xuất, tăng bên nhận) | Có — qua "Bỏ duyệt", nếu chưa Serial nào đi tiếp |
| Phiếu điều chuyển | Đã duyệt | Mới | Người có thẩm quyền phê duyệt bấm "Bỏ duyệt" — CHỈ khi mọi Serial của phiếu còn nguyên tại Kho nhận (chưa dùng cho phiếu khác đã "Đã duyệt"); bắt buộc nhập Lý do bỏ duyệt | Có — lặp lại được nhiều lần (Phê duyệt ⇄ Bỏ duyệt), miễn Serial chưa đi tiếp. Hệ thống ghi giao dịch hoàn tồn kho theo từng Serial (tăng lại bên xuất, giảm lại bên nhận) bằng bút toán đảo ngược, không xóa giao dịch gốc của lần Phê duyệt trước đó — giữ nguyên lịch sử biến động tồn kho |
| Phiếu điều chuyển | Đã duyệt | (không đổi — chặn) | Người có thẩm quyền phê duyệt bấm "Bỏ duyệt" nhưng có ≥1 Serial đã dùng làm nguồn cho phiếu khác đã "Đã duyệt" | Không — hệ thống chặn |

## 6. Màn hình

### 6.1 Điều chuyển SPMM (danh sách) — `danh-sach-phieu-dieu-chuyen`

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/dieu-chuyen-flow.md#screen-danh-sach-phieu-dieu-chuyen--danh-sách-phiếu-điều-chuyển) · HTML wireframe: chưa có (chạy `/wireframe-html`) · Figma: Frame "196:6" (page "DCSPMM", section "Điều chuyển SPMM v2").

| # | Items | Control type | Data type | Description |
|---|-------|---------------|-----------|---------------|
| 1 | Số phiếu | Label/Link | Text | Click mở màn Phiếu điều chuyển (Mục 6.2). |
| 2 | Trạng thái | Tag | Enum | Mới / Đã duyệt — chung cho cả 4 loại. |
| 3 | Ngày chuyển SPMM | Label | Date | Ngày Phê duyệt; để trống ("—") khi còn "Mới". |
| 4 | Loại điều chuyển | Label + bộ lọc | Text | Tên loại đầy đủ; có bộ lọc riêng theo Loại điều chuyển. |
| 5 | Căn cứ | Không hiển thị | — | Xem trong chi tiết phiếu (Mục 6.2 field 4). |
| 6 | Đơn vị xuất | Label | Text | Format "Mã đơn vị - Tên đơn vị" (vd "CYX-05 - Cơ yếu X"). |
| 7 | Đơn vị nhận | Label | Text | Format giống field 6. |
| 8 | Người tạo | Label | Text | Format "Tài khoản - Họ tên đầy đủ". |
| 9 | Thời gian tạo | Label | Datetime | `dd/mm/yyyy hh:mm`. |
| 11 | Thao tác | Button group (icon) | — | — |
| 12 | Bộ lọc (loại/trạng thái/đơn vị/thời gian) | Dropdown + Date range | — | Lọc theo phạm vi dữ liệu Mục 4.1. |
| 13 | Nút "+ Điều chuyển SPMM" | Button | — | Mở màn Phiếu điều chuyển ở trạng thái Mới. |


### 6.2 Phiếu điều chuyển (tạo/xem — dùng chung cho 4 loại) — `tao-phieu-dieu-chuyen` (Mới) / `phieu-dieu-chuyen-daduyet` (Đã duyệt)

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/dieu-chuyen-flow.md#screen-tao-phieu-dieu-chuyen--lậpxem-phiếu-trạng-thái-mới) · HTML wireframe: chưa có (chạy `/wireframe-html`). Figma: 3 biến thể cùng màn — Frame "196:381" (Theo Số phiếu căn cứ), "196:2927" (Theo SPMM), "216:4921" (loại 4, tham khảo trực quan) — đều trong page "DCSPMM", section "Điều chuyển SPMM v2".

**Cấu trúc:** A. Thông tin chung → B1. Thông tin chi tiết (cây 2 view + modal "Danh sách tồn kho chi tiết" + modal "Cập nhật số serial SPMM" + "Phân bổ tồn kho" + ô quét Serial; loại (4) khác ở Đơn vị nhận/Kho nhận, ẩn cột hạn mức, thêm cột Vị trí kho nhận) → C. Thao tác dùng chung (Lưu/Hủy bỏ/Phê duyệt/Bỏ duyệt — vòng đời Mục 5).

**A. Thông tin chung**

Bố cục: Số phiếu · Ngày điều chuyển · Loại điều chuyển · Căn cứ điều chuyển → Đơn vị xuất · Kho xuất · Đơn vị nhận · Kho nhận → Mô tả · Lý do bỏ duyệt.

| # | Items | Control type | Data type | Description |
|---|-------|---------------|-----------|---------------|
| 1 | Số phiếu | Label | Text | Tự sinh khi lưu "Mới" lần đầu. |
| 2 | Ngày điều chuyển | Date input | Date | Mặc định hôm nay. Bắt buộc. Khóa sau "Đã duyệt". |
| 3 | Loại điều chuyển | Dropdown | Text | Chọn 1 trong 4 loại; tạm thời hiển thị đủ cả 4 loại cho mọi người dùng, không lọc theo Loại đơn vị (quyết định tạm — xem `OQ-13`). Quyết định căn cứ hợp lệ ở field 4. Chỉ sửa khi "Mới". |
| 4 | Căn cứ điều chuyển | Dropdown/Search multi-select | Text | Loại (1): Hợp đồng sản xuất (chọn nhiều). Loại (2)/(3): QĐGCTKH, chọn nhiều (`BR-dieu-chuyen-spmm-002`). Loại (4): Số công văn quyết định — nhập text. Loại (1)/(2)/(3) chỉ chọn căn cứ còn hạn mức (`FR-dieu-chuyen-spmm-011`). Bắt buộc. |
| 5 | Đơn vị xuất | Dropdown | Text | Mặc định = đơn vị người tạo, chọn lại trong phạm vi phân quyền. Loại (4): Đơn vị nhận = Đơn vị xuất. Chỉ sửa khi "Mới". |
| 6 | Kho xuất | Dropdown | Text | Bắt buộc. Danh sách theo Đơn vị xuất; tự chọn mặc định nếu xác định được. Chỉ sửa khi "Mới". |
| 7 | Đơn vị nhận | Dropdown/Readonly | Text | Loại (1)/(3): theo Căn cứ. Loại (2): Đơn vị xuất hoặc đơn vị con. Loại (4): = Đơn vị xuất, readonly. Bắt buộc. Chỉ sửa khi "Mới". |
| 8 | Kho nhận | Dropdown | Text | Bắt buộc, khác Kho xuất. Loại (4): cùng đơn vị với Kho xuất (`FR-dieu-chuyen-spmm-029`), vẫn chọn tay. Chỉ sửa khi "Mới". |
| 9 | Mô tả | Textarea | Text | Ghi chú tự do, không bắt buộc. Chỉ sửa khi "Mới". |
| 9.1 | Lý do bỏ duyệt | Textbox readonly | Text | Ghi qua popup "Bỏ duyệt" (khối C); hiển thị lại trên phiếu, ghi đè mỗi lần Bỏ duyệt. |

**B1. Thông tin chi tiết — loại (1)/(2)/(3)**

Cây 3 cấp, đổi chiều nhóm qua "Xem theo": cấp 1/2 = Số phiếu căn cứ và Mã SPMM (thứ tự tùy view), cấp 3 = Serial (mặc định ẩn). Số liệu tổng hợp (Tồn kho, SL đề nghị, SL đề nghị còn lại, Số lượng chuyển) hiển thị ở dòng nhóm, không lặp ở dòng Serial.

*B1.1 Thành phần màn hình*

| # | Items | Control type | Data type | Description |
|---|-------|---------------|-----------|---------------|
| 10 | Xem theo | Dropdown | Enum | "Theo Số phiếu căn cứ" (mặc định) / "Theo SPMM" — đổi chiều nhóm cấp 1/2, dùng chung 1 dataset. |
| 11 | Thông tin chi tiết | Table (cây 3 cấp) | — | Xem mô tả cấu trúc ở trên. |
| 12 | Số phiếu căn cứ | Label | Text | Ở dòng nhóm theo "Xem theo" (cấp 1 nếu đang "Theo Số phiếu căn cứ", cấp 2 nếu "Theo SPMM"). |
| 13 | Mã SPMM · Tên SPMM · ĐVT | Label | Text | Ở dòng nhóm còn lại (ngược field 12). |
| 14 | Tồn kho | Label | Number | Tồn vật lý tại Kho xuất, tổng theo dòng nhóm. |
| 15 | SL đề nghị | Label | Number | SL được đề nghị/duyệt theo (các) căn cứ thuộc nhóm. |
| 16 | SL đề nghị còn lại | Label | Number | Hạn mức còn lại (`FR-dieu-chuyen-spmm-011`). |
| 17 | Số lượng chuyển | Number input | Number | Nhập tại dòng nhóm cấp 2. Bắt buộc. Vượt SL đề nghị còn lại → cảnh báo ngay tại ô; chặn khi Phê duyệt (`BR-dieu-chuyen-spmm-002`). |
| 18 | Serial (cấp 3) | Label | Text | Mặc định thu gọn, mở qua icon ▾ ở dòng nhóm. |
| 19 | Vị trí kho xuất (cấp 3) | Label | Text | Vị trí tồn kho nguồn của Serial. |
| 20 | "+" (thêm dòng tồn kho) | Icon button | — | Mở modal "Danh sách tồn kho chi tiết" (B1.2) cho đúng dòng nhóm. |
| 21 | Phân bổ tồn kho | Button (dưới "Xem theo") | — | Tự chọn tồn kho theo FIFO cho dòng nhóm đang chọn (`FR-dieu-chuyen-spmm-006`); bấm lại thì tính lại từ đầu theo tồn kho mới nhất, không cộng dồn. Chỉ khả dụng khi "Mới". |
| 21.1 | Kết xuất tồn kho | Button (cạnh field 21) | — | Xuất Excel toàn bộ tồn kho hiện tại tại Kho xuất — cột STT/Vị trí lưu kho/Serial/Mã SPMM/Tên SPMM/Phiếu nhập kho/Ngày nhập kho. Không phụ thuộc dòng nhóm đang chọn. Khả dụng cả "Mới" và "Đã duyệt". |
| 22 | Ô quét Serial | Input/Scanner | Text | Cùng hàng với field 21/21.1, lề phải trên bảng. Serial hợp lệ → tự thêm dòng cấp 3 + tăng Số lượng chuyển; không hợp lệ → chặn, báo lỗi ngay. Chỉ khả dụng khi "Mới". |
| 23 | Xóa dòng | Icon button | — | Chỉ khi "Mới". Xóa dòng (nhóm hoặc Serial) gỡ Serial ra khỏi danh sách phiếu, không ảnh hưởng tồn kho (chỉ cập nhật lúc Phê duyệt). Dòng nhóm đã có Serial → xác nhận trước khi xóa; chưa có Serial thì xóa thẳng. |
| 24 | Tổng số lượng chuyển | Label | Number | Tổng SUM(Số lượng chuyển) toàn bảng, mọi nhóm. |

> Mỗi cặp Số phiếu căn cứ × SPMM là 1 nhóm riêng, tính hạn mức độc lập theo từng căn cứ — không gộp SL khi 2 dòng cùng SPMM khác căn cứ.

*B1.2 Modal "Danh sách tồn kho chi tiết" (mở từ "+")*

| # | Items | Control type | Data type | Description |
|---|-------|---------------|-----------|---------------|
| 26 | Số phiếu căn cứ / SPMM / Loại SPMM / ĐVT / SL đề nghị còn lại / Tổng số lượng xuất | Label | — | Ngữ cảnh đầu modal, kế thừa từ dòng nhóm đã mở. |
| 27 | Danh sách tồn kho | Table + Checkbox, sắp xếp theo cột | — | Cột: STT · Vị trí kho · Số phiếu nhập (PNK) · Ngày nhập kho · SL tồn kho. Có hàng lọc dưới tiêu đề. Loại (1): chỉ PNK thuộc Hợp đồng đã chọn ở field 4; loại (2)/(3)/(4): toàn bộ tồn của SPMM tại Kho xuất. |
| 28 | Tick chọn dòng tồn kho | Checkbox | — | Chọn tay dòng tồn kho cho dòng nhóm đang thao tác. |
| 29 | Lưu | Button | — | Ghi các dòng đã tick (SPMM + Vị trí kho xuất) vào bảng chính (cấp 3, mặc định ẩn) — dùng tiếp modal "Cập nhật số serial SPMM" (B1.3) hoặc ô quét (field 22) để ghi Serial thực tế trước khi Phê duyệt. |

> Wireframe: [[../ascii-wireframe/dieu-chuyen-flow.md#screen-modal-danh-sach-ton-kho-chi-tiet--modal-danh-sách-tồn-kho-chi-tiết|modal-danh-sach-ton-kho-chi-tiet]] · Figma: Frame "196:697" (page "DCSPMM", section "Điều chuyển SPMM v2").

*B1.3 Modal "Cập nhật số serial SPMM"*

| # | Items | Control type | Data type | Description |
|---|-------|---------------|-----------|---------------|
| 31 | Mã SPMM / Tên SPMM / Số lượng SPMM cần / Số lượng thực tế ghi nhận | Label | — | Ngữ cảnh đầu modal, kế thừa từ dòng tồn kho vừa thêm. |
| 32 | Nhập/Scan số serial | Tab + Input | Text | Quét hoặc gõ tay từng Serial. |
| 33 | Nhập số Serial theo dải | Tab + Input | Text | Sinh danh sách theo Tiền tố/Hậu tố/Từ/Đến/Độ dài. |
| 34 | Thông số Serial đã ghi nhận | Table | — | Serial đã quét/nhập cho dòng SPMM + Vị trí kho xuất này. |
| 35 | Lưu | Button | — | Ghi Serial vào dòng cấp 3 tương ứng trên bảng chính. |

> Wireframe: [[../ascii-wireframe/dieu-chuyen-flow.md#screen-modal-cap-nhat-so-serial--modal-cập-nhật-số-serial-spmm|modal-cap-nhat-so-serial]] · Figma: Frame "196:1057" (page "DCSPMM", section "Điều chuyển SPMM v2").


**B1. Thông tin chi tiết — loại (4)**

Dùng chung cấu trúc bảng "Thông tin chi tiết" với loại (1)/(2)/(3) ở trên. Khác biệt:

| # | Items | Control type | Data type | Description |
|---|-------|---------------|-----------|---------------|
| 6 | Kho xuất (loại 4) | Dropdown | Text | Mặc định = kho đầu tiên của Đơn vị xuất, chọn lại được. |
| 7 | Đơn vị nhận (loại 4) | Dropdown, khóa = Đơn vị xuất | Text | = Đơn vị xuất (field 5) — chỉ chuyển nội bộ trong cùng 1 đơn vị. |
| 8 | Kho nhận (loại 4) | Dropdown, bắt buộc (*) | Text | Chọn tay trong Kho thuộc Đơn vị nhận, khác Kho xuất (field 6) — không có mặc định tự động. |
| 12 (loại 4) | Nhãn dòng nhóm cấp 1 | Label | Text | "Số chứng từ căn cứ" thay vì "Số phiếu căn cứ" (loại 1/2/3) — giá trị lấy từ field 4. |
| 15, 16 | SL đề nghị / SL đề nghị còn lại (loại 4) | Ẩn | — | Loại (4) không áp dụng hạn mức nên ẩn ở dòng nhóm. |
| 19.1 | Vị trí kho nhận (cấp 3, loại 4) | Label | Text | Song song "Vị trí kho xuất" (field 19) — vị trí cất Serial tại Kho nhận. Chỉ hiện cho loại (4), vì Kho nhận là 1 kho cụ thể khác Kho xuất trong CÙNG đơn vị (field 8) nên cần biết vị trí cất hàng nội bộ. |

Khi Phê duyệt: cập nhật tồn kho như loại (1)/(2)/(3) — giảm Kho xuất, tăng Kho nhận (2 kho thật khác nhau).

So với loại (1)/(2)/(3): chỉ khác ở field 7 (Đơn vị nhận khóa = Đơn vị xuất),
ẩn cột "SL đề nghị"/"SL đề nghị còn lại", nhãn dòng nhóm đổi thành "Số chứng
từ căn cứ" (field 12), và thêm cột "Vị trí kho nhận" (field 19.1) ở dòng
Serial — mọi thao tác khác (modal tồn kho, Phân bổ tồn kho FIFO, quét Serial,
Kết xuất tồn kho, validate...) giống hệt loại (1)/(2)/(3).

**C. Thao tác dùng chung (mọi loại điều chuyển)**

| # | Items | Control type | Data type | Description |
|---|-------|---------------|-----------|---------------|
| 40 | Lưu | Button | — | Sinh Số phiếu, chuyển "Mới". Chỉ hiện khi "Mới", cho Cán bộ đơn vị xuất. |
| 41 | Hủy bỏ | Button | — | Thoát không lưu, không sinh phiếu. Chỉ áp dụng trước lần "Lưu" đầu tiên. |
| 42 | Phê duyệt | Button | — | Chỉ hiện khi "Mới", cho người có quyền phê duyệt (Mục 2, 4.2). Kiểm tra: Số lượng chuyển không vượt hạn mức (chỉ áp dụng loại (1)/(2)/(3) — loại (4) không có hạn mức nên bỏ qua điều kiện này), bằng đúng tổng Serial đã ghi nhận, mỗi Serial còn tại Kho xuất (`FR-dieu-chuyen-spmm-010` — tự cập nhật vị trí nếu đổi chỗ, chặn nếu không còn), và tổng SL chuyển theo SPMM/Kho xuất không vượt tồn kho thực tế (`FR-dieu-chuyen-spmm-022`, áp dụng cả 4 loại) — vi phạm bất kỳ điều kiện áp dụng nào thì chặn tại dòng/Serial lỗi. Hợp lệ → "Đã duyệt", cập nhật tồn kho ngay (giảm bên xuất, tăng bên nhận). |
| 43 | Bỏ duyệt | Button + Popup | — | Chỉ hiện khi "Đã duyệt", cho người có quyền phê duyệt. Bắt buộc nhập Lý do (lưu vào field 9.1); xác nhận → hoàn tồn kho theo bút toán đảo ngược (không xóa giao dịch gốc), chuyển phiếu về "Mới". |
| 44 | Tài liệu đính kèm | Button (badge số) | Click | Sửa được (thêm/xóa) khi "Mới"; chỉ xem khi "Đã duyệt". |
| 45 | Lịch sử điều chuyển | Table (readonly) | — | Ghi các mốc Tạo/Lưu/Phê duyệt/Bỏ duyệt (kèm Lý do), mới nhất ở cuối bảng. |
| 46 | In Biên bản bàn giao | Button | — | In được ở mọi trạng thái phiếu, phục vụ bàn giao vật lý ngoài hệ thống. |

> Wireframe: [[../ascii-wireframe/dieu-chuyen-flow.md#screen-phieu-dieu-chuyen-daduyet--phiếu-trạng-thái-đã-duyệt|phieu-dieu-chuyen-daduyet]] · Figma: Frame "196:2121" (page "DCSPMM", section "Điều chuyển SPMM v2"). Nút "Bỏ duyệt" chỉ hiện với người có quyền phê duyệt (Mục 4.2/4.3).

> Wireframe: [[../ascii-wireframe/dieu-chuyen-flow.md#screen-modal-bo-duyet--popup-bỏ-duyệt|modal-bo-duyet]] · Figma: Frame "196:2476" (page "DCSPMM", section "Điều chuyển SPMM v2"). Popup hiện trên nền mờ (scrim) của màn "Phiếu điều chuyển — Đã duyệt" phía sau.


## 7. Yêu cầu chức năng không thuộc màn hình nào

> Chỉ liệt kê yêu cầu KHÔNG gắn với 1 trường/1 màn cụ thể. Yêu cầu cấp-trường/cấp-màn đã nằm trong bảng Mục 6, không lặp lại ở đây.

| ID                        | Yêu cầu                                                                                                                 | Cách kiểm                                                               |
| ------------------------- | ----------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------- |
| `FR-dieu-chuyen-spmm-004` | Chặn lập phiếu loại (1)/(2)/(3) khi căn cứ hết hạn mức. Loại (4) không áp dụng hạn mức.                                 | Căn cứ hết hạn mức không được thêm SPMM; loại (4) vẫn thực hiện được.   |
| `FR-dieu-chuyen-spmm-006` | Phân bổ tồn kho tự động theo FIFO và chỉ lấy đủ số lượng cần. Nếu thiếu tồn, lấy hết số hiện có và cảnh báo phần thiếu. | Cần 5, tồn 3+4 → lấy 3+2; cần 10, tồn 6 → lấy 6 và báo thiếu 4.         |
| `FR-dieu-chuyen-spmm-008` | Cho phép in **Biên bản bàn giao** ở mọi trạng thái phiếu.                                                               | In được khi phiếu **Mới** hoặc **Đã duyệt**.                            |
| `FR-dieu-chuyen-spmm-010` | Khi thêm Serial (quét/modal): chỉ chặn nếu sai SPMM hoặc Serial không thuộc tồn kho tại Kho xuất — không kiểm tra Serial đã thuộc phiếu nào khác. Khi Phê duyệt: kiểm tra lại từng Serial — còn tại Kho xuất thì tự động cập nhật lại Vị trí kho xuất theo vị trí hiện tại; không còn tại Kho xuất (đã bị phiếu khác lấy mất) thì chặn, báo lỗi đúng Serial. | Thêm Serial sai SPMM/không thuộc Kho xuất → chặn ngay. Phê duyệt với Serial đã bị phiếu khác lấy mất → chặn, báo đúng Serial; Serial còn nguyên nhưng đổi vị trí → tự cập nhật, vẫn duyệt được. |
| `FR-dieu-chuyen-spmm-011` | Hạn mức còn lại bằng số lượng được duyệt trừ số lượng đã điều chuyển. Bỏ duyệt sẽ hoàn lại hạn mức.                     | Dùng hết hạn mức thì bị chặn; bỏ duyệt thì hạn mức được phục hồi.       |
| `FR-dieu-chuyen-spmm-020` | Căn cứ theo loại: (1) Hợp đồng sản xuất; (2)/(3) QĐGCTKH; (4) Số công văn quyết định.                                   | Chọn loại điều chuyển thì hiển thị đúng loại căn cứ tương ứng.          |
| `FR-dieu-chuyen-spmm-022` | Khi Phê duyệt, tổng số lượng chuyển của cùng SPMM và Kho xuất (mọi dòng nhóm liên quan) không được vượt tồn kho thực tế tại thời điểm đó.                                         | Tồn 45, điều chuyển 40+40 → chặn khi duyệt; 40+5 hợp lệ.                         |
| `FR-dieu-chuyen-spmm-023` | Mỗi Serial phải gắn đúng với cặp **Căn cứ × SPMM**.                                                                     | Có thể truy ngược đúng căn cứ và SPMM của từng Serial.                  |
| `FR-dieu-chuyen-spmm-025` | Lịch sử lưu các mốc tạo, lưu, duyệt và bỏ duyệt; chỉ được xem, không sửa hoặc xóa.                                      | Lịch sử hiển thị đủ người thực hiện, thời gian, trạng thái và lý do.    |
| `FR-dieu-chuyen-spmm-029` | Loại (4) chỉ chuyển giữa hai kho khác nhau trong cùng đơn vị.                                                           | Đơn vị nhận bằng đơn vị xuất; kho nhận bắt buộc khác kho xuất.          |
| `FR-dieu-chuyen-spmm-032` | Khi duyệt, số lượng chuyển không được vượt tổng hạn mức còn lại của các căn cứ.                                         | Hạn mức 45, nhập 50 → chặn và báo lỗi đúng dòng.                        |
| `FR-dieu-chuyen-spmm-037` | Khi duyệt, số lượng chuyển phải bằng tổng số Serial đã ghi nhận.                                                        | Số lượng 20 nhưng có 5 Serial → chặn và báo thiếu 15.                   |
| `FR-dieu-chuyen-spmm-038` | Chặn bỏ duyệt nếu có Serial đã được điều chuyển tiếp bằng phiếu khác.                                                   | Hiển thị Serial vi phạm và số phiếu đã sử dụng Serial đó.               |
| `FR-dieu-chuyen-spmm-033` | Duyệt thành công sẽ chuyển tồn kho từ kho xuất sang kho nhận.                                                           | Tồn kho hai bên được cập nhật ngay sau khi duyệt.                       |
| `FR-dieu-chuyen-spmm-034` | Khi bỏ duyệt hợp lệ, bắt buộc nhập lý do, hoàn tồn theo từng Serial và chuyển phiếu về **Mới**.                         | Tồn kho được khôi phục; lịch sử giữ cả giao dịch gốc và giao dịch hoàn. |
| `FR-dieu-chuyen-spmm-035` | Loại (1) chỉ hiển thị tồn thuộc hợp đồng đã chọn; loại (2)/(3)/(4) hiển thị toàn bộ tồn tại kho xuất.                   | Danh sách tồn kho được lọc đúng theo loại điều chuyển.                  |
| `FR-dieu-chuyen-spmm-036` | Quét Serial hợp lệ sẽ tự xác định SPMM, vị trí, căn cứ và tăng số lượng chuyển.                                         | Quét một Serial → thêm đúng dòng Serial và tăng số lượng thêm 1.        |

## 8. Quy tắc nghiệp vụ

> Chỉ những quy tắc xuyên nhiều màn hình hoặc không thuộc màn nào. Luật của từng ô/trường nằm trong bảng mô tả màn ở Mục 6.

| ID | Quy tắc | Áp ở |
|----|---------|------|
| `BR-dieu-chuyen-spmm-002` | Loại (2)/(3) sử dụng căn cứ **QĐGCTKH**. Loại (1)/(2)/(3) được điều chuyển nhiều đợt trên cùng căn cứ; mỗi đợt không vượt `MIN(Tồn kho, Hạn mức còn lại)` theo `FR-dieu-chuyen-spmm-011`. Loại (4) không áp dụng hạn mức. | Loại (1)/(2)/(3) — Mục 6.2 field 4 + `FR-004/011/032` |

## 9. Tiêu chí thành công

| # | Tiêu chí | Cách đo |
|---|----------|---------|
| SC-dieu-chuyen-spmm-01 | 100% Serial đã điều chuyển có căn cứ hợp lệ đính kèm — đúng loại căn cứ theo từng loại điều chuyển (Hợp đồng sản xuất — loại (1) / QĐGCTKH — loại (2), (3) / Số công văn quyết định — loại (4)) | Đối chiếu số Serial có căn cứ hợp lệ / tổng số Serial đã điều chuyển, theo từng loại |
| SC-dieu-chuyen-spmm-02 | Tồn kho nguồn/đích khớp tuyệt đối (sai lệch = 0) ngay sau mỗi lần Phê duyệt | So tồn kho hệ thống với kiểm đếm thực tế, lấy mẫu ngẫu nhiên 10% Serial mỗi quý |
| SC-dieu-chuyen-spmm-03 | Tra cứu được kho hiện tại của Serial dựa trên giao dịch điều chuyển Đã duyệt gần nhất. | Điều chuyển một Serial qua nhiều kho, sau đó tra cứu và kiểm tra hệ thống hiển thị đúng kho nhận của phiếu Đã duyệt gần nhất. |

## 10. Câu hỏi mở

> Cột "Mức": `Block` (chặn go-live, phải chốt trước triển khai) / `Hold` (có thể trì hoãn, không chặn go-live) / `Info` (chỉ cần biết, không chặn gì).

| ID | Mức | Câu hỏi | Vì sao quan trọng | Người chốt |
|----|-----|---------|----------------------|-------------|
| OQ-13 | Hold | Đã chốt tạm: dropdown "Loại điều chuyển" (Mục 6.2 field 3) hiển thị đủ cả 4 loại cho mọi người dùng, không lọc/phân quyền theo Loại đơn vị. Giữ mức Hold vì đây là quyết định tạm thời — cần xác nhận lại khi triển khai chính thức. | Nếu sau này cần phân quyền thật theo đơn vị, phải bổ sung ma trận vai trò/đơn vị × Loại điều chuyển vào Mục 4 và kiểm tra ở backend, không chỉ ẩn trên dropdown. | đã chốt tạm |

## 11. Changelog

| Ngày cập nhật | Loại thay đổi | Nguồn/brainstorming liên quan | Người yêu cầu | Nội dung thay đổi |
|-----------------|------------------|-----------------------------------|-------------------|-------------------------|

<!-- wm:d4f7463bbbc7e5517488a623804b7507 -->
