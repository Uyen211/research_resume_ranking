# Đặc tả Kỹ thuật: Hệ thống Tiền xử lý CV Toàn diện (Comprehensive CV Pre-processing) - Version 2.5 (FINAL)

Tài liệu này xác định các tiêu chuẩn kỹ thuật để chuyển đổi CV từ tập tin văn bản chuẩn hóa sơ bộ sang cấu trúc **Feature-Rich JSON**. Mỗi quy trình trong tài liệu được trình bày dựa trên 3 trụ cột: **Trừu tượng** (Giải thích mục đích), **Logic** (Cơ chế xử lý) và **Cụ thể** (Thông số kỹ thuật).

---

## 1. Kiến trúc Hệ thống & Danh mục Thư viện

### 1.1. Luồng dữ liệu chiến lược
Hệ thống tập trung xử lý dữ liệu từ `df_resumes_normalized_full.csv` qua 5 vùng thông tin:
1.  `information_section`: Thông tin định danh.
2.  `summary_objective`: Tóm tắt năng lực.
3.  `technical_skills`: Danh sách kỹ năng tự chọn.
4.  `work_experience`: Lịch sử làm việc (Dữ liệu nền cho thâm niên).
5.  `education_certifications`: Bằng cấp và chứng chỉ.

### 1.2. Công nghệ sử dụng (Library Stack)
*   **Ngôn ngữ**: Python 3.10+
*   **Mô hình NER**: `GLiNER` (Model: `urchade/gliner_multi-v2.1`).
*   **Cơ sở dữ liệu Vector**: `ChromaDB` (Lưu trữ Vector trí tuệ nhân tạo).
*   **Mô hình Embedding**: `Sentence-Transformers` (Model: `all-MiniLM-L6-v2`).
*   **Xử lý dữ liệu & Thời gian**: `pandas`, `numpy`, `regex` (re), `python-dateutil`.

---

## 2. Quy trình Xử lý Chi tiết (3-Layer Specification)

### Bước 1: Trình bóc tách Thông tin Hành chính (Header Parser)

*   **Lớp Trừu tượng (Tường thuật)**:
    Hãy tưởng tượng bạn đang đọc một tấm danh thiếp. Bạn không cần đọc hết văn bản mà chỉ tìm các "nhãn" như "Email:" hay "Số điện thoại:". Khi thấy nhãn tiếp theo, bạn biết thông tin trước đó đã kết thúc. Chúng ta mô phỏng cách đọc lướt này để tách biệt các thông tin cá nhân cơ bản của ứng viên.

*   **Lớp Logic (Toán học/Quy trình)**:
Sử dụng thuật toán **Field-to-Field Delimiter Parsing** với cơ chế **Lookahead Splitter**.
1.  Xác định vị trí của Nhãn A.
2.  Nhìn phía trước (Lookahead) để tìm vị trí của Nhãn B (nhãn kế tiếp trong danh sách).
3.  Cắt chuỗi văn bản nằm giữa A và B.
4.  Làm sạch khoảng trắng, chuẩn hóa nhiễu. Bất kỳ giá trị `NaN`, `None` hay các chuỗi "nan", "null", "n/a", "-" từ nguồn Pandas sẽ được lọc, làm sạch và gán lại an toàn thành `Null/None` để không bị công nghệ AI hay Regex nhận diện sai. Ngoài ra, chuỗi trích xuất còn được cấu hình cắt bỏ đuôi dấu câu thừa (như dấu phẩy, dấu nháy kép, dấu chấm phẩy) bằng `.rstrip(",;'\"")` để đảm bảo output thuộc tính sạch sẽ.

*   **Lớp Cụ thể (Kỹ thuật thực thi)**:
    *   **Đầu vào**: Cột `information_section`.
    *   **07 Trường thông tin trích xuất**: `Name`, `Phone`, `Email`, `Location`, `LinkedIn`, `job_title`, `years_of_experience`.
    *   **Xử lý đặc biệt**: Trường `years_of_experience` được tách số bằng Regex và ép kiểu về `float` (làm tròn 0.1). Đây là giá trị "Trần kinh nghiệm" cho toàn bộ Pipeline.

