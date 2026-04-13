
# Đặc tả Kỹ thuật CŨ: Pipeline Tiền xử lý CV Toàn diện (Comprehensive CV Pre-processing) - Version FINAL

Tài liệu này xác định các tiêu chuẩn kỹ thuật và quy trình xử lý dữ liệu để chuyển đổi CV từ tập tin chuẩn hóa sơ bộ (`df_resumes_normalized_full.csv`) sang cấu trúc **Feature-Rich JSON**, phục vụ trực tiếp cho thuật toán so khớp "Não Kép".

---

## 1. Kiến trúc Dữ liệu & Nguồn đầu vào (Data Architecture)

Nguồn dữ liệu duy nhất: `data/resumes_normalized/df_resumes_normalized_full.csv`. Quy trình xử lý tập trung vào 5 vùng dữ liệu chiến lược:

1.  **`information_section`**: Chứa thông tin định danh và hành chính (Name, Contact, Job Title gốc).
2.  **`summary_objective`**: Tóm tắt năng lực và mục tiêu nghề nghiệp.
3.  **`technical_skills`**: Danh sách kỹ năng công nghệ tự khai.
4.  **`work_experience`**: Lịch sử công tác chi tiết (Dữ liệu nền cho Skill Depth).
5.  **`education_certifications`**: Bằng cấp và các chứng chỉ chuyên môn.

---

## 2. Công nghệ & Thư viện sử dụng (Technology Stack)

Hệ thống được thiết kế để chạy cục bộ (Local execution) nhằm tối ưu chi phí và bảo mật dữ liệu, sử dụng các công nghệ SOTA:

*   **Ngôn ngữ lập trình**: Python 3.10+
*   **Mô hình NER**: `GLiNER` (thư viện `gliner`) - Model: `urchade/gliner_multi-v2.1`.
*   **Cơ sở dữ liệu Vector**: `ChromaDB` (thư viện `chromadb`) - Lưu trữ tại `./chroma_db`.
*   **Mô hình Embedding**: `Sentence-Transformers` - Model: `all-MiniLM-L6-v2`.
*   **Xử lý dữ liệu**: `pandas`, `numpy`.
*   **Công cụ bổ trợ**: `regex` (re), `python-dateutil` (xử lý thời gian).


## 3. Quy trình Xử lý Hạt nhân (Core Pipeline)

### Bước 1: Trình bóc tách Thông tin Hành chính (Deterministic Header Parser)
Xử lý cột `information_section` bằng thuật toán **Field-to-Field Delimiter Parsing**:
*   **Đầu vào (Input)**: Văn bản thô từ cột `information_section`.
*   **Mục tiêu**: Trích xuất chính xác 07 trường: `Name`, `Phone`, `Email`, `Location`, `LinkedIn`, `job_title`, `years_of_experience`.
*   **Logic bóc tách**:
    *   Sử dụng cơ chế quét tuần tự. Giá trị của trường A được xác định từ vị trí của nhãn `A:` cho đến vị trí của nhãn `B:` kế tiếp hoặc đến cuối chuỗi.
    *   **Xử lý trường hợp thiếu (Missing Fields)**: Nếu một nhãn không tồn tại trong chuỗi text, giá trị tương ứng sẽ được trả về là `null`.
    *   **Chuẩn hóa dữ liệu**: Trường `years_of_experience` được ép kiểu về `float`. Các trường khác được làm sạch khoảng trắng (strip).
*   **Đầu ra (Output)**: Một Dictionary `header_info` gồm 07 keys chuẩn.

### Bước 2: Tiền xử lý Hậu Gemini (Chunking & Environment Fast-track)
Trước khi đưa vào mô hình NER, dữ liệu từ CSV được xử lý để tối ưu hóa context:
1.  **Section-based NER**: Thực hiện NER độc lập cho từng vùng (`summary`, `experience`, `education`) để sử dụng bộ nhãn (labels) tối ưu cho từng vùng.
2.  **Context Windowing (Sliding Window)**: 
    *   Chia nhỏ các đoạn văn bản dài thành các Chunks ~200 từ.
    *   **Cơ chế Overlap**: Sử dụng bước nhảy (stride) cho các Chunk gối đầu nhau ~50 từ.
    *   Mục tiêu: Đảm bảo không vượt quá giới hạn 512 tokens của GLiNER, đồng thời tránh việc cắt đứt ngữ nghĩa ở ranh giới các đoạn (boundary issues).
