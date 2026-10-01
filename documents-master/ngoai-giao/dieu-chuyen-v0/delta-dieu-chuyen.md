---
type: delta
feature: dieu-chuyen
status: nhap
updated: 2026-09-08
nguon:
  - docs/ngoai-giao/srs/srs-dieu-chuyen.md
  - SourceCode/NG/frontend/mes-ui-mf/apps/warehouse/src/app/pages/warehouse-transfer-request/
---

# Điều chuyển SPMM — những chỗ bản đang chạy cần sửa

**Bản đang chạy:** `/track-and-trace/goods-transfer` → mã nguồn `apps/warehouse/src/app/pages/warehouse-transfer-request/`.

Đây là **file chỉ đường**, không phải bản rút gọn của SRS. Mỗi dòng nói *sửa cái gì* và *đọc ở đâu*; luật đầy đủ nằm trong [srs-dieu-chuyen.md](srs-dieu-chuyen.md) và trên Figma — phải mở hai chỗ đó mới đủ để code.

**Figma:** file **BCY(2)** · Page **Page 1** · KHU VỰC 8. Tên khung ghi trong bảng là tên thật trên canvas — `x` là số loại điều chuyển (**1** Từ ĐVSX · **2** Giữa các đơn vị · **3** Nội bộ đơn vị), mỗi loại một khung riêng. Mã node đầy đủ nằm ngay đầu mỗi mục trong SRS.

## Cần sửa

