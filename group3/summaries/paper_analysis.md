# Phân tích từng paper (Group 3: Transformer Models & Embedding Techniques)

## 1. Comparing BERT and S-BERT for Automated Resume Screening

* **Các vấn đề xảy ra trong bài báo**:
    * Sàng lọc thủ công quá tải, tốn thời gian và dễ tạo ra định kiến (bias).
    * BERT truyền thống chậm và không tối ưu cho so sánh độ tương đồng giữa các câu/đoạn văn lớn.
* **Dataset**:
    * **Tên dataset**: Dataset thu thập từ LinkedIn, Freshers World, v.v.
    * **Quy mô**: 223 CV, 7 Job Descriptions.
    * **Đặc điểm**: PDF chuyển sang Excel/Text.
* **Phương pháp**:
    * **Mô hình**: Transformer (BERT-base vs S-BERT MiniLM).
    * **Kỹ thuật chính**: Keyword Extraction, Sentence Embedding, Cosine Similarity.
* **Cách hoạt động**:
    1. **Preprocessing**: Với BERT, thực hiện lemmatization, stemming và loại bỏ stop words để lấy keyword. Với S-BERT, trích xuất các câu gồm cụm 10 từ.
    2. **Embedding**: Dùng BERT để tạo vector 768 chiều cho keyword; dùng S-BERT tạo vector 384 chiều cho câu.
    3. **Similarity**: Tính toán độ tương đồng Cosine giữa vector của JD và vector của CV.
    4. **Ranking**: Xếp hạng dựa trên điểm số và đối chiếu với kết quả của 3 quản lý HR độc lập.
* **Kết quả**:
    * **Metric**: Accuracy (S-BERT 90% vs BERT 86%), Screening time (S-BERT 0.061s vs BERT 1s).
* **Điểm mạnh**: S-BERT nhanh hơn gấp nhiều lần và cho kết quả sát với người thực hơn nhờ khả năng hiểu ngữ nghĩa câu thay vì chỉ keyword đơn lẻ.
* **Hạn chế**: Quy mô dataset còn nhỏ; mô hình MiniLM của S-BERT có thể bỏ sót các ngữ cảnh quá phức tạp.
* **Insight rút ra**: S-BERT là lựa chọn tối ưu cho hệ thống thực tế cần tốc độ cao và độ chính xác ổn định mà không tốn quá nhiều tài nguyên phần cứng.

---

## 2. Hybrid Transformer-Based Resume Parsing and Job Matching Using TextRank, SBERT, and DeBERTa

* **Các vấn đề xảy ra trong bài báo**:
    * CV có định dạng phi cấu trúc phức tạp (bảng biểu, hình ảnh).
    * Keyword-based matching bỏ qua ý nghĩa ngữ cảnh và mối quan hệ giữa các từ.
* **Dataset**:
    * **Tên dataset**: Dữ liệu thực tế và ground truth.
    * **Quy mô**: Không nêu rõ tổng số nhưng có 4 role mẫu (Flutter, Project Manager, Electrical, AR/VR).
    * **Đặc điểm**: Unstructured resumes.
* **Phương pháp**:
    * **Mô hình**: Hybrid (TextRank + SBERT + DeBERTa + spaCy).
    * **Kỹ thuật chính**: Extractive Summarization, NER, Composite Scoring.
* **Cách hoạt động**:
    1. **Parsing**: Dùng DeBERTa-v3 và spaCy NER để trích xuất thực thể (Name, Skills, Experience, Education). Dùng Regex cho Email/Contact.
    2. **Summarization**: Dùng SBERT (all-MiniLM-L6-v2) mã hóa các câu, xây dựng đồ thị tương đồng, sau đó dùng PageRank (TextRank) để chọn ra 3 câu quan trọng nhất làm tóm tắt (Summary).
    3. **Matching**: Tính toán 4 luồng điểm: Skill Match (Jaccard), Role Match (Difflib), Experience Match (Absolute Difference), và Context Match (SBERT Cosine).
    4. **Scoring**: Tổng hợp điểm Composite = 0.4*Skill + 0.3*Exp + 0.2*Context + 0.1*Role.
* **Kết quả**:
    * **Metric**: Precision/Recall/F1 (81.25%).
* **Điểm mạnh**: Kết hợp được cả luật cứng (Regex, Jaccard) và AI (DeBERTa, SBERT), giúp hệ thống vừa chính xác vừa có tính giải thích.
* **Hạn chế**: Công thức trọng số (weighting) mang tính chủ quan của tác giả.
* **Insight rút ra**: Việc dùng TextRank để tóm tắt CV trước khi matching giúp giảm nhiễu thông tin cực tốt.

---

## 3. Enhanced Resume Screening for Smart Hiring using Sentence-BERT (S-BERT)

* **Các vấn đề xảy ra trong bài báo**:
    * Sự lỗi thời của keyword matching dẫn đến "keyword stuffing" (ứng viên cố tình nhồi nhét từ khóa).
    * Hệ thống cũ không hiểu được các kỹ năng tương đương nhưng được viết bằng từ khác nhau.
* **Dataset**:
    * **Tên dataset**: Anonymous Job Applicants pool.
    * **Quy mô**: 223 resumes.
    * **Đặc điểm**: PDF chuyển sang CSV.
* **Phương pháp**:
    * **Mô hình**: S-BERT (Sentence-BERT).
    * **Kỹ thuật chính**: Text Normalization, Embedding Association, Cosine Distance.
