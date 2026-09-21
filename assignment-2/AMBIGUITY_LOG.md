# Assignment 2 - 模糊點清單 (Ambiguity Log)

> 用途:記錄 PDF 沒有明確規定、需要自己做假設的地方。
> 每一項決定之後都要搬進 README 的 Assumptions 區塊,並附上理由。
> 這份清單本身**不是** README,只是工作用的追蹤表。

狀態欄位說明:`[ ]` 尚未決定 / `[x]` 已決定(請補上「決定」欄)

---

## 1. Plant 相關

### 1.1 Trees and Shrubs 跟 Perennials 要不要拆成兩個 derived class?
PDF:「Trees and shrubs, and perennials, are priced per plant.」— 兩者計價方式完全一樣。
但 Brent 原文開頭又明確把它們列為兩種不同類別(跟 Assignment 1 的 category 一致):
「trees and shrubs, perennials, pot plants, and vegetable seedlings」。
- **模糊點**:PDF 要求「derived classes to capture the different types of plants」,但兩個類別行為完全相同時,是否仍要拆成兩個 class(TreesAndShrubs、Perennial),還是可以合併成一個(因為沒有行為差異)?
- **風險**:如果只做出 3 個 derived class(把 tree/shrub 和 perennial 合併),可能被判定「沒有反映 Brent 講的四種」,扣 Inheritance & Abstraction 或 Core Business Logic 分數。
- **建議傾向**:PDF 明講「四種」,且 rubric 強調 inheritance 要「responsibilities clearly divided」,拆成 4 個 class 比較保險,即使兩個的邏輯目前一樣(未來可能長出差異)。
- **決定**:[ ]

### 1.2 Pot Plant 的「size」怎麼建模?
PDF:「Pot plants are priced by pot size, small, medium, or large, not by the plant itself.」
「For pot plants, that means ten or more of the same plant in the same pot size, not a mix of sizes.」
- **模糊點**:這是全份 PDF 裡最關鍵、最容易一個人一種做法的地方。至少有兩種合理設計:
  1. **一個 Plant 物件 = 一種植物 + 一個尺寸**(例如「Fern - Large」是獨立的 Plant record,有自己的 ID、自己的價格、自己的庫存)。「兩份不同尺寸的同一種盆栽」= 兩筆不同的 plant record。
  2. **一個 Plant 物件 = 一種植物**,內部用 dict 存三種尺寸各自的價格跟庫存(`{small: (price, stock), medium: (...), large: (...)}`),下訂單時要多指定一個 size 參數。
- **為什麼重要**:這會連動到 OrderItem 要不要多存一個 `size` 欄位、庫存扣減邏輯、「同一 plant 同一 size 湊滿10件打折」的判斷邏輯全部不一樣。選錯設計不會被判「錯」,但如果沒在 README 講清楚為什麼這樣選,會被當成「沒處理好這個 edge case」。
- **決定**:[ ]

### 1.3 Vegetable seedling「每 punnet 幾株」要不要建模成資料?
PDF:「usually six to a punnet, though it depends on the type of seedling」。
- **模糊點**:這句話讀起來像是在解釋「為什麼賣的單位是 punnet」,但沒有明講系統需不需要記錄「這個 seedling 品種一 punnet 裝幾株」這個數字。
- **風險低,但要決定**:如果你的 Plant/VegetableSeedling class 完全不存這個數字,合不合理?可以合理,因為訂購、計價、扣庫存全部都是用 punnet 為單位,「每 punnet 幾株」對系統邏輯沒有影響,只是背景資訊。但如果你想加分讀者感,可以加一個屬性(不影響任何計算)。
- **決定**:[ ]

### 1.4 「Whatever unit we sell something in is the same unit we count stock in」如何跟 1.2 連動?
- 如果 1.2 選「方案 1(一個尺寸一筆 record)」,庫存自然就是用該尺寸的「盆數」為單位,沒有額外模糊。
- 如果選「方案 2(一個植物存三個尺寸)」,要確保三個尺寸各自有獨立庫存數字,不能只有一個庫存欄位。
- **決定**:跟著 1.2 走,這裡不用另外決定,只是提醒不要漏掉。

---

## 2. Order / OrderItem 相關

