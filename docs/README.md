# Lộ trình đọc trước khi ôn Anki

Các bài trong [lessons/](lessons/) giải thích cách **tự ghép câu từ ý muốn nói**. Bài 01–15 bám đúng 15 `field:Unit` của [English Grammar](../source/english-grammar/notes.csv) (**581 cards**); bài 16–24 bám đúng 9 `field:Topic` và subdeck của [Everyday English](../source/everyday-english/notes.csv) (**72 cards**). Bộ [Speaking Pilot](../source/pilot/notes.csv) có 17 thẻ thử nghiệm, hiện không nằm trong collection đang học; các bài ngữ pháp liên quan vẫn chỉ rõ khóa pilot để dùng khi cần. Không có bài nào tạo hoặc sửa thẻ Anki.

[Báo cáo rà soát và bổ sung ngữ pháp](GRAMMAR_AUDIT.md) ghi rõ nội dung được mở rộng trong từng bài, điểm còn mở và nguồn đối chiếu.

**Bảng tra cứu:** [Động từ bất quy tắc V1–V2–V3](reference/irregular-verbs.md) chia theo mức độ, có ví dụ V2/V3 và cách ghép câu. Dùng cùng bài [02 Past Simple](lessons/02-past-simple.md), [04 Present Perfect](lessons/04-present-perfect.md) và [13 Passive Voice](lessons/13-passive.md). Bảng ngắn về [danh từ/số nhiều](lessons/07-nouns-quantifiers.md), [verb patterns](lessons/09-verb-patterns.md), [giới từ](lessons/12-prepositions.md) và [so sánh](lessons/11-comparison.md) nằm ngay trong bài tương ứng.

## Cách học một bài

1. **Read Lesson:** đọc mục tiêu và ví dụ; chọn một tình huống mình thực sự gặp.
2. **Understand Grammar:** giải thích bằng lời của mình vì sao câu dùng cấu trúc đó, không chỉ đọc công thức.
3. **Practice Building Sentences:** làm bài tập trước khi xem đáp án; thay người, thời gian hoặc ý định để tạo thêm 2 câu.
4. **Review with Anki:** mở deck/subdeck ghi ở cuối bài; nói trọn câu trước khi lật thẻ.
5. **Speak Aloud:** kể một việc thật của mình bằng 2–3 câu, không nhìn mẫu.
6. **Apply in AI Conversation:** khi đã nói được câu ngắn, nhờ AI hỏi đáp 3–5 lượt trong chính tình huống đó và chỉ sửa 1–2 lỗi quan trọng.

Một câu khác đáp án mẫu vẫn đúng nếu tự nhiên và truyền đạt đúng ý. Nếu chưa nói được, quay lại phần **Sentence Building**; không cần mở thêm thẻ mới chỉ vì còn thời gian.

## Lộ trình đọc gợi ý

Các số bài giữ thứ tự nhóm card gốc; bạn có thể đọc theo thứ tự học dưới đây. Bài giao tiếp có thể bắt đầu sớm, song song với phần ngữ pháp nền tảng.

| Chặng | Đọc theo thứ tự | Mục tiêu |
|---|---|---|
| Dựng câu nền | [01](lessons/01-present-simple-continuous.md) → [08](lessons/08-pronouns.md) → [07](lessons/07-nouns-quantifiers.md) → [06](lessons/06-articles.md) → [15](lessons/15-sentence-patterns.md) | Có chủ ngữ, động từ, danh từ và câu hỏi cơ bản |
| Nói việc thật | [02](lessons/02-past-simple.md) → [03](lessons/03-future.md) → [04](lessons/04-present-perfect.md) → [12](lessons/12-prepositions.md) | Kể chuyện, nói kế hoạch và mốc thời gian |
| Nói tự nhiên | [05](lessons/05-modal-verbs.md) → [10](lessons/10-adjectives-adverbs.md) → [11](lessons/11-comparison.md) → [09](lessons/09-verb-patterns.md) | Nhờ giúp, mô tả, so sánh và nối hành động |
| Mở rộng | [13](lessons/13-passive.md) → [14](lessons/14-conditionals.md) | Đổi trọng tâm và nói điều kiện/giả định |

**Thực hành giao tiếp:** Sau bài 01 và 15, đọc [16 Greetings](lessons/16-greetings.md), [18 Asking Questions](lessons/18-asking-questions.md), [17 Daily Life](lessons/17-daily-life.md). Tiếp đến đọc [20 Plans](lessons/20-plans.md), [21 Requests](lessons/21-requests.md), [22 Feelings](lessons/22-feelings.md), [19 Expressing Opinions](lessons/19-expressing-opinions.md), [23 Work](lessons/23-work.md), rồi [24 Small Talk](lessons/24-small-talk.md). Đừng đợi học hết 15 bài ngữ pháp mới bắt đầu câu giao tiếp.

