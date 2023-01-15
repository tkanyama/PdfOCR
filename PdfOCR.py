# 各種インポート
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


# 直線検出する画像
input_file = 'page179.png'  # ここを変更
# 直掩検出と除去をしたい画像のファイル名を入力します

# 画像の読み込み
img = cv2.imread(input_file)

print('【直線を検出中・・・】直線検出する画像')
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.show()

# モノクロ・グレースケール画像へ変換（2値化前の画像処理）
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2値化（Binarization）：白（1）黒（0）のシンプルな2値画像に変換
retval, img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
# plt.imshow(img_binary)
print('【直線を検出中・・・】2値化処理画像 - Binarization')
plt.imshow(cv2.cvtColor(img_binary, cv2.COLOR_BGR2RGB))
plt.show()

# 2値化画像で行う
# rho：画素単位で計算
# theta：ラジアン単位で計算
# threshold：直線とみなされるのに必要な最低限の点の数を意味するしきい値。
# 確率的ハフ変換：
# minLineLength：検出する直線の最小の長さを表します。この値より短い線分は検出されません
# maxLineGap：二つの点を一つの直線とみなす時に許容される最大の長さを表します
# この値より小さい二つの点は一つの直線とみなされます
# 必要に応じてパラメータの数値を変更してください
lines = cv2.HoughLinesP(img_binary, rho=1, theta=np.pi/360, threshold=15, minLineLength=60, maxLineGap=5.4)

if lines is None:  # 直線が検出されない場合
    print('\n【直線の検出結果】')
    print('　直線は検出されませんでした。')
    file_name = os.path.splitext(os.path.basename(input_file))[0]
    cv2.imwrite(f'line_cut_{file_name}.png', img)
else:  # 直線が検出された場合
    print('\n【直線の検出結果】')
    print('　直線が検出されました。検出した直線を削除します。')
    for line in lines:
        x1, y1, x2, y2 = line[0]
        # 検出した直線に赤線を引く
        red_lines_img = cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 1)
    print('\n【直線検出部位の視覚化】')
    print('　赤色部分が検出できた直線。')
    plt.imshow(cv2.cvtColor(red_lines_img, cv2.COLOR_BGR2RGB))
    plt.show()

    for line in lines:
        x1, y1, x2, y2 = line[0]
        # 検出した直線を消す（白で線を引く）：2値化した際に黒で表示される
        no_lines_img = cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 1)

        # 直線を除去した画像を元のファイル名の頭に「line_cut_」をつけて保存。「0」を指定でファイル名を取得
        file_name = os.path.splitext(os.path.basename(input_file))[0]
        cv2.imwrite(f'line_cut_{file_name}.png', no_lines_img)
    print('\n【直線検出部位の削除結果：元の画像から削除】')
    print('　白色部分が検出した直線を消した場所（背景が白の場合は区別できません）。')
    plt.imshow(cv2.cvtColor(no_lines_img, cv2.COLOR_BGR2RGB))
    plt.show()

    line_cut_input_file = f'line_cut_{file_name}.png'
    img = cv2.imread(line_cut_input_file)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 2値化（Binarization）：白（1）黒（0）のシンプルな2値画像に変換
    retval, img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    print('\n【直線検出部位の削除結果：2値化処理画像 - Binarization】')
    print('　直線を除去した結果。')
    plt.imshow(cv2.cvtColor(img_binary, cv2.COLOR_BGR2RGB))
    plt.show()


# 直線検出した画像などの削除：
# 保存したい場合は、ここをコメントアウト（または削除）すると画像を保存できます。
file_name = os.path.splitext(os.path.basename(input_file))[0]
os.remove(f'line_cut_{file_name}.png')


print('\n\n＊　直線を上手く検出できない場合は「cv2.HoughLinesP」のパラメータを変更してみてください。')
