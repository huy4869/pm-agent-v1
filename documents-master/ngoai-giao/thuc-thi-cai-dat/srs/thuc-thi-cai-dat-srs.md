---
type: srs
feature: thuc-thi-cai-dat
status: approved
updated: 2026-09-08
---

# Thực thi cài đặt — Software Requirements Specification

## 1. Phạm vi

**Trong phạm vi:** Ghi nhận việc cài đặt thực tế của SPMM (thông số cài đặt, phiên bản phần mềm/firmware, thông tin người thụ hưởng) lên từng Serial, tại bất kỳ cấp đơn vị nào thực hiện việc cài đặt (Cục, Quân khu, Tỉnh, Phòng kỹ thuật Công an...).

**Ngoài phạm vi:**
- Cấu hình cờ "Cần cài đặt"/"Thông tin quản lý" tại Danh mục SPMM (thuộc chức năng Quản lý dữ liệu/Sản phẩm);
- Nghiệp vụ Nhập kho (Serial phải đã hoàn tất nhập kho trước khi tới được feature này);
- Hiển thị lịch sử cài đặt trên hồ sơ tài sản (chức năng Quản lý Tài sản/Tài sản) — feature này chỉ ghi nhận/cập nhật thông số cài đặt mới nhất khi Hoàn thành (kể cả trường hợp cài lại); phần hiển thị lịch sử sẽ đặc tả riêng sau.

> **Cấu trúc 2 cờ đọc từ Danh mục SPMM (tham khảo — feature này KHÔNG cấu hình, chỉ đọc để validate):**
> - **"Cần cài đặt"** — cờ boolean gắn ở cấp SPMM (Có/Không). Chỉ SPMM có cờ này = Có mới được đưa Serial vào Thực thi cài đặt (BR-thuc-thi-cai-dat-001).
> - **"Thông tin quản lý"** — cấu hình gồm 3 cờ con độc lập ở cấp SPMM: *Thông số cài đặt* / *Phiên bản phần mềm-Firmware* / *Người thụ hưởng* (mỗi cờ `true`/`false`). SPMM không cấu hình cờ con nào (tất cả `false`) → Serial cần ít nhất 1 trong 3 loại thông tin trước khi Hoàn thành (BR-thuc-thi-cai-dat-003); SPMM có ≥1 cờ con `true` → Serial cần đủ TẤT CẢ loại được đánh `true` (BR-thuc-thi-cai-dat-004).

## 2. Actors

| Actor | Loại (người/hệ thống/ngoài) | Mục tiêu | Trong scope? |
|-------|-----------------------------|----------|--------------|
| Cán bộ kỹ thuật tại đơn vị cài đặt | người | Tự ghi nhận tham số cài đặt thực tế ngay tại đơn vị mình cài, không phải qua Cục | Có |
| Cán bộ Trung tâm bảo đảm kỹ thuật (TTBĐKT) / quản lý kỹ thuật | người | Tra cứu phiên bản phần mềm/firmware đã cài trên từng Serial; đối chiếu license (P1) | Có |
| Chức năng Danh mục SPMM | hệ thống (trong vault, feature khác) | Cung cấp cấu hình "Cần cài đặt" + "Thông tin quản lý" cho từng SPMM | Có (dependency) |
| Chức năng Phiếu nhập kho | hệ thống (trong vault, feature khác) | Xác nhận Serial tồn tại + thuộc đúng đơn vị trước khi cho thao tác | Có (dependency) |
| QĐTK / QĐGCTKH | chức năng | Căn cứ pháp lý cho bản ghi Thực thi cài đặt | Có (dependency) |
| Module Tài sản | hệ thống (trong vault, feature khác) | Lưu thông tin tham số cài đặt, phiên bản phần mềm/Firmware... sau khi cấp phát | Có |

## 3. Quy trình nghiệp vụ

| # | Ai làm | Làm gì | Ở đâu |
|---|--------|--------|-------|
| 1 | Cán bộ kỹ thuật | Mở Danh sách, bấm "Tạo mới" | 6.1 |
| 2 | Hệ thống | Mở màn Tạo — Số phiếu CHƯA sinh, hiển thị placeholder "(tự sinh khi Lưu)" | 6.2 |
| 3 | Cán bộ kỹ thuật | Chọn Kho, chọn Căn cứ — ưu tiên QĐTK, dùng QĐGCTKH nếu chưa có QĐTK | 6.2 |
| 4 | Cán bộ kỹ thuật | Thêm Serial qua 1 trong 3 cách: Thêm 1 dòng đơn / Nhập hàng loạt Serial / Nhập từ Excel | 6.2, 6.3, 6.8 |
| 5 | Hệ thống | Kiểm tra SPMM "Cần cài đặt" + Serial đã qua Nhập kho + tồn kho tại Kho đã chọn — hợp lệ thì thêm dòng, không hợp lệ thì báo lỗi tại dòng | 6.2 |
| 6 | Cán bộ kỹ thuật | Nhập hoặc áp dụng hàng loạt Thông số cài đặt, Phiên bản phần mềm/Firmware, Người thụ hưởng cho từng Serial | 6.4, 6.6, 6.7 |
| 7 | Cán bộ kỹ thuật | Bấm "Lưu" để ghi tạm không validate (sinh Số phiếu nếu là lần Lưu đầu tiên) — HOẶC bấm "Hoàn thành" để validate trực tiếp trên dữ liệu đang nhập (không cần Lưu trước) | 6.2 |
| 8 | Hệ thống | Kiểm tra có Serial đã Hoàn thành từ trước không (mở xác nhận cài lại) | 6.10 |
| 9 | Hệ thống | Validate Thông tin quản lý theo đúng cấu hình của từng SPMM — không đạt thì chặn toàn bộ | 6.9 |
| 10 | Hệ thống | Chuyển trạng thái bản ghi sang Hoàn thành | 6.2 |
| 11 | Cán bộ kỹ thuật / TTBĐKT | Tra cứu lại bản ghi, lọc theo Căn cứ / Trạng thái / Đơn vị thực hiện / Người tạo / Thời gian tạo | 6.1 |
| 12 | Cán bộ kỹ thuật / TTBĐKT | Mở Chi tiết để xem lại bản ghi | 6.11 |

## 4. Phân quyền

### 4.1 Quyền theo vai trò

| Quyền | Cho phép |
|-------|----------|
| Xem bản ghi | Mở Danh sách, xem Chi tiết (đọc) |
| Tạo bản ghi | Tạo phiếu mới, thêm/xoá Serial, nhập liệu, Lưu, Hoàn thành, Huỷ bỏ |

- Chỉ cán bộ kỹ thuật được cấp quyền Tạo bản ghi. Đối với bản ghi trạng thái Mới, quyền truy cập/thao tác kiểm soát theo phân quyền người dùng và phạm vi đơn vị: cán bộ thuộc đơn vị tạo bản ghi thao tác theo quyền được cấp; cán bộ thuộc đơn vị khác — nếu chỉ có quyền Xem thì mở được ở **chế độ đọc** (không bị từ chối); còn chỉnh sửa/Lưu/Hoàn thành/Xoá cần được cấp quyền tương ứng (BR-thuc-thi-cai-dat-016).
- TTBĐKT/quản lý kỹ thuật có quyền xem tất cả.

### 4.2 Thao tác theo trạng thái

| Thao tác trên bản ghi | Mới | Hoàn thành |
|--------------------------|:---:|:-------------:|
| Xem chi tiết (chế độ sửa — đơn vị tạo hoặc được cấp quyền sửa) / (chế độ đọc — tài khoản chỉ có quyền Xem) | ✓ (mọi tài khoản có quyền Xem đều mở được, khác nhau ở chế độ sửa/đọc) | ✓ (mọi đơn vị) |
| Thêm/xoá dòng Serial trong bảng | ✓ (đơn vị tạo, hoặc đơn vị khác nếu được cấp quyền sửa) | ✗ |
| Sửa Thông số/Firmware/Người thụ hưởng | ✓ (đơn vị tạo, hoặc đơn vị khác nếu được cấp quyền sửa) | ✗ |
| Lưu (không validate) | ✓ (đơn vị tạo, hoặc đơn vị khác nếu được cấp quyền sửa) | ✗ |
| Hoàn thành | ✓ (đơn vị tạo, hoặc đơn vị khác nếu được cấp quyền sửa) | ✗ |
| Huỷ bỏ (thoát màn, không lưu) | ✓ (đơn vị tạo, hoặc đơn vị khác nếu được cấp quyền sửa) | ✗ |
| Xoá bản ghi (xoá hẳn, tại màn Danh sách) | ✓ (quyền `WH.IE.IE.DL` — đơn vị tạo hoặc được cấp quyền) | ✗ |

