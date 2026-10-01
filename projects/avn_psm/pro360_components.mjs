// Run with a connected cua Tab, not Node alone. Never reads browser credentials.
// Default is preview-only: await updateOpenComponent(tab, record).
// Explicit fill (no Save): await updateOpenComponent(tab, record, { fill: true }).
export const components = [
  [34, 'Kế hoạch KH, Slide & BBH kickoff -Bộ kế hoạch nội bộ (KHCF, KHDS, KHCH,KHCL)', 'Tài liệu quản trị dự án:- Kế hoạch dự án nội bộ + khách hàng;- Tài liệu kickoff dự án: slide và biên bản họp', 'Khởi động và khảo sát', '01/09/2026', '30/09/2026', '19434600', '-Kê hoạch KH, slide & BBH kickoff được KH xác nhận qua email\n-Bộ kế hoạch nội bộ được PQA review và phê duyệt theo PQUQ'],
  [36, 'Sơ đồ quy trình', 'Tài liệu quy trình nghiệp vụ', 'Khởi động và khảo sát', '01/09/2026', '30/09/2026', '58303800', 'Bàn giao và KH xác nhận qua email'],
  [37, 'Bản tổng hợp yêu cầu nghiệp vụ', 'Tài liệu yêu cầu/ tài liệu GAP', 'Khởi động và khảo sát', '01/09/2026', '30/09/2026', '77738400', 'Bàn giao và KH xác nhận qua email'],
  [38, 'RMSheet giai đoạn khởi động', 'Tài liệu quản lý yêu cầu (RMSheet)', 'Khởi động và khảo sát', '01/09/2026', '30/09/2026', '9717300', 'PQA review'],
  [40, 'Tài liệu thiết kế giải pháp và kỹ thuật tổng thể', 'Tài liệu giải pháp chi tiết cho các hạng mục cần chỉnh sửa/Thiết kế chi tiết', 'Thiết kế', '01/09/2026', '30/09/2026', '58303800', 'Bàn giao và KH xác nhận qua email'],
  [41, 'Testcase GAP', 'Testcase cho GAP', 'Thiết kế', '01/10/2026', '30/10/2026', '19434600', 'PM xác nhận qua email'],
  [42, 'Gói phần mềm đã phát triển', 'Chương trình đã được chỉnh sửa', 'Thiết kế', '01/10/2026', '30/11/2026', '97173000', 'Gói phần mềm đã triển khai thành công trên môi trường Staging. BB hoặc email xác nhận'],
  [43, 'Tài liệu HDSD hệ thống', 'Tài liệu Hướng dẫn sử dụng;Tài liệu thông số cấu hình hệ thống', 'Thiết kế', '01/10/2026', '30/11/2026', '29151900', 'Bàn giao và KH xác nhận qua email'],
  [44, 'RMSheet giai đoạn thiết kế', 'Tài liệu quản lý yêu cầu (RMSheet) cập nhật đến giai đoạn Customization', 'Thiết kế', '01/10/2026', '30/11/2026', '9717300', 'PQA review'],
  [48, 'Testcase UAT', 'Testcase cho UAT', 'Kiểm thử', '01/11/2026', '30/11/2026', '48586500', 'Bàn giao và KH xác nhận qua email'],
  [49, 'Kế hoạch UAT', 'Kế hoạch UAT (Bao gồm phạm vi, tiêu chí hoàn thành UAT)', 'Kiểm thử', '01/11/2026', '30/11/2026', '48586500', 'Bàn giao và KH xác nhận qua email'],
  [50, 'BBNT UAT', 'Biên bản nghiệm thu UAT', 'Kiểm thử', '01/12/2026', '30/12/2026', '194346000', 'BBNT được xác nhận bởi PM 2 bên'],
  [51, 'RMSheet giai đoạn kiểm thử', 'Tài liệu quản lý yêu cầu (RMSheet) cập nhật đến giai đoạn Kiểm thử chấp nhận', 'Kiểm thử', '01/12/2026', '30/12/2026', '9717300', 'PQA review'],
  [53, 'Kế hoạch golive', 'Kế hoạch triển khai', 'Triển khai', '30/11/2026', '30/12/2026', '19434600', 'Bàn giao và KH xác nhận qua email'],
  [54, 'Checklist kiểm tra an toàn thông tin trước khi triển khai ứng dụng cho golive', 'Checklist kiểm tra an toàn thông tin trước khi triển khai ứng dụng cho khách hàng', 'Triển khai', '30/11/2026', '30/12/2026', '19434600', 'Bàn giao và KH xác nhận qua email'],
  [58, 'Biên bản xác nhận hoàn thành golive', 'Biên bản xác nhận hoàn thành triển khai', 'Triển khai', '30/11/2026', '30/12/2026', '242932500', 'BBNT được xác nhận bởi PM 2 bên'],
  [61, 'Báo cáo tổng kết dự án', 'Báo cáo tổng kết dự án', 'Triển khai', '30/11/2026', '30/12/2026', '9717300', 'PQA review, PD phê duyệt'],
].map(([row, name, standard, version, start, release, revenue, conditions]) =>
  ({ row, name, standard, version, start, release, revenue, conditions, deliverable: 'Yes' }));

const normalize = s => s.replace(/\s+/g, ' ').trim();
const nodes = state => state.split('\n').map(line => {
  const m = line.match(/^\s*(\d+) (.*)$/);
  return m ? { id: Number(m[1]), text: m[2] } : null;
}).filter(Boolean);

function field(list, label) {
  const at = list.findIndex(n => n.text === `text ${label} :`);
  if (at < 0) throw new Error(`Missing field label: ${label}`);
  for (const n of list.slice(at + 1, at + 5)) {
    if (n.text.startsWith('text field')) return n.id;
  }
  throw new Error(`No input next to ${label}`);
}

// Stop on ambiguity or an unavailable dropdown option. Do not guess mappings.
export async function updateOpenComponent(tab, record, { fill: shouldFill = false } = {}) {
  const snapshot = async () => await tab.getAXState({ disableDiffing: true, emit: false });
  let state = await snapshot();
  const modal = () => {
    const list = nodes(state);
    const at = list.findLastIndex(n => n.text === 'text Component Details');
    if (at < 0) throw new Error('Open the component edit dialog first.');
    return list.slice(at);
  };
  if (!modal().some(n => normalize(n.text) === `text ${normalize(record.name)}`)) {
    throw new Error(`Wrong open component: expected ${record.name}`);
  }
  if (!shouldFill) return { mode: 'preview', record };
  const choose = async (label, value) => {
    const id = field(modal(), label);
    await tab.click(id);
    state = await snapshot();
    const matches = nodes(state).filter(n => normalize(n.text) === `text ${normalize(value)}`);
    // Visible list can contain the selected value and the dropdown option.
    if (matches.length !== 1) throw new Error(`Ambiguous/missing option ${label}: ${value}`);
    await tab.click(matches[0].id);
    state = await snapshot();
  };
  const fill = async (label, value) => {
    await tab.setValue(field(modal(), label), value);
    state = await snapshot();
  };
  await choose('Version', record.version);
  await choose('Standard Component', record.standard);
  await choose('Is Deliverable', record.deliverable);
  await fill('Planned Start Date', record.start);
  await fill('Planned Release Date', record.release);
  await fill('Planned Revenue', record.revenue);
  await fill('Complete Conditions', record.conditions);
  // Leave review and Save to the caller until date widget behavior is verified.
  return { mode: 'filled-not-saved', name: record.name, state };
}
