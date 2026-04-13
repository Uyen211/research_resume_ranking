# Phân tích từng paper (Group 4: Applied Systems)

## 1. Design and Development of Machine Learning Based Resume Ranking System

* **Các vấn đề xảy ra trong bài báo**:
    * Sàng lọc thủ công tốn thời gian và dễ sai sót.
    * Thách thức trong việc tìm đúng ứng viên phù hợp với yêu cầu JD từ hàng nghìn hồ sơ.
* **Dataset**:
    * **Tên dataset**: Kaggle Resume Dataset & Collected resumes.
    * **Quy mô**: ~50 resumes (Java Developer, Project Manager).
    * **Đặc điểm**: Văn bản thuần được trích xuất từ file doc/docx/pdf.
* **Phương pháp**:
    * **Mô hình**: Machine Learning truyền thống (KNN, TF-IDF).
    * **Kỹ thuật chính**: Content-based filtering, MCQ Screening (kiểm tra kiến thức cơ bản trước khi nộp CV), Cosine Similarity.
* **Cách hoạt động**:
    1. **MCQ Screening**: Ứng viên phải làm bài kiểm tra trắc nghiệm; chỉ khi đạt điểm tối thiểu mới được tải CV lên.
    2. **Text Pre-processing**: Loại bỏ khoảng trắng, stop words, stemming. Dùng `gensim` để tóm tắt văn bản.
    3. **Vectorization**: Dùng TF-IDF để chuyển CV và JD sang không gian vector.
    4. **Ranking**: Tính Cosine Similarity. Dùng KNN để tìm và xếp hạng top K ứng viên có khoảng cách gần nhất với JD.
* **Kết quả**:
    * **Metric**: Parsing Accuracy (85%), Ranking Accuracy (92%).
* **Điểm mạnh**: Tích hợp vòng kiểm tra (MCQ) giúp lọc bớt ứng viên không đạt yêu cầu kỹ thuật cơ bản, giảm tải cho bước xử lý AI.
* **Hạn chế**: Quy mô dataset thử nghiệm quá nhỏ (50 CV); TF-IDF không hiểu được ngữ nghĩa sâu.
* **Insight rút ra**: Việc thêm một bước "Pre-screening" (như Test hoặc Survey) trước khi AI rank CV là một chiến thuật thực tế hiệu quả để đảm bảo chất lượng ứng viên đầu vào.

---

## 2. Improved Candidate-Career Matching Using Comparative Semantic Resume Analysis

* **Các vấn đề xảy ra trong bài báo**:
    * Khoảng cách ngữ nghĩa (semantic gap) giữa cách con người đánh giá (so sánh tương đối) và máy tính đánh giá (điểm số tuyệt đối).
    * Khó nhận diện những khác biệt nhỏ giữa các ứng viên xuất sắc nếu chỉ dùng điểm số đơn thuần.
* **Dataset**:
    * **Tên dataset**: Collected Technical Resumes (GitHub, Kaggle, LinkedIn).
    * **Quy mô**: 228 resumes chuyên gia kỹ thuật.
    * **Đặc điểm**: Đa định dạng (pdf, docx, txt).
* **Phương pháp**:
    * **Mô hình**: RankSVM (Ranking Support Vector Machine).
    * **Kỹ thuật chính**: Comparative Semantic Analysis, NER (spaCy), Relative Attributes.
* **Cách hoạt động**:
    1. **Feature Extraction**: Trích xuất 13 thuộc tính ngữ nghĩa (Education, Exp, Skills, Hobbies, v.v.).
    2. **Relative Labeling**: Gán nhãn tương đối (Very High đến None) cho mỗi thuộc tính của từng CV.
    3. **Comparative Analysis**: Thực hiện so sánh cặp (pairwise comparison) giữa tất cả các CV. Ví dụ: CV A "Cao hơn" CV B về kỹ năng chuyên môn.
    4. **Ranking via SVM**: Dùng RankSVM để học từ các so sánh cặp này và đưa ra thứ tự xếp hạng cuối cùng.
* **Kết quả**:
    * **Metric**: Accuracy 92% (cao hơn hẳn so với việc chỉ dùng điểm số tuyệt đối - 33%). F1-score trung bình 0.98.
* **Điểm mạnh**: Khả năng phân loại cực tốt (unique scores), tránh được tình trạng nhiều ứng viên bị trùng điểm số (redundant scores) như các hệ thống cũ.
* **Hạn chế**: Chi phí tính toán cho việc so sánh cặp (pairwise) sẽ tăng rất nhanh khi số lượng CV lớn (N x N-1).
* **Insight rút ra**: Thay vì chỉ chấm điểm 1-10, việc dạy AI so sánh "CV nào tốt hơn CV nào" (Pairwise Ranking) mang lại kết quả xếp hạng trung thực hơn nhiều.