## 5. Vòng đời trạng thái

| Entity | Từ trạng thái | Sang trạng thái | Trigger | Quay lại được? |
|--------|-----------------|--------------------|---------|-------------------|
| Bản ghi Thực thi cài đặt | (khởi tạo) | Mới | Bấm "Tạo mới", sinh Số phiếu | — |
| Bản ghi Thực thi cài đặt | Mới | Mới (tự lặp) | Bấm "Lưu", không validate — đơn vị tạo hoặc đơn vị khác nếu được cấp quyền (BR-thuc-thi-cai-dat-016) | Có (lặp lại nhiều lần) |
| Bản ghi Thực thi cài đặt | Mới | Hoàn thành | Bấm "Hoàn thành", đạt validation theo cấu hình SPMM — đơn vị tạo hoặc đơn vị khác nếu được cấp quyền (BR-thuc-thi-cai-dat-016) | Không — một chiều, là trạng thái cuối |
| Bản ghi Thực thi cài đặt | Mới | (đã xoá) | Bấm "Xoá" tại màn Danh sách — đơn vị tạo hoặc đơn vị khác nếu được cấp quyền `WH.IE.IE.DL` (BR-thuc-thi-cai-dat-019) | — |

## 6. Màn hình

### 6.1 danh-sach-thuc-thi-cai-dat — Danh sách thực thi cài đặt

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/thuc-thi-cai-dat-flow.md#screen-danh-sach-thuc-thi-cai-dat--danh-sách-thực-thi-cài-đặt) · [HTML wireframe](../html-wireframe/thuc-thi-cai-dat-flow.html#s1)

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| — | Nút "+ Tạo mới" | Button | Click | • **Navigate** sang màn Tạo thực thi cài đặt, Trạng thái khởi tạo *Mới*, Số phiếu CHƯA sinh (hiện placeholder "(tự sinh khi Lưu)") — chỉ sinh mã thật khi bấm Lưu lần đầu (FR-thuc-thi-cai-dat-019). |
| 1 | STT | Label | ReadOnly | • Căn giữa, đánh số theo trang hiện tại. |
| 2 | Số phiếu | Link | Click | • Mã hệ thống tự sinh khi Lưu lần đầu. Click → *Mới*: đơn vị tạo hoặc đơn vị khác được cấp quyền sửa → mở lại màn Tạo (chế độ sửa); đơn vị khác chỉ có quyền Xem → mở màn Tạo ở **chế độ đọc** (BR-thuc-thi-cai-dat-016); hoàn toàn không có quyền nào → từ chối (E-thuc-thi-cai-dat-009) · *Hoàn thành* mở xem Chi tiết (chỉ đọc). |
| 3 | Căn cứ | Tag | ReadOnly (filter) | • 2 giá trị: *QĐTK* (ưu tiên nếu có) hoặc *QĐGCTKH* (dùng khi chưa có QĐTK). |
| 4 | Số QĐGCTKH/QĐTK | Label | ReadOnly | • Hiển thị đúng số hiệu đã nhập tự do lúc tạo (field 4, Mục 6.2) — không còn navigate (bỏ link, vì input tự do không đảm bảo khớp đúng 1 bản ghi QĐTK/QĐGCTKH thật). |
| 5 | Trạng thái | Tag (màu) | Select (filter) | • *Mới* (lam) / *Hoàn thành* (lục) — theo `COMMON_STATUS_COLOR`. *Hoàn thành* = đã bấm nút Hoàn thành ở màn Tạo, hết dòng lỗi. |
| 6 | Đơn vị thực hiện | Label | ReadOnly (filter) | • Đơn vị đã ghi nhận bản ghi này — bất kỳ cấp nào (Cục/Quân khu/Tỉnh/Phòng kỹ thuật...). |
| 7 | Người tạo | Label | ReadOnly (filter) | • Tài khoản đã tạo bản ghi. |
| 8 | Thời gian tạo | Label | ReadOnly (filter) | • Ngày giờ tạo bản ghi lần đầu. |
| — | Hàng lọc (dưới header cột) | Dropdown "Chọn..." theo cột | Select | • Lọc ngay tại từng cột — tất cả cột đều là dropdown chọn giá trị có sẵn (không có ô Tìm kiếm rời, không có calendar filter riêng). |
| — | Thao tác | Button (icon, không nền) | Click | • *(xem)* mở Chi tiết (`chi-tiet-thuc-thi-cai-dat`) · *(xoá)* chỉ hiện với bản ghi trạng thái *Mới* — xoá hẳn bản ghi, theo quyền `WH.IE.IE.DL` (đơn vị tạo hoặc được cấp quyền, BR-thuc-thi-cai-dat-019), yêu cầu xác nhận trước khi xoá. |
| — | Empty state | Label | ReadOnly | • Hiện khi chưa có bản ghi nào khớp bộ lọc — bảng chỉ còn header + hàng lọc. |