### 2.1 Order 要不要保留自己的 `total` 欄位?
PDF:「each item has its own plant, quantity, and the cost for that item's quantity, not just one lump total for the whole order」— 這句話否定的是「只有一個總數、看不到每項明細」,不代表 Order 完全不能有一個總計欄位。
- **模糊點**:Order 的總金額(給顧客折扣前後)要不要存成屬性,還是每次用 method 即時算(`get_total()` 加總 items 再套用 customer 折扣)?
- **風險**:兩種都合理,但如果存成屬性,要注意「新增/取消 item」或「customer 資訊變動」時有沒有跟著同步,否則會有資料不一致的 bug(這是 rubric「Edge Cases」跟「Core Business Logic」會抓的)。
- **建議傾向**:用 method 即時計算比較不會有同步問題,但如果堅持存屬性也可以,只要在文件講清楚什麼時候會重新計算。
- **決定**:[ ]

### 2.2 一張訂單裡,同一個 plant 可以出現在兩個不同 item 嗎?
PDF:「If someone wants four griselinias ... two of the large pot ferns, and a punnet of tomato seedlings in one go, that all sits under the one order ... with each different plant as its own item」— 暗示「一個 plant 對應一個 item」,但沒有明講「重複下同一個 plant 兩次會怎樣」(該擋掉、還是合併成一個 item、還是允許兩個 item 各自累計)。
- **決定**:[ ]

### 2.3 Order 上的同商品 10% 折扣門檻,是看單一 item 的 quantity,還是同一 plant 在整張訂單裡的總量?
- 承接 2.2:如果允許同一 plant 拆成兩個 item(例如分兩批下單同一批貨),10% 折扣門檻(≥10)是分別看每個 item 的 quantity,還是把同一 plant(同 size)的所有 item 加總後再判斷?
- PDF 文字「The existing 10% discount for ordering ten or more of the same plant still applies per item」比較偏向「per item」判斷,但如果 2.2 決定禁止重複 plant,這條就不會有歧義了。
- **建議**:如果 2.2 決定「同一 plant 只能出現一次」,這條自動不模糊。
- **決定**:[ ]

---

## 3. Customer 相關

### 3.1 Staff/Student 的 $100 上限,檢查時機是「下單前餘額」還是「下單後餘額」?
PDF:「If a staff or student's amount owing goes above $100, we should not let them order more until it is paid down.」
- **模糊點 A(檢查時機)**:是檢查「目前餘額(下單前)是否已經 > $100」,還是「這筆新訂單加上去後會不會讓餘額 > $100」?
  - 讀法 1(pre-check):只要目前餘額還沒超過 $100,這筆訂單無論多大都放行,即使下單後會遠超過 $100。
  - 讀法 2(prospective/post-check):新訂單金額會讓餘額超過 $100 就直接擋掉。
- 這跟 Assignment 1「stock 不能扣到負的」那條規則很像 — 都是「事前擋 vs 事後補救」的選擇,而 PDF 沒有明講。
- **風險**:這是 Core Business Logic 的核心規則之一(佔分不小),兩種讀法都「合理」,但選錯又沒解釋清楚,可能被判「business rule 沒有一致套用」。
- **決定**:[ ]

### 3.2 Community customer 的「pending order」何時解除?
PDF:「Community customers can only have one order pending at a time, and they need to pay it off in full before it can be collected, so they cannot place another order until that one is settled and picked up.」
- **模糊點**:句子裡出現「settled(付清)」跟「picked up(取貨/collected)」兩個條件,用「and」連接。這代表:
  - 讀法 1:community customer 要「同時滿足」付清 **且** 完成 collect,才能下新訂單(也就是「pending」的解除點是 collect,不是付清)。
  - 讀法 2:只要付清(balance=0)就算「settled」,不下新單的限制就解除,不需要等到真正 collect。
- 這條文字本身有點自相矛盾(「pay off in full before it can be collected」暗示付清是 collect 的前提,「until settled and picked up」又暗示兩者都要發生才能下新單),需要你自己選一個讀法並解釋。
- **決定**:[ ]

### 3.3 Community customer 有沒有 $100 類的金額上限?
PDF 只對 staff/student 講了 $100 上限,對 community 完全沒提到金額上限,只提「一次一張 pending 訂單」的限制。
- **模糊點**:要不要假設 community 完全沒有金額上限(只受「一張訂單」限制),還是也套用某個保守上限?
- **建議傾向**:PDF 沒提就不要加規則,明確假設「community 沒有 $100 類上限,只受單一 pending 訂單限制」,並在 README 寫清楚「PDF 沒有要求,因此不額外套用」。
- **決定**:[ ]

---

## 4. Payment 相關

