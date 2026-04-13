# Phân tích Chấm điểm CV vs JD thủ công theo Kiến trúc "Composite Scoring Pipeline"

Tài liệu này minh họa cách thuật toán sẽ "tính toán tay" điểm số cho ứng viên trong `scratch/inputoutput.md` (Senior Java Developer) ứng tuyển vào vị trí từ file `JD_SW_1_cleaned.json` (Front End Developers nhưng ruột yêu cầu Java rặt).

## 1. Thiết lập Tham số (Parameters config)
- **Hard Score Weight (W_Hard):** 0.8  (80% điểm cốt lõi là Kỹ năng IT)
- **Constraint Weight (W_Constraints):** 0.2 (20% điểm cốt lõi là Bằng cấp & Năm kinh nghiệm tối thiểu)
- **Bonus Soft Skill (B_Soft):** +1.5 điểm / Kỹ năng mềm match
- **Bonus Certificate (B_Cert):** +3.0 điểm / Chứng chỉ hợp lệ

- **Logic Max Dựa trên "Ứng viên Hoàn Hảo" (Max Years = 5)**:
  - Hàm logarit số năm (YOE): `Multiplier = 1 + ln(years + 1)`
  - Kịch bản Max YOE của JD = 5 năm => Tối đa `Multiplier = 1 + ln(6) = 2.79`.

---

## 2. Tính Tự Động: Ứng viên Hoàn Hảo (Denominator/Mẫu số nền)
Một ứng viên Perfect Match của JD này phải có toàn bộ Must_Have (W=1.0), Nice_To_Have (W=0.7) và Expansion (W=0.3), tất cả đều có 5 năm kinh nghiệm.

- **Must_Have** (8 skills): `java`, `apache kafka`, `nft`, `API Gateway`, `Domain Expertise`, `hsk`, `api testing`, `Basic knowledge`
  > Điểm: `8 * (1.0 * 2.79) = 22.32`
- **Nice_To_Have** (3 skills): `scrum of scrums`, `Basic understanding`, `English`
  > Điểm: `3 * (0.7 * 2.79) = 5.86`
- **Expansion** (46 skills): `spring boot`, `hibernate`, `j2ee`, `spring mvc`, `jpa`, `struts`, `tdd`, v.v.
  > Điểm: `46 * (0.3 * 2.79) = 38.50`

=> **MAX_HARD_SCORE = 22.32 + 5.86 + 38.50 = 66.68 Điểm**

---

## 3. Khớp Kỹ Năng cứng của Candidate (Candidate_Hard_Score)
Chúng ta lấy danh sách Kỹ năng và Số năm *Thực tế* trong `inputoutput.md` ráp vào rổ của JD để tính theo công thức `W * (1 + ln(years + 1))`.

**A. Khớp Rổ Must_Have (W=1.0)**:
- `Java` (14.0 năm) -> Match! => Điểm: `1.0 * (1 + ln(15)) = 3.71`

**B. Khớp Rổ Nice_To_Have (W=0.7)**:
- `scrum of scrums` (Agile/Scrum trong CV - có mapping taxonomy) (2.7 năm) -> Match! => Điểm: `0.7 * (1 + ln(3.7)) = 0.92`

**C. Khớp Rổ Expansion (W=0.3)**:
CV rất mạnh mảng Java. Trúng đậm bộ expansion của JD này:
- `spring boot` (11.5 năm) -> `0.3 * (1 + ln(12.5)) = 0.3 * 3.53 = 1.06`
- `hibernate` (13.8 năm) -> `0.3 * (1 + ln(14.8)) = 0.3 * 3.69 = 1.11`
- `j2ee` (14.0 năm) -> `0.3 * (1 + ln(15.0)) = 0.3 * 3.71 = 1.11`
- `spring` (14.0 năm) -> `1.11`
- `jpa` (0.0 năm) -> `0.3 * (1 + ln(1.0)) = 0.3 * 1.0 = 0.30`
- `struts` (2.3 năm) -> `0.3 * (1 + ln(3.3)) = 0.3 * 2.19 = 0.66`
- `tdd` (2.7 năm) -> `0.3 * (1 + ln(3.7)) = 0.3 * 2.31 = 0.69`
> **Tổng cộng Expansion: 6.04 điểm**

