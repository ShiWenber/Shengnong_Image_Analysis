```C++
// hello_opencv.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include <opencv2\opencv.hpp>
#include <iostream>
#include <fstream>

using namespace std;
using namespace cv;




int main()
{
    /*
    Mat src = imread("C:\\Users\\shiwenbo\\OneDrive\\images\\proc.jpg", IMREAD_GRAYSCALE);
	namedWindow("输入窗口",WINDOW_FREERATIO);
	imshow("输入窗口", src);
	waitKey(100000);
	destroyAllWindows();
    */
    // 图片路径
	string imagePath = "C:\\Users\\shiwenbo\\OneDrive\\images\\4-21\\2022-04-21T17_00_26+08_00\\proc.jpg";


    Mat src = imread(imagePath, IMREAD_GRAYSCALE);

	imshow("输入窗口", src);
	waitKey(0);
	destroyAllWindows();



    // 二值化图像分割

    system("color F0");  //更改输出界面颜色
    //对图像进行距离变换
    Mat img = imread(imagePath);
    if (img.empty())
    {
        cout << "请确认图像文件名称是否正确" << endl;
        return -1;
    }
    imshow(imagePath, img);
    Mat leaves, leavesBW;

    //将图像转成二值图像，用于统计连通域
    cvtColor(img, leaves, COLOR_BGR2GRAY);
    threshold(leaves,leavesBW, 50, 255, THRESH_BINARY);

    //生成随机颜色，用于区分不同连通域
    RNG rng(10086);
    Mat out, stats, centroids;
    //统计图像中连通域的个数
    int number = connectedComponentsWithStats(leavesBW, out, stats, centroids, 8, CV_16U);
    vector<Vec3b> colors;
    for (int i = 0; i < number; i++)
    {
        //使用均匀分布的随机数确定颜色
        Vec3b vec3 = Vec3b(rng.uniform(0, 256), rng.uniform(0, 256), rng.uniform(0, 256));
        colors.push_back(vec3);
    }

    // 生成文件
    // 
    //以不同颜色标记出不同的连通域
    Mat result = Mat::zeros(leaves.size(), img.type());
    int w = result.cols;
    int h = result.rows;
    for (int i = 1; i < number; i++)
    {
        // 中心位置
        int center_x = centroids.at<double>(i, 0);
        int center_y = centroids.at<double>(i, 1);
        //矩形边框
        int x = stats.at<int>(i, CC_STAT_LEFT);
        int y = stats.at<int>(i, CC_STAT_TOP);
        int w = stats.at<int>(i, CC_STAT_WIDTH);
        int h = stats.at<int>(i, CC_STAT_HEIGHT);
        int area = stats.at<int>(i, CC_STAT_AREA);

        // 中心位置绘制
        circle(img, Point(center_x, center_y), 2, Scalar(0, 255, 0), 2, 8, 0);
        // 外接矩形
        Rect rect(x, y, w, h);
        rectangle(img, rect, colors[i], 1, 8, 0);
        putText(img, format("%d", i), Point(center_x, center_y),
            FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 255), 1);
        cout << "number: " << i << ",area: " << area << endl;


    }
    //显示结果
    imshow("标记后的图像", img);

    waitKey(0);
    return 0;







}

// 运行程序: Ctrl + F5 或调试 >“开始执行(不调试)”菜单
// 调试程序: F5 或调试 >“开始调试”菜单

// 入门使用技巧: 
//   1. 使用解决方案资源管理器窗口添加/管理文件
//   2. 使用团队资源管理器窗口连接到源代码管理
//   3. 使用输出窗口查看生成输出和其他消息
//   4. 使用错误列表窗口查看错误
//   5. 转到“项目”>“添加新项”以创建新的代码文件，或转到“项目”>“添加现有项”以将现有代码文件添加到项目
//   6. 将来，若要再次打开此项目，请转到“文件”>“打开”>“项目”并选择 .sln 文件

```