### 4.1 信用卡 1.5% surcharge,算不算進「還了多少錢」?
PDF:「when paying there is a 1.5% surcharge added to the amount the customer pays」
- **模糊點**:假設訂單還欠 $100,顧客想用信用卡「付清 $100」:
  - 讀法 1:顧客實際要付 $101.50(給銀行/手續費),但記在 Payment 上、算進「已還多少錢」的金額還是 $100(surcharge 只是額外成本,不算在還款裡)。
  - 讀法 2:Payment 記錄的金額直接是 $101.50(含 surcharge),等於顧客多還了 $1.50,這樣會跟「no single payment can be more than what is still owed」互相衝突(因為 $101.50 > $100 owed),除非 surcharge 本來就不算在這條限制內。
- **風險**:這條文字上真的兩種讀法都說得通,PDF 沒有交代「先判斷 owed 上限、還是先加完 surcharge 再判斷」的順序。這是最像 Assignment 1「collected 能不能改回 pending」的那種——完全開放給你自己假設、但一定要交代理由的題目。
- **建議傾向**:讀法 1 比較合理(surcharge 是給銀行的手續費,不是還給店家的錢),這樣也不會跟「不能超過欠款」的規則衝突。
- **決定**:[ ]

### 4.2 Payment 要不要能對「已結清 / 已取消」的訂單付款?
PDF:「we accept a payment from any customer at any time」聽起來很寬鬆,但「no single payment can be more than what is still owed on that order」自然會擋掉「還款超過剩餘欠款」的情況(欠款 0 時,任何正數付款都會超過)。
- **模糊點**:是要明確擋下「這張訂單已經沒有欠款/已取消,不能再付款」並丟一個自訂例外,還是單純靠「金額不可超過欠款」這條規則自然堵住?
- **建議傾向**:兩者其實是同一件事的兩種實作角度,但明確做一個獨立的檢查/例外(例如 `OrderAlreadySettledException`)會讓 Exception Handling 那 10 分更好拿滿,而不是靠邊界情況自然擋住。
- **決定**:[ ]

### 4.3 Payment 要不要同時存 customer 參考 跟 order 參考?(對應 Assignment-1 舊傷)
PDF 明講 Payment 要記錄「which customer it was for, which order it was paying toward」— 兩個都要存,即使 order 本身就能查到 customer(等於有點重複)。
- **這正是 Assignment 1 沒講清楚、被當模糊地帶扣分的同一類問題(存 ID 還是存物件參考)。**
- **模糊點**:customer/order 這兩個欄位存的是 **ID(字串/數字)** 還是 **物件參考(直接存 Customer/Order 物件)**?
- **風險**:這次不能再讓它「自然發生」,因為你已經知道這是教師會盯的點。Assignment 2 因為要做 serialisation(存檔),用物件參考互相指來指去在 pickle 時通常可行,但如果之後想換成 JSON,物件參考會很難序列化,通常要轉成 ID。**這是這次要主動決定並在 README 講清楚的地方,不要重演 Assignment 1 那種「沒意識到這是決定點」的狀況。**
- **決定**:[ ](建議在動手前就想清楚,因為這個決定會牽動 Order 內部怎麼存 OrderItem、Order 怎麼存 Customer 等一整組類似問題)

---

## 5. NurserySystem 相關

### 5.1 「see our different types of customers separately」要怎麼實作?
PDF 只講需求(能分開看三種 customer),沒講介面長什麼樣。
- **模糊點**:是要三個獨立的 method(`get_staff_customers()`, `get_student_customers()`, `get_community_customers()`),還是一個共用的 `get_customers_by_type(type)`?兩者都合理,只是要挑一個並保持一致風格(跟 Assignment 1 現有的 plant/customer/order 查詢方法命名風格一致)。
- **決定**:[ ]

### 5.2 Payment 查詢方法要提供哪些?
PDF 明確列了 3 種查詢需求:
1. 某個顧客的付款歷史
2. 某張訂單收到的所有付款
3. 全部顧客的付款總表
- 這條不算模糊(PDF 講得很清楚),但要注意**三個都要做**,不要漏掉其中一個(這正是 Assignment 1「find by id method for all collections」被誤判缺少的重演風險 — 這次要主動列出來,confirm 三個都有做,driver program 也要三個都展示到)。
- **決定**:[x] 三個查詢都要做,無需額外假設,列在這裡只是提醒別漏。

---

## 6. Persistence(存檔/讀檔)相關

### 6.1 用什麼格式存檔?
PDF 只講「save data to a file... load that data back in」,完全沒指定格式。
- **模糊點**:pickle / JSON / CSV 都沒被排除。
  - pickle:最簡單,能直接存物件(含 class 繼承關係),但如果用了物件參考(見 4.3),pickle 通常能正確處理循環參考。
  - JSON:需要自己寫序列化/反序列化邏輯(把物件轉成 dict、讀回來要判斷是哪個 subclass 再重建),比較能展示「你有處理多型的存讀」,但工作量大很多。
