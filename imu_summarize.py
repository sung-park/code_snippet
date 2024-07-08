import pandas as pd
import json

def process_wearable_data(input_file, output_file):
    # 1. 데이터 로드 및 불필요한 열 제거
    df = pd.read_csv(input_file, usecols=['timestamp', 'Activity', 'Activity2'])

    # 2. activity 값 처리
    df['Activity'] = df.apply(lambda row: row['Activity2'] if pd.isna(row['Activity']) else row['Activity'], axis=1)
    df.drop('Activity2', axis=1, inplace=True)

    # 3. 1초 간격 샘플링
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df.resample('1S').first().reset_index()

    # 4. timestamp_start, timestamp_end 생성
    df['timestamp_end'] = df['timestamp'] + pd.Timedelta(seconds=1)
    df.rename(columns={'timestamp': 'timestamp_start'}, inplace=True)

    # 5. 동일한 activity 통합
    merged_data = []
    current_activity = None
    for _, row in df.iterrows():
        if row['Activity'] != current_activity:
            if current_activity is not None:
                merged_data[-1]['timestamp_end'] = row['timestamp_start']
            merged_data.append(row.to_dict())
            current_activity = row['Activity']
    merged_df = pd.DataFrame(merged_data)

    # 6. JSON 변환 및 저장
    merged_df['timestamp_start'] = merged_df['timestamp_start'].astype(str)
    merged_df['timestamp_end'] = merged_df['timestamp_end'].astype(str)
    result_json = merged_df.to_json(orient='records')

    with open(output_file, 'w') as f:
        json.dump(json.loads(result_json), f, indent=2)

# 예시 실행
input_file = 'input_data.csv'  # 입력 파일 경로
output_file = 'processed_data.json'  # 출력 파일 경로
process_wearable_data(input_file, output_file)