* **Cách hoạt động**:
    1. **Preprocessing**: Thực hiện Lemmatization và Stemming kết hợp để đưa từ về gốc chuẩn.
    2. **Concatenation**: Nối các keyword quan trọng thành một "câu giả" (pseudo-sentence) đại diện cho CV.
    3. **Embedding**: Đưa câu này qua S-BERT để tạo dense vector.
    4. **Matching**: Tính Cosine Similarity giữa CV embedding và JD embedding.
* **Kết quả**:
    * **Metric**: Accuracy (90%), Precision (85%), Recall (75%).
* **Điểm mạnh**: Khả năng chống lại "keyword stuffing" nhờ hiểu ngữ nghĩa thay vì đếm từ.
* **Hạn chế**: Việc nối keyword thành "câu giả" có thể phá vỡ cấu trúc ngữ pháp tự nhiên của model S-BERT.
* **Insight rút ra**: Để tăng độ chính xác, cần kết hợp cả Stemming lẫn Lemmatization trước khi đưa vào model Transformer.

---

## 4. AI-Driven Resume Parsing and Ranking: Leveraging NLP and ML

* **Các vấn đề xảy ra trong bài báo**:
    * Khó khăn trong việc xử lý định dạng file đa dạng (docx, pdf, text).
    * Sự thiếu hụt cơ chế phản hồi (feedback loop) để model tự học từ quyết định của HR.
* **Dataset**:
    * **Tên dataset**: Masked resumes & Job posts.
    * **Quy mô**: 500 CV, 50 job posts.
    * **Đặc điểm**: Đa định dạng (Word, PDF, Text).
* **Phương pháp**:
    * **Mô hình**: Hybrid (DistilBERT + Random Forest + TF-IDF).
    * **Kỹ thuật chính**: NER (spaCy), Contextual Extraction, Ensemble Learning.
* **Cách hoạt động**:
    1. **Parsing**: Dùng spaCy NER trích xuất thực thể và DistilBERT để hiểu ngữ cảnh các block text.
    2. **Vectorization**: Dùng TF-IDF để chuyển đổi text thành vector đặc trưng.
    3. **Classification**: Dùng mô hình Random Forest để dự đoán độ phù hợp ("Suitable" vs "Not Suitable").
    4. **Feedback Loop**: Tích hợp giao diện Flask để HR chấm điểm lại, từ đó huấn luyện lại Random Forest để thích nghi với tiêu chí mới.
* **Kết quả**:
    * **Metric**: Processing time (2.3s/CV).
* **Điểm mạnh**: Có cơ chế dự đoán tính phù hợp và gợi ý Skill Gap cho ứng viên.
* **Hạn chế**: TF-IDF là kỹ thuật cũ, không mạnh bằng Dense Embedding của Transformer trong việc hiểu ngữ nghĩa sâu.
* **Insight rút ra**: Random Forest là model "top-layer" rất tốt để kết hợp các feature từ Transformer, giúp hệ thống dễ giải thích hơn.

---

## 5. Resume2Vec: Intelligent Resume Embeddings for Precise Candidate Matching

* **Các vấn đề xảy ra trong bài báo**:
    * Thử thách trong việc lựa chọn kiến trúc Transformer tối ưu (Encoder vs Decoder) cho bài toán matching.
    * Sự khác biệt giữa kết quả AI và đánh giá cảm tính của con người ở các ngành nghề khác nhau.
* **Dataset**:
    * **Tên dataset**: Kaggle Resume Dataset & LinkedIn scraped JDs.
    * **Quy mô**: 15,000 CV, 2,500 Job Descriptions (10 ngành nghề).
    * **Đặc điểm**: Anonymized resumes.
* **Phương pháp**:
    * **Mô hình**: So sánh BERT, RoBERTa, DistilBERT (Encoders) và GPT-4, Gemini, Llama (Decoders).
    * **Kỹ thuật chính**: Neural Embeddings, PCA (Principal Component Analysis), Cosine Similarity.
* **Cách hoạt động**:
    1. **Preprocessing**: Làm sạch text, xóa HTML, chuẩn hóa ký tự.
    2. **Embedding**: Sử dụng song song các model từ truyền thống (BERT) đến hiện đại (Llama 3, Gemini) để tạo vector cho CV và JD.
    3. **Dimension Reduction**: Dùng PCA để giảm chiều dữ liệu và trực quan hóa (cluster) độ tương đồng giữa các nhóm ngành.
    4. **Matching**: Sử dụng Llama-based embeddings (được chứng minh là tốt nhất) để tính Cosine Similarity và xếp hạng.
* **Kết quả**:
    * **Metric**: nDCG (tăng 15.85%), RBO (Rank-Biased Overlap tăng 15.94%) so với ATS truyền thống. Accuracy phân loại ngành đạt 95.5% với Llama + Random Forest.
* **Điểm mạnh**: Chứng minh rằng mô hình Decoder-only (Llama) tạo ra embedding chất lượng hơn Encoder-only trong bài toán matching CV-JD.
* **Hạn chế**: Chi phí tài nguyên và API lớn khi dùng các model Decoder khổng lồ.
* **Insight rút ra**: Llama là state-of-the-art hiện nay cho việc tạo embedding. RBO là metric tốt hơn Accuracy để đo lường độ tương đồng giữa thứ tự xếp hạng của AI và con người.
