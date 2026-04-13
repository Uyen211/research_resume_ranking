# Research: Hệ Thống Xếp Hạng CV Tự Động (Hybrid Dual-Brain Taxonomy)

Dự án này tập trung vào việc nghiên cứu và xây dựng một hệ thống đánh giá, xếp hạng CV tối ưu cho CPU, sử dụng mô hình "Não Kép" (Dual-Brain) để kết hợp giữa khớp kỹ năng kỹ thuật (Hard Skills) chính xác và phân tích ngữ nghĩa kỹ năng mềm (Soft Skills).

---

## 📁 Cấu Trúc Thư Mục (Project Structure)

Dưới đây là chi tiết ý nghĩa và nhiệm vụ của từng thư mục trong dự án:

### 1. `data/` (Kho Lưu Trữ Dữ Liệu Thực Nghiệm)
Đây là nơi chứa toàn bộ dữ liệu đầu vào và kết quả trung gian của hệ thống.

*   **`data/JD/`**: Tập hợp **17 bản mô tả công việc** thực tế được phân loại theo 5 vai trò nòng cốt:
    *   `JD_BA`: Business Analyst.
    *   `JD_DA_DE`: Data Analyst / Data Engineer.
    *   `JD_PM`: Project Manager.
    *   `JD_SM`: Scrum Master.
    *   `JD_SW`: Software Engineer.
*   **`data/taxonomy/`**: Lưu trữ "Bộ não" tri thức nền. Thư mục `taxonomy_processed/` chứa 2 file JSON đã được rút gọn 57% nhiễu ngữ nghĩa: `tech_ontology.json` (6 domain công nghệ) và `soft_skills_ontology.json`.
*   data/Cleaned_JD_V2/`**: Tập hợp **17 bản mô tả công việc** đã được làm sạch và chuẩn hóa.
*   data/resumes_normalized: tập hợp CV đã: tóm tắt, phân đoạn, chuẩn hóa job_title. df_resumes_normalized_full.csv là file csv tổng hợp.

### 2. `pipline/` (Kiến trúc Logic & Quy trình Hệ thống)
Thư mục lưu trữ toàn bộ "linh hồn" thuật toán và các báo cáo nghiên cứu kỹ thuật cốt lõi của dự án.
*   **`pipline/pipeline_process_JD/`**: Tài liệu đặc tả **Pipeline 0 (JD Enrichment)**. Quy trình biến đổi văn bản JD thô thành Structured JSON bằng urchade/gliner_multi-v2.1 và S-BERT. Tập trung vào các kỹ thuật: Đệ quy phẳng hóa cây, Reverse Lookup (Nhìn ngược), và Lan truyền đồ thị (Topological Graph Enrichment) để làm giàu kỹ năng Nice-to-have.
*   **`pipline/pipeline_process_taxonomy/`**: Báo cáo chiến lược **Hệ sinh thái Taxonomy**. Ghi chép quá trình tái cấu trúc từ tệp dữ liệu gốc (2022), phương pháp làm sạch nhiễu ngữ nghĩa (Semantic Noise), thanh lọc domain và chiến lược thiết kế "Não Kép" để giảm 57% chi phí tính toán.
*   **`pipline/pipline_evaluate/`**: Tài liệu về **Composite Scoring Pipeline**. Đặc tả 5 bước đánh giá ứng viên: Tính điểm nền (Base Score Max 100), Điểm thưởng mở rộng (Bonus Score không giới hạn), xử lý Đỉnh Tràn (Spillover) và **Quy tắc So khớp Kép (Dual-Matching Rule)** qua Taxonomy ID chống lạm phát từ khóa.

### 3. `group1/` - `group4/` (Cơ Sở Tài Liệu Nghiên Cứu)
Các thư mục này được phân bổ để lưu trữ các tài liệu nghiên cứu khoa học phục vụ cho bài báo cáo. Mỗi group bao gồm:
*   **`papers/`**: Tập hợp các bài báo khoa học quốc tế (PDF/Text) liên quan đến Resume Ranking, NER, và Ontologies.
*   **`summaries/`**: Các bản tóm tắt thu hoạch kỹ thuật, liệt kê các phương pháp hay có thể áp dụng vào dự án từ các bài báo đó.

### 4. `prompt/` (Xưởng Sản Xuất Mã Nguồn)
Nơi lưu trữ các "Chỉ thị lập trình cấp cao". Thay vì code thủ công, dự án sử dụng các Prompt chi tiết (Vd: `prompt_code_JD_pipeline.md`) để điều khiển AI thế hệ mới sinh ra mã nguồn Python chuẩn xác, tích hợp sẵn ChromaDB và GLiNER theo đúng thiết kế hệ thống.

### 5. `overview/` (Tài Liệu Cấp Cao)
*   `system_design_overview.md`: Mô tả bức tranh tổng thể về luồng dữ liệu từ JD -> Enrichment -> Ranking -> Result.
*   `groupInformation.md`: Đặc tả chi tiết thông tin phân loại và đặc điểm của các nhóm dữ liệu trong dự án.

### 6. `project/`
Chứa các file liên quan đến quản lý dự án, cấu hình môi trường phát triển hoặc các bản phác thảo sơ đồ kiến trúc đang được hoàn thiện.

### 7. `scratch/` (Khu Vực Thử Nghiệm)
Chứa các script Python thử nghiệm quy trình. Nổi bật là `cv_preprocessing.py` (Làm sạch CV bằng thuật toán Regex boundaries cho kỹ năng ngắn), `gen_nb.py` (Tự động sinh mã nguồn môi trường Colab), và **`composite_scoring_colab.ipynb`** (Bảng điều khiển lõi Ranking tự động xuất hàng loạt báo cáo CSV).

---

## 🚀 Công Nghệ Cốt Lõi (Core Technologies)

*   **NER Model**: `urchade/gliner_multi-v2.1` (Trích xuất thực thể đa ngữ).
*   **Embedding Model**: `all-MiniLM-L6-v2` (Vector hóa ngôn ngữ cục bộ).
*   **Vector Database**: `ChromaDB` (Lưu trữ và truy vấn vector dưới ổ cứng).
*   **Logic**: Python (Recursive Flattening, Set Difference Deduplication, Logarithmic Cap & Spillover Calculus).
*   **Engine Deployment**: Google Colab Notebook (Xử lý Dataframes lớn song song).

---

## 📝 Ghi Chú
*   Hệ thống được thiết kế hướng tới **XAI (Explainable AI)**: Mọi quyết định xếp hạng (Base / Bonus / Overflow) đều được trả về bảng csv rõ ràng, ngăn chặn Black-box model hoàn toàn.
*   **Tối ưu CPU**: Luồng toán học cực nhẹ cho phép hàng nghìn hồ sơ được nghiền nát bằng Colab RAM siêu tốc.

---
*Dự án đang trong giai đoạn chuyển hóa Thuật toán Xếp hạng thành Pipeline tự động trên Colab.*
