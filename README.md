# Dashboard-Kemenkes

Presentation/client layer untuk **SI-HIS — Kemenkes National Health Intelligence**.

```text
Multi Data Sources
       ↓
SI-HIS Data Hub
       ↓
Data Quality / Standardization / FHIR
       ↓
SI-HIS Intelligence
       ↓
/api/intelligence/kemenkes
       ↓
Dashboard-Kemenkes
```

Dashboard ini tidak menggantikan engine analitik SI-HIS. Mode `demo` memakai intelligence sintetis untuk validasi UI. Mode `api` membaca endpoint:

`GET /api/intelligence/kemenkes`

Konfigurasi API:
`SIHIS_API_BASE_URL=https://alamat-sihis`

Jalankan:
```bash
pip install -r requirements.txt
streamlit run app.py
```

Catatan: data demo bukan data kesehatan nyata. Sinyal EWS/KLB/spasial/prediksi membutuhkan validasi, definisi operasional, kualitas data, dan governance sebelum penggunaan operasional.
