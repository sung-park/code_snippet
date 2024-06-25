import gpxpy
from datetime import datetime, timedelta

def split_segments_by_date(input_file, output_file='output.gpx'):
    with open(input_file, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    for track in gpx.tracks:
        new_segments = []
        current_segment = gpxpy.gpx.GPXTrackSegment()
        current_date = None

        for point in track.segments[0].points:
            date = point.time.date()
            if current_date is None:
                current_date = date

            if date != current_date:
                # 날짜가 변경되면 새로운 세그먼트 생성
                new_segments.append(current_segment)
                current_segment = gpxpy.gpx.GPXTrackSegment()
                current_date = date

            current_segment.points.append(point)

        # 마지막 세그먼트 추가
        new_segments.append(current_segment)

        # 기존 세그먼트를 새로운 세그먼트로 교체
        track.segments = new_segments

    with open(output_file, 'w') as f:
        f.write(gpx.to_xml())

# 예시 실행
split_segments_by_date('input.gpx')