3.  **Environment Fast-track**: 
    *   Sử dụng Regex để bóc tách riêng khối `Environment: [...]` do Gemini đã chuẩn hóa ở bước trước.
    *   Các thực thể trong khối này được đưa thẳng vào bước Mapping Taxonomy mà không cần qua mô hình NER.
*   **Đầu ra (Output)**: Danh sách các đối tượng `Chunk {text, zone_type}` và danh sách `env_entities` (nếu có).

### Bước 3: Trích xuất thực thể Phân vùng (Zonal NER - GLiNER)
Hệ thống áp dụng NER có chọn lọc trên các mảnh văn bản (Chunks) đã được xử lý ở Bước 2:
*   **Vùng `summary_objective`**: Quét NER để bóc tách `["Job Title", "Tool", "Methodology", "Technical Skill", "Soft Skill"]`. Việc này giúp giữ lại các thông tin quý giá như "8 years experience" vốn dễ bị hòa tan nếu chỉ dùng vector tổng thể.
*   **Vùng `technical_skills` & `work_experience`**: Quét `["Technical Skill", "Tool", "Methodology", "Job Title", "Soft Skill"]`.
*   **Vùng `education_certifications`**: Trích xuất `["Education Major", "Certification"]`.
*   **Giải pháp Khử trùng sớm (Early Deduplication)**: Do sử dụng Sliding Window với Overlap 50 từ, hệ thống sẽ thực hiện khử trùng thực thể dựa trên nội dung text và vị trí tương đối (span) **chỉ trong phạm vi cùng một vùng dữ liệu (Section)**. Việc lặp lại giữa các vùng khác nhau sẽ được giải quyết ở bước Hợp nhất cuối cùng.
*   **Đầu ra (Output)**: Danh sách `raw_entities {text, label, zone_type}` đã được khử trùng.

### Bước 4: Định danh Taxonomy & Neo giữ Phân tầng (Mapping & Anchoring)
*   **Đầu vào (Input)**: 
    *   Danh sách `raw_entities` (từ Bước 3).
    *   Danh sách `env_entities` (từ Bước 2).
    *   `Job_Title_Original` (từ `header_info` ở Bước 1).
    *   Kết nối tới ChromaDB (`tech_ontology`, `soft_skills_ontology`).
*   **Mục tiêu**: Đảm bảo tính trung thực (No Enrichment) qua các giai đoạn:

1.  **Giai đoạn 1: Chuẩn hóa chức danh (Job Title Standardizing)**: 
    *   Lấy `job_title` bóc tách từ Bước 1.
    *   Sử dụng S-BERT tính Cosine Similarity với danh sách các "Roles" (là các Keys/Categories trong `tech_ontology.json` như Frontend, Backend, Data_and_AI...).
    *   Nếu khớp > 0.75, gán giá trị cho trường `Job_Title_Standardized` không thì để là null.

2.  **Giai đoạn 2: Nút lá cụ thể nhất (Leaf-Node Mapping)**: Thực thể (Vd: "HTM") phải được quy đổi về đúng nút lá cụ thể nhất (Vd: `HTML`). Tuyệt đối không quy đổi về nút cha (Vd: Frontend) để tránh làm giàu ảo.

3.  **Giai đoạn 3: Xử lý Xung đột & Ngưỡng Mapping (Mapping Thresholds)**:
    *   Sử dụng S-BERT tính Cosine Similarity với kho tri thức Taxonomy.
    *   **Quy đổi Metric**: Lưu ý ChromaDB sử dụng `Distance`. Công thức quy đổi: `Distance = 1 - Similarity`.
    *   **Thiết lập Ngưỡng (Thresholds)**:
        *   **Technical Skills**: `Similarity > 0.85` (tương đương `Distance < 0.15`). Bắt buộc khớp cao để tránh gán sai công nghệ.
        *   **Soft Skills**: `Similarity > 0.75` (tương đương `Distance < 0.25`). Nhẹ nhàng hơn để chấp nhận các biến thể ngôn ngữ.
    *   **Xử lý kỹ năng không khớp (Unmapped Skills)**: Nếu độ tương đồng dưới ngưỡng, giữ `taxonomy_id = null`.
    *   **Giải pháp Collision Resolution (Tie-breaking)**: Nếu một từ (Vd: "SQL") khớp với nhiều nút trong Taxonomy:
        *   **Ưu tiên 1**: Sử dụng mỏ neo `Job_Title_Standardized` để chọn nhánh chuyên mục phù hợp (Vd: Database vs BI).
        *   **Ưu tiên 2**: Nếu mỏ neo trống, chọn nút có **Similarity cao nhất**. 
        *   **Ưu tiên 3**: Nếu bằng điểm tuyệt đối, chọn ngẫu nhiên/nút đầu tiên.

