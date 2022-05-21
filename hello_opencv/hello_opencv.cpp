// hello_opencv.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//
#include <opencv2\opencv.hpp>
#include <iostream>
#include <fstream>

using namespace std;
using namespace cv;

vector<Vec3b> colors;
Mat displayImage(Mat, Mat);
int imageId = 1;
void statsWrite(string, Mat);


Mat removeRow(Mat src, Mat& dst, int row) {
    if (src.rows == 1) {
        dst = src;
        return src;
    }
    Mat res1;
    Mat res2;
    Mat input = src.clone();
    input(Range(0, row), Range(0, input.cols)).copyTo(res1);
    // 如果res2行数为0，合并就会报错
    if (row + 1 < input.rows) {
        input(Range(row + 1, input.rows), Range(0, input.cols)).copyTo(res2);
        // 合并两块
        vconcat(res1, res2, res1);
        dst = res1.clone();
    } else {
        dst = res1.clone();
        
    }
    return res1;

}



// 合并连通域框
Mat combineStats(Mat src, Mat& dst, Mat img, float threshold = 0) {
    Mat input = src.clone();
    for (int i = 1; i < input.rows; i++) {
        int x1 = input.at<int>(i, CC_STAT_LEFT);
        int y1 = input.at<int>(i, CC_STAT_TOP);
        int w1 = input.at<int>(i, CC_STAT_WIDTH);
        int h1 = input.at<int>(i, CC_STAT_HEIGHT);
        int area1 = input.at<int>(i, CC_STAT_AREA);

        for (int j = i + 1; j < input.rows; j++) {
            int x2 = input.at<int>(j, CC_STAT_LEFT);
            int y2 = input.at<int>(j, CC_STAT_TOP);
            int w2 = input.at<int>(j, CC_STAT_WIDTH);
            int h2 = input.at<int>(j, CC_STAT_HEIGHT);
            int area2 = input.at<int>(j, CC_STAT_AREA);
            // 判断1 ， 2两区域是否重叠 计算式原理：见leetcode相关题目，https://blog.csdn.net/qq_43539599/article/details/104952828
            // int notOverlapped = (x1 + w1 < x2 || x2 + w2 < x1 || y1 + h1 < y2 || y2 + h2 < y1);
            int overlapped = (x1 < x2 + w2 && x2 < x1 + w1 && y1 < y2 + h2 && y2 < y1 + h1);

            if (overlapped == 0) {
                continue;
            }

            // 确定重叠区边界
            int left = max(x1, x2);
            int top = max(y1, y2);
            int right = min(x1 + w1, x2 + w2);
            int bottom = min(y1 + h1, y2 + h2);


            // 计算重叠区域面积
            int overlap = (right - left) * (bottom - top);

            // 如果重叠区域面积大于阈值，则合并区域
            if (overlap > threshold) {
                // 确定合并区域的 x, y, w, h, area
                int x = min(x1, x2);
                int y = min(y1, y2);
                int w = max(x1 + w1, x2 + w2) - x;
                int h = max(y1 + h1, y2 + h2) - y;
                int area = area1 + area2;
                input.at<int>(i, CC_STAT_LEFT) = x;
                input.at<int>(i, CC_STAT_TOP) = y;
                input.at<int>(i, CC_STAT_WIDTH) = w;
                input.at<int>(i, CC_STAT_HEIGHT) = h;
                input.at<int>(i, CC_STAT_AREA) = area;
                // 删除被合并的x2区域
                if (input.rows == 2) {
                    dst = input.clone();
                    return input;
                }
                removeRow(input, input, j);
                // 更新区域1
                x1 = x;
                y1 = y;
                w1 = w;
                h1 = h;
                area1 = area;

                j--; // 复位
                // displayImage(img, input); // 测试使用
            }


        }


    }
    dst = input.clone();
    return input;
}

Mat sortrows(Mat src, Mat& dst, int sort_col) {
    Mat input = src.clone();
    // 用冒泡排序暴力排序mat
    for (int i = 0; i < input.rows; i++) {
        for (int j = 0; j < input.rows - i - 1; j++) {
            if (input.at<int>(j, sort_col) < input.at<int>(j + 1, sort_col)) {
                Mat temp = input.row(j + 1).clone();
                input.row(j).copyTo(input.row(j + 1));
                temp.row(0).copyTo(input.row(j));
            }
        }
    }
    dst = input.clone();
    return input;

}

void statsWrite(string filepath, Mat stats) {
    // 新建一个文件流记录数据
	ofstream outfile;
	outfile.open(filepath, ios::out); // 创建或者覆盖文件
    // 表头
    outfile << "id" << ", " << "area" << "," << "x" << ", " << "y" << ", " << "w" << ", " << "h" << endl;
    for (int i = 1; i < stats.rows; i++) {
        int x = stats.at<int>(i, CC_STAT_LEFT);
        int y = stats.at<int>(i, CC_STAT_TOP);
        int w = stats.at<int>(i, CC_STAT_WIDTH);
        int h = stats.at<int>(i, CC_STAT_HEIGHT);
        int area = stats.at<int>(i, CC_STAT_AREA);

        outfile << i << ", " << area << "," << x << ", " << y << ", " << w << ", " << h << endl;

    }
    outfile.close();
}