### 6.2 tao-thuc-thi-cai-dat — Tạo thực thi cài đặt

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/thuc-thi-cai-dat-flow.md#screen-tao-thuc-thi-cai-dat--tạo-thực-thi-cài-đặt) · [HTML wireframe](../html-wireframe/thuc-thi-cai-dat-flow.html#s2) (chế độ Trải phẳng: [#s2b](../html-wireframe/thuc-thi-cai-dat-flow.html#s2b))

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| — | Nút "Hủy bỏ" | Button | Click | • Có dữ liệu chưa Lưu (FR-thuc-thi-cai-dat-022) → cảnh báo mất dữ liệu trước khi thoát; không thì thoát thẳng về `danh-sach-thuc-thi-cai-dat`. |
| — | Nút "Lưu" | Button | Click | • Lần Lưu đầu tiên: hệ thống **sinh Số phiếu chính thức** (FR-thuc-thi-cai-dat-019). KHÔNG validate Thông tin quản lý (Thông số/Firmware/Người thụ hưởng — BR-thuc-thi-cai-dat-005) — lưu nguyên trạng dù còn thiếu. Có ≥1 dòng lỗi cứng (Serial chưa nhập kho/chưa chọn Kho hợp lệ) → **chặn toàn bộ nút Lưu**, không lưu được dòng nào cho tới khi sửa lại Serial hoặc xoá dòng lỗi đó.Trường hợp bản ghi đã được người dùng khác cập nhật (Lưu hoặc Hoàn thành) trong thời gian người dùng hiện tại đang thao tác, hệ thống không cho phép lưu đè dữ liệu. Hiển thị thông báo yêu cầu người dùng tải lại bản ghi để lấy dữ liệu mới nhất trước khi tiếp tục chỉnh sửa (E-thuc-thi-cai-dat-008). |
| — | Nút "Hoàn thành" | Button | Click → có thể mở modal lỗi | • **Không yêu cầu bấm Lưu trước** — validate chạy trực tiếp trên dữ liệu đang nhập trên màn. Nút LUÔN cho bấm (không disable trong bất kỳ trường hợp nào, kể cả 0 Serial).<br>• **Kiểm tra danh sách Serial**: Bảng Thông tin chi tiết phải có ít nhất 01 Serial. Nếu không có Serial → chặn Hoàn thành và thông báo "Chưa có Serial nào."<br>• **Kiểm tra Thông tin quản lý của từng Serial**: Hệ thống đọc cấu hình hiện tại (live) của SPMM tại thời điểm người dùng bấm Hoàn thành và validate từng Serial (BR-thuc-thi-cai-dat-002/003/004/012) — SPMM không cấu hình cụ thể Thông tin quản lý → Serial phải có ít nhất 01 trong 03 loại thông tin: Thông số cài đặt / Firmware / Người thụ hưởng; SPMM có cấu hình Thông tin quản lý → Serial phải có đầy đủ tất cả các loại thông tin được cấu hình `true`. Cờ "Cần cài đặt" KHÔNG được đọc lại (live) ở bước này — chỉ gate một lần lúc thêm Serial (BR-thuc-thi-cai-dat-001), đổi cờ giữa chừng không ảnh hưởng tới Hoàn thành.<br>• **Kiểm tra lại tồn kho theo Kho hiện tại**: Nếu người dùng đã đổi field "Kho" (2b) sau khi thêm Serial, hệ thống validate lại tồn kho của TỪNG Serial theo đúng Kho đang chọn tại thời điểm Hoàn thành (live) — Serial nào không có tồn tại ở Kho hiện tại → chặn Hoàn thành, báo lỗi tại dòng đó (E-thuc-thi-cai-dat-017, cùng modal `2-5-khong-the-hoan-thanh`).<br>• **Kiểm tra trường hợp cài lại**: Nếu có ít nhất 01 Serial đã từng thuộc một bản ghi Hoàn thành trước đó → hiển thị modal Xác nhận cài lại (FR-thuc-thi-cai-dat-023, màn `tao-thuc-thi-cai-dat-2-6-xac-nhan-cai-lai`). Chỉ tiếp tục Hoàn thành khi người dùng xác nhận cài lại.<br>• **Kiểm tra xung đột phiên bản (concurrent)**: Nếu bản ghi đã được người dùng khác cập nhật (Lưu hoặc Hoàn thành) trong thời gian người dùng hiện tại đang thao tác → chặn Hoàn thành, thông báo yêu cầu tải lại bản ghi trước khi tiếp tục (E-thuc-thi-cai-dat-008, áp dụng cùng cơ chế như nút Lưu).<br>• **Xử lý khi không đạt validation**: Nếu bất kỳ Serial nào không đáp ứng một trong các điều kiện bắt buộc → chặn toàn bộ thao tác Hoàn thành. Không Serial nào được xử lý/chuyển trạng thái riêng lẻ. Hiển thị modal `tao-thuc-thi-cai-dat-2-5-khong-the-hoan-thanh`, chỉ rõ Serial và nội dung cần bổ sung/xử lý (E-thuc-thi-cai-dat-004, BR-thuc-thi-cai-dat-006).<br>• **Xử lý khi tất cả điều kiện hợp lệ**: Chuyển trạng thái toàn bộ bản ghi sang Hoàn thành; không quản lý trạng thái Hoàn thành riêng trên từng Serial. Điều hướng người dùng về màn Danh sách Thực thi cài đặt.<br>• **Phân quyền**: Người dùng thuộc đơn vị tạo bản ghi thao tác theo quyền được cấp; người dùng thuộc đơn vị khác chỉ thực hiện được khi có quyền tương ứng (BR-thuc-thi-cai-dat-016). |
| 1 | Số phiếu | Label | ReadOnly | • Trước khi Lưu: hiện placeholder "(tự sinh khi Lưu)". Mã hệ thống tự sinh khi bấm Lưu lần đầu, không sửa được (FR-thuc-thi-cai-dat-019). |
| 2 | Đơn vị thực hiện | Label | ReadOnly | • Tự động = đơn vị đang đăng nhập. |
| 2b | Kho | Dropdown | Select | • **Bắt buộc**. Danh sách chỉ liệt kê các Kho thuộc Đơn vị thực hiện (field 2) đang đăng nhập. Mặc định tự động chọn Kho đầu tiên trong danh sách, cho phép chọn lại. Mọi validate tồn kho của Serial (field 8, modal Nhập hàng loạt Serial, Nhập từ Excel) áp dụng theo đúng Kho đã chọn ở đây (BR-thuc-thi-cai-dat-010, E-thuc-thi-cai-dat-017). Đổi Kho SAU KHI đã có Serial trong bảng → giữ nguyên các dòng Serial đã thêm (không xoá, không validate lại ngay); hệ thống validate lại tồn kho theo Kho mới tại bước Hoàn thành — Serial nào không có tồn tại ở Kho mới sẽ báo lỗi và chặn Hoàn thành (E-thuc-thi-cai-dat-017). |
| 3 | Căn cứ | Dropdown | Select | • **Bắt buộc**. 2 giá trị: QĐTK (ưu tiên) / QĐGCTKH (dùng khi chưa có QĐTK) — FR-thuc-thi-cai-dat-001. |
| 4 | Số QĐGCTKH/QĐTK | Textbox | Text | • **Bắt buộc**. Nhập trực tiếp số hiệu QĐGCTKH/QĐTK (không chọn từ danh sách). |
| 5 | Người tạo | Label | ReadOnly | • Tài khoản đang đăng nhập. |
| 6 | Thời gian tạo | Label | ReadOnly | • Tự sinh lúc bắt đầu tạo. |
| 7 | Ghi chú | Textbox | Text | • Không bắt buộc. |
| — | Tài liệu đính kèm | File upload | Upload | • Không bắt buộc — đính kèm chứng từ liên quan (biên bản cài đặt...), FR-thuc-thi-cai-dat-018. |
| — | Nút "+ Thêm 1 dòng" | Button | Click | • Chèn thẳng 1 dòng trống EDITABLE vào cuối bảng (Serial/SPMM/Firmware/Thông số/Người thụ hưởng nhập trực tiếp trên dòng) — FR-thuc-thi-cai-dat-002. Danh sách chọn SPMM chỉ liệt kê SPMM "Cần cài đặt"=Có (FR-thuc-thi-cai-dat-005). |
| — | Nút "Nhập hàng loạt Serial" | Button | Click → mở modal | • Mở `tao-thuc-thi-cai-dat-2-1-nhap-hang-loat-serial` (FR-thuc-thi-cai-dat-003). |
| — | Nút "Nhập từ Excel" | Button | Click → mở modal 2 bước | • Mở `tao-thuc-thi-cai-dat-2-4-nhap-tu-excel` (FR-thuc-thi-cai-dat-004). |
| — | Toggle "Chế độ xem" | Segmented control | Select | • *Theo SPMM* (mặc định — nhóm Serial theo Mã SPMM, gập/mở) / *Trải phẳng* (1 dòng = 1 Serial) — dùng chung 1 nguồn dữ liệu, đổi chế độ KHÔNG mất lựa chọn checkbox đang tick (FR-thuc-thi-cai-dat-021). |
| — | Hàng lọc (dưới header cột) | Textbox/Dropdown theo cột | Text/Select | • *Theo SPMM*: tìm Mã SPMM/Tên SPMM/Serial. *Trải phẳng*: thêm lọc Mã SPMM. |
| — | Dòng nhóm SPMM (Theo SPMM) | Row gập/mở | Click → expand/collapse | • Hiện tên SPMM đầy đủ + icon ⓘ + tổng số Serial. |
| — | Icon ⓘ (cạnh SPMM) | Icon button | Click → mở popover | • Mở popover "Yêu cầu thông tin quản lý" của đúng SPMM đó — liệt kê thông tin bắt buộc theo cấu hình, hoặc "cần ≥1 trong 3 loại" nếu SPMM không cấu hình gì (FR-thuc-thi-cai-dat-020). |
| — | Checkbox dòng/nhóm | Checkbox | Select | • Chọn Serial để dùng với Thanh hành động. Checkbox nhóm = chọn toàn bộ Serial thuộc SPMM đó. |
| — | Thanh hành động (hiện khi có dòng được tick) | Contextual bar | — | • "Đã chọn N Serial" + nút: *Áp dụng thông số cài đặt* (chỉ enable khi mọi Serial đang chọn CÙNG 1 SPMM — mở `2-2-ap-dung-thong-so-hang-loat`, FR-thuc-thi-cai-dat-009, BR-thuc-thi-cai-dat-009) · *Áp dụng Firmware* (cùng điều kiện — mở `2-2c-ap-dung-firmware`, FR-thuc-thi-cai-dat-010) · *Nhập nhanh người thụ hưởng* (mở `2-3-nhap-nhanh-nguoi-thu-huong`, FR-thuc-thi-cai-dat-011) · *Xoá các dòng đã chọn* (≥2 dòng bắt buộc xác nhận — FR-thuc-thi-cai-dat-012) · *Bỏ chọn*. |
| 8 | Serial | Textbox (chọn/gõ) | Text/Select | • **Bắt buộc**. Phải đã tồn tại/qua Nhập kho — chưa tồn tại thì báo lỗi tại dòng, chặn thêm dòng đó (E-thuc-thi-cai-dat-001). SPMM tương ứng phải "Cần cài đặt"=Có tại thời điểm thêm dòng, ngược lại chặn cứng (E-thuc-thi-cai-dat-002). Serial đã có sẵn trong phiếu đang tạo → chặn thêm trùng (E-thuc-thi-cai-dat-010, BR-thuc-thi-cai-dat-014). Serial phải **có tồn kho tại Kho đã chọn** (field 2b) — tồn tại nhưng ở Kho khác (kể cả cùng Đơn vị thực hiện) → chặn thêm, báo lỗi tại dòng (BR-thuc-thi-cai-dat-010, E-thuc-thi-cai-dat-017). |
| 9 | Đơn vị tính | Label | ReadOnly | • Tự động lấy theo cấu hình của SPMM tương ứng — luôn đi kèm SPMM, không nhập tay, không sửa được ở dòng Serial. |
| 10 | SPMM (Mã + Tên) | Label | ReadOnly | • Ở Theo SPMM: tên đầy đủ trên dòng nhóm + cột "SPMM" riêng trên từng dòng Serial (đối chiếu nhanh, không thay thế dòng nhóm). Ở Trải phẳng: mỗi dòng hiện cả Mã + Tên SPMM. |
| 11 | Thông số cài đặt | Link "N thông số ›" hoặc "Chưa nhập ›" | Click → mở modal | • Bắt buộc hay không phụ thuộc cấu hình SPMM — field LUÔN cho nhập kể cả khi không bắt buộc (FR-thuc-thi-cai-dat-006). Modal con: Tên thông số (text tự do)/Giá trị/Ngày hết hạn (tuỳ chọn) — chặn Lưu (báo lỗi inline) nếu: sai định dạng `dd/mm/yyyy`; HOẶC ngày không tồn tại theo lịch (vd 31/02, 30/02); HOẶC ngày hết hạn **nhỏ hơn ngày cài đặt** (E-thuc-thi-cai-dat-006). |
| 12 | Phiên bản phần mềm/Firmware | Textbox | Text | • Bắt buộc hay không phụ thuộc cấu hình SPMM, nhưng LUÔN hiện + cho nhập (FR-thuc-thi-cai-dat-007). |
| 13 | Người thụ hưởng | Link "{Họ tên} ›" hoặc "Chưa nhập ›" | Click → mở modal | • Bắt buộc hay không phụ thuộc cấu hình SPMM, field vẫn LUÔN mở được để nhập (FR-thuc-thi-cai-dat-008). Modal 4 trường Họ tên/Mã định danh/Chức vụ/Đơn vị triển khai — cả 4 bắt buộc-khi-mở, thiếu ≥1 → chặn dòng đó, highlight trường thiếu (E-thuc-thi-cai-dat-005). |
| — | Thao tác (mỗi dòng, menu kebab) | Button (icon " ⋮ ") | Click → mở menu | • "Xoá dòng" — xoá 1 dòng khỏi bảng trước khi Lưu, KHÔNG cần xác nhận (FR-thuc-thi-cai-dat-012). |
| — | Dòng lỗi cứng (Serial chưa nhập kho / không tồn tại tại Kho đã chọn) | Label (đỏ) | ReadOnly | • Chặn **toàn bộ** nút Lưu (không lưu được bất kỳ dòng nào, kể cả dòng hợp lệ khác) cho tới khi sửa lại Serial hoặc xoá dòng lỗi đó. |
| — | Mọi thao tác trên bảng | — | — | • Chỉ là dữ liệu NHÁP trên màn đang mở, CHƯA lưu chính thức — mất nếu đóng màn/mất kết nối trước khi Lưu (BR-thuc-thi-cai-dat-011). Mất kết nối/lỗi hệ thống khi Lưu/Hoàn thành → giữ nguyên dữ liệu đang nhập, báo lỗi, cho thử lại (E-thuc-thi-cai-dat-011). |

