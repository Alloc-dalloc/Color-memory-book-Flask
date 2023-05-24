import cv2
import webcolors
import numpy as np
from sklearn.cluster import KMeans
import requests


class ColorAnalyzer:
    def __init__(self):
        self.webcolors = webcolors

    def closest_color(self, rgb_tuple):
        min_colors = {}
        for key, name in self.webcolors.CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = self.webcolors.hex_to_rgb(key)
            rd = (r_c - rgb_tuple[0]) ** 2
            gd = (g_c - rgb_tuple[1]) ** 2
            bd = (b_c - rgb_tuple[2]) ** 2
            min_colors[(rd + gd + bd)] = name
        return min_colors[min(min_colors.keys())]

    def analyze_color(self, image_path):
        # 이미지 다운로드
        response = requests.get(image_path)
        image_data = response.content
        # 이미지 열기
        image = cv2.imdecode(np.frombuffer(image_data, np.uint8), cv2.IMREAD_COLOR)
        # 이미지 RGB 값으로 변환
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # 이미지 reshape
        pixel_values = image.reshape((-1, 3))
        # k-means 알고리즘을 사용하여 색상 분류
        kmeans = KMeans(n_clusters=5)
        kmeans.fit(pixel_values)
        # 라벨링된 색상 정보
        labels = kmeans.labels_
        # 라벨링된 색상 정보를 이용하여 색상별 비율 계산
        counts = np.bincount(labels)
        percentages = counts / len(pixel_values)
        percentages.sort()
        # 색상별 비율 출력
        result = []
        for i, percentage in enumerate(percentages):
            color = kmeans.cluster_centers_[i]
            rgb = [int(x) for x in color.tolist()]
            color_name = self.closest_color(rgb)
            color_info = {
                'colorPercentage': round(percentage * 100),
                'colorName': color_name
            }
            result.append(color_info)
            # print("색상 {}: {:.2f}%, 값: {}".format(i + 1, percentage * 100, color_name))
        # result.sort(key=lambda x: x['percentage'], reverse=True)
        return result
