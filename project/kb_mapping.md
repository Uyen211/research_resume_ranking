# Sơ đồ Đối chiếu Tri thức (Resume Ranking Knowledge Base Mapping)

Bản đối chiếu này kết nối trực tiếp các thách thức thực tế của dự án với các phương pháp giải quyết tối ưu (Pipeline) đang được triển khai thực tiễn trong codebase. Thiết kế hệ thống bám sát tinh thần ứng dụng tính minh bạch và chi phí thực thi tối ưu (Explainable AI - XAI).

## 1. Thách thức: Trích xuất thực thể từ văn bản siêu dài và lộn xộn
*   **Vấn đề**: CV có độ dài lớn (2000 - 6000 từ), cấu trúc trình bày vô vàn biến thể, không thể parse bằng Regex thông thường. Đồng thời, việc đưa toàn bộ vào LLM gây rủi ro ảo giác (Hallucination) và tốn kém Token (Rate Limit).
*   **Giải quyết**: Sử dụng quy trình tiếp cận nhiều tầng (Multi-layer):
    *   **Tầng 1 (Gemini 3.1 Flash Lite)**: Tiền phân mảnh đoạn dữ liệu theo thẻ XML (Segmenting) để gom mục đích nội dung theo cụm (Summary, Skills, Experience, Education).
    *   **Tầng 2 (GLiNER Zonal NER)**: Chia nhỏ văn bản thành các Chunk ~200 từ, gối đầu 50 từ (Overlap). Sử dụng mô hình Machine Learning Nhãn Không Cần Dữ Liệu Lớn (`urchade/gliner_multi-v2.1`) trích xuất kỹ năng chính xác theo từng vùng (Zonal Context).

## 2. Thách thức: Chuẩn hóa ngóc ngách chuyên môn & Dữ liệu không hoàn hảo (Semantic Gap)
*   **Vấn đề**: "Machine Learning" do máy nhận diện có thể nằm trong vùng kỹ năng cứng, hoặc nằm trong một chứng chỉ. "Bán hành" và "Sales" thực chất giống nghĩa. Cần 1 xương sống đối chiếu vững chắc và đồng nhất.
*   **Giải quyết**: Chuyển đổi toàn bộ kỹ năng trích ra Vector thông qua mô hình Embedding **S-BERT (`all-MiniLM-L6-v2`)**.
    *   Lưu trữ không gian điểm Vector vào hệ cơ sở dữ liệu siêu tốc **ChromaDB**.
    *   **Dual-Brain Ontology**: Đưa ra quyết định "Lọc cứng - Mapping Tech" hoặc "Lọc mềm - Mapping Soft Skill" dựa trên ngưỡng Distance `< 0.4`. Kỹ thuật này giúp phân định rạch ròi kỹ năng thực sự thay vì đếm từ khóa (Keyword match) mù quáng.

## 3. Thách thức: Mở rộng nhu cầu JD mà không bị "Ảo Giác" (JD Enrichment)
*   **Vấn đề**: HR thường viết JD một cách nghèo nàn hoặc quá hàn lâm. CV ứng viên có "FastAPI" nhưng JD chỉ ghi "Python". Nếu so chuẩn thì ứng viên trượt, nhưng thực tế lập trình viên đó có tiềm năng sâu.
*   **Giải quyết**: **Top-K Sibling Expansion**.
    *   Trong Pipeline xử lý JD, sau khi dùng GLiNER bắt được nhãn chính (Must-have), hệ thống sẽ đâm vào cây tri thức **Taxonomy** để lôi ra tối đa 10 kỹ năng họ hàng gần nhất (Siblings) thả vào rổ Nice-to-have (Expansion). Tránh hoàn toàn việc sử dụng Text Generation của LLM tự biên bịa các kỹ năng không tồn tại.

## 4. Thách thức: Công bằng trong Xếp hạng và Đánh giá Thâm niên
*   **Vấn đề**: Làm sao so sánh giá trị một chuyên gia làm Java 5 năm so với Fresher Java 1 năm? Đánh gộp tất cả có nguy cơ cào bằng.
*   **Giải quyết**: 
    *   **Interval Merging thuật toán (Thuật toán hợp nhất khoảng thời gian)**: Xuyên suốt luồng phân tích Kinh nghiệm, hệ thống tính toán và hợp nhất chính xác tổng mốc thời gian kinh nghiệm (`float years`) của mỗi Skill.
    *   **Composite Scoring Pipeline**: Kết xuất bằng công thức Logarit cho hệ số kinh nghiệm `(1 + ln(years+1))` để thưởng điểm lũy thừa không tuyến tính. Điểm giới hạn (Capping) chặn ở 100 điểm trần cho JD khớp cơ bản, điểm phụ dôi dư tính vào Spillover Bonus để vinh danh các ứng viên vượt chuẩn (Overqualified).

## Bảng Tóm tắt Mapping Thực hành

| Thách thức Dự án | Kiến trúc Pipeline (Solution File) | Công nghệ / Thuật toán Cốt lõi |
| :--- | :--- | :--- |
| **CV siêu dài vượt Context Window** | `preprocessDataCV.ipynb` | LLM Phân đoạn (Gemini 3.1), XML tagging |
| **Tránh nhiễu văn cảnh CV (NER)** | `cv_dna_colab_v1.ipynb` | GLiNER Zonal Nhận diện, Chunking 200 từ |
| **Không trùng khớp câu chữ Job/Skill** | `cv_dna_colab_v1.ipynb`, `preprocessJD_V2.ipynb` | Dual-Brain Ontology, S-BERT, ChromaDB Vector |
| **Mở rộng JD an toàn chống Hallucination** | `preprocessJD_V2.ipynb` | Sibling Expansion (Top-10), Set Deduplication |
| **Tính khoảng thời gian tinh xảo** | `cv_dna_colab_v1.ipynb` | Timestamp Regex, Date Interval Merging |
| **Đánh giá Xếp hạng Minh bạch & Công bằng** | `composite_scoring_colab.ipynb` | Logarithmic Experience Multiplier, 5-Component Scoring, Spillover Bonus |