4.  **Giai đoạn 4: Tự sửa lỗi nhãn (Category Correction - MỚI)**:
    *   Nếu mô hình NER gắn nhãn thực thể là `Certification` nhưng kết quả tra cứu ChromaDB cho thấy `path` thuộc về nhánh `Tools` hoặc `Technologies`.
    *   Hệ thống sẽ tự động sửa lại nhãn thành `Technical Skill` để đảm bảo tính đồng nhất dữ liệu với Pipeline JD.

5.  **Giai đoạn 5: Neo giữ địa chỉ (Ontological Anchoring)**:
    *   Ghi lại đường dẫn tuyệt đối (`path`) của kỹ năng trong Taxonomy.
    *   **Nguyên tắc No-Enrichment**: Khác với JD, Pipeline CV **KHÔNG** thực hiện mở rộng kỹ năng anh em (Siblings Expansion). Chỉ ghi nhận những gì ứng viên thực sự có hoặc được dùng làm bằng chứng trong kinh nghiệm.

*   **Đầu ra (Output)**: Danh sách `mapped_entities {text, taxonomy_id, path, label}`.

### Bước 5: Phân tích Thâm niên thực chiến (Work Experience Analysis)
*   **Đầu vào (Input)**: Văn bản thô vùng `work_experience` và danh sách `mapped_entities`.
*   **Thuật toán tính `years`**:
    1.  **Timeline Retrieval (Regex)**: Tìm các mẫu thời gian như `Jan 2015 - Dec 2018` hoặc `2020 - Present` để gán cho từng Role.
    2.  **Duration Calculation**: Tính số năm (Vd: `Duration = (End_Date - Start_Date)`).
    3.  **Contextual Association**: Kỹ năng A xuất hiện trong văn bản của Role X sẽ nhận `Years_A = Duration_Role_X`.
    4.  **Aggregation**: Cộng dồn `Total_Years = Σ(Duration)` cho cùng một `taxonomy_id`.
    5.  **Defaulting**: Nếu một kỹ năng được trích xuất từ `technical_skills` hoặc `summary_objective` nhưng không tìm thấy minh chứng trong `work_experience`, giá trị `years` sẽ được gán mặc định là **0**. Trạng thái này sẽ nhận điểm cơ bản nhưng không có điểm thưởng thâm niên trong Pipeline Scoring.
*   **Đầu ra (Output)**: Danh sách `skills_with_experience {skill, taxonomy_id, path, years, zones}`.

---

## 3. Logic Hợp nhất & Khử trùng (Aggregation Logic)

Quy trình hợp nhất (Merging) được thực hiện theo thứ tự để tạo ra JSON cuối cùng:

1.  **Bước 1: Khởi tạo khung JSON**: Lấy `header_info` làm block `Information`.
2.  **Bước 2: Hợp nhất Kỹ năng & Khử trùng liên vùng (Cross-section Aggregation)**:
    *   Sử dụng `taxonomy_id` làm khóa chính. Nếu `taxonomy_id = null`, sử dụng chính `text` (đã lower-case) làm khóa chính.
    *   **Giải quyết trùng lặp liên vùng**: Nếu cùng một kỹ năng xuất hiện ở Summary, Technical Skills và Experience, hệ thống sẽ gộp lại: cộng dồn `years` từ Bước 5 và hợp nhất danh sách `evidence_zones`.
    *   **Xử lý Unmapped Skills**: Các kỹ năng có `taxonomy_id = null` **vẫn được giữ lại** trong danh sách `Direct_Mention`. Điều này cho phép thuật toán Scoring so khớp Exact-match khi gặp kỹ năng tương ứng trong JD gốc.
3.  **Bước 3: Tách rổ Certification**: Các thực thể có label `Certification` được đưa vào mảng `Certifications` riêng biệt trong rổ `Hard_Skills`.
4.  **Bước 4: Hợp nhất Soft Skills (Brain Right)**: Tương tự Hard Skills nhưng lưu vào mảng `Soft_Skills`.
5.  **Bước 5: Xử lý Education**: Lấy thực thể có label từ vùng `education` để điền vào block `Education`.

---