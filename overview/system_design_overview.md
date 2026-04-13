# Tài liệu Kiến trúc Hệ thống Resume Ranking Tổng thể

## 1. Bản chất bài toán

*   **Resume Ranking thực chất là gì?**: Là quá trình tự động xác định mức độ phù hợp của một tập hợp hồ sơ ứng viên (Resumes) so với một bản mô tả công việc (Job Description) cụ thể, từ đó sắp xếp chúng theo thứ tự ưu tiên giảm dần.
*   **Phân loại bài toán**:
    *   **Information Retrieval (IR)**: JD đóng vai trò là "Truy vấn" (Query), Resumes là "Tài liệu" (Documents).
    *   **Recommendation System**: Gợi ý các "Item" (Ứng viên) tốt nhất cho "User" (Nhà tuyển dụng).
    *   **Learning to Rank (LTR)**: Sử dụng các mô hình học máy để tối ưu hóa hàm xếp hạng thay vì chỉ tính toán độ tương đồng thuần túy.
*   **Input / Output**:
    *   **Input**: File CV (PDF/Docx/Ảnh), Job Description (Text), và các tiêu chí lọc biên (Kinh nghiệm, Địa điểm).
    *   **Output**: Danh sách ứng viên đã xếp hạng, Điểm số (Score), Giải thích sự phù hợp (Explanations), và Phân tích khoảng cách kỹ năng (Skill-gap Analysis).

## 2. Các thách thức chính

*   **Semantic Gap**: Sự khác biệt trong cách dùng từ giữa ứng viên và nhà tuyển dụng (ví dụ: "Backend Developer" vs "NodeJS Specialist"). Sự so khớp từ khóa đơn thuần không giải quyết được vấn đề này.
*   **CV không chuẩn format**: Layout đa dạng (nhiều cột, bảng biểu, đồ họa, ảnh) khiến các công cụ OCR truyền thống đọc sai thứ tự văn bản, làm mất ngữ nghĩa.
*   **Data Sparsity**: Các kỹ năng hiếm hoặc các thuật ngữ mới xuất hiện (ví dụ: "Prompt Engineering") có thể không có đủ dữ liệu để mô hình học tốt.
*   **Bias (Định kiến)**: Các mô hình AI có thể học theo các định kiến lịch sử về giới tính, tuổi tác hoặc trường học từ dữ liệu tuyển dụng cũ.
*   **Explainability**: Các mô hình Transformer (Black-box) thường khó giải thích tại sao một ứng viên lại bị xếp hạng thấp hơn người khác, gây khó khăn cho việc thuyết phục HR.
*   **Adversarial CV (Gaming CV)**: Ứng viên sử dụng kỹ thuật "nhồi từ khóa" (với cỡ chữ 0 hoặc màu trắng) để đánh lừa hệ thống.

## 3. Dataset & Dữ liệu

*   **Các loại dataset phổ biến**: Kaggle Resume Dataset, LinkedIn Scraped Data, và các bộ dữ liệu NER chuyên dụng như Resume-Entities.
*   **Thách thức thu thập dữ liệu thật**: 
    *   **Quyền riêng tư (PII)**: Dữ liệu CV chứa thông tin cá nhân nhạy cảm, cần quy trình ẩn danh hóa (Anonymization) cực kỳ nghiêm ngặt.
    *   **Thiếu nhãn "Negative"**: Rất khó để có được dữ liệu về những người bị loại một cách công bằng; dữ liệu thường chỉ có những ứng viên đã được nhận.
*   **Data Leakage**: Việc CV và JD có các đoạn văn bản giống hệt nhau (do ứng viên copy từ JD vào CV) có thể làm model bị "overfit", đánh giá cao quá mức sự tương đồng bề mặt.

## 4. Các hướng tiếp cận chính

### 4.1. Rule-based & Regex
*   **Nguyên lý**: Sử dụng các tập luật cứng và biểu thức chính quy để đếm từ khóa và bóc tách thông tin cấu trúc (Email, SĐT).
*   **Khi nào dùng**: Vòng lọc thô đầu tiên (Hard constraints) để loại các ứng viên thiếu tiêu chuẩn bắt buộc (ví dụ: "Phải có bằng lái xe").

### 4.2. Classical Machine Learning (SVM, Random Forest)
*   **Nguyên lý**: Dùng TF-IDF hoặc Bag-of-Words để chuyển văn bản thành vectơ và dùng các mô hình phân loại để dự đoán độ phù hợp.
*   **Khi nào dùng**: Khi tài nguyên tính toán hạn chế và cần một mô hình nhanh, dễ triển khai.

