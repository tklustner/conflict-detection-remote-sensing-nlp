import geopandas as gpd
import pandas as pd
from satellite.fusion import filter_temporal_matches, classify_fusion

def run_fusion_pipeline(text_path, sat_path, delta_days=14, output_path=None):
    text_gdf = gpd.read_file(text_path)
    sat_gdf = gpd.read_file(sat_path)

    text_gdf = text_gdf.to_crs(epsg=4326)
    sat_gdf = sat_gdf.to_crs(epsg=4326)

    sat_gdf['change_date'] = pd.to_datetime(sat_gdf['change_date'])
    sat_gdf = sat_gdf.rename(columns = {'mean':'change_mag'})

    spatial_matches = gpd.sjoin(sat_gdf, text_gdf, predicate='intersects', how='left')

    valid_matches = filter_temporal_matches(spatial_matches, delta_days=delta_days)

    fused_gdf = classify_fusion(text_gdf, sat_gdf, valid_matches)

    if 'change_date' in fused_gdf.columns:
        fused_gdf['change_date'] = fused_gdf['change_date'].astype(str)

    if 'report_date' in fused_gdf.columns:
        fused_gdf['report_date'] = fused_gdf['report_date'].astype(str)

    if output_path:
        fused_gdf.to_file(output_path, driver='GPKG')

    return fused_gdf

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--text_path", required=True)
    parser.add_argument("--sat_path", required=True)
    parser.add_argument("--delta_days", type=int, default=14)
    parser.add_argument("--output_path", required=False)

    args = parser.parse_args()

    run_fusion_pipeline(
        text_path=args.text_path,
        sat_path=args.sat_path,
        delta_days=args.delta_days,
        output_path=args.output_path
    )
