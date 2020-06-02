run file main.py 
$ python3 main.py
output: List of post have been Sorted - Type: DataFrame
example: 
    Id            Species  Weight  Height Color Accessory        Area        Time     Status  Similarity Rate
0   6      Affenpinscher       3      25   Đen     Không   Hoàng Mai  2020-05-25  Khỏe mạnh         0.817176
1   3           Không rõ      10      47   Xám   Vòng cổ   Hoàng Mai  2020-05-16  Khỏe mạnh         0.432143
2   2           Komondor      35      50   Đen     Không  Thanh Xuân  2020-05-20  Khỏe mạnh         0.275376
3   1  Italian Greyhound      15      45   Đen     Không  Thanh Xuân  2020-05-19  Khỏe mạnh         0.246407

To get the first post (the most Similar Post):
try: outputs.loc[[0]] 
-->
    Id        Species  Weight  Height Color Accessory       Area        Time     Status  Similarity Rate
0   6  Affenpinscher       3      25   Đen     Không  Hoàng Mai  2020-05-25  Khỏe mạnh         0.817176

To get an attribute of first Post (example: Species):
try: outputs.loc[0]['Species']
  -->  Affenpinscher

  y