---

### Bước 2: Nhận diện thực thể theo vùng (Zonal NER)

*   **Lớp Trừu tượng (Tường thuật)**:
    Một người tuyển dụng thông minh sẽ tìm "Kỹ năng lập trình" ở mục Kinh nghiệm làm việc, nhưng sẽ tìm "Bằng cấp" ở mục Học vấn. Quy trình này giúp máy tính thay đổi "tiêu cự" của kính lúp nhận diện tùy theo vùng dữ liệu nó đang đọc, tránh việc nhầm lẫn ngữ cảnh.

*   **Lớp Logic (Toán học/Quy trình)**:
    1.  **Phân mảnh (Chunking)**: Chia nhỏ văn bản thành các đoạn (Chunks) ~200 từ, gối đầu (Overlap) 50 từ để không mất ngữ cảnh tại điểm cắt.
    2.  **Nhận diện (Extraction)**: Sử dụng GLiNER với bộ nhãn (labels) thay đổi linh hoạt theo vùng (Zone).
    3.  **Lọc dữ liệu**: Áp dụng ngưỡng tin cậy để loại bỏ các phỏng đoán yếu của AI.

*   **Lớp Cụ thể (Kỹ thuật thực thi)**:
    *   **Tham số Threshold linh hoạt**:
        *   Các vùng văn xuôi tự nhiên (`summary`, `work_experience`, `education`): `threshold = 0.5` (Đảm bảo lọc sạch các danh từ rác không liên quan).
        *   Vùng liệt kê dày đặc (`technical_skills`): `threshold = 0.15` (Do dữ liệu liệt kê không có cấu trúc ngữ pháp, độ tự tin dự đoán thường rất thấp. Việc hạ threshold xuống giúp vớt trọn vẹn toàn bộ các list kỹ năng công nghệ mà không bị phớt lờ).
    *   **Bộ lọc rác**: Loại bỏ thực thể có độ dài < 2 hoặc chỉ chứa chữ số.
    *   **Bộ nhãn phân vùng**:
        *   Vùng Summary & Experience, technical_skills: `["Technical Skill", "Tool", "Methodology", "Soft Skill"]`.
        *   Vùng Education: `["Education Major", "Certification"]`.
    *   **Đầu ra**: Danh sách `raw_entities` gồm `{text, label, zone_type}`.

---

### Bước 3: Định danh và Neo giữ kỹ năng (Mapping & Anchoring)

*   **Lớp Trừu tượng (Tường thuật)**:
    Khi ứng viên ghi "Java", chúng ta cần biết họ nói về ngôn ngữ lập trình hay hòn đảo Java. Bằng cách sử dụng chức danh chuẩn của họ làm "Mỏ neo", chúng ta xác định được "tọa độ" chính xác của kỹ năng đó trên bản đồ tri thức (Taxonomy).

*   **Lớp Logic (Toán học/Quy trình)**:
    1.  **Tính tương đồng**: Chuyển đổi từ ngữ thành Vector và tính **Cosine Similarity** (thể hiện qua `Distance = 1 - Similarity`) trong ChromaDB.
    2.  **Mỏ neo (Anchoring)**: Sử dụng `Job_Title_Standardized` để định hướng nhánh chuyên mục nếu không rỗng (Ví dụ: Backend vs Data).
    3.  **Giải quyết xung đột (Tie-breaking)**:
        *   *Ưu tiên 1*: Nhánh phù hợp với Mỏ neo.
        *   *Ưu tiên 2*: Nút có khoảng cách ngắn nhất (Distance nhỏ nhất).
        *   *Ưu tiên 3*: Lấy kết quả đầu tiên nếu bằng điểm.
    4.  **Sửa lỗi nhãn (Category Correction)**: Kiểm tra đường dẫn (Path) trong Taxonomy. Nếu Path xác định là công cụ (Tools) nhưng NER gán là Chứng chỉ (Certification), hệ thống sẽ ghi đè nhãn thành `Technical Skill`.

