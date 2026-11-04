# Everyday English — câu giao tiếp theo chủ đề

**Trạng thái:** 72 notes/cards trong [CSV](../source/everyday-english/notes.csv) và [schema](../source/everyday-english/notes.schema.json), chia đều 9 subdecks dưới `Everyday English`: Greetings, Daily Life, Work, Asking Questions, Expressing Opinions, Requests, Plans, Feelings, Small Talk. Mỗi subdeck có 8 cards và đã được mở trong danh sách Decks của Anki. Batch đầu 36 thẻ có gói `.apkg` thử nghiệm ở `private/imports/Everyday English-pilot.apkg`; batch thứ hai thêm trực tiếp bằng CSV/sync. **Đã import vào Anki chính sau khi người dùng xác nhận.** `English Grammar` và `DE Knowledge` không bị chỉnh sửa.

## Vì sao dùng dạng thẻ này

Người học đã biết từ đơn nhưng chưa ráp câu cần một câu ngắn để bắt đầu, rồi một khung có thể đổi từ. Mặt trước đưa **tình huống tiếng Việt**, không đưa từ tiếng Anh để chọn. Người học nói một câu thành tiếng trước khi lật. Mặt sau đưa **một cách nói tự nhiên**, **pattern**, **hai biến thể**, giải thích rất ngắn và **một tình huống mới để tự nói**. Đây là cầu nối từ nhớ câu mẫu sang tạo câu, không coi việc lặp đúng từng chữ là đích cuối.

Nghiên cứu về các cụm diễn đạt quen dùng cho thấy chúng có vai trò trong xử lý và sử dụng ngôn ngữ thứ hai; lặp nhiệm vụ có biến đổi có thể hỗ trợ độ trôi chảy, nhưng chuyển sang tình huống mới vẫn cần được kiểm tra ([tổng quan Cambridge về formulaic sequences](https://www.cambridge.org/core/journals/annual-review-of-applied-linguistics/article/abs/experimental-and-intervention-studies-on-formulaic-sequences-in-a-second-language/A2ACDF54604CFAC4443240748360C403), [nghiên cứu task repetition](https://www.cambridge.org/core/journals/studies-in-second-language-acquisition/article/abs/task-repetition-and-second-language-speech-processing/0EA95A4C7D9E90CD2AB30043F84A4635)). Lịch học và ngưỡng tiến giai đoạn dưới đây là đề xuất thực hành cần kiểm nghiệm cá nhân, không phải mức hiệu quả đã được bảo đảm.

## Cấu trúc

Một note tạo một card. Fields: `Key`, `Topic`, `SituationVI`, `Answer`, `Pattern`, `Variations`, `NoteVI`, `PracticeVI`. `Key` ổn định để sync idempotent. `Variations` có hai câu, ngăn bằng `<br>`. Mặt sau dùng `{{tts en_US:Answer}}` để Anki phát âm câu mẫu bằng giọng có trên thiết bị; không tải hay cam kết một giọng cụ thể. [Anki hướng dẫn TTS](https://docs.ankiweb.net/templates/fields.html#text-to-speech-for-individual-fields).

Cột `_deck` trong CSV lưu đường dẫn subdeck, ví dụ `Everyday English::Greetings`. Khi thêm card mới, chọn một trong các đường dẫn đó để `sync` đưa card vào đúng chủ đề. Gói `.apkg` tạo từ CSV cũng giữ cấu trúc subdeck.

Ví dụ: **Tình huống:** bạn muốn biết đồng nghiệp có rảnh chiều nay. **Câu mẫu:** “Are you free this afternoon?” **Pattern:** “Are you free + time?” **Biến thể:** “Are you free tomorrow?” / “Do you have time this evening?” **Tự nói:** hỏi đồng nghiệp có rảnh sáng mai không. Câu trả lời khác vẫn đúng nếu phù hợp tình huống, tự nhiên và đúng ngữ pháp.

Chấm **Again** nếu không thể nói trọn ý hoặc chỉ nhận ra đáp án sau khi lật; **Hard** nếu cần gợi ý hoặc dừng lâu; **Good** nếu nói được câu tự nhiên và thử thay ít nhất một thành phần; **Easy** chỉ khi tình huống mới cũng nói được dễ dàng. Không bắt buộc trùng chữ với `Answer`.

## Lộ trình và buổi học gợi ý

| Giai đoạn | Bài tập | Dấu hiệu chuyển tiếp |
|---|---|---|
| 1. Câu mẫu | Nói câu theo tình huống trước khi lật; nghe TTS sau đó nói lại | Đa số câu mẫu nói được không cần đọc mặt sau |
| 2. Thay đổi | Thay người, vật, thời gian, phủ định hoặc đổi thành câu hỏi; dùng hai biến thể làm mẫu | Tự đổi được ít nhất một thành phần mà câu vẫn đúng |
| 3. Tự tạo câu | Dùng `PracticeVI` hoặc tình huống mới tương tự, không nhìn câu mẫu | Truyền đạt đúng ý bằng một câu mới, không cần giống đáp án |
| 4. Hỏi đáp ngắn | AI hoặc người học cùng đưa một câu hỏi/đáp ngắn theo pattern; thêm một câu hỏi tiếp | Trả lời được khi lượt hỏi đổi nhẹ |
| 5. Hội thoại | Hội thoại AI ngắn 3–5 phút, chọn một tình huống quen; nhận sửa 1–2 lỗi đáng chú ý | Có thể duy trì vài lượt trao đổi mà không chỉ đọc thuộc câu mẫu |

**Buổi học ngắn 20 phút nếu cần:** 6–8 phút review `English Grammar`, 7–8 phút review `Everyday English`, 4–5 phút nói biến thể/tình huống mới. Khi có nhiều thời gian, có thể học nhiều hơn theo sức mình và dành thêm thời gian nói câu mới từ các pattern. `DE Knowledge` giữ lịch riêng, không trộn vào buổi tiếng Anh này.

Sau 2 tuần, thử 10 tình huống chưa có nguyên văn trong CSV: đếm số câu nói được trong khoảng 8 giây, số câu đúng ý và số câu tự thay được thành phần. Chỉ thêm 5–10 mẫu mới khi các câu hiện tại chuyển được sang tình huống mới. Mục tiêu dài hạn 100–200 pattern hữu ích là giới hạn chất lượng, không phải chỉ tiêu phải đạt bằng số thẻ.

## Kiểm chứng kỹ thuật

`validate` chấp nhận đủ 72 dòng, 72 `Key` và 72 `Answer` khác nhau; mỗi câu mẫu tối đa 12 từ và mỗi card có đúng hai biến thể. Batch thứ hai cho kết quả `diff` **36 ADD, 36 SKIP, 0 UPDATE/CONFLICT** trước sync. Backup ngay trước batch thứ hai ở `private/backups/2026-11-04-before-everyday-batch-2/`. Sau sync, 72 cards hiện trong Anki, chia đều 9 chủ đề.

**Preset:** `Everyday English` và cả 9 subdeck dùng preset riêng `Everyday English - No Daily Cap`: giới hạn thẻ mới và thẻ ôn đều là 9.999/ngày, tức gần như không giới hạn trong thực tế. Đây là trần hiển thị của Anki, không phải mục tiêu cần học hết. Preset của `English Grammar` và `DE Knowledge` giữ nguyên.