**D. Khớp Rổ Surplus (Kỹ năng có trong CV mà JD không thèm ghi) - Vớt điểm rác (W=0.2)**:
Ứng viên này có AWS (14.0 năm), Docker (11.5 năm), Jenkins (12.8 năm), Oracle 12c (12.8 năm), AngularJS (11.5 năm), NodeJS (11.5 năm) và hơn 30 kỹ năng xịn xò khác.
*(Giả sử tính sơ bộ 30 kỹ năng xịn trung bình 8.0 năm = `30 * 0.2 * (1+ln(9.0))`)*
> **Tổng cộng Surplus ~ 19.18 điểm**

=> **CANDIDATE_HARD_SCORE = 3.71 + 0.92 + 6.04 + 19.18 = 29.85 Điểm**
*(Có Hard_Score này, %Hard_Match sẽ là: `(29.85 / 66.68) * 100 = 44.77%`)*
*Nhờ tăng trọng số Surplus lên 0.2, điểm số của một ứng viên thừa mứa kỹ năng out-trình JD đã tăng vọt.*

---

## 4. Ràng Buộc Cơ Bản (Constraints) - Binary Match
JD yêu cầu:
- `Min_Experience_Years: 8`: Ứng viên có YOE = 14.0 -> **Tuyệt đối đạt (1.0)**
- `Required_Degree: Bachelor's degree`: Ứng viên có "Degree: Master" -> **Tuyệt đối đạt (1.0)**

=> **Score_Constraints = (1.0 * 0.5) + (1.0 * 0.5) = 1.0 (100% rổ ràng buộc)**

---

## 5. Điểm Tổng Kết (Base Score + Bonus)

### 5.1. Base Score (Hệ số Kỹ năng 80% + Ràng buộc 20%)
- Điểm Kỹ năng (W_Hard): `0.8 * 44.77% = 35.81 (Điểm trên 80)`
- Điểm Ràng buộc (W_Constraints): `0.2 * 100% = 20.0 (Điểm trên 20)`
=> **BASE_SCORE = 55.81 / 100**

*Phân tích Base Score:* Điểm 55.81 là một bước nhảy vọt so với mức điểm cũ khi W=0.1. Mặc dù anh ta trượt rất nhiều kỹ năng lôm côm trong tập Expansion của JD, nhưng lượng kiến thức khổng lồ ngoài lề (Surplus) mà anh ta mang lại (nhờ W=0.2) đã "cứu" anh ta, kéo điểm cốt lõi lên qua mốc 50% một cách cực kỳ thuyết phục.

### 5.2. Bonus Score (Chỉ cộng thêm, không trừ đi)
- Kỹ năng mềm (Soft Skills) trong CV: `[]` (Array rỗng, không extract được) => `0 * 1.5 = 0 điểm`
- Chứng chỉ (Certifications) trong CV: `[]` (Không có chứng chỉ) => `0 * 3.0 = 0 điểm`
=> **BONUS_SCORE = 0**

---

## 6. Kết luận & UI Hiển Thị
UI trên bảng điều khiển Quản lý Tuyển dụng sẽ hiện:

> **Candidate: Candidate12 (Senior Java Developer)**
> **FINAL SCORE: 55.8/100 (+ 0.0 Bonus)** 
> - **Constraints Match**: 100% (Passed 8 Years Exp & Education Requirement)
> - **Skills Match**: 44.7% (Core Fit: Java 14 Years, AWS 14 Years, Docker 11.5 Years)
> - **Missing Must-have**: apache kafka, nft, hsk

**Nhận xét quá trình tính toán Algorithm:**
1. **Rất Công Bằng:** Việc không có Soft Skill không làm ứng viên bị bốc hơi 20 điểm ra khỏi Base Score 100 (tử huyệt đã vá). Kỹ sư Code giỏi vẫn giữ được cái giá trị ranh giới Hard Skill của mình.
2. **Hệ số Logarithmic (ln) xuất sắc:** Java 14 năm (W=1.0) đút túi trọn **3.71 điểm**, gánh còng lưng gần 10 kỹ năng Expansion như JPA, Struts. Kinh nghiệm thực chiến vẫn "ăn đứt" việc nhồi nhét keyword rác của 1 thằng fresher (JPA 0 năm chỉ tính 0.3 điểm).
3. **Mẫu số Thực tế:** Dùng chính JD làm Ideal Max Score giúp điểm quy về thang 100 rất dễ nhìn, thay vì là một điểm trôi nổi ví dụ như 20.26 / Vô cực.