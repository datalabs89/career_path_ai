# Ringkasan Aplikasi: AI Career Path Planner

Aplikasi ini bertujuan untuk membantu pengguna merencanakan jalur karir mereka melalui serangkaian pertanyaan interaktif yang dianalisis oleh AI untuk menghasilkan rencana yang dipersonalisasi.

---

### 1. Fitur Utama

*   **Kuesioner Adaptif:** Aplikasi memulai dengan pertanyaan umum, lalu AI akan membuat pertanyaan lanjutan yang lebih spesifik berdasarkan jawaban pengguna.
*   **Generasi Rencana Karir oleh AI:** Inti dari aplikasi, di mana AI menganalisis semua jawaban untuk membuat jalur karir yang disarankan.
*   **Visualisasi Flowchart:** Rencana karir disajikan dalam bentuk flowchart yang mudah dipahami (misalnya menggunakan Mermaid.js).
*   **Penjelasan Rinci (Markdown):** Setiap langkah dalam flowchart akan disertai dengan penjelasan mendalam dalam format Markdown, mencakup skill yang dibutuhkan, estimasi waktu, dan sumber daya yang relevan.
*   **Riwayat Sesi:** Pengguna dapat melihat kembali hasil perencanaan karir yang pernah dibuat sebelumnya.

---

### 2. Alur Aplikasi
1.  **Mulai Sesi:** Pengguna memulai sesi perencanaan baru.
2.  **Screening Awal:** Aplikasi menampilkan serangkaian pertanyaan umum (misalnya: minat, keahlian saat ini, latar belakang pendidikan, preferensi industri).
3.  **Analisis & Pertanyaan Lanjutan:** Jawaban awal dikirim ke AI. AI menganalisisnya dan menghasilkan pertanyaan-pertanyaan yang lebih mendalam dan relevan dengan konteks pengguna.
4.  **Screening Detail:** Pengguna menjawab pertanyaan-pertanyaan lanjutan dari AI.
5.  **Pembuatan Rencana:** Seluruh data percakapan (pertanyaan dan jawaban) dikirim kembali ke AI untuk diproses menjadi sebuah rencana karir yang utuh.
6.  **Tampilan Hasil:** Aplikasi menampilkan hasil yang digenerate oleh AI, yang terdiri dari:
    *   Sebuah flowchart visual.
    *   Teks penjelasan dalam format Markdown.
7.  **Simpan Hasil:** Hasil sesi disimpan ke dalam database untuk bisa diakses kembali oleh pengguna.

---

### 3. Skema Database (PostgreSQL)

Berikut adalah skema database sederhana untuk mendukung aplikasi ini.

```sql
-- Tabel untuk menyimpan data pengguna (opsional jika tidak ada login)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Tabel untuk setiap sesi perencanaan karir
CREATE TABLE career_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id), -- Bisa NULL jika pengguna tidak login
    created_at TIMESTAMPTZ DEFAULT now(),
    status VARCHAR(50) NOT NULL -- e.g., 'started', 'completed', 'failed'
);

-- Tabel untuk menyimpan riwayat interaksi (Q&A) dalam satu sesi
CREATE TABLE session_interactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES career_sessions(id),
    prompt TEXT NOT NULL, -- Pertanyaan dari AI
    response TEXT, -- Jawaban dari user
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Tabel untuk menyimpan hasil akhir dari sebuah sesi
CREATE TABLE career_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL UNIQUE REFERENCES career_sessions(id),
    flowchart_data TEXT NOT NULL, -- Data untuk render flowchart (misal: sintaks Mermaid)
    markdown_explanation TEXT NOT NULL, -- Penjelasan dalam format markdown
    created_at TIMESTAMPTZ DEFAULT now()