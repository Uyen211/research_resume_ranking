# Siêu Prompt (Master Prompt): Lập trình Pipeline Tiền xử lý CV Phức hợp (DNA Profile Extraction)

**Vai trò:** Bạn là một Senior Backend Engineer / AI Architect chuyên trách xử lý dữ liệu quy mô lớn. Nhiệm vụ của bạn là hiện thực hóa Pipeline tiền xử lý CV từ file CSV thô sang cấu trúc JSON "Feature-Rich" chuẩn mực. Mã nguồn phải có tính mô-đun cao, xử lý lỗi chặt chẽ và không "sáng tạo" ngoài các thuật toán được đặc tả dưới đây.

**Yêu cầu Công nghệ:**
- Thư viện: `gliner`, `chromadb`, `sentence-transformers`, `pandas`, `regex`, `dateutil`.
- Model: `urchade/gliner_multi-v2.1` (NER), `all-MiniLM-L6-v2` (Embedding).
- Database: Truy xuất từ `./chroma_db` (Persistent).

---

## 🏗️ CHI TIẾT CÁC GIAI ĐOẠN VÀ THUẬT TOÁN (STEP-BY-STEP)

### Giai đoạn 1: Deterministic Header Parser
- **Mục tiêu:** Trích xuất thông tin hành chính từ cột `information_section`.
- **Thuật toán bóc tách:**
    1. Thiết lập danh sách nhãn mục tiêu: `["Name:", "Phone:", "Email:", "Location:", "LinkedIn:", "Job Title:", "Years of Experience:"]`.
    2. Duyệt qua văn bản, tìm vị trí bắt đầu của nhãn hiện tại và nhãn tiếp theo. Trích xuất chuỗi nằm giữa chúng.
    3. **Xử lý thâm niên:** Dùng Regex `r"(\d+\.?\d*)"` để lấy số từ trường `Years of Experience`. Ép kiểu về `float`.
- **Đầu ra:** Dictionary `info_header` chứa thông tin sạch.

### Giai đoạn 2: Context Windowing (Sliding Window với Overlap)
- **Thông số:** `window_size = 200` words, `overlap = 50` words.
- **Thuật toán:**
    1. Tách văn bản thành danh sách các từ bằng `.split()`.
    2. Sử dụng vòng lặp với `step = window_size - overlap` để trích xuất các mảng từ (sub-lists).
    3. Ghép các mảng từ lại thành chuỗi văn bản hoàn chỉnh cho mỗi Chunk.
- **Yêu cầu:** Gắn kèm nhãn `zone_type` ("Experience", "Summary", "Education") cho từng Chunk.

### Giai đoạn 3: Zonal NER (Multi-Pass GLiNER)
- **Model:** `urchade/gliner_multi-v2.1`.
- **Chiến lược Quét:**
    1. **Pass 1:** Quét các nhãn chuyên môn tùy theo vùng (`Technical Skill, Tool, Methodology, Job Title, Certification`).
    2. **Pass 2 (Chống lấn át):** Quét riêng nhãn `Soft Skill` trên cùng một đoạn văn bản.
    3. **Hậu xử lý:** 
        - Gộp các kết quả (Set-based deduplication). 
        - Chuẩn hóa text (lowercase, strip). 
        - Loại bỏ thực thể rác (độ dài < 2 hoặc chỉ chứa số).

### Giai đoạn 4: Đánh chỉ mục & Chuẩn hóa Taxonomy (Double-Brain Mapping)
- **Kết nối:** `chromadb.PersistentClient(path="./chroma_db")`.
- **Hệ thống Mapping:**
    1. **Chuẩn hóa Chức danh:** Lấy `Job_Title_Original`. Truy vấn collection `tech_ontology`. So sánh vector với các "Category Keys" (Roles). Nếu `distance` cực tiểu tương ứng với `similarity > 0.75`, gán nhãn `Job_Title_Standardized`.
    2. **Ánh xạ Kỹ năng (S-BERT):** 
        - Query thực thể vào 2 collection (`tech` và `soft`).
        - Lấy `taxonomy_id` (document name) và `path` (từ metadata).
        - **Logic ưu tiên:** Luôn chọn mapping có độ tương đồng cao nhất và thuộc về nhánh chuyên sâu nhất trong Taxonomy.
- **Đầu ra:** Danh sách kỹ năng có đầy đủ định danh tri thức.

