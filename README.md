# conflict-detection-remote-sensing-nlp

A Streamlit-ready pipeline that fuses open-source conflict reports with satellite-based land change detections (e.g., NDVI drops). Designed to verify violence-linked environmental change and support humanitarian monitoring in real-world settings like Myanmar.

---

## 🛰 Overview

This project:
- Scrapes or accepts geolocated conflict reports
- Detects NDVI-based vegetation change using Sentinel-2 imagery
- Matches events to land change via spatial + temporal rules
- Outputs a GeoDataFrame for inspection or downstream analysis

---

## 🚀 How to Run the Fusion Pipeline

```bash
python src/satellite/run_fusion.py \
  --text_path data/sample_inputs/gdf_text_sample.gpkg \
  --sat_path data/sample_inputs/ndvi_sample.geojson \
  --output_path outputs/output_fused_matches.gpkg \
  --delta_days 14

**Arguments**:
- `--text_path`: path to conflict reports file (GeoPackage or GeoJSON)
- `--sat_path`: path to NDVI change detections (GeoJSON)
- `--output_path`: where to save matched output (GeoPackage or GeoJSON)
- `--delta_days`: (optional) max days between conflict and satellite change

## 📁 Example Inputs

Included in [`data/sample_inputs/`](data/sample_inputs/) are:
- `gdf_text_sample.gpkg`: dummy conflict reports from northern Shan State, Myanmar
- `ndvi_sample.geojson`: simulated vegetation loss zones

## 📌 Why This Matters

Verifying violent events with multi-source data fusion supports:
- Detecting burned villages and scorched-earth patterns
- Identifying underreported or delayed conflict activity
- Informing timely humanitarian response and accountability work