- **風險**:rubric Data Persistence 那 7 分裡,「Excellent」等級寫的是「all objects correctly reconstructed」,隱含著批改者會實際跑存檔+重開程式,看 4 種 plant/3 種 customer/2 種 payment 的 subclass 有沒有正確變回原本的類別(而不是變成 dict 或變成基底類別)。這是選 pickle 或 JSON 都要注意的重點,不是選哪個的問題,而是要小心測試。
- **決定**:[ ]

### 6.2 什麼時候觸發存檔?
PDF:「save data to a file when the program exits」— 但 Python 的「程式離開」有很多種:正常執行完畢、拋出未捕捉的例外、使用者按 Ctrl+C。
- **模糊點**:要不要用 `atexit` register,還是單純在 driver program 最後手動呼叫 `system.save()`?如果 driver program 中途丟出未捕捉的例外導致提前結束,存檔會不會跟著沒執行到?
- **建議傾向**:PDF 說的應該是「正常結束時存檔」這種程度,手動在 driver 最後呼叫 `save()` 應該就足夠,不用做到處理當機情境,但如果想加分,`atexit.register()` 是更貼近「system 自動處理」精神的做法(PDF 用詞是「central system class to automatically save」,這個「automatically」字眼比較支持 atexit 或在 __del__ 之類的做法,而不是靠 driver program 手動呼叫)。
- **決定**:[ ]

---

## 7. 跟 Assignment 1 相同踩雷模式的風險提醒(不是新模糊點,是舊傷會不會重演)

1. **驗證邏輯放錯 class**(Assignment 1 教師扣分主因之一,已存入長期記憶)。Assignment 2 新增了更多跨 class 的規則(customer 下單上限、pot plant size 折扣門檻、payment 金額上限),職責分工只會更複雜。**每加一條規則前,先問「這個檢查該由 Customer 自己的方法做,還是該由 Order/NurserySystem 做」,並保持全系統一致的原則**(例如:所有人可以自己驗證問題都應該放在 Customer/Plant 自己身上,跨物件的規則放在 NurserySystem 或 Order)。
2. **Driver program 沒有展示到某個規則就等於沒做**(Assignment 1 教師誤判「沒有展示 individual stock check」)。這次規則變多、例外也要求至少 4 個,driver program 需要覆蓋的情境清單會比 Assignment 1 長很多,建議照本清單(第 8 節)一條條打勾,不要漏。
3. **README 假設是否寫清楚理由**:本清單裡標「決定:[ ]」的每一項,做完決定後都要搬到 README,並附上「為什麼選這個」的一句話理由(不是只寫「我假設 X」,要寫「我假設 X,因為 PDF 只講了 Y,沒有講 Z,所以...」)。

---

## 8. Driver Program 需要展示到的情境清單(先列,之後動手時逐條核對)

- [ ] 4 種 plant subclass 各自建立、各自的 pricing 邏輯
- [ ] 3 種 customer subclass 各自建立
- [ ] 一張訂單包含多個不同 plant type 的 item(照 PDF 範例:griselinia + pot fern + tomato seedling)
- [ ] 同一 item 內數量 ≥10 觸發 per-item 10% 折扣(含 pot plant 同 size 才算、seedling 同 punnet 類型才算)
- [ ] Staff/Student/Community 三種 customer 折扣(1%/5%/0%)套用在訂單總額上
- [ ] Community customer 已有一張 pending 訂單時,擋下第二張訂單(對應例外)
- [ ] Staff/Student 餘額超過 $100 時,擋下新訂單(對應例外)
- [ ] Order 取消:只能在 pending 且尚未付款時取消,取消後 stock 跟 balance 都要復原
- [ ] 嘗試取消已 collect 或已付款的訂單 → 例外
- [ ] 多筆分期付款(partial payments)累加還清同一張訂單
- [ ] 單筆付款金額超過該訂單剩餘欠款 → 例外
- [ ] 信用卡付款 surcharge 計算展示
- [ ] 借記卡(debit card)付款展示
- [ ] 三種 payment 查詢(某顧客付款歷史 / 某訂單所有付款 / 全部付款列表)都展示到
- [ ] 三種 customer 分開列表展示
- [ ] 存檔後重新啟動程式(或至少呼叫 save/load),確認資料(含各 subclass)正確還原
- [ ] 承接 Assignment 1 舊有情境仍要保留展示:個別 plant 庫存檢查、加入重複 ID 的 plant/customer 被擋下、加入 0 數量或負價格被擋下