### 4.3. Transformer & Embedding (S-BERT, DeBERTa)
*   **Nguyên lý**: Chuyển text sang không gian Dense Vector (384-768 chiều). Tính toán Cosine Similarity để đo mức độ tương đồng ngữ nghĩa.
*   **Khi nào dùng**: Cốt lõi của mọi hệ thống hiện đại để giải quyết bài toán "Search" và "Semantic Gap".

### 4.4. Learning to Rank (RankSVM, Pairwise Ranking)
*   **Nguyên lý**: Không chấm điểm độc lập, mà huấn luyện mô hình để so sánh cặp (Pairwise). AI học cách nhận diện: "Giữa A và B, ai tốt hơn cho JD này?".
*   **Khi nào dùng**: Khi cần sự tinh tế trong xếp hạng, giúp phân loại rõ ràng các ứng viên có điểm số gần bằng nhau.

### 4.5. Multi-agent System & LLM
*   **Nguyên lý**: Chia hệ thống thành các Agent chuyên biệt (Agent bóc tách, Agent đánh giá kỹ năng, Agent Moderator). Sử dụng LLM để "suy luận" và tóm tắt.
*   **Khi nào dùng**: Khi cần tính giải thích cao, hỗ trợ đa ngôn ngữ xuất sắc và cần khả năng tương tác/phản hồi (Feedback loop) cho ứng viên.

## 5. Kiến trúc hệ thống đề xuất (Proposed Architecture)

### Pipeline xử lý:
1.  **Layout Analysis**: Sử dụng YOLOv9 hoặc LayoutLM để nhận diện các vùng Functional Blocks (Skills, Experience, Education) trên hình ảnh/PDF CV.
2.  **Multimodal OCR**: Trích xuất text theo phân vùng đã nhận diện để duy trì thứ tự ngữ nghĩa.
3.  **Semantic Parsing**: Dùng Bi-LSTM-CRF hoặc GLiNER để bóc tách thực thể (Skills, Years of Exp, Job Titles).
4.  **Hybrid Scorer**:
    *   *Hard-score*: Khớp từ khóa và năm kinh nghiệm (Jaccard).
    *   *Soft-score*: Tính độ tương đồng ngữ nghĩa (S-BERT Cosine Similarity).
5.  **Re-ranking Layer**: Dùng Cross-Encoder hoặc LLM-Agent để so sánh chi tiết Top 10 ứng viên tiềm năng nhất.
6.  **Explainability Engine**: Sinh các đoạn văn bản giải thích lý do xếp hạng và gợi ý Skill-gap.

### Công nghệ đề xuất:
*   **CV**: YOLOv9, EasyOCR / Tesseract.
*   **NLP Core**: S-BERT (HuggingFace), spaCy, GLiNER.
*   **Orchestration**: LangChain hoặc CrewAI (cho Multi-agent).
*   **Vector DB**: Pinecone hoặc Weaviate để lưu trữ và tìm kiếm vector CV nhanh chóng.

## 6. Evaluation (Đánh giá)

*   **NDCG (Normalized Discounted Cumulative Gain)**: Metric quan trọng nhất, đánh giá xem các ứng viên tốt nhất có thực sự nằm ở vị trí đầu danh sách hay không.
*   **RBO (Rank-Biased Overlap)**: Đo lường mức độ tương đồng giữa thứ tự xếp hạng của AI và thứ tự xếp hạng của chuyên gia nhân sự (HR).
*   **MRR (Mean Reciprocal Rank)**: Đánh giá vị trí trung bình của ứng viên "phù hợp nhất" đầu tiên.
*   **A/B Testing**: Đo lường sự thay đổi trong hiệu suất tuyển dụng thực tế (Time-to-hire, Screen-to-interview ratio).

## 7. Hạn chế và Hướng phát triển

*   **Bias**: Cần các kỹ thuật **Debiasing** (ví dụ: ẩn tên, giới tính khi AI chấm điểm).
*   **Vấn đề Gaming CV**: Cần kết hợp thêm dữ liệu từ mạng xã hội chuyên nghiệp (LinkedIn, GitHub) để kiểm chứng tính xác thực (Nhóm 2).
*   **Tính động của dữ liệu**: Kỹ năng ngành IT thay đổi hàng tháng. Hệ thống cần cơ chế **Continuous Learning** để update các vector nhúng từ điển kỹ năng mới.
*   **Tâm lý người dùng**: HR thường chưa tin tưởng AI hoàn toàn. Giải pháp là chuyển từ "Tự động quyết định" sang "Hỗ trợ ra quyết định" (Decision Support System).