---

## 3. An Artificial Intelligence Resume Analysis and Career Position Prognosis System

* **Các vấn đề xảy ra trong bài báo**:
    * Hệ thống ATS truyền thống quá phụ thuộc vào keyword, bỏ qua ngữ cảnh.
    * Thiếu sự định hướng và phản hồi cho ứng viên về khoảng cách kỹ năng (skill gap).
* **Dataset**:
    * **Tên dataset**: Anonymized candidate profiles (public repositories + simulated data).
    * **Quy mô**: Không nêu rõ tổng số, nhưng bao phủ 5 lĩnh vực IT (Software Dev, Data Science, v.v.).
    * **Đặc điểm**: Unstructured text.
* **Phương pháp**:
    * **Mô hình**: Hybrid (ML: Random Forest + Transformer: BERT).
    * **Kỹ thuật chính**: NER, Contextual Embeddings, Skill-Gap Analysis.
* **Cách hoạt động**:
    1. **Parsing**: Trích xuất thông tin cấu trúc bằng NLP (NER).
    2. **Role Prediction**: Dùng BERT để lấy vector ngữ cảnh và đưa vào Random Forest/SVM để dự đoán vị trí nghề nghiệp phù hợp nhất.
    3. **Skill-Gap Analysis**: So sánh kỹ năng của ứng viên với "Skill Repository" của ngành để chỉ ra những gì còn thiếu.
    4. **Recommendation**: Gợi ý các khóa học hoặc chứng chỉ để ứng viên hoàn thiện hồ sơ.
* **Kết quả**:
    * **Metric**: Accuracy cho dự đoán Career Role đạt 95.5% (vượt trội so với baseline 90.3%).
* **Điểm mạnh**: Kết hợp giữa "Xếp hạng" và "Tư vấn" (Career Advice), tạo ra giá trị cho cả nhà tuyển dụng và ứng viên.
* **Hạn chế**: Phụ thuộc nhiều vào chất lượng của bộ từ điển kỹ năng ngành (Skill Repository).
* **Insight rút ra**: Hệ thống không nên chỉ dừng ở việc "Rank", mà nên chỉ ra "Tại sao trượt" và "Cần học gì" (Skill Gap Analysis) để tăng tính minh bạch và trải nghiệm người dùng.

---

## 4. AI Powered Multimodal Resume Ranking Web Application for Wide Scale Hiring

* **Các vấn đề xảy ra trong bài báo**:
    * Sự phức tạp của bố cục CV (layout) ảnh hưởng đến độ chính xác của việc trích xuất text (OCR).
    * Cần một hệ thống xử lý được khối lượng lớn (wide-scale) với độ trễ thấp.
* **Dataset**:
    * **Tên dataset**: Custom dataset từ các nguồn royalty-free, Builders, Portals.
    * **Quy mô**: 2,751 resumes.
    * **Đặc điểm**: Multimodal (ảnh CV, PDF, DOCX).
* **Phương pháp**:
    * **Mô hình**: Multimodal (YOLOv9 + BERT + GLiNER).
    * **Kỹ thuật chính**: Object Detection (Layout analysis), OCR, Zero-shot NER, Hybrid Matching (Cosine + BM25).
* **Cách hoạt động**:
    1. **Visual Segmentation**: Dùng **YOLOv9** để nhận diện các vùng tiêu đề, nội dung trên ảnh CV (Layout Analysis).
    2. **OCR**: Dùng **EasyOCR** để đọc text trong các vùng đã segment.
    3. **Classification & NER**: Dùng **mBERT** để phân loại đoạn văn và **GLiNER** (Zero-shot) để trích xuất thực thể mà không cần training lại.
    4. **Hybrid Matching**: Kết hợp điểm Semantic (Cosine Similarity của dense vector) và điểm Keyword (BM25) để rank.
* **Kết quả**:
    * **Metric**: YOLOv9 đạt mAP vượt trội hơn DETR hay Detectron2. Xếp hạng đạt độ tin cậy cao nhờ hiểu được layout.
* **Điểm mạnh**: Xử lý cực tốt các CV có layout phức tạp (nhiều cột, bảng biểu) nhờ bước nhận diện vùng (Layout Detection) trước khi đọc OCR.
* **Hạn chế**: OCR vẫn còn lỗi ở các font chữ nghệ thuật hoặc độ phân giải ảnh thấp.
* **Insight rút ra**: **Layout Analysis** (nhận diện vùng) là chìa khóa để xử lý CV thực tế. Đừng ném cả file vào OCR, hãy cắt nhỏ CV ra từng phần (Header, Skills, Exp) rồi mới đọc text.