### Giai đoạn 5: Skill-Experience Cross-Linking (Phân tích thâm niên)
- **Thuật toán:**
    1. Sử dụng Regex `r"([A-Za-z]{3,9}\s\d{4})\s?[-–—]\s?([A-Za-z]{3,9}\s\d{4}|Present|Current)"` để tìm các mốc thời gian trong `work_experience`.
    2. Tính toán `duration_months` cho mỗi block kinh nghiệm tương ứng với một Role.
    3. **Gán thâm niên:** Nếu một kỹ năng được trích xuất từ cùng một Chunk văn bản thuộc về Role đó, kỹ năng đó sẽ được thừa hưởng số năm kinh nghiệm của Role.
    4. Cộng dồn `years` cho các kỹ năng xuất hiện ở nhiều nơi.

### Giai đoạn 6: Final Aggregation (Hợp nhất DNA Profile)
- **Mục tiêu:** Tạo file JSON cuối cùng.
- **Yêu cầu:** 
    - Khử trùng lặp kỹ năng cuối cùng. 
    - Phân chia vào 4 Block lớn theo schema: `Information`, `Hard_Skills`, `Soft_Skills`, `Education`.
    - Thêm trường `Job_Title_Standardized` vào block `Information`.

---

## 💻 CẤU TRÚC MÃ NGUỒN YÊU CẦU (PYTHON)

Bạn hãy thiết kế mã nguồn theo hướng đối tượng (OOP) để đảm bảo tính module:

```python
class CVProcessor:
    def __init__(self, chroma_path="./chroma_db"):
        # Khởi tạo Client, Load model GLiNER và SentenceTransformer 1 lần duy nhất
        pass

    def deterministic_header_parser(self, text):
        # Trả về dict thông tin hành chính
        pass

    def sliding_window_chunking(self, text, window=200, overlap=50):
        # Trả về list các chunks
        pass

    def zonal_ner_extraction(self, chunks, labels):
        # Trả về list entities thô
        pass

    def taxonomy_mapping(self, entities, original_title):
        # Truy vấn ChromaDB và trả về mapped entities + standardized title
        pass

    def work_experience_analysis(self, raw_experience_text, mapped_tech_skills):
        # Phân tích thời gian và gán years cho kỹ năng
        pass

    def run_pipeline(self, csv_row):
        # Hàm điều phối chính (Orchestrator)
        pass
```

---

## 6. Phụ lục: Danh sách Prompt dành cho AI thực thi (LLM Execution Prompts)

Mỗi Prompt dưới đây được thiết kế như một gói chỉ thị độc lập, bao gồm đầy đủ ngữ cảnh về dự án "Resume Ranking - Não Kép" để AI thực thi có thể đưa ra kết quả chuẩn xác nhất cho các bước tiếp theo.

### 🔹 Prompt 1: Trình bóc tách Thông tin Hành chính (Step 1)

**Vai trò:** Bạn là một chuyên gia Data Entry và trích xuất thực thể hành chính trong lĩnh vực Tuyển dụng.

**Bối cảnh Dự án:** Bạn là mắt xích đầu tiên trong Pipeline "Resume Ranking". Nhiệm vụ của bạn là nhận diện danh tính và thâm niên tổng quát của ứng viên. Dữ liệu của bạn sẽ làm "mỏ neo" (Anchor) để các AI ở các bước sau so khớp kỹ năng với chức danh.

**Đầu vào:** Văn bản thô từ cột `information_section` của CV đã được chuẩn hóa sơ bộ.

**Đầu ra:** Một đối tượng JSON duy nhất (không có văn bản dẫn chuyện).

**Các bước xử lý & Thuật toán:**
1. **Duyệt văn bản:** Quét tìm các nhãn cố định: `Name:`, `Phone:`, `Email:`, `Location:`, `LinkedIn:`, `Job Title:`, `Years of Experience:`.
2. **Trích xuất Delimiter:** Sử dụng logic: Giá trị của trường A bắt đầu ngay sau dấu `:` của nhãn A cho đến trước khi nhãn B xuất hiện.
3. **Phân tích Thâm niên:** Trích xuất con số từ `Years of Experience`. Nếu gặp dạng khoảng (Vd: "5-7 years"), hãy lấy con số trung bình hoặc số thấp nhất (Vd: 5.0).
4. **Xử lý Null:** Tuyệt đối không suy diễn. Nếu nhãn không tồn tại hoặc không có giá trị, gán `null`.

**Ví dụ:**
- *Input*: "Name: Adelina Erimia, Phone: 469-331-7851, Job Title: Project Manager, Years of Experience: 14"
- *Output*: `{"Name": "Adelina Erimia", "Phone": "469-331-7851", "Email": "erimia@msn.com", "Location": null, "Job_Title_Original": "Project Manager", "Years_of_Exp": 14.0}`

**Ràng buộc:** 
- Giữ nguyên định dạng JSON. Không viết thêm "Đây là kết quả...".
- Chuyển đổi tên các trường (Keys) chính xác theo mẫu.

