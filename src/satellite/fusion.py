import geopandas as gpd
import ee
import pandas as pd
from datetime import datetime, timedelta
import shapely

# Load data
text_gdf = gpd.read_file(
    "/Users/timklustner/Downloads/Projects/Python/Sat_NLP/data/raw/gdf_text.gpkg"
)
sat_gdf = gpd.read_file(
    "/Users/timklustner/Downloads/Projects/Python/Sat_NLP/outputs/rw_007_ndvi_drop.geojson"
)

# Prep satellite data
sat_gdf["change_date"] = pd.to_datetime(sat_gdf["change_date"])
sat_gdf = sat_gdf.rename(columns={"mean": "change_mag"})

# Reproject
text_gdf = text_gdf.to_crs(epsg=4326)
sat_gdf = sat_gdf.to_crs(epsg=4326)
text_gdf["text_geometry"] = text_gdf.geometry

# Spatial join
spatial_matches = gpd.sjoin(sat_gdf, text_gdf, predicate="intersects", how="left")


# Temporal filter
def filter_temporal_matches(spatial_matches, delta_days=14):
    spatial_matches = spatial_matches.copy()
    spatial_matches["date_diff"] = (
        spatial_matches["change_date"] - spatial_matches["report_date"]
    ).abs()
    return spatial_matches[spatial_matches["date_diff"] <= timedelta(days=delta_days)]


valid_matches = filter_temporal_matches(spatial_matches, delta_days=200)


# Fusion classification
def classify_fusion(text_gdf, sat_gdf, valid_matches):
    matched = valid_matches.copy()
    matched["fusion_type"] = "text-confirmed"
    matched["norm_mag"] = matched["change_mag"].abs()

    # Compute match_score components
    matched["date_diff_days"] = matched["date_diff"].dt.days

    # 1. Temporal score (closer = better)
    max_days = matched["date_diff_days"].max()
    matched["time_score"] = (
        0 if max_days == 0 else 1 - (matched["date_diff_days"] / max_days)
    )

    # 2. NDVI magnitude score (larger = better)
    max_mag = matched["norm_mag"].max()
    matched["mag_score"] = matched["norm_mag"] / max_mag if max_mag != 0 else 0

    # 3. Overlap ratio disabled for Point data
    matched["overlap_ratio"] = 1
    matched["match_score"] = 0.5 * matched["time_score"] + 0.5 * matched["mag_score"]

    # Unmatched satellite detections
    matched_sat_ids = matched["id"].dropna().unique()
    unmatched_sat = sat_gdf[~sat_gdf["id"].isin(matched_sat_ids)].copy()
    unmatched_sat["fusion_type"] = "satellite-only"
    unmatched_sat["change_date"] = pd.to_datetime(unmatched_sat["change_date"])

    # Unmatched text reports
    text_id_col = "report_id"
    if "report_id" not in matched.columns:
        text_id_col = [col for col in matched.columns if "report_id" in col][0]

    matched_text_ids = matched[text_id_col].dropna().unique()

    unmatched_text = text_gdf[~text_gdf["report_id"].isin(matched_text_ids)].copy()

    unmatched_text = text_gdf[~text_gdf["report_id"].isin(matched_text_ids)].copy()
    unmatched_text["fusion_type"] = "text-only"
    unmatched_text["change_date"] = pd.NaT
    unmatched_text["change_mag"] = None
    unmatched_text["change_type"] = None

    # Combine
    final_cols = matched.columns.union(unmatched_sat.columns).union(
        unmatched_text.columns
    )
    matched = matched[final_cols.intersection(matched.columns)]
    unmatched_sat = unmatched_sat[final_cols.intersection(unmatched_sat.columns)]
    unmatched_text = unmatched_text[final_cols.intersection(unmatched_text.columns)]

    fused = pd.concat([matched, unmatched_sat, unmatched_text], ignore_index=True)
    fused = gpd.GeoDataFrame(fused, geometry="geometry", crs="EPSG:4326")
    fused = fused[~fused.geometry.is_empty & fused.geometry.notnull()]
    fused = fused.drop(columns=["date_diff"], errors="ignore")

    print(fused["fusion_type"].value_counts())

    return fused


fused_gdf = classify_fusion(text_gdf, sat_gdf, valid_matches)

# Move key columns for clarity
cols = [
    "fusion_type",
    "change_date",
    "change_mag",
    "location_name",
    "report_id",
    "title",
    "geometry",
]
fused_gdf = fused_gdf[
    [c for c in cols if c in fused_gdf.columns]
    + [c for c in fused_gdf.columns if c not in cols]
]

# Drop blank geometries and unsupported dtypes
fused_gdf = fused_gdf[~fused_gdf.geometry.is_empty & fused_gdf.geometry.notnull()]
if "date_diff" in fused_gdf.columns:
    fused_gdf["date_diff_days"] = fused_gdf["date_diff"].dt.days
    fused_gdf = fused_gdf.drop(columns=["date_diff"])

fused_gdf["change_date"] = fused_gdf["change_date"].astype(str)
fused_gdf["report_date"] = fused_gdf["report_date"].astype(str)
fused_gdf["text_geometry"] = fused_gdf["text_geometry"].to_wkt()

fused_gdf.to_file("fused_gdf_match_score.gpkg", driver="GPKG")