*   **Lớp Cụ thể (Kỹ thuật thực thi)**:
    *   **Ngưỡng Mapping (Thresholds)**:
        *   `Technical Skills`: **Distance < 0.25** (Tương đương Similarity > 0.75).
        *   `Soft Skills`: **Distance < 0.25**.
    *   **Đầu ra**: `mapped_entities` chứa `taxonomy_id` và `path` từ cây tri thức.

---

### Bước 4: Phân tích và Tính toán thâm niên làm việc

*   **Lớp Trừu tượng (Tường thuật)**:
    Quy trình này đóng vai trò như một cỗ máy thời gian, quét qua lịch sử làm việc để xem mỗi kỹ năng đã đồng hành cùng ứng viên trong bao lâu. Nó biến những dòng mô tả công việc thành những con số "thời gian thực chiến" cụ thể.

*   **Lớp Logic (Toán học/Quy trình)**:
Bước 1: Chia nhỏ khối kinh nghiệm (Chunking theo Template)
Dựa vào template trích xuất "cứng" của Resume từ Parser, mỗi dự án/kinh nghiệm đều kết thúc bằng cụm từ khóa có chứa danh sách kỹ năng môi trường `Environment: [...]`. Code sẽ cắt khối work_experience thành từng đoạn (Job block). Hệ thống tìm kiếm theo Regex khoảng `Environment` cho đến vị trí đóng `]`, và cắt rời đoạn text từ mốc đầu đến sau khoảng `]`. Cách "tách cắt neo cấu trúc" này đảm bảo các block kinh nghiệm không bao giờ lọt và giúp chia rẽ biệt lập nội dung skill giữa các giai đoạn của ứng viên. Mọi block kinh nghiệm sẽ có Date và skill map riêng của nó.

Bước 2: Trích xuất khoảng thời gian (Date Parsing)
Với mỗi nhóm Job Block đã cắt ở bước trên, hệ thống dùng Regex để tìm cặp ngày bắt đầu - ngày kết thúc (ví dụ: 2018 - 2021 hoặc 2020 - Present).
Các mốc thời gian này được thiết lập thành các khoảng thời gian (Intervals) cụ thể có dạng `(start_date, end_date)`. Nếu block đó không có thời gian Date Parsing hợp lệ, hệ thống sẽ bỏ qua để không nhầm lẫn date từ module dưới.

Bước 3: Đối chiếu Kỹ năng và Hợp nhất Thời gian (Skill Matching & Interval Merging)
Đây là bước quan trọng để tránh tính lặp số năm kinh nghiệm.
- Code sẽ lấy danh sách các kỹ năng (mapped_entities) và kiểm tra xem tên kỹ năng đó có xuất hiện trong đoạn văn bản đang xét hay không.
- Nếu có, khoảng thời gian `(start, end)` của dự án sẽ được thêm vào danh sách quản lý thời gian của kỹ năng đó.
- **Hợp nhất (Merging)**: Khác với việc cộng dồn thô sơ, hệ thống tiến hành hộp nhất các khoảng thời gian bị chồng lấn (overlap) của một kỹ năng (Ví dụ: `(2018, 2021)` và `(2020, 2024)` sẽ được gộp thành một khoảng duy nhất `(2018, 2024)`).
- Tổng thời gian (tính bằng năm) được tính cộng dồn từ các khoảng thời gian đã được hợp nhất để đảm bảo không bị tính đúp.

