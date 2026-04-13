# Đối chiếu Knowledge Base (Resume Ranking KB Mapping)

Bản đối chiếu này kết nối các thách thức thực tế của dự án với các phương pháp nghiên cứu đã được phân tích từ 4 nhóm bài báo công nghệ.

## 1. Thách thức: Phân tách cấu trúc từ file .docx phức tạp
*   **Vấn đề thực tế**: CV có nhiều cột, bảng biểu, định dạng không chuẩn (Work History vs Experience).
*   **Giải pháp (Group 4)**: Sử dụng mô hình **YOLOv9** hoặc các kiến trúc **LayoutLM** để nhận diện vùng (Layout Analysis). Không nên đọc văn bản theo dòng từ trên xuống dưới một cách mù quáng; thay vào đó, cần phân đoạn CV thành các "Block" chức năng (Skills, Edu, Exp) trước khi trích xuất nội dung.
*   **Ứng dụng**: Áp dụng cho bước tiền xử lý để đảm bảo thông tin "Skills" trong bảng Technical Skills không bị trộn lẫn với mô tả dự án.

## 2. Thách thức: Noisy Labels & Job Title chuẩn hóa
*   **Vấn đề thực tế**: Hơn 50 biến thể cho chỉ vài chức danh chính (BA, Java Dev, PM).
*   **Giải pháp (Group 2)**: Sử dụng kiến trúc **Multi-agent và LLM Automation**. Triển khai một Agent chuyên trách việc "Data Cleansing" và "Taxonomy Mapping". Agent này sử dụng tri thức từ LLM (Gemini 2.0 Flash) để ánh xạ các nhãn nhiễu về một bộ từ điển chuẩn (Standard Job Dictionary).
*   **Giải pháp (Group 3)**: Sử dụng **S-BERT** để đo khoảng cách ngữ nghĩa giữa các nhãn nhiễu. Các nhãn có độ tương đồng >0.85 có thể được gộp lại sau khi được LLM kiểm chứng.

## 3. Thách thức: CV quá dài (>6000 từ) và Skill hiếm
*   **Vấn đề thực tế**: Trình độ ứng viên rất cao (Sr., Architect), nội dung cực kỳ chi tiết, dễ gây tràn Context window.
*   **Giải pháp (Group 3)**: Sử dụng các mô hình Transformer như **DistilBERT** hoặc **DeBERTa** để trích xuất thực thể (NER). Thay vì rank toàn bộ CV, hệ thống chỉ rank các "Contextual Embeddings" của các kỹ năng thực tế và kinh nghiệm trọng tâm.
*   **Giải pháp (Group 4)**: **Skill-Gap Analysis**. So sánh từng kỹ năng chuyên ngành (Hadoop, v.v.) với tập yêu cầu của công việc để tạo ra ma trận kỹ năng, thay vì đánh giá cảm tính.

## 4. Thách thức: Độ chính xác và Tính minh bạch trong xếp hạng
*   **Vấn đề thực tế**: Làm thế nào để phân biệt giữa "Sr. Java" và "Java Lead" khi cả hai đều giỏi?
*   **Giải pháp (Group 4)**: **Pairwise Ranking (RankSVM)**. Thay vì dùng điểm số tuyệt đối, ta sử dụng mô hình so sánh cặp. Cách tiếp cận này giúp AI phát hiện ra các chi tiết nhỏ (ví dụ: chứng chỉ chuyên sâu) giúp một ứng viên vượt lên người khác.
*   **Ứng dụng thực tế**: Sử dụng LLM (với cơ chế Chain-of-Thought) để so sánh cặp 5 ứng viên đứng đầu và đưa ra lý do (Explainability) cho HR.

## Bảng tóm tắt Mapping

| Vấn đề thực tế | Nhóm bài báo hỗ trợ | Công nghệ khóa |
| :--- | :--- | :--- |
| Trích xuất bố cục (.docx) | Group 1 & 4 | YOLOv9, Layout Detection |
| Chuẩn hóa Job Titles nhiễu | Group 2 | LLM Agent, Clustering |
| Đối sánh kỹ năng chuyên sâu | Group 3 | S-BERT, DeBERTa NER |
| **Dự báo nghề nghiệp (CV -> JD)** | **Group 4 (Paper 3)** | **Career Position Prognosis** |
| **Phân tích khoảng cách kỹ năng** | **Group 4 (Paper 3)** | **Skill-Gap Analysis Engine** |
| **Xử lý JD đơn giản (Generic JD)** | **Group 2 (Paper 4)** | **JD Expansion & Enrichment** |
| Xếp hạng tinh tế Top 10 | Group 4 | RankSVM, Pairwise Comparison |
