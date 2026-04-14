# Research: Hệ Thống Xếp Hạng CV Tự Động (Hybrid Dual-Brain Taxonomy)

Dự án này tập trung vào việc nghiên cứu và xây dựng một hệ thống đánh giá, xếp hạng CV tối ưu cho CPU, sử dụng mô hình "Não Kép" (Dual-Brain) để kết hợp giữa khớp kỹ năng kỹ thuật (Hard Skills) chính xác và phân tích ngữ nghĩa kỹ năng mềm (Soft Skills).

---

## 📁 Cấu Trúc Thư Mục (Project Structure)

Dưới đây là chi tiết ý nghĩa và nhiệm vụ của từng thư mục phản ánh đúng trạng thái thực tế của dự án:

### 1. `code/` (Mã Nguồn Thực Thi)
Nơi chứa toàn bộ mã nguồn thực thi chính của dự án (chủ yếu qua định dạng Jupyter Notebook cho Google Colab và các script Python).
*   **`cv_processing/`**: Script tiền xử lý và bóc tách cấu trúc (DNA profile) từ CV ứng viên (`cv_dna_colab_v1.ipynb`, `preprocessDataCV.ipynb`).
*   **`jd_processing/`**: Script làm sạch, phân tích taxonomy và làm giàu dữ liệu từ Yêu cầu công việc (JD) (`clean_taxonomy.py`, `preprocessJD_V2.ipynb`).
*   **`scoring/`**: Động cơ chấm điểm đa tầng (Composite Scoring) thực hiện đọ khớp JD - CV và xuất bảng xếp hạng CSV (`composite_scoring_colab.ipynb`).

### 2. `data/` (Kho Lưu Trữ Dữ Liệu Thực Nghiệm)
Nơi chứa toàn bộ dữ liệu đầu vào và các phân đoạn lưu trữ kết quả trung gian.
*   **`JD/`**: 17 bản mô tả công việc gốc (text thô) thuộc 5 role cốt lõi.
*   **`Cleaned_JD_V2/`**: Các file JD đã được làm sạch và chuẩn hóa siêu cấu trúc JSON.
*   **`clean_resumes/` & `resumes_segment4/`**: Bộ dữ liệu CV của ứng viên đã qua làm sạch và phân đoạn.
*   **`chroma_db/`**: Cơ sở dữ liệu Vector cục bộ (ChromaDB) chuyên đảm nhiệm việc truy vấn ngữ nghĩa song song thần tốc.
*   **`taxonomy/`**: Lưu trữ "Bộ não" tri thức nền (Bộ từ điển đa ngành, kỹ năng).

### 3. `project/` (Đặc Tả Quy Trình & Kiến Trúc Thuật Toán)
Thư mục lưu trữ toàn bộ "linh hồn" thuật toán, đặc tả kiến trúc bằng văn bản và hướng dẫn tích hợp:
*   **`pipeline/`**: Phân rã thành 3 luồng xử lý:
    *   **`CV/`**: Đặc tả luồng bóc tách CV (`cv_dna_colab_v1.md`, `preprocessDataCV.md`).
    *   **`pipeline_process_JD/`**: Đặc tả luồng xử lý và làm giàu JD (`pipelineProcessJD.md`).
    *   **`pipline_evaluate/`**: Tài liệu lõi về công thức điểm nền, điểm vượt trần của hệ thống chấm điểm (`composite_scoring_pipeline.md`).
*   **`summaries_pipeline/`**: Chứa **Ai Integration Guide** (Hướng dẫn cho Software Engineer tích hợp AI vào API/Backend nội bộ).
*   **`dataset_overview.md` & `kb_mapping.md`**: Tài liệu thống kê thông tin tổng quan của dữ liệu và hệ ontology.

### 4. `group1/` đến `group4/` (Bộ Sưu Tập Nghiên Cứu Khoa Học)
Lưu trữ các tài liệu, bài báo khoa học phục vụ cho thiết kế lõi:
*   **`papers/`**: Tập hợp các bài báo SOTA PDF đã được parser hóa sáng định dạng Markdown về AI Ranking, NER.
*   **`summaries/`**: Các bản tóm tắt thu hoạch, diễn giải ý tưởng thuật toán áp dụng.

### 5. `overview/` (Tài Liệu Cấp Cao)
*   **`system_design_overview.md`**: Bức tranh tổng thể hệ thống (Architecture flow).
*   **`groupInformation.md`**: Ghi chú về từng cụm dữ liệu dự án.

### 6. `prompt/` (Xưởng Sản Xuất Mã Nguồn)
Lưu trữ các "Chỉ thị thiết kế" (Prompts) nhằm tái sử dụng hoặc điều khiển LLM sinh code tự động cho dự án mà không cần gõ mã thủ công.

### 7. `scratch/` (Khu Vực Thử Nghiệm)
Chứa các script và notebook nháp, là nơi sandbox bóc tách thuật toán hoặc thử nghiệm các thư viện mới trước khi đóng gói nhúng mượt vào thư mục `code/`.

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