### 6.3 tao-thuc-thi-cai-dat-2-1-nhap-hang-loat-serial — Nhập hàng loạt Serial (modal 1 màn)

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/thuc-thi-cai-dat-flow.md#screen-tao-thuc-thi-cai-dat-2-1-nhap-hang-loat-serial--nhập-hàng-loạt-serial-modal-1-màn) · [HTML wireframe](../html-wireframe/thuc-thi-cai-dat-flow.html#s3)

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| 1 | SPMM | Dropdown (search) | Select | • **Bắt buộc**. 1 lần nhập hàng loạt chỉ áp dụng cho 1 SPMM. Danh sách chỉ liệt kê SPMM "Cần cài đặt"=Có. |
| 2 | Quét/Nhập Serial | Textbox (hỗ trợ scanner) | Text | • Nhập tay hoặc quét mã vạch → Enter → Serial tự động thêm vào "Danh sách Serial" bên phải. Vượt 5.000 Serial → báo lỗi ngay, chặn tiếp tục (E-thuc-thi-cai-dat-016, NFR-thuc-thi-cai-dat-003). |
| 3 | Danh sách Serial | List (đọc/xoá từng dòng) | — | • Hiện các Serial đã quét/nhập, đồng bộ realtime với bảng "Kết quả kiểm tra" bên dưới ở trạng thái "Chưa kiểm tra". |
| — | Nút "Kiểm tra Serial" | Button | Click | • Validate toàn bộ danh sách — mỗi Serial nhận *Hợp lệ* hoặc lỗi cụ thể (*Serial không tồn tại* / *Không thuộc SPMM đã chọn* / *Không có tồn tại tại Kho đã chọn*, E-thuc-thi-cai-dat-017). Bấm lại được nhiều lần. |
| 4 | Bảng "Kết quả kiểm tra" | Table (readonly) | — | • Mỗi dòng: STT/Serial/Kết quả. KHÔNG có case "Khác đơn vị" — chỉ *Hợp lệ* hoặc lỗi chặn. |
| — | Nút "Huỷ" | Button | Click | • Đóng modal, không thêm gì vào bảng chính. |
| — | Nút "Xác nhận" | Button | Click, **disabled mặc định** | • Chỉ enable sau khi đã bấm "Kiểm tra Serial" và có ≥1 Serial *Hợp lệ*. Bấm → insert các Serial *Hợp lệ* vào bảng "Thông tin chi tiết" của màn chính ở trạng thái CHƯA có thông số/firmware/người thụ hưởng, đóng modal (FR-thuc-thi-cai-dat-003). |

### 6.4 tao-thuc-thi-cai-dat-2-2-ap-dung-thong-so-hang-loat — Áp dụng thông số hàng loạt (modal)

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/thuc-thi-cai-dat-flow.md#screen-tao-thuc-thi-cai-dat-2-2-ap-dung-thong-so-hang-loat--áp-dụng-thông-số-hàng-loạt-modal) · [HTML wireframe](../html-wireframe/thuc-thi-cai-dat-flow.html#s4)

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| — | "Áp dụng cho: N Serial" + link "Xem danh sách" | Label + Link | Click → bung/thu danh sách | • Soát lại đúng N Serial nào đang được áp dụng trước khi ghi. |
| — | SPMM đang áp dụng | Label | ReadOnly | • Xác nhận lại đúng 1 Mã SPMM của các Serial đang chọn (BR-thuc-thi-cai-dat-009). Hiện kèm Đơn vị tính tự động theo SPMM đó. |
| 1 | Thông số cài đặt (bảng con) | Table inline (Tên thông số/Giá trị/Ngày hết hạn) | Text | • Mở LUÔN 1 dòng TRỐNG (không preload). Ngày hết hạn không bắt buộc nhưng sai `dd/mm/yyyy`, ngày không tồn tại theo lịch, hoặc nhỏ hơn ngày cài đặt → lỗi inline, chặn Áp dụng (E-thuc-thi-cai-dat-006). |
| — | Nút "Huỷ" | Button | Click | • Đóng modal, không đổi gì. |
| — | Nút "Áp dụng" | Button | Click, **disabled mặc định** | • Enable khi ≥1 dòng có ĐỦ cả Tên thông số và Giá trị. Bấm → mở tiếp `tao-thuc-thi-cai-dat-2-2b-xac-nhan-ap-dung` TRƯỚC khi ghi thật (FR-thuc-thi-cai-dat-009). |

