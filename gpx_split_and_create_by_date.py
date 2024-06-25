import gpxpy
import os
from datetime import datetime

def split_gpx_by_date(input_file, output_dir):
    """
    GPX 파일을 날짜별로 분할하여 개별 GPX 파일로 저장합니다.

    Args:
        input_file (str): 입력 GPX 파일 경로
        output_dir (str): 출력 디렉토리 경로
    """

    with open(input_file, 'r') as f:
        gpx = gpxpy.parse(f)

    for track in gpx.tracks:
        for segment in track.segments:
            # 첫 번째 포인트의 시간에서 날짜 추출
            date_str = segment.points[0].time.strftime("%Y-%m-%d")

            # 새로운 GPX 객체 생성
            new_gpx = gpxpy.gpx.GPX()
            new_gpx.tracks.append(gpxpy.gpx.GPXTrack(name=date_str))
            new_gpx.tracks[0].segments.append(segment)

            # 출력 파일 경로 생성
            output_file = os.path.join(output_dir, f"{date_str}.gpx")

            # GPX 파일 저장
            with open(output_file, 'w') as f:
                f.write(new_gpx.to_xml())

# 사용 예시
input_file = "input.gpx"  # 입력 파일 경로
output_dir = "output_gpx"  # 출력 디렉토리 경로

# 출력 디렉토리 생성 (존재하지 않을 경우)
os.makedirs(output_dir, exist_ok=True)

split_gpx_by_date(input_file, output_dir)