| # | Chức năng | Sửa gì | Figma | SRS |
|:--:|---|---|---|---|
| 1 | Loại điều chuyển | Ba giá trị: *Từ đơn vị sản xuất · Giữa các đơn vị · Nội bộ đơn vị*. Đối chiếu lại `transferScope` và bỏ hẳn hai loại cũ `RETURN_TO_COMPANY` · `FREQUENT_STOCK_TRANSFER_DOCKING` | ĐC x.2 Lập phiếu | 1 · 5.4 |
| 2 | Trạng thái phiếu | Bốn trạng thái *Mới · Chờ nhận · Đã nhận · Đã nhận thiếu*, thay cho `NEW`/`PENDING_APPROVAL`/`APPROVED`. **Bỏ *Bỏ duyệt*** và hộp thoại lý do bỏ duyệt | — | 4 · 3.2 |
| 3 | Bên nhận xác nhận | Toàn bộ nhánh này **chưa có trong mã nguồn**: bên nhận quét đối chiếu, khai khối *Thông tin nhập kho*, bấm *Xác nhận nhận*; thiếu mã thì phiếu sang *Đã nhận thiếu* và mã còn lại thành *Thất lạc* | ĐC x.7 · x.8 Xác nhận nhận · ĐC 04 Thất lạc | 5.11 · 5.12 · 5.14 |
| 4 | Tồn kho đổi hai lần | *Xác nhận gửi* trừ kho xuất, *Xác nhận nhận* cộng kho nhận. Giữa hai mốc mã không thuộc kho nào | — | 6 `FR-dieu-chuyen-006` |
| 5 | Phiếu căn cứ | Gộp bốn ô căn cứ đang có (*Số Công văn đề nghị · Số Quyết định triển khai · Số QĐ cài đặt và cấp phát · Số phiếu căn cứ điều chuyển*) thành **một ô**, đổi nội dung theo loại: hợp đồng · QĐGCTKH năm · ẩn. Chọn xong ô chỉ hiện mã, không kèm ngày | ĐC x.1 Chọn căn cứ | 5.3 |
| 6 | Nạp dòng theo căn cứ | Chọn căn cứ thì tự nạp dòng SPMM. Chọn lại chính căn cứ đó thì nạp bù dòng đang thiếu, không hỏi. Đổi sang căn cứ khác khi đã có mã thì hỏi trước rồi mới xoá | ĐC x.1 Chọn căn cứ | 5.3 `[4] [5]` |
| 7 | Trần theo căn cứ | Cột *SL còn lại theo HĐ* (loại 1 — **chặn**) và *SL còn lại theo QĐ* (loại 2 — **không chặn**, chỉ cảnh báo). Trần chỉ trừ phần đã *Xác nhận gửi* | ĐC x.2 Lập phiếu | 5.4 `[16] [17]` · 6 `FR-dieu-chuyen-004` |
| 8 | Lưới chi tiết | Còn **một lưới phẳng, một dòng một SPMM** — hiện đang là hai lưới (`equipment-list` + `supplies-list`). Bỏ nút *Phân bổ tồn kho*, bỏ dòng con theo lô, bỏ cột *Vị trí kho xuất* | ĐC x.2 Lập phiếu | 5.4 |
| 9 | Cột tiền | Bỏ *Đơn giá · Thành tiền · Tổng tiền · Tiền tệ* khỏi lưới chi tiết, hộp thoại chọn SPMM và màn danh sách | ĐC 01 Danh sách · ĐC x.2 Lập phiếu | 5.1 · 5.4 |
| 10 | Hộp thoại thêm SPMM | Nút *Chọn SPMM* đổi tên thành *＋ Thêm SPMM* và **chỉ hiện ở loại 2 và loại 3** — loại 1 đi đúng hợp đồng, không có nút. Hộp thoại đang liệt kê **theo lô** (Số phiếu nhập · Ngày nhập · Vị trí · Đơn giá) → gộp lại **một dòng một SPMM**, chỉ còn ☐ · STT · Mã · Tên · ĐVT · SL tồn, tìm theo từng cột | ĐC 05 Chọn SPMM từ tồn kho | 5.4 `[22]` · 5.6 |
| 11 | Ô quét chung | Ô quét dùng chung cho cả lưới, tra tồn kho *Kho xuất* rồi tự vào đúng dòng — không phải chọn dòng trước. Lỗi hiện bằng **thông báo nổi**, không dán dưới ô; chỉ kêu tiếng báo nhận khi mã hợp lệ | ĐC x.2 Lập phiếu | 5.4 `[13]` |
| 12 | Hộp thoại serial | **Phải tra tồn kho — hiện chưa tra.** `onScanSerial()` chỉ so trùng trong chính phiếu rồi đẩy thẳng chuỗi vừa gõ vào bảng; `onGenerateRangeSerial()` **sinh chuỗi** từ tiền tố + dải số + hậu tố. Không có lệnh nào hỏi kho xuất. Sửa thành: quét xong tra tồn kho *Kho xuất*, có thì lấy, không có thì báo. Thêm ba cột chỉ đọc *Vị trí · Phiếu nhập kho · Ngày nhập kho* phần mềm tự điền theo mã, thêm hàng tìm theo cột. Thẻ *Chọn theo dải* bỏ *Tiền tố · Hậu tố · Độ dài dải*, chỉ còn *Giá trị từ / Giá trị đến* và **chỉ lấy mã có thật trong kho** | ĐC x.4 Chọn số serial | 5.7 |
| 13 | Xác nhận gửi | Nút mới thay *Duyệt*, **năm điều kiện**; thiếu thì tô đỏ tại từng mục, không dựng hộp thoại liệt kê. Đủ thì mở hộp thoại xác nhận, phiếu sang *Chờ nhận* | ĐC x.5 · x.6 Xác nhận gửi | 5.8 · 5.9 |
| 14 | Giữ chỗ mã định danh | Mã bị giữ chỗ từ lúc *Lưu*, và **kiểm lại ngay tại lúc *Lưu*** xem phiếu khác có giữ mất không. Xoá phiếu *Mới* nhả mã ngay | — | 5.4 `[23]` · 6 `FR-dieu-chuyen-001` |
| 15 | Chống ghi đè | Phiếu đã bị người khác xử lý thì không ghi đè — áp cho *Lưu · Xác nhận gửi · Xác nhận nhận · Xoá* | — | 6 `FR-dieu-chuyen-008` |
| 16 | Làm hộ | Cấp trên thao tác thay đơn vị nhận khi đơn vị đó mang cờ *Cho phép cấp trên thao tác hộ*; màn hiện dải ghi vết ai đang làm thay ai | ĐC x.7 Xác nhận nhận | 3.3 · 5.11 `[2]` |
| 17 | Danh sách phiếu | Bỏ cột *Tổng tiền*. Lọc riêng từng cột, ô lọc nằm trong lưới dưới tiêu đề cột | ĐC 01 · 02 Danh sách | 5.1 · 5.2 |
| 18 | Đơn vị xuất / nhận | `issueDepartment` · `receiptDepartment` là **đơn vị có kho**. Người xác nhận nhận là tài khoản thuộc đơn vị nhận — tài khoản hiện gắn ở **đơn vị**, chưa có tài khoản gắn ở phòng ban | ĐC x.2 Lập phiếu | 1 · 5.4 |
| 19 | Ba số chứng từ | Tách rõ ba thứ: **Mã phiếu** phần mềm sinh khi *Lưu* · **Số phiếu xuất kho** bên gửi khai khi *Xác nhận gửi* · **Số phiếu nhập kho** bên nhận khai khi *Xác nhận nhận*. Code đang gộp vào ô `code` và `goodsReceiptCode` | ĐC x.2 Lập phiếu · ĐC x.7 Xác nhận nhận | 5.4 `[1] [2]` · 5.11 `[5]` |
| 20 | Tài liệu đính kèm | **Chưa có trong mã nguồn.** Bắt buộc đính trước khi *Xác nhận gửi* và trước khi *Xác nhận nhận*; nút mang số tệp đang có | ĐC x.2 Lập phiếu · ĐC x.7 Xác nhận nhận | 5.4 · 5.11 `[8]` |
| 21 | Ô *Chuyển kho backdate* | Bỏ. Ô đánh dấu này cho phép ghi phiếu lùi ngày và kéo theo màn cảnh báo *phiếu đề nghị sai ngày chứng từ*. SRS đã có *Ngày xuất kho* và *Ngày nhập kho* khai riêng, lùi ngày được ngay tại hai ô đó | ĐC x.2 Lập phiếu | 5.4 |
| 22 | Xuất PDF phiếu | SRS chưa đặc tả. Giữ nguyên bản đang có, chờ chốt sau | — | — |

## Giữ nguyên, không phải sửa

Khuôn màn (thanh bên, đường dẫn, cụm nút góc phải), lưới `lib-master-listing`, cơ chế phân quyền `*libUserRoleAuthorize`, bốn trường vết ghi *Người tạo · Ngày tạo · Người sửa · Ngày sửa*, và cách đính kèm tệp — SRS đi theo đúng những gì đang có.

## 📝 Changelog

| Ngày cập nhật | Loại thay đổi | Nguồn liên quan | Người yêu cầu | Nội dung thay đổi |
|---|---|---|---|---|
| 2026-09-08 | thêm mới | `docs/ngoai-giao/srs/srs-dieu-chuyen.md` · mã nguồn `warehouse-transfer-request/` | @quynhdtn17 | Bản đầu tiên. 22 mục cần sửa, đối chiếu bản đang chạy `/track-and-trace/goods-transfer` với SRS và Figma. Chốt: tài khoản gắn ở đơn vị nên `issueDepartment`/`receiptDepartment` là đơn vị có kho; bỏ ô *Chuyển kho backdate* |