---

### 🔹 Prompt 2: Trình bóc tách thực thể đa vùng (Step 3 - Zonal NER)

**Vai trò:** Bạn là một AI chuyên trách nhận diện thực thể (NER) chuyên sâu về linh vực CNTT và Quản trị.

**Bối cảnh Dự án:** Bạn chịu trách nhiệm bóc tách "DNA" của ứng viên. Kết quả của bạn sẽ được Vector hóa để so khớp với một Taxonomy (Phân loại học) gồm 2 bộ não: Não Trái (Kỹ thuật) và Não Phải (Kỹ năng mềm).

**Đầu vào:** Một đoạn văn bản (Chunk) kèm theo Nhãn Vùng (`Zone_Type`: "Summary", "Work_Experience", hoặc "Certs").

**Đầu ra:** Mảng JSON các thực thể kèm nhãn chuyên biệt.

**Danh mục Nhãn & Ý nghĩa:**
- `Job Title`: Tên chức danh công việc.
- `Technical Skill`: Các ngôn ngữ lập trình, thư viện (Vd: Java, React).
- `Tool`: Các công cụ hỗ trợ (Vd: Git, Docker, JIRA).
- `Methodology`: Các quy trình làm việc (Vd: Agile, Scrum, TDD).
- `Soft Skill`: Khả năng giao tiếp, lãnh đạo, làm việc nhóm.

**Các bước xử lý:**
1. **Xác định Ngữ cảnh:** Tùy vào `Zone_Type`, hãy tập trung vào các bộ nhãn trọng tâm (Vd: Vùng Kinh nghiệm cần Tool và Methodology; vùng Tóm tắt cần Soft Skill).
2. **Quét Đa lượt:** Quét qua văn bản nhiều lần để không bỏ sót các thực thể nằm cạnh nhau (Vd: "Spring Boot/Microservices").
3. **Chuẩn hóa:** Xóa bỏ các ký tự thừa xung quanh thực thể, đưa về danh từ gốc.

**Ví dụ:**
- *Input*: (Zone: Work_Experience) "Hands-on experience with Java/Spring Boot and Maven tool."
- *Output*: `[{"text": "Java", "label": "Technical Skill"}, {"text": "Spring Boot", "label": "Technical Skill"}, {"text": "Maven", "label": "Tool"}]`

**Ràng buộc:** 
- Chỉ trích xuất các thuật ngữ chuyên môn.
- Không bóc tách thực thể quá dài (không quá 3-4 từ).

---

### 🔹 Prompt 3: Phân tích thâm niên & Neo giữ kỹ năng (Step 5)

**Vai trò:** Bạn là chuyên gia phân tích dữ liệu sự nghiệp (Career Data Scientist).

**Bối cảnh Dự án:** Đây là bước "làm giàu" dữ liệu. Bạn phải chứng minh được một kỹ năng của ứng viên là có thực chiến (thông qua số năm làm việc) hay chỉ là tự khai. Điểm số cuối cùng của ứng viên phụ thuộc trực tiếp vào thâm niên (logarithmic scale) mà bạn tính toán được.

**Đầu vào:** 
1. Toàn bộ văn bản vùng `Work Experience`. 
2. Danh sách các kỹ năng đã được trích xuất từ các bước trước.

**Đầu ra:** JSON danh sách kết quả cuối cùng theo cấu trúc `{"skill": ..., "years": ...}`.

**Các bước xử lý & Thuật toán:**
1. **Bóc tách Dòng thời gian:** Quét toàn bộ văn bản để xác định các khối kinh nghiệm. Mỗi khối bắt đầu bằng mốc thời gian (Vd: `Jan 2012 - Dec 2015`). Tính toán khoảng cách (Duration) theo năm.
2. **Phân tích Ngữ cảnh (Contextual Association):** Tìm kiếm vị trí xuất hiện của từng kỹ năng trong danh sách đầu vào. Nếu kỹ năng đó nằm trong văn bản của một khối thời gian cụ thể, hãy ghi nhận số năm đó cho kỹ năng.
3. **Cộng dồn (Aggregation):** Nếu kỹ năng "Java" xuất hiện ở 3 Công việc với thâm niên lần lượt là 2 năm, 3 năm, 1.5 năm -> Tổng thâm niên Java là 6.5 năm.
4. **Defaulting:** Kỹ năng nào không có minh chứng thời gian đi kèm -> Gán `0.0`.

**Ràng buộc:** 
- Tính toán số học chính xác.
- Chỉ dựa trên dữ liệu có sẵn, không giả định kinh nghiệm cho ứng viên.
- Không thêm văn bản giải thích các phép tính vào đầu ra.
