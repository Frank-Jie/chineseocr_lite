基于ouyanghuiyu chineseocr_lite

1.去除了多余的code，去除可视化相关code。
2.针对自身项目只检测横向文字，去除了竖向检测网络，去除了方向分类网络。
3.针对自身需要，精简了返回格式。
3.使用redis 作为MQ 在实际项目中作为主要接收途径。
4.同时使用flask作为其他接口。

使用版本：
pytorch 1.4.0
torchvision 0.5.0
cuda 10.1
cudnn 7.6.4

4.7日更新
针对识别文字有偏旁缺失问题，修改了psnet回归b-box结果x，y值
针对opencv 对rgba通道的异常进行处理

4.10 更新
gunicorn只用单线程

4.15 更新
去掉boxrect过程
缩小input到80%
