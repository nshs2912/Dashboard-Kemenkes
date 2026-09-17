# Dashboard-Kemenkes

Dashboard presentasi nasional untuk mengonsumsi intelligence dari SI-HIS.

## Arsitektur
Multi-source data → SI-HIS Data Hub → Standardisasi/FHIR → SI-HIS Intelligence
→ `/api/intelligence/kemenkes` → Dashboard-Kemenkes.

## Mode
- SI-HIS Demo: memakai `data/demo/intelligence_kemenkes.json`
- SI-HIS API: memakai `SIHIS_API_BASE_URL`

Dashboard tidak menggantikan engine epidemiologi/ML di repository SI-HIS-Intelligence.