## Mục lục và mapping card

### English Grammar

Lọc cột `field:Unit` hoặc prefix của `field:Key` trong CSV. Một bài ứng với **toàn bộ** card của đơn vị đó, không chỉ vài ví dụ trích trong bài.

| Bài học | Unit / prefix khóa | Cards |
|---|---|---:|
| [01 Thói quen và việc đang diễn ra](lessons/01-present-simple-continuous.md) | Present Simple & Present Continuous / `present_simple_continuous.` | 73 |
| [02 Kể việc đã xảy ra](lessons/02-past-simple.md) | Past Simple / `past_simple.` | 41 |
| [03 Dự định và lịch hẹn](lessons/03-future.md) | Future: will · be going to · Present Continuous / `future.` | 32 |
| [04 Kinh nghiệm và kết quả](lessons/04-present-perfect.md) | Present Perfect vs Past Simple / `present_perfect.` | 42 |
| [05 Modal verbs](lessons/05-modal-verbs.md) | Modal Verbs / `modals.` | 41 |
| [06 Mạo từ](lessons/06-articles.md) | Articles: a / an / the / zero / `articles.` | 32 |
| [07 Danh từ và lượng từ](lessons/07-nouns-quantifiers.md) | Nouns, Quantifiers & Determiners / `nouns_quantifiers.` | 42 |
| [08 Đại từ](lessons/08-pronouns.md) | Pronouns / `pronouns.` | 27 |
| [09 V-ing hay to V](lessons/09-verb-patterns.md) | Gerund & Infinitive / `verb_patterns.` | 41 |
| [10 Tính từ và trạng từ](lessons/10-adjectives-adverbs.md) | Adjectives & Adverbs / `adjectives_adverbs.` | 36 |
| [11 So sánh](lessons/11-comparison.md) | Comparison / `comparison.` | 33 |
| [12 Giới từ](lessons/12-prepositions.md) | Prepositions / `prepositions.` | 37 |
| [13 Bị động](lessons/13-passive.md) | Passive Voice / `passive.` | 30 |
| [14 Điều kiện](lessons/14-conditionals.md) | Conditionals (Type 0 · 1 · 2 · 3) / `conditionals.` | 31 |
| [15 There, It, câu hỏi, cảm thán](lessons/15-sentence-patterns.md) | Sentence Patterns: There · It · Questions · Exclamations / `sentence_patterns.` | 43 |

### Everyday English

Mở subdeck dưới `Everyday English` hoặc lọc `field:Topic` / prefix `field:Key` trong CSV.

| Bài học | Subdeck / prefix khóa | Cards |
|---|---|---:|
| [16 Greetings](lessons/16-greetings.md) | `Everyday English::Greetings` / `everyday.greetings.` | 8 |
| [17 Daily Life](lessons/17-daily-life.md) | `Everyday English::Daily Life` / `everyday.daily-life.` | 8 |
| [18 Asking Questions](lessons/18-asking-questions.md) | `Everyday English::Asking Questions` / `everyday.asking-questions.` | 8 |
| [19 Expressing Opinions](lessons/19-expressing-opinions.md) | `Everyday English::Expressing Opinions` / `everyday.expressing-opinions.` | 8 |
| [20 Plans](lessons/20-plans.md) | `Everyday English::Plans` / `everyday.plans.` | 8 |
| [21 Requests](lessons/21-requests.md) | `Everyday English::Requests` / `everyday.requests.` | 8 |
| [22 Feelings](lessons/22-feelings.md) | `Everyday English::Feelings` / `everyday.feelings.` | 8 |
| [23 Work](lessons/23-work.md) | `Everyday English::Work` / `everyday.work.` | 8 |
| [24 Small Talk](lessons/24-small-talk.md) | `Everyday English::Small Talk` / `everyday.small-talk.` | 8 |

## Khi thêm card hoặc bài học

CSV vẫn là source of truth cho card. Bài `.md` chỉ giải thích và trỏ tới `field:Unit`, `field:Topic`, `field:Key`; không cần thêm field `lesson_id` vào note type. Nếu một chủ đề mới được thêm vào CSV, cập nhật mục lục và phần **Anki Review**. Với card mới trong chủ đề cũ, prefix khóa vẫn dùng được; cập nhật số lượng ghi ở mục lục khi cần.
