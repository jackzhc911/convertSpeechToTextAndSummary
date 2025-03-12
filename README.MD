# 會議紀錄整理系統雛形系統

## 特別說明
1. 這個應用有趣的地方在於，90%的程式碼都是採用VSCode內建的AI及Gemini AI產生的
2. 為了測試docker，在呼叫whisper方面以docker desktop for windows 建構服務，所使用的image是：didmar/whisper-api-server
3. 另外在本機安裝ollama提供LLM服務；之所以沒有使用docker建LLM服務是因為沒有顯卡 XD

## 第一版目標
1. 可以在Linux (Ex: Ubuntu) 上跑
2. 用python設計
3. 使用者只要上傳檔案，等系統處理完再給下載連結
4. 處理時使用whisper將語音轉成文字
5. 接著把文字丟到開源模型整理（例如: llama或TAIDE）
6. 整理完後就可以產生連結提供下載
7. 統計各科室使用量
8. whisper & llama 都要放在Docker裡面跑

## 第二版目標
1. 不同使用者可以看到各自的連結
2. 使用進度條顯示