### 6.5 tao-thuc-thi-cai-dat-2-2b-xac-nhan-ap-dung — Xác nhận áp dụng thông số (modal, con của 2-2)

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/thuc-thi-cai-dat-flow.md#screen-tao-thuc-thi-cai-dat-2-2b-xac-nhan-ap-dung--xác-nhận-áp-dụng-thông-số-modal-con-của-2-2) · [HTML wireframe](../html-wireframe/thuc-thi-cai-dat-flow.html#s5)

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| — | Danh sách thông số sắp áp dụng | Label list | ReadOnly | • Liệt kê từng cặp Tên thông số = Giá trị vừa nhập, để soát lại trước khi ghi. |
| — | Cảnh báo ghi đè | Banner (vàng/đỏ tuỳ mức) | ReadOnly | • Đếm trong N Serial đang chọn, bao nhiêu đã có giá trị cho tên thông số vừa nhập → "{K} Serial đang có giá trị... sẽ bị ghi đè". K=0 → có thể bỏ qua bước xác nhận, ghi thẳng. |
| — | Nút "Quay lại" | Button | Click | • Đóng modal xác nhận, quay về modal `2-2` với dữ liệu còn nguyên, chưa ghi gì. |
| — | Nút "Xác nhận" | Button | Click | • Ghi thật giá trị xuống toàn bộ N Serial (ghi đè Serial đã có + thêm mới Serial chưa có), đóng cả 2 modal, về bảng chính. |

### 6.6 tao-thuc-thi-cai-dat-2-2c-ap-dung-firmware — Áp dụng Firmware (modal)

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/thuc-thi-cai-dat-flow.md#screen-tao-thuc-thi-cai-dat-2-2c-ap-dung-firmware--áp-dụng-firmware-modal) · [HTML wireframe](../html-wireframe/thuc-thi-cai-dat-flow.html#s6)

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| — | "Áp dụng cho: N Serial" + link "Xem danh sách" | Label + Link | Click → bung/thu danh sách | • Số Serial đang được áp dụng Firmware trong lượt này. |
| — | SPMM đang áp dụng | Label | ReadOnly | • Xác nhận lại đúng 1 SPMM của các Serial đang chọn (điều kiện enable nút mở modal). Hiện kèm Đơn vị tính tự động theo SPMM đó. |
| 1 | Phiên bản phần mềm/Firmware | Textbox | Text | • Không bắt buộc với mọi SPMM (tuỳ cấu hình) nhưng LUÔN cho nhập — ghi giá trị áp dụng chung cho toàn bộ N Serial (FR-thuc-thi-cai-dat-010). |
| — | Nút "Huỷ" | Button | Click | • Đóng modal, không đổi gì. |
| — | Nút "Áp dụng" | Button | Click, **disabled mặc định** | • Enable khi đã nhập Firmware. Bấm → ghi thẳng xuống toàn bộ N Serial, đóng modal — KHÔNG có bước xác nhận ghi đè riêng (chỉ 1 giá trị áp cho cả lô). |

### 6.7 tao-thuc-thi-cai-dat-2-3-nhap-nhanh-nguoi-thu-huong — Nhập nhanh người thụ hưởng (modal)

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/thuc-thi-cai-dat-flow.md#screen-tao-thuc-thi-cai-dat-2-3-nhap-nhanh-nguoi-thu-huong--nhập-nhanh-người-thụ-hưởng-modal) · [HTML wireframe](../html-wireframe/thuc-thi-cai-dat-flow.html#s7)

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| — | "Áp dụng cho: N Serial" + link "Xem danh sách" | Label + Link | Click → bung/thu danh sách | • Số Serial đang được nhập người thụ hưởng trong lượt này. |
| 1 | Grid Serial × 4 trường (Họ và tên/Mã định danh/Chức vụ/Đơn vị triển khai) | Table nhập tay (mỗi ô 1 textbox/dropdown) | Text/Select | • **Bắt buộc cả 4 trường MỖI dòng**. Khác "Áp dụng thông số" — KHÔNG copy 1 người cho N Serial, mỗi dòng nhập độc lập (FR-thuc-thi-cai-dat-011). |
| — | "{x}/{N} Serial đã đủ thông tin" | Label | ReadOnly | • Cập nhật REALTIME theo từng thay đổi trên bất kỳ ô nào. |
| — | Nút "Huỷ" | Button | Click | • Đóng modal, không lưu gì. |
| — | Nút "Xác nhận" | Button | Click | • Validate TỪNG dòng — dòng thiếu → highlight trường thiếu, KHÔNG submit dòng đó; dòng đã đủ 4 trường → ghi ngay. Dòng còn thiếu vẫn giữ "Chưa nhập ›" trên bảng chính, sửa tiếp lần sau (E-thuc-thi-cai-dat-005). |

### 6.8 tao-thuc-thi-cai-dat-2-4-nhap-tu-excel — Nhập từ Excel (modal 2 bước)

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/thuc-thi-cai-dat-flow.md#screen-tao-thuc-thi-cai-dat-2-4-nhap-tu-excel--nhập-từ-excel-modal-2-bước) · [HTML wireframe](../html-wireframe/thuc-thi-cai-dat-flow.html#s8) (bước 2: [#s8b](../html-wireframe/thuc-thi-cai-dat-flow.html#s8b))

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| — | Link "Tải file Excel mẫu" (Bước 1) | Link | Click → download | • Tải file mẫu đúng cấu trúc cột hệ thống yêu cầu. |
| 1 | Vùng kéo-thả / Chọn file (Bước 1) | File upload | Upload | • **Bắt buộc**. Nhận file `.xlsx` theo mẫu — sai cấu trúc/không đọc được → báo lỗi ngay, chặn sang Bước 2 (E-thuc-thi-cai-dat-012). |
| — | Nút "Kiểm tra dữ liệu" (Bước 1) | Button | Click → Bước 2 | • Đọc file, validate từng dòng, chuyển sang preview. Vượt 5.000 dòng → báo lỗi (E-thuc-thi-cai-dat-016, NFR-thuc-thi-cai-dat-003). |
| 2 | Bộ đếm Tổng/Hợp lệ/Lỗi (Bước 2) | Label | ReadOnly | • Chỉ 2 nhóm — không còn "Cảnh báo". |
| 3 | Lọc kết quả (Bước 2) | Dropdown | Select | • Lọc bảng preview theo *Tất cả / Hợp lệ / Lỗi*. |
| 4 | Bảng preview (Bước 2) | Table (readonly) | — | • Mỗi dòng: Dòng/Mã SPMM/Serial/Đơn vị tính/Số thông số/Người thụ hưởng/Kết quả — Đơn vị tính tự động lấy theo Mã SPMM của dòng đó, không nhập tay. 2 nhóm kết quả: *Hợp lệ* (kể cả khi 0 thông số, và khi cột Người thụ hưởng để trống hoàn toàn 0/4 trường) hoặc lỗi chặn — *Serial chưa tồn tại* / *SPMM "Cần cài đặt"=Không* / *Không có tồn tại tại Kho đã chọn* (E-thuc-thi-cai-dat-017) / **Người thụ hưởng nhập thiếu trường (1-3/4)** (E-thuc-thi-cai-dat-018). |
| — | Link "Tải danh sách lỗi" (Bước 2) | Link | Click → download | • Xuất riêng các dòng lỗi để sửa lại. |
| — | Nút "Quay lại" (Bước 2) | Button | Click → Bước 1 | • Chọn lại file khác. |
| — | Nút "Nhập {N} dòng" (Bước 2) | Button | Click | • Nhập các dòng *Hợp lệ* vào bảng chính ở trạng thái CHƯA validate Thông tin quản lý, đóng modal (FR-thuc-thi-cai-dat-004). |

### 6.9 tao-thuc-thi-cai-dat-2-5-khong-the-hoan-thanh — Không thể hoàn thành (modal)

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/thuc-thi-cai-dat-flow.md#screen-tao-thuc-thi-cai-dat-2-5-khong-the-hoan-thanh--không-thể-hoàn-thành-modal) · [HTML wireframe](../html-wireframe/thuc-thi-cai-dat-flow.html#s9)

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| 1 | Danh sách Serial còn thiếu | Label (nhiều dòng) | ReadOnly | • Mỗi dòng: mã Serial + loại thông tin còn thiếu theo đúng cấu hình SPMM đó (E-thuc-thi-cai-dat-004). |
| — | Nút "Đóng" | Button | Click | • Đóng modal, không đổi gì — ở lại màn Tạo, không dòng nào đổi trạng thái. |
| — | Nút "Xem dòng cần bổ sung" | Button | Click | • Đóng modal, lọc/highlight các dòng đang thiếu ngay trên bảng chính. |

