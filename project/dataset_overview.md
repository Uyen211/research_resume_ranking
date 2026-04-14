# Tổng quan Tập dữ liệu & Cấu trúc Phân tích (Resume Ranking Project)

Tài liệu này cung cấp bức tranh toàn cảnh về tập dữ liệu đầu vào và các hệ thống tri thức (Taxonomy) đang được sử dụng trong dự án Xếp hạng phân loại CV (Resume Ranking) ở thời điểm hiện tại.

## 1. Thành phần Dataset Hiện tại

Hệ thống đang xử lý và phân loại tập dữ liệu phức tạp bao gồm 3 lõi chính: Tập CV ứng viên, Tập Yêu cầu công việc (JD), và Hệ thống Tri thức chuyên môn (Taxonomy).

### 1.1. Tập dữ liệu Hồ sơ ứng viên (Resumes Dataset)
*   **Số lượng**: 228 hồ sơ (CV) chất lượng cao.
*   **Định dạng hiện tại**: Đã được số hóa và phân mảnh từ định dạng ban đầu sang dạng JSON cấu trúc hóa (`clean_resumes/` và `resumes_segment4/`).
*   **Đặc điểm văn bản & Thách thức**:
    *   **Siêu dài & Phức tạp**: Chiều dài dao động lớn, đa số vượt ngưỡng 2000 từ, tối đa >6000 từ. 
    *   **Nhiễu loạn cấu trúc**: Chứa lịch sử làm việc dày đặc thuật ngữ kỹ thuật, xen kẽ với bảng biểu, cột sidebar và thành tích đa dạng.

### 1.2. Tập dữ liệu Yêu cầu công việc (Job Descriptions - JD)
*   **Số lượng & Phân mục**: Hơn 15 mẫu JD thực tế được phân loại vào 5 nhóm chức danh chính, bao gồm:
    *   **BA**: Business Analyst (4 mẫu)
    *   **DA_DE**: Data Analyst / Data Engineer (3 mẫu)
    *   **PM**: Project Manager (2 mẫu)
    *   **SM**: Scrum Master (2 mẫu)
    *   **SW**: Software Engineer / Developer (6 mẫu)
*   **Định dạng**: File văn bản thô (.txt) ban đầu tại `data/JD/` đã được đi qua luồng Pipeline xử lý JD thành các đối tượng JSON chuẩn hóa tại `data/Cleaned_JD_V2/`.

### 1.3. Hệ quản trị Tri thức & Vector (Taxonomy & ChromaDB)
*   **Định dạng**: Từ điển tri thức dạng JSON chứa các cây kỹ năng phân tầng (Taxonomy gốc tại `data/taxonomy/`). 
*   **Vector Database (`data/chroma_db/`)**: Thể hiện hệ thống não bộ sử dụng mô hình S-BERT (`all-MiniLM-L6-v2`) mã hóa toàn bộ cây tri thức dưới dạng Vector 384 chiều, phục vụ tính toán Cosine Distance.
*   **Não Kép (Dual-Brain Ontology)**: Chia rẽ tách biệt 2 nguồn dữ liệu `tech_ontology` (kỹ năng cứng/công nghệ có threshold chuẩn xác < 0.4) và `soft_skills_ontology` (kỹ năng mềm có threshold < 0.4).

---

## 2. Luồng Tiền xử lý Dữ liệu (ETL Data Pipeline)

Để giải quyết các thách thức từ văn bản tự do, tập CV đã trải qua các bước tiền xử lý chuyên sâu:

1.  **Làm sạch (Text Cleaning)**: Chuẩn hóa Unicode NFC, xử lý dấu ký tự điều hướng không chuẩn (Bullet formatting) và chuẩn hóa khoảng trắng.
2.  **Phân mảnh thông minh (Semantic Segmentation)**: 
    *   Sử dụng AI siêu nhẹ và tốc độ cao (**Gemini 3.1 Flash Lite Preview**).
    *   CV trên 2000 từ được phân mảnh kết hợp tóm tắt (Summarize), trong khi CV dưới 2000 từ được phân đoạn thuần túy. 
    *   Output đóng gói dữ liệu vào 5 thẻ XML-like: `<INFORMATION_SECTION>`, `<SUMMARY_SECTION>`, `<SKILLS_SECTION>`, `<EXPERIENCE_SECTION>`, `<EDUCATION_SECTION>`.
3.  **Lưu kết quả**: Dữ liệu sau được lưu tập trung tại file `df_resumes_segmented_final.csv`, sẵn sàng để Pipeline CV DNA quét lại bằng hệ thống học sơ đồ (GLiNER).

## 3. Bản chất của Vấn đề Cốt lõi & Hướng Giải quyết

*   **Vấn đề Context Window & Nghẽn Cổ Chai AI**: Đưa CV trên 6000 từ trực tiếp vào mô hình Vector truyền thống hoặc LLM trực tiếp thường gây mất thông tin (Loss in the middle) và tốn tài nguyên. -> *"Giải quyết qua việc dùng Gemini 3.1 thu gọn thành Segment trước, và Zonal Chunking (cắt khúc 200 từ) ở giai đoạn NER kế tiếp."*
*   **Khoảng cách Ngữ nghĩa (Semantic Gap)**: Lỗi chính tả hay từ đồng nghĩa (VD: React vs ReactJS) sẽ làm thất bại thuật toán string match thông thường. -> *"Giải quyết thông qua việc map Vector với Hệ tri thức Não Kép áp dụng S-BERT."*
