import gpxpy
import pandas as pd
from datetime import timedelta

def analyze_gpx_time_intervals(gpx_file_path):
    """
    GPX 파일의 각 trk 내 trkpt 시간 간격을 분석하고 통계를 출력하는 함수

    Args:
        gpx_file_path (str): GPX 파일 경로

    Returns:
        pd.DataFrame: 각 trk별 trkpt 시간 간격 통계 데이터프레임
    """

    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    results = []

    for track_idx, track in enumerate(gpx.tracks):
        time_intervals = []
        for segment in track.segments:
            for i in range(1, len(segment.points)):
                prev_point = segment.points[i - 1]
                curr_point = segment.points[i]
                time_interval = curr_point.time - prev_point.time
                time_intervals.append(time_interval.total_seconds())

        if time_intervals:  # trkpt가 2개 이상인 경우에만 통계 계산
            results.append({
                'track_index': track_idx,
                'track_name': track.name,
                'mean_interval': timedelta(seconds=pd.Series(time_intervals).mean()),
                'median_interval': timedelta(seconds=pd.Series(time_intervals).median()),
                'min_interval': timedelta(seconds=pd.Series(time_intervals).min()),
                'max_interval': timedelta(seconds=pd.Series(time_intervals).max()),
                'std_dev_interval': timedelta(seconds=pd.Series(time_intervals).std())
            })

    return pd.DataFrame(results)

# GPX 파일 경로
gpx_file_path = 'your_gpx_file.gpx'  # 실제 GPX 파일 경로로 변경

# GPX 파일 분석 및 결과 출력
results_df = analyze_gpx_time_intervals(gpx_file_path)
print(results_df)