### 6.10 tao-thuc-thi-cai-dat-2-6-xac-nhan-cai-lai — Xác nhận cài đặt lại (modal)

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/thuc-thi-cai-dat-flow.md#screen-tao-thuc-thi-cai-dat-2-6-xac-nhan-cai-lai--xác-nhận-cài-đặt-lại-modal) · [HTML wireframe](../html-wireframe/thuc-thi-cai-dat-flow.html#s11)

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| 1 | Danh sách Serial đã cài trước đó | Label (nhiều dòng) | ReadOnly | • Trường hợp có Serial đã từng được thực thi cài đặt và Hoàn thành, modal Xác nhận cài lại hiển thị lần Hoàn thành gần nhất của từng Serial, gồm: Mã Serial, Số phiếu và Ngày Hoàn thành để người dùng đối chiếu trước khi xác nhận tiếp tục (FR-thuc-thi-cai-dat-023). |
| — | Nút "Huỷ" | Button | Click | • Đóng modal, KHÔNG Hoàn thành, ở lại bảng chính như trước khi bấm Hoàn thành — không dòng nào đổi trạng thái. |
| — | Nút "Xác nhận" | Button | Click | • Tiếp tục sang bước validate Thông tin quản lý theo cấu hình SPMM (đọc live, BR-thuc-thi-cai-dat-012) như bình thường — đạt hết thì Hoàn thành, không đạt thì mở modal `2-5-khong-the-hoan-thanh`. Sau khi Hoàn thành (kể cả trường hợp cài lại), hệ thống ghi nhận Thông số cài đặt/Firmware/Người thụ hưởng vừa nhập là thông số cài đặt **mới nhất** của Serial đó, cập nhật vào hồ sơ tài sản tại chức năng Quản lý Tài sản/Tài sản — dữ liệu cài đặt trước đó (nếu có) không bị xoá khỏi bản ghi Thực thi cài đặt cũ, nhưng hồ sơ tài sản chỉ phản ánh giá trị mới nhất (phần hiển thị lịch sử cài đặt nằm ngoài phạm vi, xem Mục 1). |

### 6.11 chi-tiet-thuc-thi-cai-dat — Chi tiết thực thi cài đặt

> **Viết lại 2026-08-26**: bản chất là màn Tạo (6.2) nhưng TOÀN BỘ field ở chế độ disable (read-only) — dùng chung bố cục, chỉ khác không có 3 nút Hủy bỏ/Lưu/Hoàn thành và không có các thao tác thêm/sửa/xoá dữ liệu. **Tạm thời bỏ tab "Lịch sử thao tác"** (xem Mục 11 — cơ chế Lịch sử thao tác đang là câu hỏi mở, chưa có FR/BR chính thức).