Bước 4: Kiểm soát và Giới hạn (Limiting)
Cuối cùng, để tránh việc số năm kinh nghiệm của một kỹ năng bị "thổi phồng" (do làm nhiều dự án song song), code sẽ đối chiếu với tổng số năm kinh nghiệm thực tế (Years_of_Exp) trích xuất từ Header:

Nếu tổng số năm của kỹ năng > Tổng số năm làm việc của ứng viên, code sẽ tự động hạ xuống bằng mức Years_of_Exp để đảm bảo tính logic.

*   **Lớp Cụ thể (Kỹ thuật thực thi)**:
    *   **Đầu vào**: Văn bản thô vùng `work_experience` và danh sách `mapped_entities`.
    *   **Regex Thời gian**: Nhận diện các định dạng `Jan 2015`, `01/2015`, `2015 - Present`, v.v.
    *   **Đầu ra**: Danh sách kỹ năng kèm số năm kinh nghiệm (`years`) và danh sách các vùng ghi nhận (`zones`).

---

### Bước 3: Hợp nhất và Chuẩn hóa dữ liệu (Aggregation & Consolidation)

*   **Lớp Trừu tượng (Tường thuật)**:
    Sau khi đã bóc tách và định danh mọi thứ, chúng ta gom tất cả các mảnh ghép lại để tạo ra một bản hồ sơ DNA hoàn chỉnh. Bước này đảm bảo không có thông tin nào bị trùng lặp và mọi thứ đều nằm đúng vị trí của nó.

*   **Lớp Logic (Toán học/Quy trình)**:
    1.  **Khử trùng liên vùng**: Nếu kỹ năng A xuất hiện ở cả Summary và Experience, hệ thống sẽ gộp lại và lấy hợp (Union) các vùng xuất hiện (`zones`).
    2.  **Phân loại rổ dữ liệu**: Tách riêng Kỹ năng cứng (Hard Skills), Kỹ năng mềm (Soft Skills), Chứng chỉ (Certifications) và Học vấn để đưa vào cấu trúc JSON.
    3.  **Học vấn (Education Level)**: Nhận dạng Regex được ưu tiên thứ tự từ bậc học cao nhất đến thấp nhất (`PhD` -> `Master` -> `Bachelor`) để tránh cắt ngang mạch khi ứng viên cung cấp danh sách học vị ở một dòng string dài và bị bỏ sót thông tin `Master` bởi chữ `Bachelor` ở sau.
    4.  **Giữ lại Unmapped**: Các kỹ năng không tìm thấy trong Taxonomy vẫn được giữ lại với `taxonomy_id = null` để phục vụ so khớp từ khóa thô.

*   **Lớp Cụ thể (Kỹ thuật thực thi)**:
    *   **Đầu ra**: Cấu trúc JSON cuối cùng gồm 4 block chính: `Information`, `Hard_Skills` (Direct_Mention & Certifications), `Soft_Skills`, và `Education`.

---

## 3. Cấu trúc Output Mong đợi (DNA Profile JSON)

```json
{
  "Information": {
    "Name": "Adelina Erimia",
    "Years_of_Exp": 14.0,
    "Job_Title_Original": "Project/Program Manager",
    "Job_Title_Standardized": "Project_Management_and_Business_Analysis"
  },
  "Hard_Skills": {
    "Direct_Mention": [
      { "skill": "Java", "taxonomy_id": "Java_Ecosystem", "years": 8.5, "zones": ["experience", "technical_skills"] },
      { "skill": "Unmapped_Skill", "taxonomy_id": null, "years": 0.0, "zones": ["summary"] }
    ],
    "Certifications": ["PMP", "AWS Certified Cloud Practitioner"]
  },
  "Soft_Skills": [
    { "skill": "Stakeholder Management", "taxonomy_id": "management-skills" }
  ],
  "Education": {
    "Major": "Business Administration",
    "Degree": "Master"
  }
}
```

Tài liệu này là cam kết kỹ thuật để xây dựng một hệ thống xử lý CV khoa học, công bằng và có độ chính xác cao.