Mat displayImage(Mat img, Mat stats) {
    Mat temp_img = img.clone();
    int number = stats.rows;
    sortrows(stats, stats, CC_STAT_AREA);
    cout << stats << endl;

    // 最大连通域是全部图像，因此最大面积或者stats第一行要去除
    for (int i = 1; i < number; i++)
    {
        // 中心位置
        int center_x = stats.at<int>(i, CC_STAT_LEFT) + stats.at<int>(i, CC_STAT_WIDTH) / 2;
		int center_y = stats.at<int>(i, CC_STAT_TOP) + stats.at<int>(i, CC_STAT_HEIGHT) / 2;
            //矩形边框
        int x = stats.at<int>(i, CC_STAT_LEFT);
        int y = stats.at<int>(i, CC_STAT_TOP);
        int w = stats.at<int>(i, CC_STAT_WIDTH);
        int h = stats.at<int>(i, CC_STAT_HEIGHT);
        int area = stats.at<int>(i, CC_STAT_AREA);

        // 画框之前先遍历矩阵查找是否存在可以合并的内容

        // 中心位置绘制
        //circle(temp_img, Point(center_x, center_y), 2, Scalar(0, 255, 0), 2, 8, 0);
        circle(temp_img, Point(center_x, center_y), 2, colors[i], 2, 8, 0);
        // 外接矩形
        Rect rect(x, y, w, h);
        rectangle(temp_img, rect, colors[i], 1, 8, 0);
        //putText(temp_img, format("%d", i + 1), Point(center_x, center_y),
        //    FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 255), 1);
        putText(temp_img, format("%d", i), Point(center_x, center_y),
            FONT_HERSHEY_SIMPLEX, 0.5, colors[i], 1);

        cout << "number: " << i << ",area: " << area <<
            ",x: " << x <<
            ",y: " << y <<
            ",w: " << w <<
            ",h: " << h << endl;


    }
    //显示结果
    
    imshow(to_string(imageId++), temp_img);

    waitKey(0);
    return temp_img;

}


int main(int argc, string argv[])
{
    /*
    Mat src = imread("C:\\Users\\shiwenbo\\OneDrive\\images\\proc.jpg", IMREAD_GRAYSCALE);
	namedWindow("输入窗口",WINDOW_FREERATIO);
	imshow("输入窗口", src);
	waitKey(100000);
	destroyAllWindows();
    */
    // 图片路径
	// string imagePath = "C:\\Users\\shiwenbo\\OneDrive\\images\\4-21\\2022-04-21T17_00_26+08_00\\";
    string imagePath = argv[1];
    string imageFileName = "proc.jpg";





    // 二值化图像分割

    system("color F0");  //更改输出界面颜色
    //对图像进行距离变换
    Mat img = imread(imagePath + imageFileName);
    Mat originImage = img.clone();
    if (img.empty())
    {
        cout << "请确认图像文件名称是否正确" << endl;
        return -1;
    }
    imshow(imagePath + imageFileName, img);

    Mat leaves, leavesBW;

    //将图像转成二值图像，用于统计连通域
    cvtColor(img, leaves, COLOR_BGR2GRAY);
    threshold(leaves,leavesBW, 50, 255, THRESH_BINARY);

    //生成随机颜色，用于区分不同连通域
    RNG rng(10086);
    Mat out, stats, centroids;
    //统计图像中连通域的个数
    int number = connectedComponentsWithStats(leavesBW, out, stats, centroids, 8, CV_16U);
    for (int i = 0; i < number; i++)
    {
        //使用均匀分布的随机数确定颜色
        Vec3b vec3 = Vec3b(rng.uniform(0, 256), rng.uniform(0, 256), rng.uniform(0, 256));
        colors.push_back(vec3);
    }

    // 生成文件
    // 
    //以不同颜色标记出不同的连通域
    //Mat result = Mat::zeros(leaves.size(), img.type());
	
    //int w = result.cols;
    //int h = result.rows;
    sortrows(stats, stats, CC_STAT_AREA);
    cout << stats << endl;
    
    // 最大连通域是全部图像，因此最大面积或者stats第一行要去除
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

		
		// 画框之前先遍历矩阵查找是否存在可以合并的内容

        // 中心位置绘制
        //circle(img, Point(center_x, center_y), 2, Scalar(0, 255, 0), 2, 8, 0);
        circle(img, Point(center_x, center_y), 2, colors[i], 2, 8, 0);
        // 外接矩形
        Rect rect(x, y, w, h);
        rectangle(img, rect, colors[i], 1, 8, 0);
        //putText(img, format("%d", i + 1), Point(center_x, center_y),
        //    FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 0, 255), 1);
        putText(img, format("%d", i), Point(center_x, center_y),
            FONT_HERSHEY_SIMPLEX, 0.5,colors[i], 1);


        cout << "number: " << i + 1 << ",area: " << area << endl;


		
        // 新建一个文件流记录数据
		ofstream outfile;
		outfile.open(imagePath + "proc.csv", ios::app); // ios::app如果没有文件，生成空文件，如果存在文件，就在文件尾追加

	    outfile << "number: " << i << ",area: " << area  << 
            ",x: " << x <<
            ",y: " << y <<
			",w: " << w <<
			",h: " << h << endl;
        outfile.close();
        

    }
    //显示结果
    imshow("标记后的图像", img);

    imwrite(imagePath + "proc2.jpg", img);

    waitKey(0);

    Mat temp;
    combineStats(stats, temp,originImage, 0);
    sortrows(temp, temp, CC_STAT_AREA);
    Mat resImg = displayImage(originImage, temp);
    // 保存结果图
    imwrite(imagePath + "proc3.jpg", resImg);
    // 保存结果stats联通情况
    statsWrite(imagePath + "combined_stats.csv", temp);


	

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