**Thiết kế:** [ASCII wireframe](../ascii-wireframe/tra-cuu-sua-thuc-thi-cai-dat-flow.md#screen-chi-tiet-thuc-thi-cai-dat--chi-tiết-thực-thi-cài-đặt) · [HTML wireframe](../html-wireframe/tra-cuu-sua-thuc-thi-cai-dat-flow.html#s10)

| # | Items | Control type | Data type | Description |
|---|-------|--------------|-----------|--------------|
| 1 | Số phiếu | Label | ReadOnly | • Mã hệ thống, không sửa được. |
| 2 | Đơn vị thực hiện | Label | ReadOnly | • Đơn vị đã tạo bản ghi. |
| 2b | Kho | Label | ReadOnly | • Kho đã chọn lúc tạo, khoá vĩnh viễn. |
| 3 | Căn cứ | Label | ReadOnly | • QĐTK hoặc QĐGCTKH đã chọn lúc tạo, khoá vĩnh viễn. |
| 4 | Số QĐGCTKH/QĐTK | Label | ReadOnly | • Số hiệu QĐTK/QĐGCTKH đã chọn lúc tạo. |
| 5 | Người tạo | Label | ReadOnly | • Tài khoản đã tạo bản ghi. |
| 6 | Thời gian tạo | Label | ReadOnly | • Thời điểm tạo bản ghi lần đầu. |
| 7 | Ghi chú | Label | ReadOnly | • Nội dung đã nhập lúc tạo (nếu có). |
| — | Trạng thái | Label | ReadOnly | • Luôn hiển thị "Hoàn thành" ở màn này. |
| — | Tài liệu đính kèm | File (đọc) | ReadOnly | • Xem lại danh sách tài liệu đã đính kèm, không thêm/xoá được. |
| — | Toggle "Chế độ xem" | Segmented control | Select | • *Theo SPMM* / *Trải phẳng* — giống 6.2, chỉ đổi cách hiển thị, không phải chỉnh sửa. |
| — | Hàng lọc (dưới header cột) | Textbox/Dropdown theo cột | Text/Select | • Giống 6.2 — dùng để tra cứu, không ảnh hưởng dữ liệu. |
| — | Dòng nhóm SPMM (Theo SPMM) | Row gập/mở | Click → expand/collapse | • Hiện tên SPMM đầy đủ + icon ⓘ + tổng số Serial, giống 6.2. |
| — | Icon ⓘ (cạnh SPMM) | Icon button | Click → mở popover | • Xem lại yêu cầu Thông tin quản lý của SPMM đó — thông tin tham khảo, không phải validate (bản ghi đã Hoàn thành). |
| 8 | Serial | Label | ReadOnly | • Không sửa được (khoá vĩnh viễn sau khi tạo). |
| 9 | Đơn vị tính | Label | ReadOnly | • Tự động lấy theo cấu hình của SPMM tương ứng — luôn đi kèm SPMM. |
| 10 | SPMM (Mã + Tên) | Label | ReadOnly | • Giống cột SPMM ở 6.2. |
| 11 | Thông số cài đặt | Link "N thông số ›" | Click → mở modal (chỉ xem) | • Read-only — mở modal xem danh sách Tên thông số/Giá trị/Ngày hết hạn, không sửa/thêm/xoá được. |
| 12 | Phiên bản phần mềm/Firmware | Label | ReadOnly | • Read-only. |
| 13 | Người thụ hưởng | Link "{Họ tên} ›" | Click → mở modal (chỉ xem) | • Read-only — mở modal xem 4 trường Họ tên/Mã định danh/Chức vụ/Đơn vị triển khai, không sửa được. |

## 7. Yêu cầu chức năng không thuộc màn hình nào

| ID | Yêu cầu | Cách kiểm |
|----|---------|-----------|
| FR-thuc-thi-cai-dat-005 | Gate "Cần cài đặt" đồng nhất 3 phương thức thêm Serial: chỉ SPMM có "Cần cài đặt"=Có mới được đưa vào Thực thi cài đặt, áp dụng như nhau cho cả Thêm 1 dòng / Nhập hàng loạt Serial / Nhập từ Excel. | test — thử thêm 1 SPMM "Cần cài đặt"=Không qua cả 3 lối, đều bị chặn |

## 8. Quy tắc nghiệp vụ

| ID | Quy tắc | Áp ở |
|----|---------|------|
| BR-thuc-thi-cai-dat-001 | Chỉ Serial thuộc SPMM có "Cần cài đặt"=Có mới được đưa vào danh sách Thực thi cài đặt — chặn cứng ngay từ bước thêm, qua cả 3 phương thức. | Thêm Serial (mọi phương thức), FR-thuc-thi-cai-dat-005 |
| BR-thuc-thi-cai-dat-002 | Yêu cầu dữ liệu bắt buộc (Thông số/Firmware/Người thụ hưởng) hoàn toàn xác định theo cấu hình "Thông tin quản lý" của SPMM tại Danh mục SPMM — không hard-code theo tên/loại sản phẩm. | Hoàn thành, FR-thuc-thi-cai-dat-014 |
| BR-thuc-thi-cai-dat-003 | SPMM không cấu hình cụ thể loại "Thông tin quản lý" nào → Serial cần có ít nhất 1 trong 3 loại thông tin trước khi Hoàn thành. | Hoàn thành, SPMM không cấu hình gì |
| BR-thuc-thi-cai-dat-004 | SPMM có cấu hình ≥1 cờ "Thông tin quản lý" → Serial cần đủ TẤT CẢ loại được cấu hình `true` trước khi Hoàn thành. | Hoàn thành, SPMM có cấu hình |
| BR-thuc-thi-cai-dat-005 | "Lưu" KHÔNG BAO GIỜ validate Thông tin quản lý — chỉ "Hoàn thành" mới validate. | Lưu, FR-thuc-thi-cai-dat-013 |
| BR-thuc-thi-cai-dat-006 | Hoàn thành không đạt cho ≥1 Serial → chặn TOÀN BỘ, không Serial nào đổi trạng thái — không có Hoàn thành một phần. | Hoàn thành, có Serial không đạt |
| BR-thuc-thi-cai-dat-009 | Áp dụng thông số/Firmware hàng loạt chỉ enable khi TẤT CẢ Serial đang tick chọn thuộc CÙNG 1 SPMM. | Mở modal Áp dụng thông số / Áp dụng Firmware |
| BR-thuc-thi-cai-dat-010 | Serial đưa vào Thực thi cài đặt phải **có tồn kho tại Kho đã chọn** (field 2b, Mục 6.2) — validate ngay khi thêm, qua cả 3 phương thức (Thêm 1 dòng / Nhập hàng loạt / Nhập Excel). Serial tồn tại nhưng ở Kho khác (kể cả cùng Đơn vị thực hiện) → chặn cứng, không thêm được vào bảng. | Thêm Serial (mọi phương thức), E-thuc-thi-cai-dat-017 |
| BR-thuc-thi-cai-dat-011 | Mọi thao tác trong bảng "Thông tin chi tiết" (thêm/xoá dòng, áp dụng hàng loạt, sửa qua modal con) chỉ thay đổi dữ liệu NHÁP trên màn đang mở, CHƯA lưu chính thức — mất nếu đóng màn/mất kết nối trước khi Lưu. Chỉ "Lưu" hoặc "Hoàn thành" mới ghi nhận chính thức. | Bất kỳ thao tác nhập liệu nào trên bảng |
| BR-thuc-thi-cai-dat-012 | Validate khi bấm "Hoàn thành" đọc cấu hình "Thông tin quản lý" của SPMM TẠI THỜI ĐIỂM BẤM HOÀN THÀNH (live) — không phải cấu hình snapshot lúc Serial được thêm. **Phạm vi "đọc live" CHỈ áp dụng cho "Thông tin quản lý" (BR-002/003/004)** — cờ "Cần cài đặt" (BR-001) KHÔNG đọc lại ở bước Hoàn thành, chỉ gate một lần lúc thêm Serial; đổi cờ "Cần cài đặt" giữa chừng không ảnh hưởng Serial đã thêm. | Hoàn thành |
| BR-thuc-thi-cai-dat-014 | Không cho thêm trùng 1 Serial 2 lần trong cùng 1 phiếu (cả 3 phương thức) — Serial đã có trong bảng của phiếu đang tạo thì lần thêm sau bị chặn tại dòng đó. | Thêm Serial đã có sẵn trong cùng phiếu |
| BR-thuc-thi-cai-dat-016 | Đối với bản ghi trạng thái Mới, quyền truy cập và thao tác được kiểm soát theo phân quyền người dùng và phạm vi đơn vị. Người dùng thuộc đơn vị tạo bản ghi được phép thao tác theo quyền được cấp; người dùng thuộc đơn vị khác — có quyền Xem → mở được ở **chế độ đọc** (KHÔNG bị từ chối, toàn bộ field disable như màn Chi tiết 6.11); muốn chỉnh sửa/Lưu/Hoàn thành/Xoá thì cần được cấp quyền sửa tương ứng. Hoàn toàn không có quyền nào (kể cả Xem) → từ chối (E-thuc-thi-cai-dat-009). | Mở lại / Lưu / Hoàn thành / Xoá bản ghi trạng thái Mới |
| BR-thuc-thi-cai-dat-018 | **[TẠM THỜI NGƯNG ÁP DỤNG — 2026-09-08, xem Mục 11 OQ]** ~~Serial đang thuộc 1 bản ghi trạng thái Mới (chưa Hoàn thành) — dù của đơn vị nào — chặn Hoàn thành bản ghi đang tạo, tránh 2 quy trình cùng xử lý 1 thiết bị.~~ Quyết định 2026-09-08: KHÔNG chặn Hoàn thành trong trường hợp này nữa — Serial vẫn thêm được vào bảng và Hoàn thành bình thường dù đang thuộc phiếu Mới khác. BR-thuc-thi-cai-dat-014 (chặn trùng trong cùng phiếu) vẫn giữ nguyên hiệu lực. | (ngưng áp dụng tạm thời) |
| BR-thuc-thi-cai-dat-019 | Bản ghi trạng thái Mới có thể **Xoá hẳn** tại màn Danh sách (nút icon cột Thao tác) — theo quyền `WH.IE.IE.DL`, đơn vị tạo hoặc đơn vị khác nếu được cấp quyền tương ứng. Yêu cầu xác nhận trước khi xoá. Bản ghi Hoàn thành KHÔNG xoá được. | Xoá bản ghi tại màn Danh sách |

## 9. Yêu cầu phi chức năng

| ID | Yêu cầu | Cách kiểm |
|----|---------|-----------|
| NFR-thuc-thi-cai-dat-001 | Thời gian phản hồi khi Lưu/Hoàn thành 1 bản ghi — không đặt SLA riêng cho feature này, dùng theo mặt bằng hiệu năng chung của hệ thống. | Không áp dụng riêng |
| NFR-thuc-thi-cai-dat-002 | Giờ vận hành cần khả dụng — không đặt khung giờ riêng, dùng theo khả dụng chung của hệ thống. | Không áp dụng riêng |
| NFR-thuc-thi-cai-dat-003 | Số bản ghi/Serial xử lý mỗi lần nhập hàng loạt hoặc Excel: tối đa **5.000 dòng/lần** cho cả "Nhập hàng loạt Serial" và "Nhập từ Excel". | test — nhập 5.001 dòng phải bị chặn (E-thuc-thi-cai-dat-016) |

## 10. Tiêu chí thành công

| # | Tiêu chí | Cách đo |
|---|----------|---------|
| 1 | **Đơn vị cấp dưới (Quân khu/Tỉnh/Phòng kỹ thuật...) tự ghi nhận cài đặt thực tế mà không cần qua Cục duyệt** | Đăng nhập tài khoản 1 đơn vị cấp dưới → tạo và Hoàn thành 1 bản ghi Thực thi cài đặt trọn vẹn mà không có bước duyệt/chuyển qua Cục nào chen giữa (SC-thuc-thi-cai-dat-01) |
| 2 | **Firmware đã cài tra cứu lại đúng 100%** | Mở Chi tiết 1 bản ghi Hoàn thành có Serial thuộc SPMM cấu hình bắt buộc Firmware → giá trị Phiên bản phần mềm/Firmware hiển thị khớp đúng giá trị đã nhập lúc Hoàn thành (SC-thuc-thi-cai-dat-02) |
| 3 | **Không Serial nào Hoàn thành khi còn thiếu Thông tin quản lý bắt buộc** | Bấm Hoàn thành 1 bản ghi có ≥1 Serial thiếu dữ liệu theo cấu hình SPMM → hệ thống chặn toàn bộ, không Serial nào chuyển trạng thái, mở modal liệt kê Serial còn thiếu |

## 11. Câu hỏi mở

| Mức | Câu hỏi | Vì sao quan trọng | Người chốt |
|-----|---------|---------------------|------------|
| Hold | Ngưỡng cụ thể cho việc kiểm soát 1 đĩa cài/license đã cài ra bao nhiêu máy, và khi vượt ngưỡng thì chặn cứng hay chỉ cảnh báo? | Nhằm mục đích Đối chiếu được số máy đã cài từ 1 gói license/đĩa cài so với giới hạn cho phép | Chưa xác định |
| Hold | Bản ghi Thực thi cài đặt sau khi Hoàn thành hiện là read-only vĩnh viễn (không còn tính năng Sửa). Nghiệp vụ có cần cơ chế cập nhật/sửa lại thông tin cài đặt (Thông số cài đặt, Phiên bản phần mềm/Firmware, Người thụ hưởng) khi phát hiện sai sót sau này không, và nếu có thì theo quy tắc/quyền nào? | Ảnh hưởng Mục 4.2, Mục 5, Mục 6.11 — cần chốt trước khi thiết kế lại cơ chế cập nhật thông tin cài đặt sau Hoàn thành | Chưa xác định |
| Resolved | ~~Đổi field "Kho" (2b, Mục 6.2) SAU KHI đã thêm Serial vào bảng — giữ nguyên các Serial đã thêm (có thể sai Kho mới) hay bắt xoá hết/validate lại toàn bộ?~~ **Đã chốt (2026-09-08):** giữ nguyên Serial đã thêm, không xoá/validate ngay — validate lại tồn kho theo Kho mới tại bước Hoàn thành, báo lỗi nếu không có tồn tại (xem field 2b Mục 6.2, nút Hoàn thành). | Ảnh hưởng trực tiếp BR-thuc-thi-cai-dat-010 (tồn kho theo Kho) | @maihuong (2026-09-08) |
| Resolved | ~~Đơn vị thực hiện chỉ có đúng 1 Kho — field "Kho" (2b) có ẩn/tự chọn sẵn không, hay luôn hiện dropdown dù chỉ 1 lựa chọn?~~ **Đã chốt (2026-09-08):** luôn hiện dropdown, tự động chọn sẵn Kho đầu tiên trong danh sách, cho phép chọn lại (xem field 2b Mục 6.2). | Ảnh hưởng UX màn Tạo (Mục 6.2) | @maihuong (2026-09-08) |
| Hold | **[theo dõi quyết định tạm thời 2026-09-08]** BR-thuc-thi-cai-dat-018 (chặn deadlock Serial ở 2 phiếu Mới) đã tạm ngưng áp dụng — cần thiết kế cơ chế triệt để hơn (cảnh báo sớm lúc thêm Serial trùng phiếu Mới khác, hoặc cách gỡ khi phát sinh xung đột dữ liệu giữa 2 phiếu cùng Hoàn thành 1 Serial)? | Rủi ro: 2 phiếu Mới có thể cùng ghi nhận thông số khác nhau cho cùng 1 Serial mà không có cảnh báo, dữ liệu Module Tài sản chỉ giữ bản ghi nhận sau cùng | Chưa xác định |

## 12. Changelog

| Ngày cập nhật | Loại thay đổi | Nguồn/brainstorming liên quan | Người yêu cầu | Nội dung thay đổi |
|-----------------|------------------|-----------------------------------|-------------------|-------------------------|
| 2026-08-26 | Làm rõ nghiệp vụ | Trao đổi trực tiếp | @maihuong | Xác nhận cài lại (6.10): ghi rõ Xác nhận sẽ cập nhật thông số cài đặt mới nhất vào hồ sơ tài sản; hiển thị lịch sử cài đặt là ngoài phạm vi, đặc tả sau (Mục 1) |
| 2026-08-26 | Làm rõ nghiệp vụ | Trao đổi trực tiếp | @maihuong | Mục 1: bổ sung mô tả cấu trúc 2 cờ đọc từ Danh mục SPMM ("Cần cài đặt" boolean; "Thông tin quản lý" gồm 3 cờ con) để người đọc hiểu rõ BR-002/003/004 |
| 2026-09-04 | update | user request (validate Serial theo tồn kho Đơn vị thực hiện + đổi field Số QĐGCTKH/QĐTK) | @maihuong | (1) **Sửa nghiệp vụ thật** — `BR-thuc-thi-cai-dat-010` đảo ngược hoàn toàn: trước "không kiểm tra/chặn theo đơn vị của Serial", nay **Serial phải có tồn kho tại Đơn vị thực hiện mới được thêm** — chặn cứng nếu Serial thuộc đơn vị khác. Thêm lỗi mới `E-thuc-thi-cai-dat-017` ("Không có tồn tại Đơn vị thực hiện"), đồng bộ vào: field 8 Serial (Mục 6.2), nút "Kiểm tra Serial" (Mục 6.3 — modal Nhập hàng loạt Serial), bảng preview Nhập Excel (Mục 6.8). (2) Field 4 "Số QĐGCTKH/QĐTK" (Mục 6.2, màn Tạo) đổi control type từ **Dropdown (search)/Select** sang **Textbox/Text** — **nhập tự do, chỉ validate bắt buộc nhập** (không kiểm tra số hiệu có tồn tại/đã ban hành hay không — theo xác nhận trực tiếp của user). Field 4 (Mục 6.1, Danh sách) đổi từ **Link navigate** sang **Label** thuần — bỏ hẳn hành vi navigate sang QĐTK/QĐGCTKH (input tự do ở màn Tạo không đảm bảo khớp đúng 1 bản ghi thật, theo xác nhận trực tiếp của user), chỉ còn hiển thị đúng số hiệu đã nhập. Xác nhận: không đổi FR nào, thêm đúng 1 error ID mới (`E-017`), 1 BR sửa nội dung (không đổi ID), không còn reference "traceability"/"Navigate" nào tới field này trong toàn tài liệu. |
| 2026-09-08 | update | 17 điểm cần làm rõ phát hiện khi test (xem `DIEM-CAN-LAM-RO.md`), user chốt từng điểm trực tiếp | @maihuong | Chốt 15/17 điểm (2 điểm CLR-06/CLR-16 không cần sửa SRS — là bug phía build): (1) **CLR-01** Số phiếu sinh khi bấm Lưu lần đầu (không phải khi vào màn) — sửa Mục 3, field 1 Mục 6.2, nút Lưu, FR-019. (2) **CLR-02** Hoàn thành validate trực tiếp trên dữ liệu đang nhập, không cần Lưu trước — sửa Mục 3 bước 7, nút Hoàn thành Mục 6.2. (3) **CLR-03** giữ nguyên: nút Hoàn thành luôn cho bấm, báo lỗi "Chưa có Serial nào." khi 0 Serial — làm rõ thêm trong Mục 6.2. (4) **CLR-04/05** thêm field mới **"Kho"** (2b, dropdown, danh sách theo Đơn vị thực hiện) vào Mục 6.2 + 6.11; đổi `BR-thuc-thi-cai-dat-010` + `E-thuc-thi-cai-dat-017` từ validate theo "Đơn vị thực hiện" sang theo "Kho đã chọn" (đồng bộ field 8, Mục 6.3, Mục 6.8); thêm 2 OQ mới (đổi Kho giữa chừng, ẩn field khi 1 kho). (5) **CLR-07** thêm nút Xoá bản ghi Mới tại cột Thao tác màn Danh sách (Mục 6.1), thêm `BR-thuc-thi-cai-dat-019`, thêm transition Xoá vào Mục 5, sửa Mục 4.2. (6) **CLR-08/17** đơn vị khác chỉ có quyền Xem → mở bản ghi Mới ở chế độ đọc thay vì bị từ chối 403 — sửa `BR-thuc-thi-cai-dat-016`, Mục 4.1, 4.2, field 2 Mục 6.1. (7) **CLR-09** tạm thời NGƯNG áp dụng `BR-thuc-thi-cai-dat-018` (chặn deadlock Serial 2 phiếu Mới) — xoá bước kiểm tra tương ứng khỏi nút Hoàn thành + Mục 3 bước 8, thêm OQ theo dõi rủi ro. (8) **CLR-10** Hàng lọc Danh sách đổi thành toàn bộ dropdown "Chọn..." (Mục 6.1). (9) **CLR-11** làm rõ phạm vi "đọc live" của `BR-thuc-thi-cai-dat-012` CHỈ áp dụng Thông tin quản lý, KHÔNG áp dụng cờ "Cần cài đặt". (10) **CLR-12** mở rộng `E-thuc-thi-cai-dat-008` (version-conflict) áp dụng cho cả Hoàn thành, không chỉ Lưu. (11) **CLR-13** đổi "lưu một phần" thành "chặn toàn bộ nút Lưu" khi có dòng lỗi cứng (Mục 6.2). (12) **CLR-14** mở rộng `E-thuc-thi-cai-dat-006` thêm 2 case: ngày không tồn tại theo lịch, ngày hết hạn nhỏ hơn ngày cài đặt (Mục 6.2, 6.4). (13) **CLR-15** thêm lỗi mới `E-thuc-thi-cai-dat-018` cho Import Excel: Người thụ hưởng thiếu 1-3/4 trường (Mục 6.8). Chi tiết đầy đủ từng điểm + căn cứ: xem `docs/thuc-thi-cai-dat/DIEM-CAN-LAM-RO.md` cột "Phản hồi". |

<!-- wm:d4f7463bbbc7e5517488a623804b7507 -->
</content>
</invoke>
